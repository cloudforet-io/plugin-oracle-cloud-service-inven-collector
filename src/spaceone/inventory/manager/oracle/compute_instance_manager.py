from spaceone.inventory.libs.manager import OCIManager
from spaceone.inventory.libs.schema.base import ReferenceModel
from spaceone.inventory.model.compute_instance.data.compute import Compute
from spaceone.inventory.model.compute_instance.data.oracle_cloud import OracleCloud
from spaceone.inventory.model.compute_instance.data.os import OS
from spaceone.inventory.model.compute_instance.data.hardware import HardWare
from spaceone.inventory.model.compute_instance.data.compartment import Compartment
from spaceone.inventory.connector.compute_instance import ComputeInstanceConnector


class ComputeInstanceManager(OCIManager):

    def __init__(self, transaction, **kwargs):
        super().__init__(transaction, **kwargs)
        self.connector_name = 'ComputeInstanceConnector'

    def get_server_info(self, instance, images, network_security_groups, console_connections, compartment, tenancy_id):
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

        match_image = self._get_match_image(instance.get('image_id'), images)

        server_dict = self.get_server_dict(instance, match_image)
        os_data = self.get_os_data(match_image, self._get_os_type(match_image))
        oracle_data = self.get_oracle_data(instance)
        hardware_data = self._get_hardware_date(instance.get('shape_config'))
        compartment_data = self._get_compartment(compartment, tenancy_id)
        compute_data = self.get_compute_data(instance, match_image, console_connections,network_security_groups, tenancy_id)
        server_dict.update({
            'data': {
                'os': os_data,
                'oracle_cloud': oracle_data,
                'compartment': compartment_data,
                'hardware': hardware_data,
                'compute': compute_data
            }
        })

        return server_dict

    def get_server_dict(self, instance, image):
        server_data = {
            'name': instance.get('display_name', ''),
            'os_type': self._get_os_type(image),
            'region_code': instance.get('region')
        }

        return server_data

    def get_os_data(self, image, os_type):
        os_data = {
            'os_distro': self._get_os_distro(image.get('operating_system_version'), os_type),
            'os_details': image.get('display_name'),
            'os_arch': 'x86_64'
        }

        return OS(os_data, strict=False)

    def get_oracle_data(self, instance):
        launch_options = instance.get("launch_options")
        oracle_data = {
            'fault_domain': instance.get('fault_domain'),
            'launch_mode': instance.get('launch_mode'),
            'boot_volume_type' : launch_options.get('boot_volume_type'),
            'network_type': launch_options.get('network_type'),
            'tags': self._get_tags_only_string_values(instance.get("defined_tags"), instance.get("freeform_tags"))
        }

        return OracleCloud(oracle_data, strict=False)

    def get_compute_data(self, instance, image, console_connections, security_groups, tenancy_id):
        compute_data = {
            'keypair': self._get_console_connection(console_connections, instance.get('id')),
            'ad': instance.get('availability_domain'),
            'instance_state': instance.get('lifecycle_state'),
            'launched_at': instance.get('time_created'),
            'instance_id': instance.get('id'),
            'instance_name': instance.get('display_name'),
            'image': image.get('display_name'),
            'account': tenancy_id,
            'instance_type': instance.get('shape'),
            'security_groups': self._get_security_groups(security_groups),
            'tags': {
                'image_id': instance.get("image_id"),
                'firmware': instance["launch_options"]["firmware"],
                'id': instance.get('id')
            }
        }
        return Compute(compute_data, strict=False)

    @staticmethod
    def _get_os_distro(image_os_version, os_type):

        os_distro_string = None
        if os_type == 'WINDOWS':
            os_string_split = image_os_version.split()
            window_version_cmp = os_string_split[1]
            os_distro_string = f'win{window_version_cmp}'

            if 'R2' in os_string_split:
                os_distro_string = f'{os_distro_string}r2'

        elif os_type == 'LINUX':
            if 'Ubuntu' in image_os_version.split():
                return 'ubuntu'

            os_distro_string = ''.join(image_os_version.split()).lower()

        return os_distro_string

    @staticmethod
    def _get_os_type(image):
        return 'WINDOWS' if image.get('operating_system') == 'Windows' else 'LINUX'

    @staticmethod
    def _get_hardware_date(shape_config):
        hardware_data = {}
        hardware_data.update({
            'core': shape_config.get('ocpus'),
            'memory': shape_config.get('memory_in_gbs'),
            'cpu_model': shape_config.get('processor_description')
        })

        return HardWare(hardware_data, strict=False)



    @staticmethod
    def _get_match_image(image_id, images):
        for image in images:
            if image.get('image_id') == image_id:
                return image
        return {}

    @staticmethod
    def _get_tags_only_string_values(defined_tags, freeform_tags):
        tags = {}
        for k, v in defined_tags.items():
            if k == "Oracle-Tags":
                tags.update({
                    "CreatedBy": defined_tags["Oracle-tags"]["CreatedBy"]
                })

            if isinstance(v, str):
                tags.update({k: v})

        for k, v in freeform_tags.items():
            tags.update({k: v})

        return tags

    @staticmethod
    def _get_compartment(compartment, tenacy_id):
        compartment_data = {
            'compartment_name': compartment.name,
            'compartment_id': compartment.id,
            'tenancy_id': tenacy_id
        }

        return Compartment(compartment_data, strict=False)

    @staticmethod
    def _get_console_connection(console_connections, instance_id):
        connection_string = None
        for connection in console_connections:
            if connection.get('instance_id') == instance_id:
                return connection.get('connection_string')

        return connection_string

    @staticmethod
    def _get_security_groups(security_groups):
        sg_list = []
        for sg in security_groups:
            sg_dict = {
                'name': sg.get('display_name'),
                'id': sg.get('id'),
                'vnc_id': sg.get('vcn_id')
            }
            sg_list.append(sg_dict)

        return sg_list






