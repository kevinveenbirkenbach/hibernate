#!/usr/bin/env python3

import subprocess
import os
import re
import argparse

SWAPFILE = "/swapfile"
FSTAB = "/etc/fstab"
GRUB_CONF = "/etc/default/grub"
MKINITCPIO = "/etc/mkinitcpio.conf"

def run(cmd, capture=False):
    if capture:
        return subprocess.check_output(cmd, shell=True, text=True).strip()
    subprocess.run(cmd, shell=True, check=True)

def create_swapfile(size_gb):
    print(f"[+] Creating {size_gb}G swapfile...")
    run(f"fallocate -l {size_gb}G {SWAPFILE}")
    run(f"chmod 600 {SWAPFILE}")
    run(f"mkswap {SWAPFILE}")
    run(f"swapon {SWAPFILE}")

def update_fstab():
    print("[+] Ensuring swapfile is in /etc/fstab...")
    with open(FSTAB, "r") as f:
        if SWAPFILE in f.read():
            print("[-] Swapfile already in fstab.")
            return
    with open(FSTAB, "a") as f:
        f.write(f"{SWAPFILE} none swap defaults 0 0\n")

def get_swap_uuid():
    print("[+] Getting swap UUID...")
    uuid = run(f"findmnt -no UUID -T {SWAPFILE}", capture=True)
    return uuid

def get_resume_offset():
    print("[+] Calculating resume_offset...")
    out = run(f"filefrag -v {SWAPFILE}", capture=True)
    match = re.search(r"^\s*0:\s+(\d+)", out, re.MULTILINE)
    if match:
        return match.group(1)
    raise RuntimeError("Couldn't find resume offset.")

def update_grub(uuid, offset):
    print("[+] Updating GRUB_CMDLINE_LINUX_DEFAULT...")
    with open(GRUB_CONF, "r") as f:
        lines = f.readlines()
    for i, line in enumerate(lines):
        if line.startswith("GRUB_CMDLINE_LINUX_DEFAULT"):
            line = re.sub(r'resume=UUID=\S+', '', line)
            line = re.sub(r'resume_offset=\S+', '', line)
            new = f'resume=UUID={uuid} resume_offset={offset}'
            if '"' in line:
                lines[i] = re.sub(r'"$', f' {new}"', line)
            else:
                lines[i] = line.strip() + f' {new}\n'
            break
    with open(GRUB_CONF, "w") as f:
        f.writelines(lines)
    run("update-grub")

def update_mkinitcpio():
    print("[+] Ensuring resume hook in mkinitcpio.conf...")
    with open(MKINITCPIO, "r") as f:
        lines = f.readlines()
    for i, line in enumerate(lines):
        if line.startswith("HOOKS="):
            if "resume" not in line:
                line = line.strip().rstrip(")") + " resume)"
                lines[i] = line + "\n"
            break
    with open(MKINITCPIO, "w") as f:
        f.writelines(lines)
    run("mkinitcpio -P")

def main():
    if os.geteuid() != 0:
        print("This script must be run as root.")
        return

    parser = argparse.ArgumentParser(description="Configure hibernation with optional swapfile setup.")
    parser.add_argument("--create-swapfile", action="store_true", help="Create and configure a swapfile")
    parser.add_argument("--swap-size", type=int, default=32, help="Swapfile size in GB (default: 32)")
    args = parser.parse_args()

    if args.create_swapfile:
        create_swapfile(args.swap_size)
        update_fstab()

    uuid = get_swap_uuid()
    offset = get_resume_offset()
    update_grub(uuid, offset)
    update_mkinitcpio()

    print("\n✅ Hibernate setup complete. Please reboot your system:")
    print("    sudo reboot")

if __name__ == "__main__":
    main()

