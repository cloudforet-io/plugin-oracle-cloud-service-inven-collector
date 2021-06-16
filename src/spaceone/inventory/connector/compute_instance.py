import logging
from oci.pagination import list_call_get_all_results_generator
from oci.exceptions import ServiceError
from spaceone.inventory.libs.connector import OCIConnector
import json
import datetime
from pprint import pprint
from spaceone.inventory.error import *


__all__ = ['ComputeInstanceConnector']
_LOGGER = logging.getLogger(__name__)


class ComputeInstanceConnector(OCIConnector):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.secret_data = kwargs.get('secret_data')
        self.set_connect(kwargs.get('secret_data'))

    def list_instance(self, compartment):
        vm_instance = []
        try:
            for response in list_call_get_all_results_generator(
                    self.compute_client.list_instances, 'response', compartment.id):
                for instance in response.data:
                    vm_instance.append(json.dumps(str(instance)))
        except ServiceError as e:
            print(f'[ERROR: OCI LIST INSTANCE Info]: {e}')
        return vm_instance

    def list_image(self, compartment):
        result = []
        try:
            for response in list_call_get_all_results_generator(
                    self.compute_client.list_images, 'response', compartment.id):
                for image in response.data:
                    result.append(json.dumps(str(image)))
        except ServiceError as e:
            print(f'[ERROR: OCI LIST IMAGE Info]: {e}')
        return result

    def list_vnic(self, compartment):
        result = []
        try:
            for response in list_call_get_all_results_generator(
                    self.compute_client.list_vnic_attachments, 'response', compartment.id):
                for vnic in response.data:
                    vnic = json.loads(json.dumps(str(vnic)))
                    vnic_data = self.get_vnic(vnic.get('vnic_id'))
                    vnic.update({
                        'hostname_label': vnic_data.get('hostname_label'),
                        'is_primary': vnic_data.get('is_primary'),
                        'mac_address': vnic_data.get('mac_address'),
                        'nsg_ids': vnic_data.get('nsg_ids'),
                        'private_ip': vnic_data.get('private_ip'),
                        'public_ip': vnic_data.get('public_ip')
                    })
                    result.append(vnic)
        except ServiceError as e:
            print(f'[ERROR: OCI LIST VNIC Info]: {e}')
        return result

    def get_vnic(self, nic_id):
        try:
            response = self.virtual_network_client.get_vnic(vnic_id=nic_id)
            if response.data is None:
                return {}

        except ServiceError as e:
            print(f'[ERROR: OCI GET VNIC Info]: {e}')

        return json.loads(json.dumps(str(response.data)))

    def list_subnet(self, compartment):
        result = []
        try:
            for response in list_call_get_all_results_generator(
                   self.virtual_network_client.list_subnets):
                for subnet in response.data:
                    result.append(json.dumps(str(subnet)))
        except ServiceError as e:
            print(f'[ERROR: OCI LIST SUBNETS Info]: {e}')
        return result

    def list_vcn(self, compartment):
        result = []
        try:
            for response in list_call_get_all_results_generator(
                    self.virtual_network_client.list_vcns, 'response', compartment.id):
                for vcn in response.data:
                    result.append(json.dumps(str(vcn)))
        except ServiceError as e:
            print(f'[ERROR: OCI LIST VCN Info]: {e}')

        return result

    def get_vcn(self, vcn_id):
        vcn_response = None

        try:
            vcn_response = self.virtual_network_client.get_vnic(vcn_id = vcn_id)
            vcn_response = json.loads(json.dumps(str(vcn_response.data)))

        except ServiceError as e:
            print(f'[ERROR: OCI GET VCN Info]: {e}')

        return vcn_response

    def list_private_ip(self, vnic_id):
        private_ip_list = []
        try:
            for response in list_call_get_all_results_generator(
                    self.virtual_network_client.list_private_ips, 'response', vnic_id=vnic_id):
                for ip in response.data:
                    private_ip_list.append(json.loads(json.dumps(str(ip))))
        except ServiceError as e:
            print(f'[ERROR: OCI LIST PRIVATE IP Info]: {e}')

        return private_ip_list

    def list_volume(self, compartment):
        result = []
        try:
            for response in list_call_get_all_results_generator(
                    self.compute_client.list_volume_attachments, 'response', compartment.id):
                for volume in response.data:
                    volume_dict = json.loads(json.dumps(str(volume)))
                    volume_detail_info = self.get_volume_info(volume_dict.get('volume_id', ''))
                    volume_dict.update({
                        'lifecycle_state': volume_detail_info.get('lifecycle_state', ''),
                        'size_in_gbs': volume_detail_info.get('size_in_gbs', ''),
                        'vpus_per_gb': volume_detail_info.get('vpus_per_gb', ''),
                        'is_hydrated': volume_detail_info.get('is_hydrated', ''),
                        'kms_key_id': volume_detail_info.get('kms_key_id', '')
                    })
                    result.append(volume_dict)
        except ServiceError as e:
            print(f'[ERROR: OCI LIST VOLUME Info]: {e}')
        return result

    def get_volume_info(self, volume_id):
        volume_response = None

        try:
            volume_response = self.disk_client.get_volume(volume_id=volume_id)
            volume_response = json.loads(json.dumps(str(volume_response.data)))

        except ServiceError as e:
            print(f'[ERROR: OCI GET VOLUME Info]: {e}')

        return volume_response

    def list_boot_volume(self, availability_domain, compartment):
        result = []
        try:
            for response in list_call_get_all_results_generator(
                    self.disk_client.list_boot_volumes, 'response',
                    compartment_id=compartment.id, availability_domain=availability_domain):
                for boot in response.data:
                    result.append(json.dumps(str(boot)))
        except ServiceError as e:
            print(f'[ERROR: OCI LIST BOOT VOLUME Info]: {e}')
        return result

    def list_instance_pool(self, compartment):
        result = []
        try:
            for response in list_call_get_all_results_generator(
                    self.compute_management_client.list_instance_pools, 'response', compartment.id):
                for instance_pool in response.data:
                    result.append(json.dumps(str(instance_pool)))
        except ServiceError as e:
            print(f'[ERROR: OCI LIST INSTANCE POOL Info]: {e}')
        return result

    def list_instance_pool_instance(self, compartment, pool_id):
        result = []
        try:
            for response in list_call_get_all_results_generator(
                    self.compute_management_client.list_instance_pool_instances,
                    'response', compartment_id = compartment.id, instance_pool_id = pool_id ):
                for pool_instance in response.data:
                    result.append(json.dumps(str(pool_instance)))

        except ServiceError as e:
            print(f'[ERROR: OCI LIST INSTANCE POOL INSTANCES Info]: {e}')

        return result

    def list_nsg(self, compartment):
        result = []
        try:
            for response in list_call_get_all_results_generator(
                    self.virtual_network_client.list_network_security_groups, 'response', compartment.id):
                for nsg in response.data:
                    result.append(json.dumps(str(nsg)))
        except ServiceError as e:
            print(f'[ERROR: OCI LIST NSG Info]: {e}')
        return result

    def list_nsg_rules(self, nsg_id, nsg_name):
        result = []
        try:
            for response in list_call_get_all_results_generator(
                    self.virtual_network_client.list_network_security_group_security_rules, 'response', nsg_id):
                for rule in response.data:
                    rule = json.loads(json.dumps(str(rule)))
                    rule.update({
                        'security_group_id': nsg_id,
                        'security_group_name': nsg_name
                    })
                    result.append(rule)
        except ServiceError as e:
            print(f'[ERROR: OCI LIST NSG RULES Info]: {e}')
        return result

    def list_lb(self, compartment):
        result = []
        try:
            for response in list_call_get_all_results_generator(
                    self.load_balancer_client.list_load_balancers, 'response', compartment.id):
                for lb in response.data:
                    result.append(json.dumps(str(lb)))
        except ServiceError as e:
            print(f'[ERROR: OCI LIST LB Info]: {e}')

        return result

    def list_nlb(self, compartment):
        result = []
        try:
            for response in list_call_get_all_results_generator(
                    self.network_load_balancer_client.list_network_load_balancers, 'response', compartment.id):
                for nlb in response.data:
                    result.append(json.dumps(str(nlb)))
        except ServiceError as e:
            print(f'[ERROR: OCI LIST NLB Info]: {e}')
        return result




