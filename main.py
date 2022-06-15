import os
import json
from pathlib import Path
from typing import List

from DiskManager import DiskManager

MOUNTING_POINT = "disk"
MOUNTING_PATH = "/mnt/"
MOUNTING_SKRIPT_PATH = "./"


if __name__ == "__main__":
    config_path = Path(__file__)
    with open(config_path.parent.joinpath("conf.json"), 'r') as config_file:
        config = json.load(config_file)
        MOUNTING_POINT = config["diskName"]
        MOUNTING_PATH = config["mountingPath"]
        MOUNTING_SKRIPT_PATH = config["mountingSkriptPath"]

    dm = DiskManager()
    disks = dm.get_mountable_disk()
    lines = []

    print(MOUNTING_PATH,  MOUNTING_POINT, MOUNTING_SKRIPT_PATH, "\n")
    print(disks)
    exit()

    for i in range(len(disks)):
        lines.append(f"sudo mount /dev/{disks[i]} {MOUNTING_PATH}{MOUNTING_POINT}{i+1}")

    with open("mounting_commands.sh", 'w') as file:
        file.write('\n'.join(lines))
    os.system("chmod +x mounting_commands.sh")

    for i in range(len(disks)):
        print(f"💿 Mounting /dev/{disks[i]} to {MOUNTING_PATH}{MOUNTING_POINT}{i+1} ...")
        disk_folder = Path(f"{MOUNTING_PATH}{MOUNTING_POINT}{i+1}")
        disk_folder.mkdir(parents=True, exist_ok=True)

        if os.system(f"sudo mount /dev/{disks[i]} {MOUNTING_PATH}{MOUNTING_POINT}{i+1}") == 0:
            print(f"✅ /dev/{disks[i]} has been mounted !")
