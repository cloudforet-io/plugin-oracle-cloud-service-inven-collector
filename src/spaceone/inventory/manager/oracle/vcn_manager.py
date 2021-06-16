from spaceone.inventory.libs.manager import OCIManager
from spaceone.inventory.model.compute_instance.data.vcn import VCN
from spaceone.inventory.model.compute_instance.data.subnet import Subnet


class VcnManager(OCIManager):

    def __init__(self, transaction, **kwargs):
        super().__init__(transaction, **kwargs)
        self.connector_name = 'ComputeInstanceConnector'

    def get_vcn_info(self, subnet_id, vcn_list, subnet_list):
        subnet, vcn_id = self.get_subnet_info(subnet_id, subnet_list)

        for vcn in vcn_list:
            if vcn.get('id') == vcn_id:
                vcn_response = {
                    'display_name': vcn.get('display_name'),
                    'id': vcn.get('id'),
                    'cidr_block': vcn.get('cidr_block')
                }
                break

        return VCN(vcn_response, strict=False), Subnet(subnet, strict=False)

    @staticmethod
    def get_subnet_info(self, subnet_id, subnet_list):
        for subnet in subnet_list:
            if subnet.get('id') == subnet_id:
                subnet_response = {
                    'name': subnet.get('display_name'),
                    'id': subnet.get('id'),
                    'cidr_block': subnet.get('cidr_block'),
                    'subnet_domain_name': subnet.get('subnet_domain_name')
                }
                break

        return subnet_response, subnet.get('vcn_id')


