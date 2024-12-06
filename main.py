"""Write disk usage data to a Confluence page.

Gets data about free storage on mounted drives and HTTP PUTs them on an existing Confluence page inside a generated 
table.
User credentials for Confluence and the paths for storage devices will be read from a file titled
configuration.py, which needs to be created by the user. For instructions refer to README.md
"""

import json
import shutil
from dataclasses import dataclass
from datetime import datetime

import requests
from requests.auth import HTTPBasicAuth

import configuration

# TODO refactoring: store device capacity in a data class instead of a dictionary
@dataclass
class DiskUsageInfo:
    """Dataclass that stores information about a drive's storage capacity."""

    used_percent: float
    free_gb: int
    total_gb: int

@dataclass
class DriveInfo:
    """Dataclass that stores a drive's path and storage information(=DiskUsageInfo)."""

    path: str
    storage: DiskUsageInfo
    time_of_snapshot: str

# TODO refactoring: create function to add data to DiskUsageInfo

def check_disk_usage_dc(path:str) -> DiskUsageInfo:
    """Read storage capacity with shutil and create DiskUsageInfo with the data."""
    _total, _used, _free = shutil.disk_usage(path)

    total_gb = _total / 2**30
    used_percent = _used / _total* 100
    free_gb = _free / 2**30

    disk_usage_info_dc = DiskUsageInfo(total_gb=total_gb, used_percent=used_percent, free_gb=free_gb)

    return disk_usage_info_dc

def check_disk_usage(path: str) -> dict:
    """Use package shutil to extract information about storage of a mounted drive."""
    disk_dict = dict()
    _total, _used, _free = shutil.disk_usage(path)
    total_gb = _total / 2**30
    used_percent = _used / _total * 100
    free_gb = _free / 2**30
    time_of_snapshot = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    return {
        "used %": used_percent,
        "free GB": free_gb,
        "total GB": total_gb,
        "time of snapshot": time_of_snapshot
        }

def create_drive_registry(drive_paths: list[str]) -> list[DriveInfo]:
    """Turn a list of drive mounting points into a list of objects store their path and storage capacity."""

    registry = [
        DriveInfo(
            path=path, 
            storage=check_disk_usage_dc(path),
            time_of_snapshot = datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            ) for path in drive_paths
            ]

    return registry

def create_table_html(disk_registry: list[DriveInfo]) -> str:
    """Create HTML code for a table that displays the information of all disks in a list.

    Column labels are the keys in the dictionaries of each individual storage device.
    """
    ## create HTML code for a table with disc info
    # define an empty table
    table = ""

    # define labels for the columns
    # get the labels dataclass DriveInfo's attributes
    attributes: dict = DriveInfo.__dataclass_fields__.keys()
    # remove "_"-separators
    table_columns = [v.replace('_', ' ') for v in attributes]


    # create first table row with table column labels
    table += "<tr>"
    for column_name in table_columns:
        table += "<th><p><strong>"
        table += column_name
        table += "</strong></p></th>"
    table += "</tr>"

    for disk in disk_registry:
        new_row = ""
        # start row
        new_row += "<tr>"
        # add disk path
        new_row += f"<td><p>{disk.path}</p></td>"
        # open storage cell and fill it
        new_row += "<td><p>"
        new_row += f"<strong>used: {f"{disk.storage.used_percent:.1f}"} % </strong> <br/>"
        new_row += f"free: {f"{disk.storage.free_gb:.2f}"} GB<br/>"
        new_row += f"total: {f"{disk.storage.total_gb:.2f}"} GB<br/>"
        # close storage cell
        new_row += "</p></td>"
        # new cell for timestamp
        new_row += f"<td> <p>{disk.time_of_snapshot}</p></td>"
        # finish this row
        new_row += "</tr>"
        table += new_row
    # assemble the table
    table = f"<table><tbody>{table}</tbody></table>"

    return table

def get_page_version(url: str) -> int:
    """Get version number of confluence page."""
    headers = {"Accept": "application/json"}

    response = session.get(
        url,
        timeout=1,
        headers=headers,
        auth=authentication,
        params={
            "expand": ("body.storage", "body.version"),
            "body-format": "storage",
        },
    )

    # GET version number of current content (so it can incremented with the content update)
    page_data = response.json()
    version_number = page_data["version"]["number"]

    # for debugging:
    # print(f"version number before update: {version_number}\n")
    # response_str = response.text
    # response_pretty = json.dumps(json.loads(response_str), indent=4)
    # print(json.dumps(json.loads(response_str), sort_keys=True, indent=4, separators=(",", ": ")))
    # print(f"GET url: {response.url}")
    # print(f"GET response code: {response.status_code}")

    return version_number

def update_page_with_new_content(
    new_content: str | int,
    existing_version: int,
    ) -> str:
    """PUT new content to the relevant confluence page."""
    headers = {"Accept": "application/json", "Content-Type": "application/json"}

    new_content = table

    payload = json.dumps(
        {
            "id": CONFLUENCE_PAGE_ID,
            "status": "current",
            "title": CONFLUENCE_PAGE_TITLE,
            "body": {"representation": "storage", "value": new_content},
            "version": {"number": existing_version + 1, "message": ""},
        }
    )
    request = session.put(
        url=URL,
        data=payload,
        timeout=1,
        headers=headers,
        auth=authentication,
    )

    return request

# import information about your Confluence page from the file configuration.py
CONFLUENCE_PAGE_ID = configuration.confluence_page_id
BASE_URL = configuration.confluence_base_url
URL = f"{BASE_URL}wiki/api/v2/pages/{CONFLUENCE_PAGE_ID}"
CONFLUENCE_USER = configuration.confluence_username
CONFLUENCE_API_TOKEN = configuration.api_key
CONFLUENCE_PAGE_TITLE = configuration.confluence_page_name
authentication = HTTPBasicAuth(CONFLUENCE_USER, CONFLUENCE_API_TOKEN)

# create a session to avoid the need for repeated login
with requests.Session() as session:
    session.auth = authentication

# create and populate a list that stores the information about all the drives
drives = create_drive_registry(drive_paths=configuration.drive_paths)

# create an HTML table displaying information about the drives
table = create_table_html(disk_registry=drives)

# for debugging:create HTML file with table for debugging
# from pathlib import Path
# path = Path("table.html")
# path.write_text(table)

# get page version, needed for the put request that updates the confluence page
version_number_before_update = get_page_version(URL)

# update page with the new content
update_page_with_new_content(
    new_content=table,
    existing_version=version_number_before_update)

# #TODO implement logging
# #TODO implement SQL recording of storage device status
