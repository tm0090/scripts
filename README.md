## Scripts info:

Script- Send Via Tailscale: 
it adds a menu to nautilus to select files and send to other devices connected to tailscale net


Make it automatic (The Permanent Way)

If you don't want to run a terminal command every time you reboot, you can set it up as a permanent background service.

Run these commands one by one in your terminal:

    Create a background service folder:
    Bash

    mkdir -p ~/.config/systemd/user/

    Create the service file:
    Bash

    nano ~/.config/systemd/user/tailreceive.service

    Paste this exact text into the file:
    Ini, TOML

    [Unit]
    Description=Taildrop Auto-Receive
    After=network.target

    [Service]
    ExecStart=/usr/bin/tailscale file get --loop --conflict=rename %h/Downloads
    Restart=on-failure

    [Install]
    WantedBy=default.target

    (Save and exit nano by pressing CTRL+O, Enter, then CTRL+X)

    Start the service and enable it to run on boot:
    Bash

    systemctl --user enable --now tailreceive.service

Now, your Linux PC will automatically receive files from your phone 24/7 without you ever needing to type a command again.
