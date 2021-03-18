from spaceone.core.manager import BaseManager
from spaceone.inventory.libs.connector import OCIConnector
from spaceone.inventory.libs.schema.region import RegionResource, RegionResponse

REGION_INFO = {
    'ap-sydney-1': {'name': 'Australia East (Sydney)',
                    'tags': {'latitude': '-33.795606497812734', 'longitude': '151.14310024060555'}},
    'ap-melbourne-1': {'name': 'Australia Southeast (Melbourne)',
                       'tags': {'latitude': '-37.836437506996056', 'longitude':'144.9768338033289'}},
    'sa-saopaulo-1': {'name': 'Brazil East (Sao Paulo)',
                      'tags': {'latitude':'-23.620403486736283', 'longitude': '-46.69839504944699'}},
    'ca-montreal-1': {'name': 'Canada Southeast (Montreal)',
                      'tags': {'latitude': '48.02277893323851', 'longitude': '-72.77649927414969'}},
    'ca-toronto-1': {'name': 'Canada Southeast (Toronto)',
                     'tags': {'latitude': '43.64525039229924', 'longitude': '-79.3885163121194'}},
    'sa-santiago-1': {'name': 'Chile (Santiago)',
                      'tags': {'latitude': '-33.3928800717296', 'longitude': '-70.61810798130301'}},
    'eu-frankfurt-1': {'name': 'Germany Central (Frankfurt)',
                       'tags': {'latitude': '50.112230567678246', 'longitude': '8.672445398408382'}},
    'ap-hyderabad-1': {'name': 'US East (Virginia)',
                       'tags': {'latitude': '17.45294842605367', 'longitude': '78.37304425523932'}},
    'ap-mumbai-1': {'name': 'India West (Mumbai)',
                    'tags': {'latitude': '19.075952218384348', 'longitude': '72.8686385971879'}},
    'ap-osaka-1': {'name': 'Japan Central (Osaka)',
                   'tags': {'latitude': '37.385143655211614', 'longitude': '135.3776016588488'}},
    'ap-tokyo-1': {'name': 'Japan East (Tokyo)',
                   'tags': {'latitude': '35.67253888589379', 'longitude': '139.7183833741466'}},
    'eu-amsterdam-1': {'name': 'Netherlands Northwest (Amsterdam)',
                       'tags': {'latitude': '52.370807302221046', 'longitude': '4.9143992427622845'}},
    'me-jeddah-1': {'name': 'Saudi Arabia West (Jeddah)',
                    'tags': {'latitude': '21.55007076365963', 'longitude': '39.15359411831724'}},
    'ap-seoul-1': {'name': 'South Korea Central (Seoul)',
                   'tags': {'latitude': '37.51654192549858', 'longitude': '127.05995742636503'}},
    'ap-chuncheon-1': {'name': 'South Korea North (Chuncheon)',
                       'tags': {'latitude': '37.894442882735895', 'longitude': '127.74262581388302'}},
    'eu-zurich-1': {'name': 'Switzerland North (Zurich)',
                    'tags': {'latitude': '47.40812222241945', 'longitude': '8.51028147665295'}},
    'me-dubai-1': {'name': 'UAE East (Dubai)',
                   'tags': {'latitude': '25.10339704388869', 'longitude': '55.164826479932195'}},
    'uk-london-1': {'name': 'UK South (London)',
                    'tags': {'latitude': '51.521665680779556', 'longitude': '-0.08740731521017898'}},
    'uk-cardiff-1': {'name': 'UK West (Newport)',
                     'tags': {'latitude': '51.585983195115496', 'longitude': '-2.9916180315774574'}},
    'us-ashburn-1': {'name': 'US East (Ashburn)',
                     'tags': {'latitude': '39.005889864461935', 'longitude': '-77.45049672898982'}},
    'us-phoenix-1': {'name': 'US West (Phoenix)',
                     'tags': {'latitude': '33.47566855519292', 'longitude': '-111.92255154919961'}},
    'us-sanjose-1': {'name': 'US West (San Jose)',
                     'tags': {'latitude': '37.3330546912652', 'longitude': '-121.88957710927275'}},
}


class OCIManager(BaseManager):

    def __init__(self, transaction, **kwargs):
        super().__init__(transaction, **kwargs)

        self.connector_name = None
        self.cloud_service_types = []
        self.response_schema = None
        self.collected_region_codes = []

    def verify(self, options, secret_data, **kwargs):
        """ Check collector's status.
        """

        try:
            connector: OCIConnector = self.locator.get_connector('OCIConnector', secret_data=secret_data)
            connector.verify(secret_data)

        except Exception as e:
            print(f'[ERROR: ResourceInfo]: {e}')

    def collect_cloud_service_type(self):
        for cloud_service_type in self.cloud_service_types:
            yield cloud_service_type

    def collect_cloud_service(self, params) -> list:
        raise NotImplemented

    def collect_resources(self, params) -> list:
        resources = []

        # resources.extend(self.collect_cloud_service_type())
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

    @staticmethod
    def convert_dictionary(obj):
        return vars(obj)

    @staticmethod
    def convert_nested_dictionary(self, vm_object):
        vm_dict = self.convert_dictionary(vm_object)
        for k, v in vm_dict.items():
            if isinstance(v, object):  # object
                if isinstance(v, list):  # if vm_object is list
                    for list_obj in v:
                        vm_converse_list = list()
                        if hasattr(list_obj, '__dict__'):
                            vm_converse_dict = self.convert_nested_dictionary(self, list_obj)
                            vm_converse_list.append(vm_converse_dict)
                        vm_dict[k] = vm_converse_list

                elif hasattr(v, '__dict__'):  # if vm_object is not a list type, just an object
                    vm_converse_dict = self.convert_nested_dictionary(self, v)
                    vm_dict[k] = vm_converse_dict

        return vm_dict

    @staticmethod
    def gigabyte_to_byte(gigabyte):
        return 1073741824*gigabyte


