from oci.database.models import MaintenanceWindow
from schematics import Model
from schematics.types import ModelType, ListType, StringType,\
                             FloatType, DateTimeType, IntType, \
                             BooleanType

class Tags(Model):
    key = StringType()
    value = StringType()


class DbSystemOptions(Model):
    storage_management = StringType(deserialize_from='_storage_management')


class Maintenancewindow(Model):
    preference = StringType(deserialize_from='preference')
    months = StringType(deserialize_from='months')
    weeks_of_month = StringType(deserialize_from='weeks_of_month')
    hours_of_day = StringType(deserialize_from='hours_of_day')
    days_of_week = StringType(deserialize_from='days_of_week')
    lead_time_in_week = StringType(deserialize_from='lead_time_in_weeks')
    display = StringType(deserialize_from='display')


class MaintenanceRun(Model):
    id = StringType(deserialize_from='id')
    display_name = StringType(deserialize_from='display_name')
    description = StringType(deserialize_from='description')
    lifecycle_state = StringType(deserialize_from='lifecycle_state',
                                 choices=('SCHEDULED', 'IN_PROGRESS', 'SUCCEEDED',
                                          'SKIPPED', 'FAILED', 'UPDATING',
                                          'DELETING', 'DELETED', 'CANCELED'))
    time_scheduled = DateTimeType(deserialize_from='time_scheduled')
    time_started = DateTimeType(deserialize_from='time_started')
    time_ended = DateTimeType(deserialize_from='time_ended')
    target_resource_type = StringType(deserialize_from='target_resource_type',
                                      choices=('AUTONOMOUS_EXADATA_INFRASTRUCTURE', 'AUTONOMOUS_CONTAINER_DATABASE',
                                               'EXADATA_DB_SYSTEM', 'CLOUD_EXADATA_INFRASTRUCTURE',
                                               'EXACC_INFRASTRUCTURE', 'AUTONOMOUS_DATABASE'))
    target_resource_id = StringType(deserialize_from='target_resource_id')
    maintenance_type = StringType(deserialize_from='maintenance_type',
                                  choices=('PLANNED', 'UNPLANNED'))
    maintenance_subtype = StringType(deserialize_from='maintenance_subtype',
                                     choices=('QUARTERLY', 'HARDWARE', 'CRITICAL',
                                              'INFRASTRUCTURE', 'DATABASE', 'ONEOFF'))
    maintenance_display = StringType(deserialize_from='maintenance_display')
    maintenance_alert = StringType(deserialize_from='maintenance_alert')


class DatabaseSoftwareImage(Model):
    id = StringType(deserialize_from='_id')
    compartment_id = StringType(deserialize_from='_compartment_id')
    database_version = StringType(deserialize_from='_database_version')
    display_name = StringType(deserialize_from='_display_name')
    lifecycle_state = StringType(deserialize_from='_lifecycle_state',
                                 choices=('PROVISIONING', 'AVAILABLE', 'DELETING',
                                          'DELETED', 'FAILED', 'TERMINATING',
                                          'TERMINATED', 'UPDATING'))
    time_created = DateTimeType(deserialize_from='_time_created')
    image_type = StringType(deserialize_from='_image_type',
                            choices=('GRID_IMAGE', 'DATABASE_IMAGE'))
    image_shape_family = StringType(deserialize_from='_image_shape_family',
                                    choices=('VM_BM_SHAPE', 'EXADATA_SHAPE'))
    patch_set = StringType(deserialize_from='_patch_set')
    freeform_tags = ListType(ModelType(Tags), deserialize_from='_freeform_tags', default=[])
    database_software_image_included_patches = ListType(StringType,
                                                        deserialize_from='_database_software_image_included_patches')
    included_patches_summary = StringType(deserialize_from='_included_patches_summary')
    database_software_image_one_off_patches = ListType(StringType,
                                                       deserialize_from='_database_software_image_one_off_patches')
    ls_inventory = StringType(deserialize_from='_ls_inventory')
    is_upgrade_supported = BooleanType(deserialize_from='_is_upgrade_supported')


class DBHome(Model):
    compartment_id = StringType(deserialize_from='_compartment_id')
    database_software_image_id = StringType(deserialize_from='_database_software_image_id')
    db_home_location = StringType(deserialize_from='db_home_location')
    db_system_id = StringType(deserialize_from='_db_system_id')
    db_version = StringType(deserialize_from='_db_version')
    display_name = StringType(deserialize_from='_display_name')
    id = StringType(deserialize_from='_id')
    kms_key_id = StringType(deserialize_from='_kms_key_id')
    last_patch_history_entry_id = StringType(deserialize_from='_last_patch_history_entry_id')
    lifecycle_details = StringType(deserialize_from='_lifecycle_details')
    lifecycle_state = StringType(deserialize_from='_lifecycle_state',
                                 choices=( 'PROVISIONING', 'AVAILABLE', 'UPDATING',
                                           'TERMINATING', 'TERMINATED', 'FAILED'))
    one_off_patches = ListType(StringType, deserialize_from='_one_off_patches')
    time_created = DateTimeType(deserialize_from='_time_created')
    vm_cluster_id = StringType(deserialize_from='_vm_cluster_id')


class ConnectionStrings(Model):
    all_connection_strings = ListType(ModelType(Tags), deserialize_from='_all_connection_strings', default=[])
    cdb_default = StringType(deserialize_from='_cdb_default')
    cdb_ip_default = StringType(deserialize_from='_cdb_ip_default')


class UpgradeHistory(Model):
    id = StringType(deserialize_from='_id')
    action = StringType(deserialize_from='_action',
                        choices=('PRECHECK', 'UPGRADE', 'ROLLBACK'))
    source = StringType(deserialize_from='_source',
                        choices=('DB_HOME', 'DB_VERSION', 'DB_SOFTWARE_IMAGE'))
    lifecycle_state = StringType(deserialize_from='_lifecycle_state',
                                 choices=('SUCCEEDED', 'FAILED', 'IN_PROGRESS'))
    lifecycle_details = StringType(deserialize_from='_lifecycle_details')
    target_db_version = StringType(deserialize_from='_target_db_version')
    target_database_software_image_id = StringType(deserialize_from='_target_database_software_image_id')
    target_db_home_id = StringType(deserialize_from='_target_db_home_id')
    source_db_home_id = StringType(deserialize_from='_source_db_home_id')
    time_started = DateTimeType(deserialize_from='_time_started')
    time_ended = DateTimeType(deserialize_from='_time_ended')
    options = StringType(deserialize_from='_options')


class DataGuardAssociation(Model):
    id = StringType(deserialize_from='_id')
    database_id = StringType(deserialize_from='_database_id')
    role = StringType(deserialize_from='_role',
                      choices=('PRIMARY', 'STANDBY', 'DISABLED_STANDBY'))
    lifecycle_state = StringType(deserialize_from='_lifecycle_state',
                                 choices=('PROVISIONING', 'AVAILABLE',
                                          'UPDATING', 'TERMINATING', 'TERMINATED'))
    lifecycle_details = StringType(deserialize_from='_lifecycle_details')
    peer_db_system_id = StringType(deserialize_from='_peer_db_system_id')
    peer_db_home_id = StringType(deserialize_from='_peer_db_home_id')
    peer_database_id = StringType(deserialize_from='_peer_database_id')
    peer_data_guard_association_id = StringType(deserialize_from='_peer_data_guard_association_id')
    peer_role = StringType(deserialize_from='_peer_role',
                           choices=('PRIMARY', 'STANDBY', 'DISABLED_STANDBY'))
    apply_lag = StringType(deserialize_from='_apply_lag')
    apply_rate = StringType(deserialize_from='_apply_rate')
    protection_mode = StringType(deserialize_from='_protection_mode',
                                 choices=('MAXIMUM_AVAILABILITY',
                                          'MAXIMUM_PERFORMANCE', 'MAXIMUM_PROTECTION'))
    transport_type = StringType(deserialize_from='_transport_type',
                                choices=('SYNC', 'ASYNC', 'FASTSYNC'))
    time_created = DateTimeType(deserialize_from='_time_created')


class Database(Model):
    id = StringType(deserialize_from='_id')
    compartment_id = StringType(deserialize_from='_compartment_id')
    character_set = StringType(deserialize_from='_character_set')
    ncharacter_set = StringType(deserialize_from='_ncharacter_set')
    db_home_id = StringType(deserialize_from="_db_home_id")
    db_system_id = StringType(deserialize_from='_db_system_id')
    vm_cluster_id = StringType(deserialize_from='_vm_cluster_id')
    db_name = StringType(deserialize_from='_db_name')
    pdb_name = StringType(deserialize_from='_pdb_name')
    db_workload = StringType(deserialize_from='_db_workload')
    db_unique_name = StringType(deserialize_from='_db_unique_name')
    lifecycle_detail = StringType(deserialize_from='_lifecycle_detail')
    lifecycle_state = StringType(deserialize_from='_lifecycle_state',
                                 choices=('PROVISIONING', 'AVAILABLE', 'UPDATING',
                                          'BACKUP_IN_PROGRESS', 'UPGRADING', 'TERMINATING',
                                          'TERMINATED', 'RESTORE_FAILED', 'FAILED'))
    time_created = DateTimeType(deserialize_from='_time_created')
    last_backup_timestamp = DateTimeType(deserialize_from='_last_backup_timestamp')
    freeform_tags = ListType(ModelType(Tags), deserialize_from='_freeform_tags', default=[])
    connection_strings = ModelType(ConnectionStrings, deserialize_from='_connection_strings')
    kms_key_id = StringType(deserialize_from='_kms_key_id')
    source_database_point_in_time_recovery_timestamp = \
        DateTimeType(deserialize_from='source_database_point_in_time_recovery_timestamp')
    database_software_image_id = StringType(deserialize_from='_database_software_image_id')
    list_upgrade_history = ListType(ModelType(UpgradeHistory), deserialize_from='list_upgrade_history',
                                    default=[])
    list_dataguard_association = ListType(ModelType(DataGuardAssociation), deserialize_from='list_dataguard_association',
                                          default=[])


class ConsoleConnections(Model):
    compartment_id = StringType(deserialize_from='_compartment_id')
    connection_string = StringType(deserialize_from='_connection_string')
    db_node_id = StringType(deserialize_from='_db_node_id')
    fingerprint = StringType(deserialize_from='_fingerprint')
    id = StringType(deserialize_from='_id')
    lifecycle_state = StringType(deserialize_from='_lifecycle_state',
                                 choices=('ACTIVE', 'CREATING', 'DELETED',
                                          'DELETING', 'FAILED'))


class DbNode(Model):
    id = StringType(deserialize_from='_id')
    db_system_id = StringType(deserialize_from='_db_system_id')
    vnic_id = StringType(deserialize_from='_vnid_id')
    backup_vnic_id = StringType(deserialize_from='_backup_vnic_id')
    lifecycle_state = StringType(deserialize_from='_lifecycle_state',
                                 choices=( 'PROVISIONING', 'AVAILABLE', 'UPDATING',
                                           'STOPPING', 'STOPPED', 'STARTING',
                                           'TERMINATING', 'TERMINATED', 'FAILED'))
    hostname = StringType(deserialize_from='_hostname')
    fault_domain = StringType(deserialize_from='_fault_domain')
    time_created = DateTimeType(deserialize_from='_time_created')
    software_storage_size_in_gb = StringType(deserialize_from='_software_storage_size_in_gb')
    maintenance_type = StringType(deserialize_from='_maintenance_type')
    time_maintenance_window_start = DateTimeType(deserialize_from='_time_maintenance_window_start')
    time_maintenance_window_end = DateTimeType(deserialize_from='_time_maintenance_window_end')
    additional_details = StringType(deserialize_from='_additional_details')
    console_connections = ListType(ModelType(ConsoleConnections), deserialize_from='console_connections', default=[])


class Backup(Model):
    id = StringType(deserialize_from='_id')
    compartment_id = StringType(deserialize_from='_compartment_id')
    database_id = StringType(deserialize_from='_database_id')
    display_name = StringType(deserialize_from='_display_name')
    type = StringType(deserialize_from='_type',
                      choices=('INCREMENTAL', 'FULL', 'VIRTUAL_FULL'))
    time_started = DateTimeType(deserialize_from='_time_started')
    time_ended = DateTimeType(deserialize_from='_time_ended')
    lifecycle_details = StringType(deserialize_from='_lifecycle_details')
    availability_domain = StringType(deserialize_from='_availability_domain')
    lifecycle_state = StringType(deserialize_from='_lifecycle_state',
                                 choices=('CREATING', 'ACTIVE', 'DELETING',
                                          'DELETED', 'FAILED', 'RESTORING'))
    database_edition = StringType(deserialize_from='_database_edition',
                                  choices=('STANDARD_EDITION', 'ENTERPRISE_EDITION',
                                           'ENTERPRISE_EDITION_HIGH_PERFORMANCE',
                                           'ENTERPRISE_EDITION_EXTREME_PERFORMANCE'))
    database_size_in_gbs = FloatType(deserialize_from='_database_size_in_gbs')
    shape = StringType(deserialize_from='_shape')
    version = StringType(deserialize_from='version')
    kms_key_id = StringType(deserialize_from='_kms_key_id')


class PatchHistory(Model):
    id = StringType(deserialize_from='_id')
    patch_id = StringType(deserialize_from='_patch_id')
    action = StringType(deserialize_from='_action',
                        choices=('APPLY', 'PRECHECK'))
    lifecycle_state = StringType(deserialize_from='_lifecycle_state',
                                 choices=('IN_PROGRESS', 'SUCCEEDED', 'FAILED'))
    lifecycle_details = StringType(deserialize_from='_lifecycle_details')
    time_started = DateTimeType(deserialize_from='_time_started')
    time_ended = DateTimeType(deserialize_from='_time_ended')


class Patches(Model):
    id = StringType(deserialize_from='_id')
    description = StringType(deserialize_from='_description')
    last_action = StringType(deserialize_from='_last_action',
                             choices=('APPLY', 'PRECHECK'))
    available_action = ListType(StringType, deserialize_from='_available_action')
    lifecycle_details = StringType(deserialize_from='_lifecycle_details')
    lifecycle_state = StringType(deserialize_from='_lifecycle_details',
                                 choices=('AVAILABLE', 'SUCCESS',
                                          'IN_PROGRESS', 'FAILED'))
    time_released = DateTimeType(deserialize_from='_time_released')
    version = StringType(deserialize_from='_version')


class DbSystem(Model):
    compartment_name = StringType(deserialize_from='compartment_name')
    region = StringType(deserialize_from='region')
    id = StringType(deserialize_from='_id')
    compartment_id = StringType(deserialize_from='_compartment_id')
    display_name = StringType(deserialize_from='_display_name')
    availability_domain = StringType(deserialize_from='_availability_domain')
    fault_domains = ListType(StringType, deserialize_from='_fault_domains')
    subnet_id = StringType(deserialize_from='_subnet_id')
    backup_subnet_id = StringType(deserialize_from='_backup_subnet_id')
    nsg_id = ListType(StringType, deserialize_from='_nsg_id')
    backup_network_nsg_ids = ListType(StringType, deserialize_from='_backup_network_nsg_ids')
    shape = StringType(deserialize_from='_shape')
    db_system_options = ModelType(DbSystemOptions, deserialize_from='_db_system_options')
    ssh_public_keys = ListType(StringType, deserialize_from='_ssh_public_keys')
    time_zone = StringType(deserialize_from='_time_zone')
    hostname = StringType(deserialize_from='_hostname')
    domain = StringType(deserialize_from='_domain')
    kms_key_id = StringType(deserialize_from='_kms_key_id')
    version = StringType(deserialize_from='_version')
    cpu_core_count = IntType(deserialize_from='_cpu_core_count')
    cluster_name = StringType(deserialize_from='_cluster_name')
    data_storage_percentage = IntType(deserialize_from='_data_storage_percentage')
    database_edition = StringType(deserialize_from='_database_edition',
                                  choices=('STANDARD_EDITION', 'ENTERPRISE_EDITION',
                                           'ENTERPRISE_EDITION_HIGH_PERFORMANCE',
                                           'ENTERPRISE_EDITION_EXTREME_PERFORMANCE'))
    last_patch_history_entry_id = StringType(deserialize_from='_last_patch_history_entry_id')
    listener_port = IntType(deserialize_from='_listener_port')
    lifecycle_state = StringType(deserialize_from='_lifecycle_state',
                                 choices=('AVAILABLE', 'UPDATING', 'TERMINATING',
                                          'TERMINATED', 'FAILED', 'MIGRATED',
                                          'MAINTENANCE_IN_PROGRESS', 'NEEDS_ATTENTION'))
    time_created = DateTimeType(deserialize_from='_time_created')
    lifecycle_details = StringType(deserialize_from='_lifecycle_details', serialize_when_none=False)
    disk_redundancy = StringType(deserialize_from='_disk_redundancy',
                                 choices=('HIGH', 'NORMAL'))
    sparse_diskgroup = BooleanType(deserialize_from='_sparse_diskgroup')
    scan_ip_ids = ListType(StringType, deserialize_from='_scan_ip_ids')
    vip_ids = ListType(StringType, deserialize_from='_vip_ids')
    scan_dns_record_id = StringType(deserialize_from='_scan_dns_record_id')
    scan_dns_name = StringType(deserialize_from='_scan_dns_name')
    zone_id = StringType(deserialize_from='_zone_id')
    data_storage_size_in_gbs = IntType(deserialize_from='_data_storage_size_in_gbs')
    reco_storage_size_in_gb = IntType(deserialize_from='_reco_storage_size_in_gb')
    node_count = IntType(deserialize_from='_node_count')
    license_model = StringType(deserialize_from='_license_model',
                               choices=('LICENSE_INCLUDED', 'BRING_YOUR_OWN_LICENSE'))
    maintenance_window = ModelType(Maintenancewindow, deserialize_from='_maintenance_window')
    last_maintenance_run_id = StringType(deserialize_from='_last_maintenance_run_id')
    next_maintenance_run_id = StringType(deserialize_from='_next_maintenance_run_id')
    freeform_tags = ListType(ModelType(Tags), deserialize_from='_freeform_tags', default=[])
    source_db_system_id = StringType(deserialize_from='_source_db_system_id')
    point_in_time_data_disk_clone_timestamp = StringType(deserialize_from='_point_in_time_data_disk_clone_timestamp')
    last_maintenance_run = ModelType(MaintenanceRun, deserialize_from='last_maintenance_run')
    next_maintenance_run = ModelType(MaintenanceRun, deserialize_from='next_maintenance_run')
    list_db_Home = ListType(ModelType(DBHome), deserialize_from='list_db_home', default=[])
    list_database = ListType(ModelType(Database), deserialize_from='list_database', default=[])
    list_database_all = ListType(ModelType(Database), deserialize_from='list_database_all', default=[])
    list_db_node = ListType(ModelType(DbNode), deserialize_from='list_db_node', default=[])
    list_patch_history = ListType(ModelType(PatchHistory), deserialize_from='list_patch_history', default=[])
    list_patches = ListType(ModelType(Patches), deserialize_from='list_patches', default=[])
    list_backups = ListType(ModelType(Backup), deserialize_from='list_backups', default=[])
    list_software_images = ListType(ModelType(DatabaseSoftwareImage), deserialize_from='list_software_images', default=[])
    console_connections = ListType(ModelType(ConsoleConnections), deserialize_from='console_connections', default=[])

    def reference(self):
        return {
            "resource_id": self.id,
            "external_link": f"https://cloud.oracle.com/dbaas/dbsystems/{self.id}?region={self.region}",
        }

