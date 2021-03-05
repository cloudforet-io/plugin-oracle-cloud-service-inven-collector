from spaceone.inventory.libs.manager import OCIManager
from spaceone.inventory.libs.schema.base import ReferenceModel
from spaceone.inventory.model.autonomous_database import *
from spaceone.inventory.model.autonomous_database.cloud_service import *
from spaceone.inventory.connector.autonomous_database import AutonomousDatabaseConnector
from spaceone.inventory.model.autonomous_database.cloud_service_type import CLOUD_SERVICE_TYPES
from datetime import datetime
import time


class AutonomousDatabaseManager(OCIManager):
    connector_name = 'AutonomousDatabaseConnector'
    cloud_service_types = CLOUD_SERVICE_TYPES

    def collect_cloud_service(self, params):
        print("** Autonomous Database START **")
        start_time = time.time()
        """
        Args:
            params:
                - options
                - schema
                - secret_data
                - filter
                - regions
                - compartments
        Response:
            CloudServiceResponse
        """
        secret_data = params['secret_data']
        adb_conn: AutonomousDatabaseConnector = self.locator.get_connector(self.connector_name, **params)
        adb = []

        print(f'** Autonomous Database Finished {time.time() - start_time} Seconds **')
        return adb
