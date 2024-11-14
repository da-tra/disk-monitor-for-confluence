"""
Gets data about free storage on mounted drives and HTTP PUTs them on an 
existing Confluence page inside a generated table.
"""

import shutil
import configuration

def check_disk_usage(path: str) -> dict:
    disk_dict = dict()
    total, used, free = shutil.disk_usage(path)
    total_gb = total / 2**30
    used_percent = used / total * 100
    free_gb = free / 2**30

    disk_dict["used %"] = used_percent
    disk_dict["free GB"] = free_gb
    disk_dict["total GB"] = total_gb
    return disk_dict

print(check_disk_usage("/"))

