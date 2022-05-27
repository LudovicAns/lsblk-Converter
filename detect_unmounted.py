import os
from pathlib import Path


def get_disk_path() -> [[str, str]]:
    os.system("lsblk > lsblk.txt")
    disks = []
    with open(Path(__file__).parent.joinpath("lsblk.txt"), 'r') as file:
        lines = file.readlines()
    for i in range(len(lines)):
        line = lines[i]
        if line.startswith("sd"):
            j = 1
            if lines[i+j].startswith("└─") or lines[i+j].startswith("├─"):
                while lines[i+j].startswith("└─") or lines[i+j].startswith("├─"):
                    disk_mount_path = lines[i+j].split(" ")[-1]
                    disk_name = lines[i+j].split(" ")[0][2:]
                    disks.append([disk_name, disk_mount_path])
                    j += 1
            else:
                disks.append([line.split(" ")[0], line.split(" ")[-1]])
    return disks


def get_unmounted_disk(disks_path: [[str, str]]) -> [str]:
    result = []
    for disk_path in disks_path:
        if not str(disk_path[1]).startswith("/"):
            result.append(disk_path[0])
    return result


if __name__ == "__main__":
    disks_path = get_disk_path()
    print("📌 See below the list of unmounted disk:")
    print("\n".join(get_unmounted_disk(disks_path)))
