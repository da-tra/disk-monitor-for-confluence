"""
Gets data about free storage on mounted drives and HTTP PUTs them on an 
existing Confluence page inside a generated table.
"""

import shutil
import configuration
from pprint import pprint

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

def update_disks_list(
    disk_paths: list = configuration.drive_paths,
    disk_registry: list = disks,
):
    """Create a dictionary for each storage device and add it to the disk register ."""

    for disk_path in disk_paths:
        disk_dict = {}
        disk_dict["path"] = disk_path
        disk_dict["storage"] = check_disk_usage(disk_path)
        disk_registry.append(disk_dict)

# create a list where you can save the information about all the drives
disks = []

# update the list 'disks' with information about all drives (stored in dictionaries)
update_disks_list(disk_paths=disks)


print("{:.2f}".format(disks[0]["storage"]["used %"]))
# print(disks[1])
# print(type(disks[1]))
# print(type(check_disk_usage("/")))
# print(type(update_disks_list()))