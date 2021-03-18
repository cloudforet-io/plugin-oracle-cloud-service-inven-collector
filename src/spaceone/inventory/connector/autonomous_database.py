import logging
import oci
from spaceone.inventory.libs.connector import OCIConnector
from spaceone.inventory.error import *

__all__ = ['AutonomousDatabaseConnector']
_LOGGER = logging.getLogger(__name__)


class AutonomousDatabaseConnector(OCIConnector):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.secret_data = kwargs.get('secret_data')
        self.set_connect(kwargs.get('secret_data'))

    def list_of_autonomous_databases(self, compartment):
        result = []
        try:
            list_autonomous_db = oci.pagination.list_call_get_all_results(
                self.database_client.list_autonomous_databases,
                compartment.id,
                sort_by= "TIMECREATED"
            ).data

            result = list_autonomous_db

        except oci.exceptions.ServiceError as e:
            print(f'[ERROR: OCI API Info]: {e}')
            pass

        return result

    def list_autonomous_database_backup(self, autonomous_db_id):
        result = []

        try:
            result = self.database_client\
                            .list_autonomous_database_backups(autonomous_database_id=autonomous_db_id,
                                                             sort_by='TIMECREATED').data
        except oci.exceptions.ServiceError as e:
            print(f'[ERROR: OCI API Info]: {e}')
            pass

        return result

    def list_autonomous_database_clones(self,compartment_id, autonomous_db_id):
        result = []
        try:
            result = self.database_client.\
                    list_autonomous_database_clones(
                                        compartment_id=compartment_id,
                                        autonomous_database_id=autonomous_db_id).data

        except oci.exceptions.ServiceError as e:
            print(f'[ERROR: OCI API Info]: {e}')
            pass

        return result

    def list_autonomous_container_database(self,region, compartment):
        result = []
        list_autonomous_container_db = []

        try:
            list_autonomous_container_db = oci.pagination.list_call_get_all_results(
                self.database_client.list_autonomous_container_databases,
                compartment.id,
                sort_by="TIMECREATED"
            ).data
            list_autonomous_container_db.append({'region': region, 'compartment_name': str(compartment.name)})
            result.append(list_autonomous_container_db)

        except oci.exceptions.ServiceError as e:
            print(f'[ERROR: OCI API Info]: {e}')
            pass

        return result

    def list_autonomous_exadata_infrastructures(self, region, compartment):
        result = []
        list_autonomous_exadata_infra = []


        try:
            list_autonomous_exadata_infra = oci.pagination.list_call_get_all_results(
                self.database_client.list_autonomous_exadata_infrastructures,
                compartment.id,
                sort_by= "TIMECREATED"
            ).data
            result.append(list_autonomous_exadata_infra)
        except oci.exceptions.ServiceError as e:
            print(f'[ERROR: OCI API Info]: {e}')
            pass

        return result




