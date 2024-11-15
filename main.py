"""Gets data about free storage on mounted drives and HTTP PUTs them on an existing Confluence page inside a generated table."""

from dataclasses import dataclass
import shutil


class configuration:
    drive_paths = ["."]


@dataclass
class DiskUsageInfo:
    total_gb: int
    used_percent: float
    free_gb: int


@dataclass
class DriveInfo:
    path: str
    storage: DiskUsageInfo


def get_disk_usage(path: str) -> DiskUsageInfo:
    _total, _used, _free = shutil.disk_usage(path)

    total_gb = _total / 2**30
    used_percent = _used / _total * 100
    free_gb = _free / 2**30

    disk_usage_info = DiskUsageInfo(
        total_gb=total_gb, used_percent=used_percent, free_gb=free_gb
    )

    return disk_usage_info


def generate_drive_registry(drive_paths: list[str]) -> list[DriveInfo]:
    registry = [
        DriveInfo(path=path, storage=get_disk_usage(path)) for path in drive_paths
    ]

    return registry


disk_registry: list[DriveInfo] = generate_drive_registry(
    drive_paths=configuration.drive_paths
)

print("{:.2f}".format(disk_registry[0].storage.used_percent))
print()
print(disk_registry[0])
