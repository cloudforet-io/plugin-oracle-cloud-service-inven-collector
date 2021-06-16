from spaceone.inventory.libs.manager import OCIManager
from spaceone.inventory.model.compute_instance.data.nic import NIC


class VnicManager(OCIManager):

    def __init__(self, transaction, **kwargs):
        super().__init__(transaction, **kwargs)
        self.connector_name = 'ComputeInstanceConnector'

    def get_vnic_info(self, instance_id, vnic_list, private_ip_list, subnet_vo):
        '''
        "device_index": 0,
        "nic_type": "",
        "ip_address": [],
        "cidr

        '''
        matched_vnic = []
        primary_ip = None
        nsg_ids = []
        for vnic in vnic_list:
            if vnic.get('instance_id') == instance_id:
                vnic_response = {
                    'device_index': vnic.get('nic_index'),
                    'nic_type': 'Primary' if vnic.get('nic_index') == 0 else "Secondary",
                    'ip_addresses': self.get_ip_addresses(private_ip_list, vnic.get('vnic_id')),
                    'cidr': subnet_vo.cidr,
                    'mac_address': vnic.get('mac_address'),
                    'public_address': vnic.get('public_ip'),
                    'tags':{
                        'vnic_id': vnic.get('vnic_id'),
                        'hostname_label': vnic.get('hostname_label', '')
                    }
                }
                nsg_ids.extend(vnic.get('nsg_ids'))

                if vnic.get('is_primary'):
                    primary_ip = vnic.get('private_ip')

                matched_vnic.append(NIC(vnic_response, strict=False))

        return matched_vnic, primary_ip, nsg_ids

    @staticmethod
    def get_ip_addresses(private_ip_list, vnic_id):
        result = []
        for ip in private_ip_list:
            if ip.get('vnic_id') == vnic_id:
                result.append(ip.get('ip_address'))

        return result

