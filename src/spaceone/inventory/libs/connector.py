import os

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
            - type: ..
            - project_id: ...
            - token_uri: ...
            - ...
        """

        super().__init__(transaction=None, config=None)

    def set_connect(self, secret_data):
        pass

    def verify(self, **kwargs):
        self.set_connect(**kwargs)
        return "ACTIVE"
