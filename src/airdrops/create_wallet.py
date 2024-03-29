import sys
import os
import time

import argparse
import traceback

from uuid import uuid4

from random import randint

from colorama import init as colorama_init
from termcolor import colored

from xrpy import Wallet, XRPY


if __name__ == '__main__':
    from constants import XRP_TESTNET_URL, CREATE_WALLET_TEXT, DONATION_TEXT, DONATION_REQ, WALLETS
    from csv_func import WalletCSV
    from utils import Report
else:
    from .constants import XRP_TESTNET_URL, CREATE_WALLET_TEXT, DONATION_TEXT, DONATION_REQ, WALLETS
    from .csv_func import WalletCSV
    from .utils import Report


parser = argparse.ArgumentParser(description='Set trustline for airdrop wallets')
parser.add_argument('--debug', '-D', dest='debug', help='Debug mode', action='store_true')
args = parser.parse_args()
debug = True if args.debug else False


colorama_init()
xrpy = XRPY(XRP_TESTNET_URL)
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


def mass_wallet_creator(count: int = 10, min_sleep_time: int = 0, max_sleep_time: int = 0, __debug: bool = False):
    wallet_csv = WalletCSV(f'wallets-{str(uuid4())}.csv')
    wallet_csv.write_headers()

    print(
        colored(
            text=f"{count=} | {min_sleep_time=} | {max_sleep_time=}",
            color='cyan'
        )
    )

    if count == -1:
        count = sys.maxsize

    for i in range(count):
        try:
            print(colored(text=f'Trying To Create Wallet: [{i+1}/{count}]', color='yellow'))

            wallet = xrpy.create_wallet()

            if wallet and type(wallet) == Wallet and wallet.classic_address:
                report.add_success()
                wallet_csv.insert_to_csv(wallet)

                print(colored(f'Created wallet: {wallet.classic_address} | [{i+1}/{count}]', color='green'))

                sleep_time = randint(min_sleep_time, max_sleep_time)
                print(colored(text=f"Sleeping for {sleep_time} seconds. zZz...", color='blue'))
                time.sleep(sleep_time)

            else:
                report.add_failed()
                print(colored(f'Failed to create wallet: {wallet=} | {type(wallet)=}', color='red'))

        except Exception as e:
            report.add_failed()
            print(colored(f'Error: {e}', color='red'))
            if debug or __debug:
                print(colored(text=f'Traceback: {traceback.format_exc()}', color='red'))
            continue


def enter(__debug: bool = False):
    if debug or __debug:
        print(colored(text=f'DEBUG MODE\n\n', color='red', attrs=['blink', 'bold']))

    print(colored(text=CREATE_WALLET_TEXT, color='cyan'))

    count = int(input('Enter count: '))

    if count < -1 or count == 0:
        print(colored(text='\n\nInvalid count', color='red'))
        sys.exit()

    try:
        min_sleep_time = int(input('Enter min sleep time: '))
        max_sleep_time = int(input('Enter max sleep time: '))
    except ValueError:
        print(colored(text='\n\nInvalid sleep time should be integer', color='red'))
        sys.exit()

    if min_sleep_time < 0 or max_sleep_time < 0:
        print(colored(text='\n\nInvalid sleep time', color='red'))
        sys.exit()

    if min_sleep_time > max_sleep_time:
        print(colored(text='\n\nMin sleep time must be less than max sleep time', color='red'))
        sys.exit()

    clear()

    try:
        mass_wallet_creator(count, min_sleep_time, max_sleep_time, debug or __debug)
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
