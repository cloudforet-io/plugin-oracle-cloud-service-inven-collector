import time
import logging
import concurrent.futures

import oci
from oci.identity.models.compartment import Compartment
from spaceone.inventory.libs.manager import OCIManager
from spaceone.core.service import *
from oci.identity.identity_client import IdentityClient
from oci.pagination import list_call_get_all_results


_LOGGER = logging.getLogger(__name__)
MAX_WORKER = 10
SUPPORTED_FEATURES = ['garbage_collection']
SUPPORTED_RESOURCE_TYPE = ['inventory.CloudService', 'inventory.CloudServiceType', 'inventory.Region']
FILTER_FORMAT = []
DEFAULT_REGIONS = ('ap-seoul-1', 'us-ashburn-1', 'ap-chuncheon-1', 'ap-tokyo-1', 'eu-frankfurt-1',
                   'sa-saopaulo-1', 'us-phoenix-1', 'ca-montreal-1', 'uk-london-1', 'me-dubai-1',
                   'ca-montreal-1', 'ca-toronto-1', 'sa-santiago-1', 'ap-hyderabad-1', 'ap-mumbai-1',
                   'ap-osaka-1', 'ap-tokyo-1', 'eu-amsterdam-1', 'me-jeddah-1', 'eu-zurich-1',
                   'uk-cardiff-1', 'us-sanjose-1')


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

    @staticmethod
    def identity_read_compartments(identity, tenancy, secret_data):
        result = []
        try:
            compartments = list_call_get_all_results(
                identity.list_compartments,
                tenancy.id,
                compartment_id_in_subtree=True
            ).data

            # Add root compartment which is not part of list_compartments
            for compartment in compartments:
                if compartment.id == secret_data['tenancy'] or \
                        compartment.lifecycle_state == Compartment.LIFECYCLE_STATE_ACTIVE:
                    result.append(compartment)
            result.append(tenancy)
            return result
        except Exception as e:
            raise RuntimeError("[ERROR: ResourceInfo] Error on identity_read_compartments: " + str(e.args))

    @classmethod
    def get_regions_and_compartment(cls,secret_data):
        compartments = []
        regions = []
        tenancy = None
        for default_region in DEFAULT_REGIONS:
            secret_data.update({'region': default_region})
            try:
                identity = IdentityClient(secret_data)
                tenancy = identity.get_tenancy(secret_data["tenancy"]).data
                region_names = identity.list_region_subscriptions(tenancy.id).data
                regions = [str(es.region_name) for es in region_names]
                compartments = cls.identity_read_compartments(identity, tenancy, secret_data)
            except Exception as e:
                print("[ERROR: Collector_Service] Error on get_regions_and_compartment: " + str(e.args))
                pass
            else:
                break

        return regions, compartments, secret_data

    @staticmethod
    def _set_multi_thread_params(secret_data, regions, compartments):
        params = []
        for region in regions:
            for compartment in compartments:
                params.append({
                    'secret_data': secret_data,
                    'region': region,
                    'compartment': compartment
                })

        return params

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
        key = params['secret_data']
        print(key)
        regions, compartments, secret_data = self.get_regions_and_compartment(params['secret_data'])
        multi_thread_params = self._set_multi_thread_params(secret_data, regions, compartments)

        with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKER) as executor:
            # print("[ EXECUTOR START ]")
            future_executors = []

            for execute_manager in self.execute_managers:
                _execute_manager = self.locator.get_manager(execute_manager)

                for cloud_service_type in _execute_manager.collect_cloud_service_type():
                    yield cloud_service_type.to_primitive()

                print(f'@@@ {execute_manager} @@@')
                for mt_params in multi_thread_params:
                    mt_manager = self.locator.get_manager(execute_manager)
                    future_executors.append(executor.submit(mt_manager.collect_resources, mt_params))

            for future in concurrent.futures.as_completed(future_executors):
                for result in future.result():
                    yield result.to_primitive()

        # for manager in self.execute_managers:
        #     _manager = self.locator.get_manager(manager)
        #
        #     for resource in _manager.collect_resources(params):
        #         yield resource.to_primitive()

        print(f'TOTAL TIME : {time.time() - start_time} Seconds')
