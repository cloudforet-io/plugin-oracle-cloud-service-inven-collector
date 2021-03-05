from spaceone.inventory.libs.manager import OCIManager
from spaceone.inventory.libs.schema.base import ReferenceModel
from spaceone.inventory.model.autonomous_database import *
from spaceone.inventory.model.autonomous_database.cloud_service import *
from spaceone.inventory.connector.autonomous_database import AutonomousDatabaseConnector
from spaceone.inventory.model.autonomous_database.cloud_service_type import CLOUD_SERVICE_TYPES
from datetime import datetime
from pprint import pprint
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
        regions = params['regions']
        compartments = params['compartments']
        adb_conn: AutonomousDatabaseConnector = self.locator.get_connector(self.connector_name, **params)
        autonomous_database_list = []
        adb_container = []
        adb_exadata_infra = []
        #
        # for autonomous_database in autonomous_databases:
        #     pprint(autonomous_database)

        for region in regions:
            secret_data['region'] = region
            adb_conn.set_connect(secret_data)
            for compartment in compartments:
                basic_adb_list = adb_conn.list_of_autonomous_databases(region, compartment)
                if basic_adb_list:
                     ddd = self._set_mandatory_param(basic_adb_list, region, compartment.name)
                     pprint(ddd)
                #autonomous_database_list.append()


        print(f'** Autonomous Database Finished {time.time() - start_time} Seconds **')
        return autonomous_database_list


    def _set_mandatory_param(self, adblist, region, comp_name):
        result = []

        for adb in adblist:
            adb_primitives = self.convert_nested_dictionary(self,adb)
            adb_primitives.update({
                'region': region,
                'compartment_name': comp_name
            })
            result.append(adb_primitives)

        return result
