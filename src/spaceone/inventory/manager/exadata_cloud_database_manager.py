from spaceone.inventory.libs.manager import OCIManager
from spaceone.inventory.libs.schema.base import ReferenceModel
from spaceone.inventory.model.exadata_cloud_database import *
from spaceone.inventory.model.exadata_cloud_database.cloud_service import *
from spaceone.inventory.connector.exadata_cloud_database import ExadataCloudDatabaseConnector
from spaceone.inventory.model.exadata_cloud_database.cloud_service_type import CLOUD_SERVICE_TYPES
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

        result = []
        basic_exadata_infra_list = exa_conn.list_cloud_exadata_infra(compartment)
        exadata_image_list = exa_conn.list_database_images(compartment)
        exadata_software_image_response = self.set_image_resource(exadata_image_list, region, compartment)
        result.extend(exadata_software_image_response)

        for exadata_infra in basic_exadata_infra_list:
            exadata_infra_raw = self.convert_nested_dictionary(self, exadata_infra)
            list_vm_cluster = exa_conn.list_cloud_vm_cluster(region, compartment, exa_conn, exadata_infra_raw['_id'])
            exadata_infra_raw.update({
                'region': region,
                'compartment_name': compartment.name,
                '_maintenance_window': exa_conn.load_database_maintenance_windows(exadata_infra_raw['_maintenance_window']),
                '_freeform_tags': self.convert_tags(exadata_infra_raw['_freeform_tags']),
                'last_maintenance_run': exa_conn.load_maintenance_run(exadata_infra_raw['_last_maintenance_run_id'],
                                                                      exadata_infra_raw['_display_name']+' - '+
                                                                      exadata_infra_raw['_shape']),
                'next_maintenance_run': exa_conn.load_maintenance_run(exadata_infra_raw['_next_maintenance_run_id'],
                                                                      exadata_infra_raw['_display_name']+' - '+
                                                                      exadata_infra_raw['_shape']),
                'list_cloud_vm_cluster': self.set_vm_cluster_data(region, compartment, exa_conn, list_vm_cluster)
            })
            exadata_vm_cluster_list = exadata_infra_raw.get['list_cloud_vm_cluster']
            exadata_vm_database_list,  exadata_vm_database_backup_list = \
                self.set_database_resource(exadata_vm_cluster_list, region)
            exadata_backup_response_list = self.set_backup_resource(exadata_vm_database_backup_list, region, compartment)

            exadata_infra_data = CloudExadataInfra(exadata_infra_raw, strict=False)
            exadata_infra_resource = ExadataInfrastructureResource({
                'data': exadata_infra_data,
                'region_code': region,
                'reference': ReferenceModel(exadata_infra_data.reference()),
                'tags': exadata_infra_raw.get('_freeform_tags', [])
            })
            result.append(ExadataInfrastructureResponse({'resource': exadata_infra_resource}))
            result.extend(exadata_vm_database_list)
            result.extend(exadata_backup_response_list)


        return result

    def set_vm_cluster_data(self, region, compartment, exa_conn, vm_cluster_list):
        result = []
        for vm_cluster in vm_cluster_list:
            vm_cluster_raw = self.convert_nested_dictionary(self, vm_cluster)
            db_home, home_id = self.get_vm_cluster_db_home(exa_conn, compartment, vm_cluster_raw['_id'])
            databases, backups = self.set_vm_cluster_database(exa_conn, compartment, home_id)
            vm_cluster_raw.update({
                'region': region,
                'compartment_name': compartment.name,
                '_freeform_tags': self.convert_tags(vm_cluster_raw['_freeform_tags']),
                'list_update_history': self.set_vm_cluster_update_history(exa_conn, vm_cluster_raw['_id']),
                'list_update': self.set_vm_cluster_update(exa_conn, vm_cluster_raw['_id']),
                'list_db_home': db_home,
                'list_db_node': self.set_vm_cluster_db_node(exa_conn, compartment, vm_cluster_raw['_id']),
                'list_database': databases,
                'list_backup': backups
            })
            result.append(vm_cluster_raw)
        return result


    def set_vm_cluster_update_history(self, exa_conn, cloud_vm_cluster_id):
        result = []
        update_histories = exa_conn.list_vm_cluster_update_history(cloud_vm_cluster_id)
        for update_history in update_histories:
            update_history_raw = self.convert_dictionary(update_history)
            result.append(update_history_raw)
        return result

    def set_vm_cluster_update(self, exa_conn, cloud_vm_cluster_id):
        result = []
        cluster_updates = exa_conn.list_cloud_vm_cluster_update(cloud_vm_cluster_id)
        for cluster_update in cluster_updates:
            result.append(self.convert_dictionary(cluster_update))
        return result

    def get_vm_cluster_db_home(self, exa_conn ,compartment, cloud_cluster_id):
        result = []
        home_id = []
        db_homes = exa_conn.list_exadata_db_home(compartment, cloud_cluster_id)
        for db_home in db_homes:
            db_home_raw = self.convert_dictionary(db_home)
            result.append(db_home_raw)
            home_id.append((db_home_raw['_id'], db_home_raw['_db_version']))
        return result, home_id

    def set_vm_cluster_db_node(self, exa_conn, compartment, vm_cluster_id):
        result = []
        db_nodes = exa_conn.list_exadata_database_nodes(compartment, vm_cluster_id)
        for node in db_nodes:
            list_connection = []
            node_raw = self.convert_nested_dictionary(self, node)
            connections = exa_conn.list_exadata_console_connection(node_raw['_id'])
            for connection in connections:
                connection_raw = self.convert_nested_dictionary(self,connection)
                list_connection.append(connection_raw)

            node_raw.update({
                'console_connections': list_connection
            })
            result.append(node_raw)

        return result

    def set_vm_cluster_database(self, exa_conn, compartment, db_home_id_list):
        result = []
        backup_list = []
        for db_home_id, db_version in db_home_id_list:
            databases = exa_conn.list_exadata_databases(compartment, db_home_id)
            for database in databases:
                database_raw = self.convert_nested_dictionary(self, database)
                database_raw.update({
                    'db_version': db_version,
                    '_freeform_tags': self.convert_tags(database_raw['_freeform_tags']),
                    'list_upgrade_history': self.set_vm_cluster_database_upgrade_history(exa_conn, database_raw['_id']),
                    'list_dataguard_association': self.set_vm_cluster_database_dataguardassociation(exa_conn, database_raw['_id'])
                })
                result.append(database_raw)
                backup_list.extend(self.set_vm_cluster_database_backup(exa_conn, database_raw['_id']))
        return result, backup_list

    def set_vm_cluster_database_upgrade_history(self, exa_conn, db_id):
        upgrade_history_list = exa_conn.list_exadata_db_upgrade_history(db_id)
        result = []
        for upgrade_history in upgrade_history_list:
            upgrade_history_raw = self.convert_dictionary(upgrade_history)
            result.append(upgrade_history_raw)

        return result

    def set_vm_cluster_database_dataguardassociation(self, exa_conn, db_id):
        result = []
        association_list = exa_conn.list_exadata_dataguard_associations(db_id)
        for association in association_list:
            association_raw = self.convert_nested_dictionary(self, association)
            result.append(association_raw)

        return result

    def set_vm_cluster_database_backup(self, exa_conn, db_id):
        result = []
        backup_list = exa_conn.list_database_backups(db_id)
        for backup in backup_list:
            backup_raw = self.convert_nested_dictionary(self, backup)
            result.append(backup_raw)

        return result

    def set_image_resource(self, image_list, region, compartment):
        result = []
        for image in image_list:
            image = self.convert_dictionary(image)
            image.update({
                'region': region,
                'compartment_name': compartment.name,
                '_freeform_tags': self.convert_tags(image.get('_freeform_tags'))
            })

            image_data = DatabaseSoftwareImage(image, strict=False)
            image_resource = ExadataDatabaseSoftwareImageResource({
                'data': image_data,
                'region_code': region,
                'reference': ReferenceModel(image_data.reference()),
                'tags': image.get('_freeform_tags', [])
            })
            result.append(ExadataDatabaseSoftwareImageResponse({'resource': image_resource}))

        return result

    @staticmethod
    def set_database_resource(vm_cluster_list, region):
        result = []
        backup_list = []
        for vm_cluster in vm_cluster_list:
            db_list = vm_cluster.get('list_database', [])
            db_backup = vm_cluster.get('list_backup', [])

            for db in db_list:
                db_data = Database(db, strict=False)
                db_resource = ExadataDatabaseResource({
                    'data': db_data,
                    'region_code': region,
                    'reference': ReferenceModel(db_data.reference()),
                    'tags': db.get('_freeform_tags', [])
                })
                result.append(ExadataDatabaseResponse({'resource': db_resource}))
                backup_list.extend(db_backup)
        return result, backup_list

    @staticmethod
    def set_backup_resource(backup_list, region, compartment):
        result = []
        for backup in backup_list:
            backup.update({'region': region, 'compartment_name': compartment.name})
            backup_data = Backup(backup, strict=False)
            backup_resource = ExadataBackupResource({
                'data': backup_data,
                'region_code': region,
                'reference': ReferenceModel(backup_data.reference()),
                'tags': backup.get('_freeform_tags', [])
            })
            result.append(ExadataBackupResponse({'resource': backup_resource}))
        return result

    @staticmethod
    def convert_tags(tags):
        return [{'key': tag, 'value': tags[tag]} for tag in tags]


