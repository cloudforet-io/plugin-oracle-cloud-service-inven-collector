from spaceone.inventory.libs.manager import OCIManager
from spaceone.inventory.model.compute_instance.data.disk import Disk


class DiskManager(OCIManager):

    def __init__(self, transaction, **kwargs):
        super().__init__(transaction, **kwargs)
        self.connector_name = 'ComputeInstanceConnector'

    '''
    disk_data = {
        "device_index": 0,
        "device": "",
        "disk_type": "BlockVolume",
        "size": 100,
        "tags": {
            "volume_id": "",
            "volume_type": "",
            "iops": ""
        }
    }
    '''

    def get_disk_info(self, block_volumes, boot_volumes, instance_id, image_id):
        disk = []
        index = 0
        for boot_volume in boot_volumes:
            boot_data = {
                'device_index': index,
                'device': "",
                'size': boot_volume.get('size_in_gbs', ''),
                'tags': {
                    'volume_id': boot_volume.get('id', ''),
                    'vpus_per_gb': boot_volume.get('vpus_per_gb', ''),
                    'iops': self.get_volume_iops(boot_volume.get('vpus_per_gb'),
                                                 boot_volume.get('size_in_gbs'))
                }
            }
            disk.append(Disk(boot_data, strict=False))
            index += 1

        for block_volume in block_volumes:
            volume_data = {
                'device_index': index,
                'device': block_volume.get('device', ''),
                'size': block_volume.get('size_in_gbs', ''),
                'tags': {
                    'volume_id': block_volume.get('volume_id', ''),
                    'vpus_per_gb': block_volume.get('vpus_per_gb', ''),
                    'iops': self.get_volume_iops(int(block_volume.get('vpus_per_gb')),
                                                 int(block_volume.get('size_in_gbs')))
                }
            }
            disk.append(Disk(volume_data, strict=False))
            index += 1

        return disk

    @staticmethod
    def get_volume_iops(vpus_ver_gb, size):
        iops = 0

        # For Lower cost Options
        if vpus_ver_gb == 0: iops = 2*size
        # For Balanced cost options
        elif vpus_ver_gb == 10 : iops = 60*size
        # For Higher Performance
        else : iops = 75*size

        return iops


