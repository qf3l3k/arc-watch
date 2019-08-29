# ARC Coin Masternode Watcher
Running ARC coin masternodes showed that some of nodes might go into EXPIRED ot NEW_START_REQUIRED mode.
In some cases it is enough just to restart masternode service and in some cases blockchain has to be resynchronized.
Regardless situation it takes time to logon to identify situation and take apropriate action.
So, better way would be to automate process of detecting what happened to masternode and react accordingly.
That has been main driver for that Python script.

---
## Requirements
* ARC wallet with masternodes configuration and RPC enabled
* Ansible (for future functionality to allow node reset)
---
## Installation

---
## Features

---
## Usage

To display dashboard with nodes details:
```bash
python arc_watch.py -d
```

To run fixing process and reset or restart nodes:
```bash
python arc_watch.py -f
```

That will result in table similar to one below

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

Number of nodes displayed depends on details received from ARC wallet via RPC.

---
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

---
## Release History

---
## Meta



**Edit a file, create a new file, and clone from Bitbucket in under 2 minutes**

When you're done, you can delete the content in this README and update the file with details for others getting started with your repository.

*We recommend that you open this README in another tab as you perform the tasks below. You can [watch our video](https://youtu.be/0ocf7u76WSo) for a full demo of all the steps in this tutorial. Open the video in a new tab to avoid leaving Bitbucket.*

---

## Edit a file

You’ll start by editing this README file to learn how to edit a file in Bitbucket.

1. Click **Source** on the left side.
2. Click the README.md link from the list of files.
3. Click the **Edit** button.
4. Delete the following text: *Delete this line to make a change to the README from Bitbucket.*
5. After making your change, click **Commit** and then **Commit** again in the dialog. The commit page will open and you’ll see the change you just made.
6. Go back to the **Source** page.

---

## Create a file

Next, you’ll add a new file to this repository.

1. Click the **New file** button at the top of the **Source** page.
2. Give the file a filename of **contributors.txt**.
3. Enter your name in the empty file space.
4. Click **Commit** and then **Commit** again in the dialog.
5. Go back to the **Source** page.

Before you move on, go ahead and explore the repository. You've already seen the **Source** page, but check out the **Commits**, **Branches**, and **Settings** pages.

---

## Clone a repository

Use these steps to clone from SourceTree, our client for using the repository command-line free. Cloning allows you to work on your files locally. If you don't yet have SourceTree, [download and install first](https://www.sourcetreeapp.com/). If you prefer to clone from the command line, see [Clone a repository](https://confluence.atlassian.com/x/4whODQ).

1. You’ll see the clone button under the **Source** heading. Click that button.
2. Now click **Check out in SourceTree**. You may need to create a SourceTree account or log in.
3. When you see the **Clone New** dialog in SourceTree, update the destination path and name if you’d like to and then click **Clone**.
4. Open the directory you just created to see your repository’s files.

Now that you're more familiar with your Bitbucket repository, go ahead and add a new file locally. You can [push your change back to Bitbucket with SourceTree](https://confluence.atlassian.com/x/iqyBMg), or you can [add, commit,](https://confluence.atlassian.com/x/8QhODQ) and [push from the command line](https://confluence.atlassian.com/x/NQ0zDQ).