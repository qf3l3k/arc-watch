# ARC Coin Masternode Watcher
Running ARC coin masternodes showed that some of nodes might go into EXPIRED or NEW_START_REQUIRED mode.
In some cases it is enough just to restart masternode service and in some cases blockchain has to be resynchronized.
Regardless situation it takes time to logon to identify situation and take apropriate action.
So, better way would be to automate process of detecting what happened to masternode and react accordingly.
That has been main driver for that Python script.

arc_watch.py operates in 2 modes:
 - dashboard
 - fix


## Requirements
* Python package: prettytable
* ARC wallet with masternodes configuration and RPC enabled
* Binaries of ARC client installed on system with script (here are binaries: https://github.com/ArcticCore/arcticcoin/releases/download/v0.13.0/arc-0.13.0-linux64.tar.gz)
* Ansible

## Installation
To use script simply clone

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

### Start script
Easiest way to make arc-watch work for you is to execute script included as part of a solution, which leverages tmux.
For that simply execute commands:

```bash
cd /opt/arc-watch/tmux
./tmux_arc_watch.sh
```

That will start tmux and create 3 windows with:
* dashboard
* fixing status
* arc-watch log


## Usage manual

### Display nodes status

To display dashboard with nodes details:

```bash
cd /opt/arc-watch
python arc_watch.py -d
```

That will display table similar to one below

```text
+-------------+---------------------+---------+--------+---------+
|    alias    |       address       |  status | action | command |
+-------------+---------------------+---------+--------+---------+
|    node01   |   XX.XX.XX.XX:7209  | ENABLED |  None  |         |
|    node02   |   XX.XX.XX.XX:7209  | ENABLED |  None  |         |
|    node03   |   XX.XX.XX.XX:7209  | ENABLED |  None  |         |
|    node04   |   XX.XX.XX.XX:7209  | ENABLED |  None  |         |
|    node05   |   XX.XX.XX.XX:7209  | ENABLED |  None  |         |
+-------------+---------------------+---------+--------+---------+
```
**NOTE:** *Number of nodes displayed depends on details received from ARC wallet via RPC.*

### Fix nodes

To run fixing process and reset or restart nodes:
```bash
cd /opt/arc-watch
python arc_watch.py -f
```

This will display:

```text
Acquiring node information.
Starting fix process.
Done.
```

However, if there will be some nodes to fix script will also show progress of fixing.



## Release History

## Meta
