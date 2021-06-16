from spaceone.inventory.libs.manager import OCIManager
from spaceone.inventory.model.compute_instance.data.load_balancer import LoadBalancer


class LoadBalancerManager(OCIManager):

    def __init__(self, transaction, **kwargs):
        super().__init__(transaction, **kwargs)
        self.connector_name = 'ComputeInstanceConnector'

    def get_load_balancer_info(self, lb_id_list, load_balancers, network_load_balancers, instance_ip=None):
        '''
        lb_data = {
            'type': NLB | LB,
            'endpoint" : "152.70.93.200",
            "name": "",
            "port": [80],
            "protocol": ["TCP"],
            "scheme": "public" | "private",
            tags: {
                "lb_id": ""
            }
        }
        '''
        lb_data_list = []
        for lb_id in lb_id_list:
            if lb_id.split(".")[1] == 'loadbalancer':
                lb_data_list.extend(self.get_alb_info(lb_id, load_balancers, instance_ip))

            else:
                lb_data_list.extend(self.get_nlb_info(lb_id, network_load_balancers, instance_ip))

        return lb_data_list


    def get_alb_info(self, lb_id, load_balancers):
        result = []
        for load_balancer in load_balancers:
            if load_balancer.get('id') == lb_id:
                listeners = load_balancer.get("listeners")
                alb = {
                    "type": "LB",
                    "name": load_balancer.get('display_name'),
                    "endpoint": self.get_endpoint_ip_address(load_balancer.get("ip_addresses")),
                    "port": [listener.get('port') for listener in listeners.values()
                             if listener.get('port') is not None],
                    "protocol": [listener.get('protocol') for listener in listeners.values()
                                 if listener.get('protocol') is not None],
                    "scheme": 'private' if load_balancer.get('is_private') else "public",
                    "tags": {
                        "lb_id": load_balancer.get("id")
                    }
                }
                result.append(LoadBalancer(alb, strict=False))

        return result

    def get_nlb_info(self, lb_id, network_load_balancers):
        result = []
        for network_load_balancer in network_load_balancers:
            if network_load_balancer.get('id') == lb_id:
                listeners = network_load_balancer.get("listeners")
                nlb = {
                    "type": "NLB",
                    "name": network_load_balancer.get("display_name"),
                    "endpoint": self.get_endpoint_ip_address(network_load_balancer.get('ip_addresses')),
                    "port": [listener.get('port') for listener in listeners.values()
                             if listener.get('port') is not None],
                    "protocol": [listener.get('protocol') for listener in listeners.values()
                                 if listener.get('protocol') is not None],
                    "scheme": 'private' if network_load_balancer.get('is_private') else 'public',
                    "tags": {
                        "lb_id": network_load_balancer.get("id")
                    }
                }
                result.append(LoadBalancer(nlb, strict=False))

        return result

    @staticmethod
    def get_endpoint_ip_address(ip_addresses):
        ip = ''
        for ip_address in ip_addresses:
            if ip_address.get('is_public'):
                ip = ip_address.get('ip_address', '')
                break
        return ip



