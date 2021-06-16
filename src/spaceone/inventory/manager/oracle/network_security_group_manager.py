from spaceone.inventory.libs.manager import OCIManager
from spaceone.inventory.model.compute_instance.data.security_group import SecurityGroup


class SecurityGroupManager(OCIManager):

    def __init__(self, transaction, **kwargs):
        super().__init__(transaction, **kwargs)
        self.connector_name = 'ComputeInstanceConnector'

    def get_security_group_info(self, security_groups):
        '''
        "data.security_group" = [
                    {
                        "protocol": "",
                        "security_group_name": "",
                        "port_range_min": 0,
                        "port_range_max": 65535,
                        "security_group_id": "",
                        "description": "",
                        "direction": "inbound" | "outbound",
                        "port": "",
                        "remote": "",
                        "remote_id": "",
                        "remote_cidr": "",
                        'tags': {
                            'stateless': True | False
                        }
                    }
                ],
        '''
        sg = []
        for security_group in security_groups:

            min_port, max_port, port_range = self._get_port_from_protocol(security_group)

            if security_group['direction'] == "INGRESS":
                direction, remote, remote_type = 'inbound', 'source', 'source_type'
            else: direction, remote, remote_type = 'outbound' 'destination', 'destination_type'

            security_group_response = {
                'direction': direction,
                'description': security_group.get('description'),
                'protocol': self._get_protocol(security_group.get('protocol')),
                'security_group_id': security_group.get('security_group_id'),
                'security_group_name': security_group.get('security_group_name'),
                'port_range_min': min_port,
                'port_range_max': max_port,
                'port': port_range,
                'remote': security_group.get(remote),
                'remote_cidr': security_group.get(remote)
                if security_group.get(remote_type) != 'NETWORK_SECURITY_GROUP'
                else "",
                'remote_id': security_group.get(remote)
                if security_group.get(remote_type) == 'NETWORK_SECURITY_GROUP'
                else "",
                'tags': {
                    'stateless': security_group.get("is_stateless")
                }
            }

            sg.append(SecurityGroup(security_group_response, strict=False))

        return sg

    @staticmethod
    def _get_protocol(protocol_number):

        if protocol_number == "1": return "ICMP"
        elif protocol_number == "6": return "TCP"
        elif protocol_number == "17": return "UDP"
        elif protocol_number == "58": return "ICMPv6"
        else: return "ALL"

    @staticmethod
    def _get_port_from_protocol(security_group):
        min_port, max_port, port_range = "", "", ""
        direction = 'destination_port_range' \
            if security_group.get('direction') == 'EGRESS' \
            else 'source_port_range'

        if security_group.get('protocol') == "6":
            min_port = security_group['tcp_options'][direction]["min"]
            max_port = security_group['tcp_options'][direction]["max"]
        if security_group.get('protocol') == '17':
            min_port = security_group['udp_options'][direction]["min"]
            max_port = security_group['udp_options'][direction]["max"]

        if min_port == max_port:
            port_range = str(min_port)
        else : port_range = "{} - {}".format(min_port, max_port)

        return min_port, max_port, port_range
