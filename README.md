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

Recursively walks a parent folder — including any number of nested subfolders — and **moves** all image and video files it finds into a single flat destination folder. Built for restoring photos/videos pulled off an Android device, where media often ends up scattered across deeply nested `DCIM`, `WhatsApp`, `Pictures`, etc. folders.

**Files:** `scripts/media-scraper/`

> ⚠️ **This moves files, it does not copy them.** The source files are removed from their original location. Make sure you have a backup of the source folder before running this if you're not 100% sure, especially on a first run.

### What it does

- Recursively scans a source directory tree of any depth
- Detects media by MIME type (`image/*`, `video/*`) with an extension fallback (covers RAW formats like `.cr2`, `.nef`, `.arw`, `.dng`, and HEIC)
- Moves every match into one flat destination folder
- Auto-renames on filename collision (`IMG_0001.jpg` → `IMG_0001_1.jpg`) instead of overwriting
- Skips files already inside the destination folder, so it's safe to re-run
- Prints a live log of every file moved, plus a final summary count

### Requirements

- Python 3.x
- No external dependencies (uses only the standard library: `os`, `shutil`, `mimetypes`, `pathlib`)

### Usage

Run the script and answer the two prompts:

```bash
python3 media_scraper.py
```

```text
=== Media File Consolidator ===
Enter the parent source folder path: ~/AndroidBackup/DCIM
Enter the destination folder path: ~/RestoredPhotos
```

Paths support `~` and are resolved to absolute paths automatically.

### Example

```text
AndroidBackup/DCIM/
├── Camera/2023/IMG_001.jpg
├── WhatsApp/Media/IMG_001.jpg      <- same filename, different folder
└── Screenshots/old/shot.png
```

Result:

```text
RestoredPhotos/
├── IMG_001.jpg
├── IMG_001_1.jpg                  <- renamed to avoid overwrite
└── shot.png
```

### Notes

- Destination cannot be a subfolder of source (the script blocks this to avoid an infinite/self-referential move).
- Only images and videos are touched — audio, documents, and everything else is left untouched in place.
- There's currently no `--dry-run` or undo — if you want to preview what would move before committing, that'd be a good next feature to add.
