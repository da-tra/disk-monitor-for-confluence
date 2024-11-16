"""Gets data about free storage on mounted drives and HTTP PUTs them on an existing Confluence page inside a generated table."""

import shutil
from datetime import datetime, timezone
from pprint import pprint

import configuration


def check_disk_usage(path: str) -> dict:
    """Use package shutil to extract information about storage of a mounted drive."""
    disk_dict = dict()
    _total, _used, _free = shutil.disk_usage(path)
    total_gb = _total / 2**30
    used_percent = _used / _total * 100
    free_gb = _free / 2**30

    return {
        "used %": used_percent,
        "free GB": free_gb,
        "total GB": total_gb,
        }

def create_disks_list(
    disk_paths: list = configuration.drive_paths,
    ) -> list[dict]:
    """Create a list for storing info about all the disks. 
    Then populate it with information about all the disks' storage, including time of recording."""
    disks = []
    time_of_snapshot = datetime.now(timezone.utc).strftime("%d-%m-%Y %H:%M:%S")
    for disk_path in disk_paths:
        disk_dict = {}
        disk_dict["path"] = disk_path
        disk_dict["storage"] = check_disk_usage(disk_path)
        disk_dict["time of snapshot"] = time_of_snapshot
        disks.append(disk_dict)
    return disks

# create and populate a list that stores the information about all the drives
disks = create_disks_list()
pprint(disks)

## create HTML code for a table with disc info


#TODO create Requests PUT request for updating a given confluence page
#TODO implement logging
#TODO implement SQL recording of storage device status


print("{:.2f}".format(disks[0]["storage"]["used %"]))
# print(disks[1])
# print(type(disks[1]))
# print(type(check_disk_usage("/")))
# print(type(update_disks_list()))