# My Scripts

A collection of useful scripts for automating everyday tasks on Linux.

## 📜 Table of Contents

- [Send via Tailscale](#send-via-tailscale)
- [Media Scraper](#Media-Scraper)

---

## Send via Tailscale

Adds a right-click menu option in Nautilus (Fedora/GNOME Files) for selecting a file and sending it to another device on your Tailscale network via Taildrop.

**Files:** `scripts/send-via-tailscale/`

### Setup — Add the Right-Click Menu (Fedora / Nautilus)

Since Fedora Workstation uses GNOME by default, the right-click menu is added using a Nautilus script and `zenity` (a pop-up dialog tool) to pick the target device.

#### 1. Install Zenity

```bash
sudo dnf install zenity
```

#### 2. Create the right-click script

```bash
nano ~/.local/share/nautilus/scripts/"Send via Tailscale"
```

#### 3. Paste the script

Paste in the contents of [`scripts/send-via-tailscale/Send via Tailscale`](https://github.com/tm0090/scripts/blob/main/Send%20Via%20Tailscale) from this repo.

Save and exit nano: `CTRL+O`, `Enter`, then `CTRL+X`.

#### 4. Make it executable

```bash
chmod +x ~/.local/share/nautilus/scripts/"Send via Tailscale"
```

Now open **Files**, right-click any file → **Scripts** → **Send via Tailscale**. A window will pop up asking which device to send it to.

### Make It Automatic (The Permanent Way)

If you don't want to run a terminal command every time you reboot, set it up as a permanent background service so your PC auto-receives incoming Taildrop files.

Run these commands one by one in your terminal:

#### 1. Create a background service folder

```bash
mkdir -p ~/.config/systemd/user/
```

#### 2. Create the service file

```bash
nano ~/.config/systemd/user/tailreceive.service
```

Paste this exact text into the file:

```ini
[Unit]
Description=Taildrop Auto-Receive
After=network.target

[Service]
ExecStart=/usr/bin/tailscale file get --loop --conflict=rename %h/Downloads
Restart=on-failure

[Install]
WantedBy=default.target
```

Save and exit nano: `CTRL+O`, `Enter`, then `CTRL+X`.

#### 3. Start the service and enable it on boot

```bash
systemctl --user enable --now tailreceive.service
```

Now your Linux PC will automatically receive files from your phone 24/7 — no need to type a command again.

---

## Media Scraper

Recursively walks a parent folder — including any number of nested subfolders — and moves (or copies) all media files it finds into a single flat destination folder. Mainly built for restoring photos/videos pulled off an Android device, where files often end up scattered across deeply nested `DCIM`, `WhatsApp`, `Pictures`, etc. folders.

**Files:** `scripts/media-scraper/`

### What it does

- Scans a source directory tree of any depth
- Detects media files by extension (images, videos, etc.)
- Moves/copies them all into one destination folder
- Handles duplicate filenames (e.g. renames on conflict) — *(adjust this line to match actual behavior)*

### Requirements

- Python 3.x
- *(list any pip packages here, or "no external dependencies")*

### Usage

```bash
python3 media_scraper.py /path/to/source /path/to/destination
```

*(adjust args/flags to match your actual script — e.g. `--copy` vs `--move`, `--dry-run`, extension filters, etc.)*

### Example

```bash
python3 media_scraper.py ~/AndroidBackup/DCIM ~/RestoredPhotos
```

Before:

AndroidBackup/DCIM/
├── Camera/2023/IMG_001.jpg
├── WhatsApp/Media/IMG-20230101.jpg
└── Screenshots/old/shot.png


After:

RestoredPhotos/
├── IMG_001.jpg
├── IMG-20230101.jpg
└── shot.png
