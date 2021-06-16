import oci
from oci.identity import IdentityClient
from oci.database.database_client import DatabaseClient
from oci.core.blockstorage_client import BlockstorageClient
from oci.core.compute_client import ComputeClient
from oci.core.compute_management_client import ComputeManagementClient
from oci.core.virtual_network_client import VirtualNetworkClient
from oci.load_balancer.load_balancer_client import LoadBalancerClient
from oci.network_load_balancer.network_load_balancer_client import NetworkLoadBalancerClient
from spaceone.core.error import *
from spaceone.core.connector import BaseConnector


DEFAULT_SCHEMA = 'oci_api_key'


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
        self.disk_client = None
        self.compute_client = None
        self.compute_management_client = None
        self.virtual_network_client = None
        self.load_balancer_client = None
        self.network_load_balancer_client = None

    def set_connect(self, secret_data):
        self.identity_client = IdentityClient(secret_data)
        self.database_client = DatabaseClient(secret_data)
        self.disk_client = BlockstorageClient(secret_data)
        self.compute_client = ComputeClient(secret_data)
        self.compute_management_client = ComputeManagementClient(secret_data)
        self.virtual_network_client = VirtualNetworkClient(secret_data)
        self.load_balancer_client = LoadBalancerClient(secret_data)
        self.network_load_balancer_client = NetworkLoadBalancerClient(secret_data)

    def verify(self, secret_data):
        # TODO: Verify Oracle Client
        try:
            oci.config.validate_config(secret_data)
        except Exception as e:
            print(f'[ERROR IN CLIENT VERIFY: ResourceInfo]: {e}')

        self.set_connect(secret_data)
        return "ACTIVE"
