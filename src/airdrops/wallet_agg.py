from typing import List

import sys
import os

import argparse
import traceback

from uuid import uuid4

from colorama import init as colorama_init
from termcolor import colored


from xrpy import Wallet


if __name__ == '__main__':
    from .constants import AGGREGATE_WALLETS_TEXT, DONATION_TEXT, DONATION_REQ, WALLETS
    from csv_func import WalletCSV
    from utils import Report
else:
    from .constants import AGGREGATE_WALLETS_TEXT, DONATION_TEXT, DONATION_REQ, WALLETS
    from .csv_func import WalletCSV
    from .utils import Report


parser = argparse.ArgumentParser(description='Set trustline for airdrop wallets')
parser.add_argument('--debug', '-D', dest='debug', help='Debug mode', action='store_true')
args = parser.parse_args()
debug = True if args.debug else False


colorama_init()
report = Report()


def clear():
    if os.name == 'posix':
        os.system('clear')
    elif os.name == 'nt':
        os.system('cls')
    else:
        pass


def print_donation():
    print(
        colored(text=DONATION_TEXT, color='yellow', attrs=['blink', 'bold']) + "\n" +
        colored(text=DONATION_REQ, color='cyan') + "\n\n" +
        colored(text=WALLETS, color='white')
    )


def print_end_report():
    print('\n\n')
    print(report.get_pretty_report())
    print('\n\n\n')
    print_donation()


def aggregator(all_csv_files: List[str], __debug: bool = False):
    print(
        colored(
            text=f'{all_csv_files=}\n\n',
            color='cyan'
        )
    )

    wallet_csv_write = WalletCSV(f'Aggregated-Wallets-{str(uuid4())}.csv')
    wallet_csv_write.write_headers()

    for file_path in all_csv_files:
        wallet_csv_read = WalletCSV(file_path)
        wallet_data_read = wallet_csv_read.get_all_csv_info()[1:]

        try:
            for data in wallet_data_read:
                wallet = Wallet(data[wallet_csv_write.seed_index], data[wallet_csv_write.sequence_index])
                wallet_csv_write.insert_to_csv(wallet)
            report.add_success()
        except Exception as e:
            report.add_failed()
            print(colored(text=f'{e=}\n\n', color='red'))
            if debug or __debug:
                print(colored(text=f'Traceback: {traceback.format_exc()}', color='red'))
            continue


def enter(__debug: bool = False):
    if debug or __debug:
        print(colored(text=f'DEBUG MODE\n\n', color='red', attrs=['blink', 'bold']))

    print(colored(text=AGGREGATE_WALLETS_TEXT, color='cyan'))

    all_csv_files = []

    while True:
        file_path = input("Enter: ").strip()
        if file_path.isspace() or file_path == "":
            break
        else:
            all_csv_files.append(file_path)

    try:
        aggregator(all_csv_files, __debug)
        print_end_report()
    except KeyboardInterrupt:
        print_end_report()


if __name__ == '__main__':
    clear()
    try:
        enter()
    except KeyboardInterrupt:
        print(colored(text='\n\nExiting...', color='red'))
        sys.exit()
