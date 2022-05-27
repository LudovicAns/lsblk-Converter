import os
import json
from pathlib import Path


MOUNTING_POINT = "disk"
MOUNTING_PATH = "/mnt/"
MOUNTING_SKRIPT_PATH = "./"


def get_mountable_disk() -> [str]:
    os.system("lsblk > lsblk.txt")
    disks = []
    with open(Path("lsblk.txt"), 'r') as file:
        lines = file.readlines()
    for i in range(len(lines)):
        line = lines[i]
        if line.startswith("sd"):
            j = 1
            if lines[i+j].startswith("└─") or lines[i+j].startswith("├─"):
                while lines[i+j].startswith("└─") or lines[i+j].startswith("├─"):
                    next_line = lines[i+j].split(" ")[0][2:]
                    disks.append(next_line)
                    j += 1
            else:
                disks.append(line.split(" ")[0])
    return disks


if __name__ == "__main__":
    config_path = Path(__file__)
    with open(config_path.parent.joinpath("conf.json"), 'r') as config_file:
        config = json.load(config_file)
        MOUNTING_POINT = config["diskName"]
        MOUNTING_PATH = config["mountingPath"]
        MOUNTING_SKRIPT_PATH = config["mountingSkriptPath"]

    disks = get_mountable_disk()
    lines = []

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
