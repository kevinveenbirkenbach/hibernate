# Hibernate Setup Script

A Python-based utility for configuring hibernation on Linux systems using a swap file.  
This script automates resume configuration for GRUB and initramfs, and optionally creates a swap file of configurable size.

---

## 🛠 Features

- Create and activate a swap file (optional)
- Automatically detect UUID and resume offset
- Inject `resume` and `resume_offset` into GRUB
- Regenerate initramfs via `mkinitcpio`
- Supports Arch-based systems (Manjaro, Arch, etc.)
- Root permission required

---

## 📦 Installation

This utility is available via **Kevin’s Package Manager**:  
➡️ [github.com/kevinveenbirkenbach/package-manager](https://github.com/kevinveenbirkenbach/package-manager)

```bash
pkgmgr install setup-hibernate
```

---

## 🚀 Usage

Run the script as root:

```bash
sudo ./hibernate_setup.py [OPTIONS]
```

### Options

| Option                 | Description                                     |
|------------------------|-------------------------------------------------|
| `--create-swapfile`    | Creates a swap file at `/swapfile`             |
| `--swap-size <int>`    | Size in GB (default: `32`)                      |

### Example

```bash
sudo ./hibernate_setup.py --create-swapfile --swap-size 40
```

---

## ✅ Requirements

- Python 3
- Tools: `fallocate`, `mkswap`, `swapon`, `filefrag`, `findmnt`, `mkinitcpio`, `update-grub`
- Root privileges

No external Python packages are required (no `requirements.txt` needed).

---

## 🤖 AI-Assisted Development

This script was developed with the help of [ChatGPT](https://chat.openai.com)  
🔗 [Click here to view the development conversation](https://chatgpt.com/share/67ed158b-66d4-800f-b418-e52460c225ce)

---

## 👤 Author

Developed by **Kevin Veen-Birkenbach**  
🌐 https://www.veen.world/

---

## 📄 License

This project is licensed under the **MIT License**.  
See [LICENSE](./LICENSE) for details.
