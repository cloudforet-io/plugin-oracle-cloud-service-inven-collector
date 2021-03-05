import time
import logging
import concurrent.futures
from spaceone.inventory.libs.manager import OCIManager
from spaceone.core.service import *
from oci.identity.identity_client import IdentityClient
from oci.pagination import list_call_get_all_results


_LOGGER = logging.getLogger(__name__)
MAX_WORKER = 20
SUPPORTED_FEATURES = ['garbage_collection']
SUPPORTED_RESOURCE_TYPE = ['inventory.CloudService', 'inventory.CloudServiceType', 'inventory.Region']
FILTER_FORMAT = []


@authentication_handler
class CollectorService(BaseService):
    def __init__(self, metadata):
        super().__init__(metadata)

        self.execute_managers = [
            # set Oracle cloud service manager
            'AutonomousDatabaseManager'
        ]

    @check_required(['options'])
    def init(self, params):
        """ init plugin by options
        """
        capability = {
            'filter_format': FILTER_FORMAT,
            'supported_resource_type': SUPPORTED_RESOURCE_TYPE,
            'supported_features': SUPPORTED_FEATURES
        }
        return {'metadata': capability}

    @transaction
    @check_required(['options', 'secret_data'])
    def verify(self, params):
        """
        Args:
              params:
                - options
                - secret_data
        """
        options = params['options']
        secret_data = params.get('secret_data', {})
        if secret_data != {}:
            oci_manager = OCIManager()
            active = oci_manager.verify({}, secret_data)

        return {}

    def identity_read_compartments(self,identity, tenancy):

        try:
            compartments = list_call_get_all_results(
                identity.list_compartments,
                tenancy.id,
                compartment_id_in_subtree=True
            ).data

            # Add root compartment which is not part of list_compartments
            compartments.append(tenancy)
            return compartments
        except Exception as e:
            raise RuntimeError("[ERROR: ResourceInfo] Error on identity_read_compartments: " + str(e.args))


    def get_params(self, secret_data):
        compartments = []
        regions = []
        tenancy = None

        try:
            identity = IdentityClient(secret_data)
            tenancy = identity.get_tenancy(secret_data["tenancy"]).data
            region_name = identity.list_region_subscriptions(tenancy.id).data
            regions = [str(es.region_name) for es in region_name]
            compartments = self.identity_read_compartments(identity, tenancy)

            return regions, compartments

        except Exception as e:
            raise RuntimeError("\nError extracting compartment section - " + str(e))

    @transaction
    @check_required(['options', 'secret_data', 'filter'])
    def list_resources(self, params):
        """
        Args:
            params:
                - options
                - schema
                - secret_data
                - filter
        """

        start_time = time.time()

        print("[ EXECUTOR START: Oracle Cloud Service ]")

        # get regions
        # regions
        # get compartment
        # compartments
        regions, compartments = self.get_params(params['secret_data'])
        #compartment_ids = [comp.id for comp in compartments]
        params.update({
            'regions': regions,
            'compartments': compartments
        })
        '''
        # 여기서부터 파라미터 갱신하고, 매니저까지 넣으면 최고
        mt_params = []
        secret_data = params['secret_data']
        for region_name in [str(es.region_name) for es in regions]:
            for execute_manager in self.execute_managers:
                secret_data['region'] = region_name
                value = {
                    'region': region_name,
                    'compartment_id': compartment_id,
                    'secret_data': secret_data,
                    'manager': execute_manager
                }
                mt_params.append(value)
                
        '''
        with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKER) as executor:
            # print("[ EXECUTOR START ]")
            future_executors = []

            for execute_manager in self.execute_managers:
                print(f'@@@ {execute_manager} @@@')
                _manager = self.locator.get_manager(execute_manager)
                future_executors.append(executor.submit(_manager.collect_resources, params))

            for future in concurrent.futures.as_completed(future_executors):
                for result in future.result():
                    yield result.to_primitive()

        # for manager in self.execute_managers:
        #     _manager = self.locator.get_manager(manager)
        #
        #     for resource in _manager.collect_resources(params):
        #         yield resource.to_primitive()

        print(f'TOTAL TIME : {time.time() - start_time} Seconds')
