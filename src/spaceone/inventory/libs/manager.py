from spaceone.core.manager import BaseManager
from spaceone.inventory.libs.connector import OCIConnector
from spaceone.inventory.libs.schema.region import RegionResource, RegionResponse

REGION_INFO = {
    # SAMPLE
    # 'eastus': {'name': 'US East (Virginia)', 'tags': {'latitude': '37.3719', 'longitude': '-79.8164'}},
}


class OCIManager(BaseManager):
    connector_name = None
    cloud_service_types = []
    response_schema = None
    collected_region_codes = []

    def verify(self, options, secret_data, **kwargs):
        """ Check collector's status.
        """
        connector: OCIConnector = self.locator.get_connector('OCIConnector', secret_data=secret_data)
        connector.verify()

    def collect_cloud_service_type(self):
        for cloud_service_type in self.cloud_service_types:
            yield cloud_service_type

    def collect_cloud_service(self, params) -> list:
        raise NotImplemented

    def collect_resources(self, params) -> list:
        resources = []

        resources.extend(self.collect_cloud_service_type())
        resources.extend(self.collect_cloud_service(params))
        resources.extend(self.collect_region())

        return resources

    def collect_region(self):
        results = []
        for region_code in self.collected_region_codes:
            if region := self.match_region_info(region_code):
                results.append(RegionResponse({'resource': region}))

        return results

    def set_region_code(self, region):
        if region not in REGION_INFO:
            region = 'global'

        if region not in self.collected_region_codes:
            self.collected_region_codes.append(region)

    @staticmethod
    def convert_tag_format(tags):
        convert_tags = []

        if tags:
            for k, v in tags.items():
                convert_tags.append({
                    'key': k,
                    'value': v
                })

        return convert_tags

    @staticmethod
    def match_region_info(region_code):
        match_region_info = REGION_INFO.get(region_code)

        if match_region_info:
            region_info = match_region_info.copy()
            region_info.update({
                'region_code': region_code
            })
            return RegionResource(region_info, strict=False)

        return None

    # @staticmethod
    # def convert_dictionary(obj):
    #     return vars(obj)
    #
    # @staticmethod
    # def convert_nested_dictionary(self, vm_object):
    #     vm_dict = self.convert_dictionary(vm_object)
    #     for k, v in vm_dict.items():
    #         if isinstance(v, object):  # object
    #             if isinstance(v, list):  # if vm_object is list
    #                 for list_obj in v:
    #                     vm_converse_list = list()
    #                     if hasattr(list_obj, '__dict__'):
    #                         vm_converse_dict = self.convert_nested_dictionary(self, list_obj)
    #                         vm_converse_list.append(vm_converse_dict)
    #                     vm_dict[k] = vm_converse_list
    #
    #             if hasattr(v, '__dict__'):  # if vm_object is not a list type, just an object
    #                 vm_converse_dict = self.convert_nested_dictionary(self, v)
    #                 vm_dict[k] = vm_converse_dict
    #
    #     return vm_dict
