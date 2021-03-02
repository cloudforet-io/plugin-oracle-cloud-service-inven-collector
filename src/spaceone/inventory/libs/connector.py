import os
import oci
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

        secret_data(dict)
            - user
            - key_file
            - fingerprint
            - tenancy
            - region
        """

        super().__init__(transaction=None, config=None)
        self.client = None

    def set_connect(self, secret_data):
        # TODO: Set Oracle Client
        os.environ["USER_ID"] = secret_data['user']
        os.environ["KEY_CONTENT"] = secret_data['key_content']
        os.environ["FINGERPRINT"] = secret_data['fingerprint']
        os.environ["TENANCY"] = secret_data['tenancy']
        os.environ["OCI_REGION"] = secret_data['region']
        self.client = oci.identity.IdentityClient(secret_data)

    def verify(self, secret_data):
        # TODO: Verify Oracle Client
        try:
            oci.config.validate_config(secret_data)
        except Exception as e:
            print(f'[ERROR: ResourceInfo]: {e}')

        self.set_connect(secret_data)
        return "ACTIVE"
