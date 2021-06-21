from spaceone.inventory.libs.manager import OCIManager
from spaceone.inventory.libs.schema.base import ReferenceModel
from spaceone.inventory.connector.compute_instance import ComputeInstanceConnector
from spaceone.inventory.manager.oracle import ComputeInstanceManager, DiskManager, InstancePoolManager, \
    LoadBalancerManager, SecurityGroupManager, VcnManager, VnicManager
from spaceone.inventory.model.compute_instance.cloud_service import ComputeInstanceResponse, ComputeInstanceResource
from spaceone.inventory.model.compute_instance.cloud_service_type import CloudServiceType
import time
from pprint import pprint


class InstanceCollectorManager(OCIManager):

    def __init__(self, transaction, **kwargs):
        super().__init__(transaction, **kwargs)
        self.connector_name = 'ComputeInstanceConnector'


    def collect_cloud_service(self, params):
        start_time = time.time()
        """
        Args:
            params:
                - options
                - schema
                - secret_data
                - filter
                - region
                - compartment
        Response:
            CloudServiceResponse
        """
        secret_data = params['secret_data']
        region = params['region']
        compartment_list = params['compartment']
        secret_data.update({'region': region})

        server_vos = []
        instance_list = []
        disk_list = []
        pool_list = []
        pool_instance_list = []
        lb_list = []
        nsg_list = []
        nsg_rule_list = []
        vcn_list = []
        vnic_list = []
        subnet_list = []
        private_ip_list = []
        image_list = []
        console_connection_list = []


        instance_connector: ComputeInstanceConnector = self.locator.get_connector(self.connector_name, **params)
        instance_connector.set_connect(secret_data)

        ad_list = instance_connector.list_ad(secret_data["tenancy"])

        # Get Managers
        ins_manager: ComputeInstanceManager = ComputeInstanceManager(secret_data)
        disk_manager: DiskManager = DiskManager(secret_data)
        pool_manager: InstancePoolManager = InstancePoolManager(secret_data)
        lb_manager: LoadBalancerManager = LoadBalancerManager(secret_data)
        nsg_manager: SecurityGroupManager = SecurityGroupManager(secret_data)
        vnc_manager: VcnManager = VcnManager(secret_data)
        vnic_manager: VnicManager = VnicManager(secret_data)

        for compartment in compartment_list:

            instance_list.extend(instance_connector.list_instance(compartment))
            console_connection_list.extend(instance_connector.list_console_connections(compartment))
            image_list.extend(instance_connector.list_image(compartment))

            disk_list.extend(instance_connector.list_volume(compartment))
            disk_list.extend(self.get_boot_volumes(instance_connector, ad_list, compartment))

            pools = instance_connector.list_instance_pool(compartment)
            pool_instance_list.extend(self.get_pool_instances(instance_connector, compartment, pools))
            pool_list.extend(pools)

            lb_list.extend(instance_connector.list_lb(compartment))
            lb_list.extend(instance_connector.list_nlb(compartment))

            vnics = instance_connector.list_vnic(compartment)
            vnic_list.extend(vnics)
            private_ip_list.extend(self.get_private_ips(instance_connector, vnics))
            nsgs = instance_connector.list_nsg(compartment)
            nsg_list.extend(nsgs)
            nsg_rule_list.extend(self.get_nsg_rules(instance_connector, nsgs))
            vcn_list.extend(instance_connector.list_vcn(compartment))
            subnet_list.extend(instance_connector.list_subnet(compartment))

        for instance in instance_list:
            instance_id = instance.get('id')
            matched_vnic_list, primary_ip, nsg_ids = vnic_manager.get_vnic_info(instance_id, vnic_list, private_ip_list)
            
            pass


        return server_vos

    def get_pool_instances(self, instance_connector, compartment, pool_list):
        result = []
        for pool in pool_list:
            result.extend(instance_connector.list_instance_pool_instance(compartment, pool.get('id')))

        return result

    def get_private_ips(self, instance_connector, vnics):
        result = []
        for vnic in vnics:
            result.append(instance_connector.list_private_ip(vnic.get('id')))

        return result

    def get_nsg_rules(self, instance_connector, security_groups):
        result = []
        for sg in security_groups:
            result.extend(instance_connector.list_nsg_rules(sg.get('id'), sg.get('display_name')))

        return result

    def get_boot_volumes(self, instance_connector, ad_list, compartment):
        result = []
        for ad in ad_list:
            result.extend(instance_connector.list_boot_volume(ad.get('name'), compartment))
        return result




