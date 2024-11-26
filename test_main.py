from main import DriveInfo, DiskUsageInfo, check_disk_usage
from main import create_disks_list, create_table_html, check_disk_usage_dc
import configuration

def test_dclass_diskusageinfo(path):
    dataclass = check_disk_usage_dc(path)
    function = check_disk_usage(path)

    assert dataclass.used_percent == function["used %"]
    assert dataclass.free_gb == function["free GB"]
    assert dataclass.total_gb == function["total GB"]

def test_create_table_html():
    """Does the HTML table created from dataclass DriveInfo match the one created from dictionaries?"""

# test_dclass_diskusageinfo(configuration.drive_paths[0])