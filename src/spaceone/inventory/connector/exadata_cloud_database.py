import logging
import oci
from spaceone.inventory.libs.connector import OCIConnector
import datetime
from pprint import pprint
from spaceone.inventory.error import *

__all__ = ['ExadataCloudDatabaseConnector']
_LOGGER = logging.getLogger(__name__)


class ExadataCloudDatabaseConnector(OCIConnector):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.secret_data = kwargs.get('secret_data')
        self.set_connect(kwargs.get('secret_data'))

    def list_database_images(self, compartment):
        if compartment.name == 'ManagedCompartmentForPaaS':
            return []

        result = []
        try:
            result = oci.pagination.list_call_get_all_results(
                self.database_client.list_database_software_images,
                compartment.id,
                image_shape_family='EXADATA_SHAPE'
            ).data
        except oci.exceptions.ServiceError as e:
            print(f'[ERROR: OCI EXADATA DB IMAGE API Info {compartment.name}]: {e}')
            pass

        return result

    def list_cloud_exadata_infra(self, compartment):
        result = []
        if compartment.name == 'ManagedCompartmentForPaaS':
            return []

        try:
            result = oci.pagination.list_call_get_all_results(
                self.database_client.list_cloud_exadata_infrastructures,
                compartment.id
            ).data
        except oci.exceptions.ServiceError as e:
            print(f'[ERROR: OCI ListCloudExadataInfra API Info AT {compartment.name}]: {e}')
            pass
        return result

    def list_cloud_vm_cluster(self, compartment, exadata_infra_id):
        result = []
        if compartment.name == 'ManagedCompartmentForPaaS':
            return []

        try:
            result = oci.pagination.list_call_get_all_results(
                self.database_client.list_cloud_vm_clusters,
                compartment.id,
                cloud_exadata_infrastructure_id = exadata_infra_id
            ).data
        except oci.exceptions.ServiceError as e:
            print(f'[ERROR: OCI ListCloudVMClusters API Info]: {e}')
            pass
        return result

    def list_vm_cluster_update_history(self, cluster_id):
        result = []

        try:
            result = oci.pagination.list_call_get_all_results(
                self.database_client.list_cloud_vm_cluster_update_history_entries,
                cloud_vm_cluster_id=cluster_id
            ).data
        except oci.exceptions.ServiceError as e:
            print(f'[ERROR: OCI ListCloudVMClustersUpdateHistory API Info]: {e}')
            pass
        return result

    def list_cloud_vm_cluster_update(self, cluster_id):
        result = []
        try:
            result  = oci.pagination.list_call_get_all_results(
                self.database_client.list_cloud_vm_cluster_updates,
                cloud_vm_cluster_id = cluster_id
            ).data
        except oci.exceptions.ServiceError as e:
            print(f'[ERROR: OCI ListCloudVMClustersUpdate API Info]: {e}')
            pass
        return result

    def list_exadata_db_home(self, compartment, cluster_id):
        result = []
        if cluster_id is None:
            return result
        try:
            result = oci.pagination.list_call_get_all_results(
                self.database_client.list_db_homes,
                compartment.id,
                vm_cluster_id = cluster_id
            ).data
        except oci.exceptions.ServiceError as e:
            print(f'[ERROR: OCI EXADATA CLOUD VM CLUSTER DB HOME API Info]: {e}')
            pass

        return result

    def list_exadata_database_nodes(self,compartment, cluster_id):
        result = []
        if cluster_id is None:
            return result
        try:
            result = oci.pagination.list_call_get_all_results(
                self.database_client.list_db_nodes,
                compartment.id,
                vm_cluster_id=cluster_id
            ).data
        except oci.exceptions.ServiceError as e:
            print(f'[ERROR: OCI EXADATA CLOUD VM DB NODE API Info]: {e}')
            pass

        return result

    def list_exadata_console_connection(self, node_id):
        result = []
        if node_id is None:
            return result
        try:
            result = oci.pagination.list_call_get_all_results(
                self.database_client.list_console_connections,
                node_id
            ).data
        except oci.exceptions.ServiceError as e:
            print(f'[ERROR: OCI EXADATA CLOUD CONSOLE API Info]: {e}')
            pass

        return result

    def list_exadata_databases(self, compartment, dbhome_id):
        result = []
        if dbhome_id is None:
            return result
        try:
            result = oci.pagination.list_call_get_all_results(
                self.database_client.list_databases,
                compartment.id,
                db_home_id=dbhome_id
            ).data
        except oci.exceptions.ServiceError as e:
            print(f'[ERROR: OCI EXADATA DATABASE API Info]: {e}')
            pass

        return result

    def list_exadata_dataguard_associations(self, database_id):
        result = []
        if database_id is None:
            return result
        try:
            result = oci.pagination.list_call_get_all_results(
                self.database_client.list_data_guard_associations,
                database_id=database_id
            ).data
        except oci.exceptions.ServiceError as e:
            print(f'[ERROR: OCI EXADATA DATAGUARD API Info]: {e}')
            pass

        return result

    def list_exadata_db_upgrade_history(self, db_id):
        result = []
        if db_id is None:
            return result
        try:
            result = oci.pagination.list_call_get_all_results(
                self.database_client.list_database_upgrade_history_entries,
                db_id
            ).data
        except oci.exceptions.ServiceError as e:
            print(f'[ERROR: OCI EXADATA UPGRADE API Info]: {e}')
            pass

        return result

    def list_database_backups(self, db_id):
        result = []
        try:
            result = oci.pagination.list_call_get_all_results(
                self.database_client.list_backups,
                database_id=db_id
            ).data
        except oci.exceptions.ServiceError as e:
            print(f'[ERROR: OCI EXADATA BACKUP API Info]: {e}')
            pass

        return result

    def load_maintenance_run(self, maintenance_run_id, db_system_name):
        try:
            if not maintenance_run_id:
                return {}
            mt = self.database_client.get_maintenance_run(maintenance_run_id).data
            val = {
                'id': str(mt.id),
                'display_name': str(mt.display_name),
                'description': str(mt.description),
                'lifecycle_state': str(mt.lifecycle_state),
                'time_scheduled ': mt.time_scheduled,
                'time_started': mt.time_started,
                'time_ended': mt.time_ended,
                'target_resource_type': str(mt.target_resource_type),
                'target_resource_id': str(mt.target_resource_id),
                'maintenance_type': str(mt.maintenance_type),
                'maintenance_subtype': str(mt.maintenance_subtype),
                'maintenance_display': str(mt.display_name) + " ( " + str(mt.maintenance_type) + ", " \
                                       + str(mt.maintenance_subtype) + ", " + str(mt.lifecycle_state) + " ), Scheduled: " \
                                       + str(mt.time_scheduled)[0:16] + ((", Execution: " + str(mt.time_started)[0:16] \
                                                                          + " - " + str(mt.time_ended)[0:16]) \
                                                                             if str(mt.time_started) != 'None' else ""),
                'maintenance_alert': ''
            }

            # If maintenance is less than 14 days
            if mt.time_scheduled:
                delta = mt.time_scheduled.date() - datetime.date.today()
                if delta.days <= 14 and delta.days >= 0 and not mt.time_started:
                    val['maintenance_alert'] = "DBSystem Maintenance is in " + str(delta.days).ljust(2, ' ') \
                                               + " days, on " + str(mt.time_scheduled)[0:16] + " for " + db_system_name

            return val

        except oci.exceptions.ServiceError as e:
            print(f'[ERROR: OCI API Info]: {e}')
            pass

    @staticmethod
    def load_database_maintenance_windows(maintenance_window):
        try:
            if not maintenance_window:
                return {}
            mw = maintenance_window
            value = {
                'preference': str(mw.preference),
                'months': ", ".join([x.name for x in mw.months]) if mw.months else "",
                'months': ", ".join([x.name for x in mw.months]) if mw.months else "",
                'weeks_of_month': ", ".join([str(x) for x in mw.weeks_of_month]) if mw.weeks_of_month else "",
                'hours_of_day': ", ".join([str(x) for x in mw.hours_of_day]) if mw.hours_of_day else "",
                'days_of_week': ", ".join([str(x.name) for x in mw.days_of_week]) if mw.days_of_week else "",
                'lead_time_in_weeks': str(mw.lead_time_in_weeks) if mw.lead_time_in_weeks else ""
            }
            value['display'] = str(mw.preference) if str(mw.preference) == "NO_PREFERENCE" else (
                        str(mw.preference) + ": Months: " + value['months'] + ", Weeks: " + value[
                    'weeks_of_month'] + ", DOW: " + value['days_of_week'] + ", Hours: " + value[
                            'hours_of_day'] + ", Lead Weeks: " + value['lead_time_in_weeks'])
            return value
        except Exception as e:
                print(f'[ERROR: OCI API Info]: {e}')
                pass

