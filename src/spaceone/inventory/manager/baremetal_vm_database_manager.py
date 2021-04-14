from spaceone.inventory.libs.manager import OCIManager
from spaceone.inventory.libs.schema.base import ReferenceModel
from spaceone.inventory.model.baremetal_vm_database import *
from spaceone.inventory.model.baremetal_vm_database.cloud_service import *
from spaceone.inventory.connector.baremetal_vm_database import BareMetalVMDatabaseConnector
from spaceone.inventory.model.baremetal_vm_database.cloud_service_type import CLOUD_SERVICE_TYPES
from oci.database.models import DbSystemSummary
import time


class BareMetalVMDatabaseManager(OCIManager):

    def __init__(self, transaction, **kwargs):
        super().__init__(transaction, **kwargs)
        self.connector_name = 'BareMetalVMDatabaseConnector'
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
        bmvm_conn: BareMetalVMDatabaseConnector = self.locator.get_connector(self.connector_name, **params)
        bmvm_conn.set_connect(secret_data)

        # Get list of BareMetal,VM Database Resources
        basic_bmvm_dbsystem_list = bmvm_conn.list_database_dbsystems(params['compartment'])
        bmvm_images_list = bmvm_conn.list_database_images(params['compartment'])
        bmvm_backup_list = bmvm_conn.list_database_backups(params['compartment'])
        bmvm_database = []
        for db_system in basic_bmvm_dbsystem_list:
            '''
            if db_system.lifecycle_state == DbSystemSummary.LIFECYCLE_STATE_TERMINATED:
                continue
            '''
            db_system_raw = self.convert_nested_dictionary(self, db_system)
            db_homes = bmvm_conn.list_database_home(compartment, db_system_raw['_id'])
            db_nodes, node_conn = self._collect_db_nodes(bmvm_conn, compartment, db_system_raw.get('_id'))
            db_system_raw.update({
                'region': region,
                'compartment_name': compartment.name,
                '_db_system_options': self.convert_nested_dictionary(self, db_system_raw['_db_system_options']),
                '_maintenance_window': bmvm_conn.load_database_maintenance_windows(db_system_raw['_maintenance_window']),
                '_freeform_tags':  self.convert_tags(db_system_raw['_freeform_tags']),
                'last_maintenance_run': bmvm_conn.load_maintenance_run(db_system_raw['_last_maintenance_run_id'],
                                                                       db_system_raw['_display_name']+' - ' +
                                                                       db_system_raw['_shape']),
                'next_maintenance_run': bmvm_conn.load_maintenance_run(db_system_raw['_next_maintenance_run_id'],
                                                                       db_system_raw['_display_name'] + ' - ' +
                                                                       db_system_raw['_shape']),
                'list_db_Home': self._convert_database_homes(db_homes),
                'list_database': self._collect_matched_database(bmvm_conn, compartment, db_homes),
                'list_db_node': db_nodes,
                'console_connections': node_conn,
                'list_patch_history': self._collect_db_system_patch_history(bmvm_conn, db_system_raw.get('_id')),
                'list_patches': self._collect_db_system_patch(bmvm_conn, db_system_raw.get('_id')),
                'list_backups': self._convert_object_to_list(bmvm_backup_list),
                'list_software_images': self._update_software_images(bmvm_images_list)
            })

            db_system_data = DbSystem(db_system_raw, strict=False)
            db_system_resource = DBSystemsResource({
                'data': db_system_raw,
                'region_code': region,
                'reference': ReferenceModel(db_system_data.reference()),
                'tags': db_system_raw.get('_freeform_tags', [])
            })
            bmvm_database.append(DBSystemResponse({'resource': db_system_resource}))
            bmvm_database.extend(self.set_database_resources(db_system_raw.get('list_database', []), region))
            bmvm_database.extend(self.set_image_resources(db_system_raw.get('list_software_images', []), region))
            bmvm_database.extend(self.set_backup_resources(db_system_raw.get('list_backups', []), region))

            if bmvm_database:
                print(f"SET REGION CODE FROM BareMetal,VM DB... {params.get('region')} // {params.get('compartment').name}")
                self.set_region_code(region)

        return bmvm_database

    @staticmethod
    def _set_database_resources(databases, region):
        result = []
        for database in databases:
            database_data = Database(database, strict= False)
            database_resource = DatabaseResource({
                'data': database_data,
                'region_code': region,
                'tags': database.get('_freeform_tags', [])
            })
            result.append(DatabaseResponse({'resource': database_resource}))
        return result

    def _convert_database_homes(self, db_homes):
        result = []
        for db_home in db_homes:
            result.append(self.convert_dictionary(db_home))
        return result

    def _convert_object_to_list(self, lists):
        result = []
        for ob in lists:
            result.append(self.convert_nested_dictionary(self, ob))
        return result

    def _collect_matched_database(self, bmvm_conn, compartment, db_homes):
        result = []
        for db_home in db_homes:
            raws = bmvm_conn.list_bmvm_databases(compartment, db_home.id)
            for raw in raws:
                raw = self.convert_nested_dictionary(self, raw)
                conn_strings = self.convert_nested_dictionary(self,raw.get('_connection_strings'))
                conn_strings.update({
                    '_all_connection_strings': self.convert_tags(conn_strings.get('_all_connection_strings'))
                })

                raw.update({
                    '_connection_strings': conn_strings,
                    '_freeform_tags': self.convert_tags(raw.get('_freeform_tags')),
                    'list_upgrade_history': self._convert_object_to_list(
                        bmvm_conn.list_db_upgrade_history(raw.get('_id'))),
                    'list_dataguard_association': self._convert_object_to_list(
                        bmvm_conn.list_dataguard_associations(raw.get('_id')))
                })
                result.append(raw)
        return result

    def _collect_db_nodes(self, bmvm_conn, compartment, system_id):
        result = []
        node_console = []
        raws = bmvm_conn.list_database_nodes(compartment, system_id)

        for raw in raws:
            raw = self.convert_nested_dictionary(self, raw)
            node_connect = self.convert_nested_dictionary(self,bmvm_conn.list_console_connection(raw.get('_id')))
            raw.update({
                'console_connections': node_connect
            })
            result.append(raw)
            node_console.append(node_connect)
        return result, node_console

    def _collect_db_system_patch_history(self,bmvm_conn, system_id):
        result = []
        raws = bmvm_conn.list_db_system_patch_history(system_id)
        for raw in raws:
            raw = self.convert_dictionary(raw)
            result.append(raw)
        return result

    def _collect_db_system_patch(self, bmvm_conn, system_id):
        result = []
        raws = bmvm_conn.list_db_system_patch(system_id)

        for raw in raws:
            raw = self.convert_nested_dictionary(self, raw)
            result.append(raw)
        return result

    def _change_backups_to_dict(self, backup_list):
        result = []
        for backup in backup_list:
            backup = self.convert_nested_dictionary(self, backup)
            result.append(backup)
        return result

    def _update_software_images(self, image_list):
        result = []
        for image in image_list:
            image = self.convert_nested_dictionary(self,image)
            image.update({
                '_freeform_tags': self.convert_tags(image.get('_freeform_tags'))
            })
            result.append(image)
        return result

    @staticmethod
    def set_database_resources(databases, region):
        result = []
        for database in databases:
            database_data = Database(database, strict=False)
            database_resource = DatabaseResource({
                'data': database_data,
                'region_code': region,
                'tags': database.get('_freeform_tags', [])
            })
            result.append(DatabaseResponse({'resource': database_resource}))
        return result

    @staticmethod
    def set_image_resources(images, region):
        result = []
        for image in images:
            image_data = DatabaseSoftwareImage(image, strict=False)
            image_resource = DatabaseResource({
                'data': image_data,
                'region_code': region,
                'tags': image.get('_freeform_tags', [])
            })
            result.append(DatabaseResponse({'resource': image_resource}))
        return result

    @staticmethod
    def set_backup_resources(backups, region):
        result = []
        for backup in backups:
            backup_data = Backup(backup, strict=False)
            backup_resource =  BackupResource({
                'data': backup_data,
                'region_code': region,
                'tags': backup.get('_freeform_tags', [])
            })
            result.append(BackupResponse({'resource': backup_resource}))
        return result

    @staticmethod
    def convert_tags(tags):
        return [{'key': tag, 'value': tags[tag]} for tag in tags]



