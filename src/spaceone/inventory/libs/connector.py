import os
import oci
from spaceone.core.error import *
from spaceone.core.connector import BaseConnector


DEFAULT_SCHEMA = 'azure_client_secret'


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
        self.identity = None

    def set_connect(self, secret_data):
        # TODO: Set Oracle Client
        config = None
        self.identity = oci.identity.IdentityClient(config)

    def verify(self, secret_data):
        # TODO: Verify Oracle Client
        oci.config.validate_config(secret_data)
        return "ACTIVE"
