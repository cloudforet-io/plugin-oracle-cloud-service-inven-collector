import logging
import oci
from spaceone.inventory.libs.connector import OCIConnector
import datetime
from spaceone.inventory.error import *

__all__ = ['BareMetalVMDatabaseConnector']
_LOGGER = logging.getLogger(__name__)


class BareMetalVMDatabaseConnector(OCIConnector):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.secret_data = kwargs.get('secret_data')
        self.set_connect(kwargs.get('secret_data'))

    def list_database_dbsystems(self, compartment):
        result = []
        try:
            '''
            result = oci.pagination.list_call_get_all_results(
                self.database_client.list_db_systems,
                compartment.id,
                sort_by="TIMECREATED"
            ).data
            '''
            result = oci.pagination.list_call_get_all_results(
                self.database_client.list_db_systems,
                compartment.id,
                sort_by="DISPLAYNAME"
            ).data
        except oci.exceptions.ServiceError as e:
            print(f'[ERROR: OCI API Info]: {e}')
            pass

        return result

    def list_bmvm_databases(self, compartment, dbhome_id):
        result = []
        try:
            result = oci.pagination.list_call_get_all_results(
                self.database_client.list_databases,
                compartment.id,
                db_home_id=dbhome_id
            ).data
        except oci.exceptions.ServiceError as e:
            print(f'[ERROR: OCI API Info]: {e}')
            pass

        return result

    def list_database_images(self, compartment):
        result = []
        try:
            result = oci.pagination.list_call_get_all_results(
                self.database_client.list_database_software_images,
                compartment.id,
                image_shape_family='VM_BM_SHAPE'
            ).data
        except oci.exceptions.ServiceError as e:
            print(f'[ERROR: OCI API Info]: {e}')
            pass

        return result

    def list_database_backups(self, compartment):
        result = []
        try:
            result = oci.pagination.list_call_get_all_results(
                self.database_client.list_backups,
                compartment_id=compartment.id
            ).data
        except oci.exceptions.ServiceError as e:
            print(f'[ERROR: OCI API Info]: {e}')
            pass

        return result

    def list_database_nodes(self,compartment, dbsystem_id):
        result = []
        try:
            result = oci.pagination.list_call_get_all_results(
                self.database_client.list_db_nodes,
                compartment.id,
                db_system_id= dbsystem_id
            ).data
        except oci.exceptions.ServiceError as e:
            print(f'[ERROR: OCI API Info]: {e}')
            pass

        return result

    def list_database_home(self, compartment, dbsystem_id):
        result = []
        try:
            result = oci.pagination.list_call_get_all_results(
                self.database_client.list_db_homes,
                compartment.id,
                db_system_id=dbsystem_id
            ).data
        except oci.exceptions.ServiceError as e:
            print(f'[ERROR: OCI API Info]: {e}')
            pass

        return result

    def list_db_system_patch_history(self, dbsystem_id):
        result = []
        try:
            result = oci.pagination.list_call_get_all_results(
                self.database_client.list_db_homes,
                dbsystem_id
            ).data
        except oci.exceptions.ServiceError as e:
            print(f'[ERROR: OCI API Info]: {e}')
            pass

        return result

    def list_db_system_patch(self, dbsystem_id):
        result = []
        try:
            result = oci.pagination.list_call_get_all_results(
                self.database_client.list_db_system_patches,
                dbsystem_id
            ).data
        except oci.exceptions.ServiceError as e:
            print(f'[ERROR: OCI API Info]: {e}')
            pass

        return result

    def list_dataguard_associations(self, database_id):
        result = []
        try:
            result = oci.pagination.list_call_get_all_results(
                self.database_client.list_data_guard_associations,
                database_id=database_id
            ).data
        except oci.exceptions.ServiceError as e:
            print(f'[ERROR: OCI API Info]: {e}')
            pass

        return result

    def list_console_connection(self, node_id):
        result = []
        try:
            result = oci.pagination.list_call_get_all_results(
                self.database_client.list_console_connections,
                node_id
            ).data
        except oci.exceptions.ServiceError as e:
            print(f'[ERROR: OCI API Info]: {e}')
            pass

        return result

    def list_db_upgrade_history(self, db_id):
        result = []
        try:
            result = oci.pagination.list_call_get_all_results(
                self.database_client.list_database_upgrade_history_entries,
                db_id
            ).data
        except oci.exceptions.ServiceError as e:
            print(f'[ERROR: OCI API Info]: {e}')
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



