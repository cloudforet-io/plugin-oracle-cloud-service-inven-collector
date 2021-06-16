from spaceone.inventory.libs.manager import OCIManager
from spaceone.inventory.model.compute_instance.data.instance_pool import InstancePool


class InstancePoolManager(OCIManager):

    def __init__(self, transaction, **kwargs):
        super().__init__(transaction, **kwargs)
        self.connector_name = 'ComputeInstanceConnector'

    def get_instance_pool_info(self, instance_id, instance_pools, instance_pool_instances):
        '''
        instance_pool_data = {
            'id': '',
            'display_name': '',
            'instance_configuration_id': '',
            'size': ""

        }
        '''
        instance_pool_data = {}
        for instance_pool in instance_pools:
            lb_id_list, pool_id = self.get_lb_id_from_instances(
                instance_id, instance_pool.get('id'), instance_pool_instances)
            if (pool_id is not None) and pool_id == instance_pool.get('id'):
                instance_pool_data = {
                    'id': instance_pool.get('id', ''),
                    'display_name': instance_pool.get('display_name', ''),
                    'instance_configuration_id': instance_pool.get('instance_configuration_id', ''),
                    'size': instance_pool.get('size', '')
                }
                break

        return InstancePool(instance_pool_data, strict=False), lb_id_list

    @staticmethod
    def get_lb_id_from_instances(instance_id, instance_pool_id, instance_pool_instances):
        load_balancer_id_list = []
        matched_instance_pool_id = None

        for instance in instance_pool_instances:
            if instance.get('id') == instance_id:
                matched_instance_pool_id = instance_pool_id
                for backend in instance.get('load_balancer_backends'):
                    if backend.get('load_balancer_id') not in load_balancer_id_list:
                        load_balancer_id_list.append(backend.get('load_balancer_id'))
                break

        return load_balancer_id_list, matched_instance_pool_id