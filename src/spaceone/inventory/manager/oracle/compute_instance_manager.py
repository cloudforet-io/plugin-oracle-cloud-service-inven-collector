from spaceone.inventory.libs.manager import OCIManager
from spaceone.inventory.libs.schema.base import ReferenceModel
from spaceone.inventory.model.compute_instance.data.compute import Compute
from spaceone.inventory.model.compute_instance.data.oracle_cloud import OracleCloud
from spaceone.inventory.model.compute_instance.data.os import OS
from spaceone.inventory.model.compute_instance.data.hardware import HardWare
from spaceone.inventory.connector.compute_instance import ComputeInstanceConnector


class ComputeInstanceManager(OCIManager):

    def __init__(self, transaction, **kwargs):
        super().__init__(transaction, **kwargs)
        self.connector_name = 'ComputeInstanceConnector'

    def get_server_info(self, instance, images):
        '''
                server_data = {
                    "os_type": "LINUX" | "WINDOWS"
                    "name": ""
                    "ip_addresses": [],
                    "primary_ip_address": "",
                    "data":  {
                        "os": {
                            "os_distro": "",
                            "os_details": "",
                            "os_arch": ""
                        },
                        "oracle_cloud": {
                            "fault_domain":"",
                            "launch_mode": "PARAVIRTUALIZED" | 'SR-IOV'
                            "boot_volume_type": "",
                            "network_type": "",
                            "tags": []
                        },
                        "compartment": {
                            "compartment_name": "",
                            "compartment_id": "",
                            "tenancy_id": ""
                        },
                        "hardware": {
                            "core": 0,
                            "memory": 0.0,
                            "cpu_model": ""
                        },
                        "compute": {
                            "keypair": "",
                            "ad": "",
                            "instance_state": "",
                            "instance_type": "",
                            "launched_at": "datetime",
                            "instance_id": "",
                            "instance_name": "",
                            "security_groups": [
                                {
                                    "id": "",
                                    "name": "",
                                    "display": ""
                                },
                                ...
                            ],
                            "image": "",
                            "account": "",
                            "tags": {
                                "image_id": "",
                                "firmware": "",
                                "id": ""
                            }
                        },
                    }
                }
        '''
        pass
