# arc-watch
Checks and fixes ARC coin nodes with status EXPIRED or NEW_START_REQUIRED.

## Requirements
* Python package: prettytable
* ARC wallet with masternodes configuration and RPC enabled
* Binaries of ARC client installed on system with script (here are binaries: https://github.com/ArcticCore/arcticcoin/releases/download/v0.13.0/arc-0.13.0-linux64.tar.gz)
* Ansible

## Installation
To use script simply clone repository:

```bash
pip install prettytable
cd /opt
git clone https://github.com/qf3l3k/arc-watch
```

## Configuration
Configuration details for script to run are located in:
```bash
/opt/arc-watch/modules/config.py
```
Make sure you have all data correct in config file, so script will run without errors.

## Usage

* Check configuration in ```bash /opt/arc-watch/modules/config.py``` and make sure all data is relevant to your environment
* Run script to initiate tmix session and start arc-watch:
    ```bash
    cd /opt/arc-watch/tmux
    ./tmux_arc_watch.sh
    ```
* Alternatively run script manually:
    ```bash
    cd /opt/arc-watch
    python arc_watch.py -d # displays dashboard with nodes
    python arc_watch.py -f # runs fixing process for faulty nodes
    ```
