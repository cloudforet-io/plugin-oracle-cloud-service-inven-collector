import oci
from oci.identity import IdentityClient
from oci.database.database_client import DatabaseClient
from spaceone.core.error import *
from spaceone.core.connector import BaseConnector


DEFAULT_SCHEMA = 'oci_client_secret'


class OCIConnector(BaseConnector):

    def __init__(self, **kwargs):
        """
        kwargs
            - schema
            - options
            - secret_data
            - regions
            - compartments

        secret_data(dict)
            - user
            - key_file
            - fingerprint
            - tenancy
            - region
        """

        super().__init__(transaction=None, config=None)
        self.identity_client = None
        self.database_client = None

    def set_connect(self, secret_data):
        self.identity_client = IdentityClient(secret_data)
        self.database_client = DatabaseClient(secret_data)
        '''
        clients = []
        for clint in client_list:
            self.identity_client = IdentityClient(secret_data)
            self.database_client = DatabaseClient(secret_data)
        
        self.clints = clients
        '''


    def verify(self, secret_data):
        # TODO: Verify Oracle Client
        try:
            oci.config.validate_config(secret_data)
        except Exception as e:
            print(f'[ERROR: ResourceInfo]: {e}')

        self.set_connect(secret_data)
        return "ACTIVE"
