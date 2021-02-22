import logging

from spaceone.inventory.libs.connector import OCIConnector
from spaceone.inventory.error import *

__all__ = ['AutonomousDatabaseConnector']
_LOGGER = logging.getLogger(__name__)


class AutonomousDatabaseConnector(OCIConnector):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_connect(kwargs.get('secret_data'))

    def list_autonomous_databases(self):
        # TODO
        # Need using Paginator
        pass
