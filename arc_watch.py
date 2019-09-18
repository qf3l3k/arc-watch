#!/usr/bin/env python3

"""
Script connects to ARC coin wallet via rpc and pulls data about masternodes and their status.
First function script provides is to display acquired data with color coded masternode status.

Status color coding:
 - GREEN = ENABLED
 - YELLOW = PRE_ENABLED
 - RED = EXPIRED
 - RED = NEW_START_REQUIRED
 - BLUE = Other status not listed above

Once some nodes are identified as not properly working script can take action to fix that.

Actions to fix RED status
 - EXPIRED - recycle ARC blockchain
 - NEW_START_REQUIRED - recycle ARC blockchain and start alias

Recycle ARC blockchain means that Ansible playbook will be triggered, which will:
 - stop masternode
 - remove existing blockchain data
 - unpack properly working blockchain data
 - start masternode

This has to be done due to nature of ARC coin blockchain, which tends to stuck for no reason.
Best way to fix it is re-sync node, but full re-sync would take too long, so pre-loaded blockchain data does the job.
"""


import os
import logging
import argparse
from collections import OrderedDict
from json import JSONDecoder
from prettytable import PrettyTable
from modules import color_terminal
from modules import config


logging.basicConfig(filename='{}{}'.format(config.log_path, config.log_file),
                    filemode='a',
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


def read_parse_data(data_source_command):
    data = os.popen(data_source_command).read()

    decoder = JSONDecoder(object_pairs_hook=parse_object_pairs)
    obj = decoder.decode(data)

    return obj


def print_status_table(parsed_data):
    """
    Displays table with masternodes status information.

    Args:
        :param parsed_data: contains masternode details pulled from remote ARC wallet via RPC.

    Returns:
        :return: Nothing is returned.
    """
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
    """
    Composes command-line syntax to be executed in order to remediate faulty masternode.

    Args:
        :param node_name: name of masternode as listed in ARC wallet

        :param node_status: status of masternode, so apropriate command-line syntax will be created.

    Returns:
        :return: command-line syntax, which has to be executed in order to fix masternode.
    """

    command = ""

    if node_status == "EXPIRED":
        command = "ansible-playbook -i '{},' {}{}".format(node_name,
                                                          config.playbook_path,
                                                          config.playbook_file)
    elif node_status == "NEW_START_REQUIRED":
        command = "{} -rpcconnect={} -rpcuser={} -rpcpassword={} {} {}".format(config.mn_cli,
                                                                               config.host,
                                                                               config.rpcuser,
                                                                               config.rpcpassword,
                                                                               config.mn_start,
                                                                               node_name)
    return command


def fix_nodes(parsed_data):
    """
    Executes command-line syntax prepared by process_node function.

    Args:
        :param parsed_data: contains information about masternodes.

    Returns:
        :return: last executed fixing command.
    """

    command = ""

    for key, value in parsed_data.items():
        command = process_node(value['alias'], value['status'])

        if command:
            logging.info("Processing node {} with command: {}".format(value['alias'], command))
            exec_result = os.popen(command).read()
            print("Results: {}".format(exec_result))

    return command


def main():
    """
    Main function runs appropriate action depends on passed parameters.

    Returns:
        :return: nothing is returned from main function.
    """

    cmdparser = argparse.ArgumentParser()
    cmdparser.version = "0.2"
    cmdparser.add_argument("-d", "--dashboard", help="displays nodes status", action="store_true")
    cmdparser.add_argument("-f", "--fix", help="fixes EXPIRED and/or NEW_START_REQUIRED nodes", action="store_true")
    cmdparser.add_argument("-t", "--test", help="for testing different parts of script",  action="store_true")
    cmdparser.add_argument("-v", "--version",  action="version")
    args = cmdparser.parse_args()

    data_acquire_command = "{} -rpcconnect={} -rpcuser={} -rpcpassword={} {}".format(config.mn_cli,
                                                                                     config.host,
                                                                                     config.rpcuser,
                                                                                     config.rpcpassword,
                                                                                     config.mn_list)

    nodes_data = read_parse_data(data_acquire_command)

    if args.dashboard:
        print_status_table(nodes_data)

    elif args.fix:
        logging.info("Started in fix mode.")
        fix_nodes(nodes_data)


main()
