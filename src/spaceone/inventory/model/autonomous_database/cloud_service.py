from schematics.types import ModelType, StringType, PolyModelType

from spaceone.inventory.model.autonomous_database.data import Database
from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField
from spaceone.inventory.libs.schema.metadata.dynamic_layout import ItemDynamicLayout, TableDynamicLayout
from spaceone.inventory.libs.schema.cloud_service import CloudServiceResource, CloudServiceResponse, CloudServiceMeta

'''
Database
'''
database_meta = ItemDynamicLayout.set_fields('Database', fields=[
    TextDyField.data_source('Display Name', ''),
])

# TAB - tags
database_tags = TableDynamicLayout.set_fields('Tags', 'data.tags', fields=[
    TextDyField.data_source('Key', 'key'),
    TextDyField.data_source('Value', 'value')
])

adb_meta = CloudServiceMeta.set_layouts([database_meta, database_tags])


class AutonomousDatabaseResource(CloudServiceResource):
    cloud_service_group = StringType(default='AutonomousDatabase')


class DatabaseResource(AutonomousDatabaseResource):
    cloud_service_type = StringType(default='Database')
    data = ModelType(Database)
    _metadata = ModelType(CloudServiceMeta, default=adb_meta, serialized_name='metadata')


class DatabaseResponse(CloudServiceResponse):
    resource = PolyModelType(DatabaseResource)
