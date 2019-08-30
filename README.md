# ARC Coin Masternode Watcher
Running ARC coin masternodes showed that some of nodes might go into EXPIRED or NEW_START_REQUIRED mode.
In some cases it is enough just to restart masternode service and in some cases blockchain has to be resynchronized.
Regardless situation it takes time to logon to identify situation and take apropriate action.
So, better way would be to automate process of detecting what happened to masternode and react accordingly.
That has been main driver for that Python script.

## Requirements
* ARC wallet with masternodes configuration and RPC enabled
* Ansible (for future functionality to allow node reset)

## Installation

## Features

## Usage

To display dashboard with nodes details:
```bash
python arc_watch.py -d
```

That will display table similar to one below

```text
Every 5.0s: python arc_watch.py

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
** *NOTE:* ** *Number of nodes displayed depends on details received from ARC wallet via RPC.*


To run fixing process and reset or restart nodes:
```bash
python arc_watch.py -f
```

This will display:

```text
Acquiring node information.
Starting fix process.
Done.
```

However, if there will be some nodes to fix script will also show progress of fixing.


## Configuration
Configuration details for script to run are located in:
```bash
modules/configu.py
```
Variables in configuration:
```editorconfig
mn_cli="/usr/local/bin/arcticcoin-cli"
host="192.168.248.111"
rpcuser="arcticrpc"
rpcpassword="password12"
mn_list="goldminenode list-conf"
mn_start="goldminenode start-alias"
log_file="arc_watch.log"
log_path="logs/"
playbook_file="arc_chain_reset.yaml"
playbook_path="/home/qf3l3k/automation/crypto-automation/"
```

## Release History

## Meta

