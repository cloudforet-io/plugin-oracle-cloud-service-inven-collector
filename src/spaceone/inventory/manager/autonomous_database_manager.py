from spaceone.inventory.libs.manager import OCIManager
from spaceone.inventory.libs.schema.base import ReferenceModel
from spaceone.inventory.model.autonomous_database import *
from spaceone.inventory.model.autonomous_database.cloud_service import *
from spaceone.inventory.connector.autonomous_database import AutonomousDatabaseConnector
from spaceone.inventory.model.autonomous_database.cloud_service_type import CLOUD_SERVICE_TYPES
import time


class AutonomousDatabaseManager(OCIManager):

    def __init__(self, transaction, **kwargs):
        super().__init__(transaction, **kwargs)
        self.connector_name = 'AutonomousDatabaseConnector'
        self.cloud_service_types = CLOUD_SERVICE_TYPES

    def collect_cloud_service(self, params):
        #print(f"** Autonomous Database START ** // {params.get('region')} // {params.get('compartment').name}")
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
        adb_conn: AutonomousDatabaseConnector = self.locator.get_connector(self.connector_name, **params)
        autonomous_database_list = []
        adb_conn.set_connect(secret_data)
        basic_adb_list = adb_conn.list_of_autonomous_databases(params['compartment'])

        for basic_adb in basic_adb_list:
            adb_raw = self.convert_nested_dictionary(self, basic_adb)
            adb_raw.update({
                'region': region,
                'compartment_name': compartment.name,
                '_freeform_tags': self.convert_tags(adb_raw['_freeform_tags']),
                'db_workload_display': self._set_workload_type(adb_raw['_db_workload']),
                'size': OCIManager.gigabyte_to_byte(adb_raw['_data_storage_size_in_gbs']),  # 바이트 단위로 정규화 후 넣어주기
                '_data_storage_size_in_tbs': self.gbs_to_tbs(adb_raw['_data_storage_size_in_gbs']),
                '_license_model': self.define_license_type(adb_raw['_license_model']),
                '_permission_level': self.define_permission_level(adb_raw['_permission_level']),
                'list_autonomous_backup': self._set_backup_list(
                    adb_conn.list_autonomous_database_backup(adb_raw['_id'])),
                'list_autonomous_database_clones': self._set_clone_list(
                    adb_conn.list_autonomous_database_clones(adb_raw['_compartment_id'],
                                                             adb_raw['_id']))
            })

            autonomous_db_data = Database(adb_raw, strict=False)
            autonomous_db_resource = DatabaseResource({
                'data': autonomous_db_data,
                'region_code': autonomous_db_data.region,
                'reference': ReferenceModel(autonomous_db_data.reference()),
                'tags': adb_raw['_freeform_tags']
            })
            # self.set_region_code(autonomous_db_data.region)
            autonomous_database_list.append(DatabaseResponse({'resource': autonomous_db_resource}))
            # Must set_region_code method for region collection

        if basic_adb_list:
            print(f"SET REGION CODE FROM AUTONOMOUS DB... {params.get('region')} // {params.get('compartment').name}")
            self.set_region_code(region)

            # raw_data = self._set_mandatory_param(adb_conn, basic_adb_list,
            #                                      params['region'], params['compartment'].name)

            # autonomous_database_list.extend(self._set_resources(raw_data))
        ''' 
        for region in regions:
            secret_data['region'] = region
            adb_conn.set_connect(secret_data)
            for compartment in compartments:
                basic_adb_list = adb_conn.list_of_autonomous_databases(compartment)
                if basic_adb_list:
                    raw_data = self._set_mandatory_param(adb_conn, basic_adb_list, region, compartment.name)

                    # Must set_region_code method for region collection
                    self.set_region_code(region)
                    autonomous_database_list.extend(self._set_resources(raw_data))
        '''
        # print(f'** Autonomous Database Finished {time.time() - start_time} Seconds **')
        return autonomous_database_list

    def _set_resources(self, raw_data):
        result = []
        for raw in raw_data:
            autonomous_db_data = Database(raw, strict=False)
            autonomous_db_resource = DatabaseResource({
                'data': autonomous_db_data,
                'region_code': autonomous_db_data.region,
                'reference': ReferenceModel(autonomous_db_data.reference()),
                'tags': raw['_freeform_tags']
            })
            # self.set_region_code(autonomous_db_data.region)
            result.append(DatabaseResponse({'resource': autonomous_db_resource}))

        return result

    def _set_mandatory_param(self, adb_conn, adblist, region, comp_name):
        result = []

        for adb in adblist:
            adb_primitives = self.convert_nested_dictionary(self,adb)
            adb_primitives.update({
                'region': region,
                'compartment_name': comp_name,
                '_freeform_tags': self.convert_tags(adb_primitives['_freeform_tags']),
                'db_workload_display': self._set_workload_type(adb_primitives['_db_workload']),
                'size': OCIManager.gigabyte_to_byte(adb_primitives['_data_storage_size_in_gbs']),# 바이트 단위로 정규화 후 넣어주기
                '_data_storage_size_in_tbs': self.gbs_to_tbs(adb_primitives['_data_storage_size_in_gbs']),
                '_license_model': self.define_license_type(adb_primitives['_license_model']),
                '_permission_level': self.define_permission_level(adb_primitives['_permission_level']),
                'list_autonomous_backup': self._set_backup_list(
                    adb_conn.list_autonomous_database_backup(adb_primitives['_id'])),
                'list_autonomous_database_clones': self._set_clone_list(
                    adb_conn.list_autonomous_database_clones(adb_primitives['_compartment_id'],
                                                             adb_primitives['_id']))
            })
            result.append(adb_primitives)

        return result

    def _set_backup_list(self, backup_list):
        result = []
        for backup in backup_list:
            backup_primitives = self.convert_nested_dictionary(self, backup)
            result.append(backup_primitives)

        return result

    def _set_clone_list(self, clone_list):
        result = []
        for clone in clone_list:
            clone_primitives = self.convert_nested_dictionary(self, clone)
            result.append(clone_primitives)
        return result

    @staticmethod
    def _set_workload_type(db_workload):
        if db_workload == 'OLTP':
            db_workload = 'Autonomous Transaction Processing'
        elif db_workload == 'DW':
            db_workload = 'Autonomous Data Warehouse'
        elif db_workload == 'AJD':
            db_workload = 'Autonomous JSON'
        else:
            db_workload = 'Autonomous Database with the Oracle APEX Application'

        return db_workload

    @staticmethod
    def convert_tags(tags):
        return [{'key': tag, 'value': tags[tag]} for tag in tags]

    @staticmethod
    def gbs_to_tbs(gbs):
        return gbs*0.001

    @staticmethod
    def define_license_type(license_model):
        if license_model == 'LICENSE_INCLUDED':
            license_model = 'License Included'
        else:
            license_model = 'Bring Your Own license'
        return license_model

    @staticmethod
    def define_permission_level(permission_level):
        if permission_level == 'RESTRICTED':
            permission_level = 'Allow access only to admin users'
        else:
            permission_level = 'Allow secure access from everywhere'

        return permission_level


