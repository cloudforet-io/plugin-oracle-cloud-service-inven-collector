from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, SearchField, DateTimeDyField
from spaceone.inventory.libs.schema.cloud_service_type import CloudServiceTypeResource, CloudServiceTypeResponse, \
    CloudServiceTypeMeta


cst_adb = CloudServiceTypeResource()
cst_adb.name = 'Database'
cst_adb.provider = 'oracle_cloud'
cst_adb.group = 'AutonomousDatabase'
cst_adb.labels = ['database']
cst_adb.service_code = ''
cst_adb.is_primary = True
cst_adb.is_major = True
cst_adb.tags = {
    'spaceone:icon': ''
}

cst_adb._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('Display Name', ''),
        TextDyField.data_source('State', ''),
        TextDyField.data_source('Dedicated', ''),
        TextDyField.data_source('OCPUs', ''),
        TextDyField.data_source('Storage (TB)', ''),
        TextDyField.data_source('Workload Type', ''),
        TextDyField.data_source('Autonomous Data Guard', ''),
        DateTimeDyField.data_source('Created', ''),
    ],
    search=[
        SearchField.set(name='ID', key='data.id'),
    ]

)


CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_adb})
]
