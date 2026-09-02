# My Scripts

A collection of useful scripts for automating everyday tasks on Linux.

## 📜 Table of Contents

- [Send via Tailscale](#send-via-tailscale)

---

## Send via Tailscale

Adds a menu option to Nautilus for selecting files and sending them to other devices connected to your Tailscale network.

**Files:** `scripts/send-via-tailscale/`

### Setup

...(installation steps for the Nautilus menu itself)...

### Make It Automatic (The Permanent Way)

If you don't want to run a terminal command every time you reboot, set it up as a permanent background service.

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

<!--
## Next Script Name

Short description of what it does.

**Files:** `scripts/next-script/`

### Setup

...
-->
