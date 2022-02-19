from typing import Dict

import sys
import os

import argparse
import traceback

from colorama import init as colorama_init
from termcolor import colored

from xrpy import JsonRpcClient, get_account_info, get_reserved_balance


if __name__ == '__main__':
    from constants import XRPL_FOUNDATION, WALLET_BALANCE_TEXT, DONATION_TEXT, DONATION_REQ, WALLETS
    from csv_func import WalletCSV
    from utils import Report, Balance
else:
    from .constants import XRPL_FOUNDATION, WALLET_BALANCE_TEXT, DONATION_TEXT, DONATION_REQ, WALLETS
    from .csv_func import WalletCSV
    from .utils import Report, Balance


parser = argparse.ArgumentParser(description='Set trustline for airdrop wallets')
parser.add_argument('--debug', '-D', dest='debug', help='Debug mode', action='store_true')
args = parser.parse_args()
debug = True if args.debug else False


colorama_init()
XRP_TEST_CLIENT = JsonRpcClient(XRPL_FOUNDATION)
report = Report()
balance_report = Balance()


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
    print(balance_report.get_pretty_report())
    print('\n')
    print(report.get_pretty_report())
    print('\n\n\n')
    print_donation()


def get_wallet_balance(wallet_address: str) -> Dict:
    data = {
        'account': wallet_address,
        'free': 0,
        'reserved': 0,
        'total': 0,
    }
    account_info = get_account_info(XRP_TEST_CLIENT, wallet_address)

    balance = float(account_info.result.get('account_data', {}).get('Balance', 0)) or 0
    reserved_balance = get_reserved_balance(XRP_TEST_CLIENT, wallet_address, True)

    total = round((balance / 1000000), 2)
    reserved = round(reserved_balance, 2) if reserved_balance else 0
    free = total - reserved

    data['total'] = total
    data['reserved'] = reserved
    data['free'] = free

    return data


def mass_balance_checker(path_to_csv: str, __debug: bool = False):
    print(
        colored(
            text=f'{path_to_csv=}\n',
            color='cyan'
        )
    )

    wallet_csv = WalletCSV(path_to_csv)
    wallet_data = wallet_csv.get_all_csv_info()[1:]

    for data in wallet_data:
        print(colored(text=f'{data}', color='yellow'))
        wallet_address = data[wallet_csv.classic_address_index]

        try:
            wallet_balance_data = get_wallet_balance(wallet_address)
        except Exception as e:
            report.add_failed()
            print(colored(text=f'Error: {e}', color='red'))
            if debug or __debug:
                print(colored(text=f'Traceback: {traceback.format_exc()}', color='red'))
            continue

        print(colored(text=f'{wallet_balance_data}', color='green'))
        balance_report.add_from_dict(wallet_balance_data)
        report.add_success()


def enter(__debug: bool = False):
    if debug or __debug:
        print(colored(text=f'DEBUG MODE\n\n', color='red', attrs=['blink', 'bold']))

    print(colored(text=WALLET_BALANCE_TEXT, color='cyan'))

    path_to_csv = input('Enter path to csv file: ').strip()

    try:
        mass_balance_checker(path_to_csv, __debug or debug)
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
