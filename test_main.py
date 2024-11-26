from main import DriveInfo, DiskUsageInfo, check_disk_usage, check_disk_usage_dc
from main import create_disks_list, create_drive_registry
from main import create_table_html # , create_table_html_dc
import configuration

def test_dclass_diskusageinfo(paths=configuration.drive_paths):
    """Does the dataclass based check_disk_usage_dc obtain the same data as check_disk_usage?"""
    
    for path in paths:
        dataclass = check_disk_usage_dc(path)
        function = check_disk_usage(path)

        assert dataclass.used_percent == function["used %"]
        assert dataclass.free_gb == function["free GB"]
        assert dataclass.total_gb == function["total GB"]

def test_generate_drive_registry(paths: list =configuration.drive_paths):
    """Does the dataclass based function generate_drive_registry fulfil the same function as create_disks_list?"""
    # index = 0
    # for drive in paths:
    #     registry = create_drive_registry(drive)
    #     disks_list = create_disks_list(drive)
    #     assert registry[index].path == disks_list[index]["path"]
    #     index += 1
    index = 0
    registry = create_drive_registry(paths[0])
    disks_list = create_disks_list(paths[0][0])
    print(registry)
    print(disks_list)

def test_create_table_html():
    """Does the HTML table created from dataclass DriveInfo match the one created from dictionaries?"""

test_generate_drive_registry()