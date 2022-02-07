import requests
import sys
import os

import argparse
import traceback


from colorama import init as colorama_init
from termcolor import colored


from xrpy import Wallet


if __name__ == '__main__':
    from constants import XRP_TESTNET_URL, VALIDATE_GID_TEXT
    from csv_func import WalletCSV
    from utils import Report
else:
    from .constants import XRP_TESTNET_URL, VALIDATE_GID_TEXT
    from .csv_func import WalletCSV
    from .utils import Report


parser = argparse.ArgumentParser(description='Set trustline for airdrop wallets')
parser.add_argument('--debug', '-D', dest='debug', help='Debug mode', action='store_true')
args = parser.parse_args()
debug = True if args.debug else False


colorama_init()
report = Report()
URL = 'https://strategyengine.one/api/globalid/xrpl/whitelist'


def clear():
    if os.name == 'posix':
        os.system('clear')
    elif os.name == 'nt':
        os.system('cls')
    else:
        pass


def print_end_report():
    print('\n\n')
    print(report.get_pretty_report())
    print('\n\n')


def validate(address: str) -> bool:
    r = requests.get(
        f'{URL}/{address}',
    )

    if r.status_code == 200:
        return True
    else:
        return False


def mass_validate(path_to_csv: str, __debug: bool = False):
    if debug or __debug:
        print(colored(text=f'DEBUG MODE\n\n', color='red', attrs=['blink', 'bold']))

    print(
        colored(
            text=f'{path_to_csv=}\n\n',
            color='cyan'
        )
    )

    wallet_csv_write = WalletCSV(f'NO-{os.path.basename(path_to_csv)}.csv')
    wallet_csv_write.write_headers()

    wallet_csv_read = WalletCSV(path_to_csv)
    wallet_data_read = wallet_csv_read.get_all_csv_info()[1:]

    for data in wallet_data_read:
        print(colored(text=f'{data}', color='yellow'))

        try:
            is_validated = validate(data[wallet_csv_read.classic_address_index])
        except Exception as e:
            report.add_failed()
            print(colored(text=f'{e}', color='red'))
            if debug or __debug:
                print(colored(text=f'Traceback: {traceback.format_exc()}', color='red'))
            continue

        if is_validated:
            report.add_success()
            print(colored(text=f'{data[wallet_csv_read.classic_address_index]} is valid', color='green'))
            continue
        else:
            report.add_failed()
            wallet = Wallet(data[wallet_csv_write.seed_index], data[wallet_csv_write.sequence_index])
            wallet_csv_write.insert_to_csv(wallet)
            print(colored(text=f'{data[wallet_csv_read.classic_address_index]} is not valid', color='red'))
            continue


def enter(__debug: bool = False):
    if debug or __debug:
        print(colored(text=f'DEBUG MODE\n\n', color='red', attrs=['blink', 'bold']))

    print(colored(text=VALIDATE_GID_TEXT, color='cyan'))

    path_to_csv = input('Enter path to csv file: ').strip()

    try:
        mass_validate(path_to_csv, __debug)
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
