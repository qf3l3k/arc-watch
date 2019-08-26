#!/usr/bin/env python

# Print table with loaded data
# Status color coding:
#  - GREEN = ENABLED
#  - YELLOW = PRE_ENABLED
#  - RED = EXPIRED
#  - RED = NEW_START_REQUIRED
#  - BLUE = Other status not listed above

# Remediate RED status
#  - EXPIRED - recycle ARC blockchain
#  - NEW_START_REQUIRED - recycle ARC blockchain and start alias
# Remediation might be done from python or by triggering Ansible playbook


import os
import logging
import argparse
import configparser
from collections import OrderedDict
from json import JSONDecoder
from prettytable import PrettyTable
from modules import color_terminal

data_acquire_command = "arcticcoin-cli -rpcconnect=192.168.101.11 -rpcuser=rpcuser -rpcpassword=abc123 " \
                       "goldminenode list-conf"
start_node_command = "arcticcoin-cli -rpcconnect=192.168.101.11 -rpcuser=rpcuser -rpcpassword=abc123 " \
                       "goldminenode start-alias {}"
recycle_node_command = "ansible-playbook -i '{},' /full/path/to/playbook/arc_chain_reset.yaml"

# data_acquire_command = ""
# start_node_command = ""
# recycle_node_command = ""


config_file = "{}/config/arc_watch.conf"


logging.basicConfig(filename='logs/arc_watch.log', filemode='a',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


def make_unique(key, dct):
    counter = 0
    unique_key = key

    while unique_key in dct:
        counter += 1
        unique_key = '{}_{}'.format(key, counter)
    return unique_key


def parse_object_pairs(pairs):
    dct = OrderedDict()
    for key, value in pairs:
        if key in dct:
            key = make_unique(key, dct)
        dct[key] = value

    return dct


def read_parse_data():
    data = os.popen(data_acquire_command).read()

    decoder = JSONDecoder(object_pairs_hook=parse_object_pairs)
    obj = decoder.decode(data)

    return obj


def print_status_table(parsed_data):
    command = ""

    node_table = PrettyTable()
    node_table.field_names = ["alias", "address", "status", "action", "command"]

    for key, value in parsed_data.items():
        if value['status'] == "ENABLED":
            message_color = color_terminal.Green
            action_taken = "None"
            command = ""

        elif value['status'] == "EXPIRED":
            message_color = color_terminal.Red
            action_taken = "Recycle"
            command = process_node(value['alias'], value['status'])

        elif value['status'] == "NEW_START_REQUIRED":
            message_color = color_terminal.Red
            action_taken = "Recycle + restart"
            command = process_node(value['alias'], value['status'])

        elif value['status'] == "PRE_ENABLED":
            message_color = color_terminal.Yellow
            action_taken = "Waiting"
            command = ""

        else:
            message_color = color_terminal.Blue
            action_taken = "None"

        node_table.add_row([
            value['alias'],
            value['address'],
            message_color + value['status'] + color_terminal.Color_Off,
            action_taken,
            command[0:34]
        ])

        node_table.sortby = "alias"

    print(node_table)


def process_node(node_name, node_status):
    command = ""

    if node_status == "EXPIRED":
        command = recycle_node_command.format(node_name)

    elif node_status == "NEW_START_REQUIRED":
        command = start_node_command.format(node_name)

    return command


def fix_nodes(parsed_data):
    command = ""

    for key, value in parsed_data.items():
        command = process_node(value['alias'], value['status'])

        if command:
            logging.info("Processing node {} with command: {}".format(value['alias'], command))
            exec_result = os.popen(command).read()
            print("Results: {}".format(exec_result))

    return command


def read_config():
    # TODO: Read and parse arc_watch config file

    config_file_location = config_file.format(os.getcwd())

    config = configparser.ConfigParser()
    config.read(config_file_location)

    print("Config file: {}".format(config_file_location))

    data_acquire_command = config.get("node", "data_acquire_command")
    start_node_command = config.get("node", "start_node_command")
    recycle_node_command = config.get("node", "recycle_node_command")

    print("Data acquire: {}".format(data_acquire_command))
    print("\n")
    print("Start node: {}".format(start_node_command))
    print("\n")
    print("Recycle: {}".format(recycle_node_command))
    print("\n")
    print("Done.")

    return 1


def main():
    cmdparser = argparse.ArgumentParser()
    cmdparser.version = "0.2"
    cmdparser.add_argument("-d", "--dashboard", help="displays nodes status", action="store_true")
    cmdparser.add_argument("-f", "--fix", help="fixes EXPIRED and/or NEW_START_REQUIRED nodes", action="store_true")
    cmdparser.add_argument("-t", "--test", help="for testing different parts of script",  action="store_true")
    cmdparser.add_argument("-v", "--version",  action="version")
    args = cmdparser.parse_args()

    nodes_data = read_parse_data()

    if args.dashboard:
        logging.info("Started in dashboard mode.")
        print_status_table(nodes_data)

    elif args.fix:
        fix_nodes(nodes_data)

    elif args.test:
        read_config()


main()
