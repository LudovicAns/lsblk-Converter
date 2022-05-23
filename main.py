import os
from pathlib import Path


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
    MOUNTING_FOLDER = "hdd"
    disks = get_mountable_disk()
    lines = []
    for i in range(len(disks)):
        lines.append(f"sudo mount /dev/{disks[i]} /mnt/{MOUNTING_FOLDER}{i+1}")
    with open("mounting_commands.sh", 'w') as file:
        file.write('\n'.join(lines))
    os.system("chmod +x mounting_commands.sh")
