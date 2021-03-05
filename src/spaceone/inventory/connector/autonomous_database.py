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
        self.regions = kwargs.get('regions')
        self.compartments = kwargs.get('compartments')

    def list_of_autonomous_databases(self):
        # TODO
        # Need using Paginator
        result = []
        for region in self.regions:
            self.secret_data['region'] = region
            self.set_connect(self.secret_data)
            for compartment in self.compartments:
                list_autonomous_db = []
                if compartment.id != self.secret_data['tenancy'] and \
                        compartment.lifecycle_state != oci.identity.models.Compartment.LIFECYCLE_STATE_ACTIVE:
                    continue
                try:
                    list_autonomous_db = oci.pagination.list_call_get_all_results(
                        self.database_client.list_autonomous_databases,
                        compartment.id,
                        sort_by= "TIMECREATED"
                    ).data
                    list_autonomous_db.append({'region': region, 'compartment_name': str(compartment.name)})
                    result.append(list_autonomous_db)

                except oci.exceptions.ServiceError as e:
                    print(f'[ERROR: OCI API Info]: {e}')
                    continue

        return result

    def list_autonomous_container_database(self):
        result = []
        for region in self.regions:
            self.secret_data['region'] = region
            self.set_connect(self.secret_data)
            for compartment in self.compartments:
                list_autonomous_container_db = []
                if compartment.id != self.secret_data['tenancy'] and \
                        compartment.lifecycle_state != oci.identity.models.Compartment.LIFECYCLE_STATE_ACTIVE:
                    continue
                try:
                    list_autonomous_container_db = oci.pagination.list_call_get_all_results(
                        self.database_client.list_autonomous_container_databases,
                        compartment.id,
                        sort_by= "TIMECREATED"
                    ).data
                    list_autonomous_container_db.append({'region': region, 'compartment_name': str(compartment.name)})
                    result.append(list_autonomous_container_db)
                except oci.exceptions.ServiceError as e:
                    print(f'[ERROR: OCI API Info]: {e}')
                    continue

        return result

    def list_autonomous_exadata_infrastructures(self):
        result = []
        for region in self.regions:
            self.secret_data['region'] = region
            self.set_connect(self.secret_data)
            for compartment in self.compartments:
                list_autonomous_exadata_infra = []
                if compartment.id != self.secret_data['tenancy'] and \
                        compartment.lifecycle_state != oci.identity.models.Compartment.LIFECYCLE_STATE_ACTIVE:
                    continue
                try:
                    list_autonomous_exadata_infra = oci.pagination.list_call_get_all_results(
                        self.database_client.list_autonomous_exadata_infrastructures,
                        compartment.id,
                        sort_by= "TIMECREATED"
                    ).data
                    list_autonomous_exadata_infra.append({'region': region, 'compartment_name': str(compartment.name)})
                    result.append(list_autonomous_exadata_infra)
                except oci.exceptions.ServiceError as e:
                    print(f'[ERROR: OCI API Info]: {e}')
                    continue
        return result




