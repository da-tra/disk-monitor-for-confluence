from main import DriveInfo, DiskUsageInfo, check_disk_usage, check_disk_usage_dc
from main import create_disks_list, create_drive_registry
from main import create_table_html # , create_table_html_dc
import configuration

def test_dclass_diskusageinfo(path=configuration.drive_paths[0]):
    """Does the dataclass based check_disk_usage_dc obtain the same data as check_disk_usage?"""
    dataclass = check_disk_usage_dc(path)
    function = check_disk_usage(path)

    assert dataclass.used_percent == function["used %"]
    assert dataclass.free_gb == function["free GB"]
    assert dataclass.total_gb == function["total GB"]

def test_generate_drive_registry(path):
    """Does the dataclass based function generate_drive_registry fulfil the same function as create_disks_list?"""
    registry = crea

def test_create_table_html():
    """Does the HTML table created from dataclass DriveInfo match the one created from dictionaries?"""
