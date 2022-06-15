import os
import platform
from pathlib import Path
from typing import List


class DiskManager:
    """
    DiskManager is used to manage disk.
    For now, you can only use it on Linux and macOS.
    """

    _COMPATIBLE_OS = ["Linux", "macOS"]
    _PATH = Path().parent

    def __init__(self):
        os = platform.platform().split('-')[0]
        if os not in DiskManager._COMPATIBLE_OS:
            raise EnvironmentError(f"{os} is not a compatible OS. See list below before using it.")

        self._os = os

    def get_os(self):
        return self._os

    def _get_mountable_disk_macos(self) -> List[str]:
        os.system(f"diskutil list > {self._PATH.joinpath('diskutil_list.txt')}")
        disks = []
        with open(self._PATH.joinpath("diskutil_list.txt"), 'r') as file:
            lines = file.readlines()
        for i in range(len(lines)):
            line = lines[i]
            if line.startswith("/dev/"):
                j = 3
                while lines[i+j].startswith("   " + str(j - 2) + ":"):
                    disks.append(lines[i+j].split(" ")[-1][:-1])
                    j += 1
        return disks

    def _get_mountable_disk_linux(self) -> List[str]:
        os.system(f"lsblk > {self._PATH.joinpath('lsblk.txt')}")
        disks = []
        with open(Path("lsblk.txt"), 'r') as file:
            lines = file.readlines()
        for i in range(len(lines)):
            line = lines[i]
            if line.startswith("sd"):
                j = 1
                if lines[i + j].startswith("└─") or lines[i + j].startswith("├─"):
                    while lines[i + j].startswith("└─") or lines[i + j].startswith("├─"):
                        next_line = lines[i + j].split(" ")[0][2:]
                        disks.append(next_line)
                        j += 1
                else:
                    disks.append(line.split(" ")[0])
        return disks

    def get_mountable_disk(self) -> List[str]:
        if self._os == "macOS":
            return self._get_mountable_disk_macos()
        elif self._os == "Linux":
            return self._get_mountable_disk_linux()


if __name__ == "__main__":
    disk_manager = DiskManager()
    print(f"OS: {disk_manager.get_os()}")
    print(f"Mountable Disk: {disk_manager.get_mountable_disk()}")
