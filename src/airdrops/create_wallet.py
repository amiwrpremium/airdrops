import sys
import os
import time

from uuid import uuid4

from colorama import init as colorama_init
from termcolor import colored

from xrpy import create_wallet, Wallet, JsonRpcClient

from constants import XRP_TESTNET_URL
from csv_func import WalletCSV
from utils import Report


colorama_init()
XRP_TEST_CLIENT = JsonRpcClient(XRP_TESTNET_URL)

wallet_csv = WalletCSV(f'wallets-{str(uuid4())}.csv')
wallet_csv.write_headers()
report = Report()


def clear():
    if os.name == 'posix':
        os.system('clear')
    elif os.name == 'nt':
        os.system('cls')
    else:
        pass


def mass_wallet_creator(count: int = 10, debug: bool = False, sleep_time: int = 0):
    print(
        colored(
            text=f"{count=} | {debug=} | {sleep_time=}",
            color='cyan'
        )
    )

    if count == -1:
        count = sys.maxsize

    for i in range(count):
        try:
            if debug:
                print(colored(text=f'Trying To Create Wallet: [{i+1}/{count}]', color='yellow'))

            wallet = create_wallet(XRP_TEST_CLIENT)

            if wallet and type(wallet) == Wallet and wallet.classic_address:
                report.add_success()
                wallet_csv.insert_to_csv(wallet)

                if debug:
                    print(colored(f'Created wallet: {wallet.classic_address} | [{i+1}/{count}]', color='green'))

                time.sleep(sleep_time)

            else:
                report.add_failed()
                if debug:
                    print(colored(f'Failed to create wallet: {wallet=} | {type(wallet)=}', color='red'))

        except KeyboardInterrupt:
            return

        except Exception as e:
            report.add_failed()
            print(colored(f'{e}', color='red'))
            continue


def enter():
    count = int(input('Enter count: '))

    if count < -1 or count == 0:
        sys.exit('Invalid count')

    sleep_time = int(input('Enter sleep time: '))

    if sleep_time < 0:
        sys.exit('Invalid sleep time')

    _debug = input('Debug? (y/n): ') or 'y'

    if _debug.lower() == 'y':
        debug = True
    elif _debug.lower() == 'n':
        debug = False
    else:
        sys.exit('Invalid debug')

    clear()

    mass_wallet_creator(count, debug, sleep_time)

    print('\n\n')
    print(report.get_report())


if __name__ == '__main__':
    enter()
