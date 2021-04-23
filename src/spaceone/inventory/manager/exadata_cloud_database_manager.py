from spaceone.inventory.libs.manager import OCIManager
from spaceone.inventory.libs.schema.base import ReferenceModel
from spaceone.inventory.model.baremetal_vm_database import *
from spaceone.inventory.model.baremetal_vm_database.cloud_service import *
from spaceone.inventory.connector.exadata_cloud_database import ExadataCloudDatabaseConnector
from spaceone.inventory.model.baremetal_vm_database.cloud_service_type import CLOUD_SERVICE_TYPES
from oci.database.models import DbSystemSummary
import time
from pprint import pprint


class ExadataCloudDatabaseManager(OCIManager):

    def __init__(self, transaction, **kwargs):
        super().__init__(transaction, **kwargs)
        self.connector_name = 'ExadataCloudDatabaseConnector'
        self.cloud_service_types = CLOUD_SERVICE_TYPES

    def collect_cloud_service(self, params):
        start_time = time.time()
        """
        Args:
            params:
                - options
                - schema
                - secret_data
                - filter
                - region
                - compartment
        Response:
            CloudServiceResponse
        """
        secret_data = params['secret_data']
        region = params['region']
        compartment = params['compartment']

        secret_data.update({'region': region})
        exa_conn: ExadataCloudDatabaseConnector = self.locator.get_connector(self.connector_name, **params)
        exa_conn.set_connect(secret_data)

        '''
        TODO
        '''

        return []




