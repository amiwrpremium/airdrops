import sys
import os
import time

from colorama import init as colorama_init
from termcolor import colored

from xrpy import Wallet, JsonRpcClient, set_trust_line

from constants import XRPL_FOUNDATION
from csv_func import WalletCSV
from utils import Report


colorama_init()
XRP_MAIN_CLIENT = JsonRpcClient(XRPL_FOUNDATION)
report = Report()


def clear():
    if os.name == 'posix':
        os.system('clear')
    elif os.name == 'nt':
        os.system('cls')
    else:
        pass


def mass_trust_line(path_to_csv: str, currency: str, value: int, issuer: str, sleep_time: int = 0):
    print(
        colored(
            text=f'{path_to_csv=} | {currency=} | {value=} | {issuer=}',
            color='cyan'
        )
    )

    wallet_csv = WalletCSV(path_to_csv)
    wallet_data = wallet_csv.get_all_csv_info()[1:]

    print(colored(text=f'{len(wallet_data)} wallets imported\n\n', color='magenta'))

    for data in wallet_data:
        print(colored(text=f'{data}', color='yellow'))

        wallet = Wallet(data[wallet_csv.seed_index], data[wallet_csv.sequence_index])

        try:
            _trust_line = set_trust_line(XRP_MAIN_CLIENT, wallet, currency, str(value), issuer)

            if _trust_line and (_trust_line.result.get("meta").get("TransactionResult")) == 'tesSUCCESS':
                report.add_success()

                print(colored(
                    text=f'Status: Success',
                    color='green'
                ))

                time.sleep(sleep_time)
            else:
                report.add_failed()
                print(colored(text=f'Failed: [Unknown Error]', color='red'))
                continue

        except Exception as e:
            report.add_failed()
            print(colored(text=f'Error: {e}', color='red'))
            continue


def enter():
    path_to_csv = input('Enter path to csv file: ')

    currency = input('Enter currency: ')

    try:
        value = int(input('Enter value: '))
    except ValueError:
        sys.exit('Value must be an integer')

    issuer = input('Enter issuer: ')

    try:
        sleep_time = int(input('Enter sleep time: '))
    except ValueError:
        sys.exit('Sleep time must be an integer')

    if sleep_time < 0:
        sys.exit('Invalid sleep time')

    clear()

    mass_trust_line(path_to_csv, currency, value, issuer, sleep_time)

    print('\n\n')
    print(report.get_report())


if __name__ == '__main__':
    enter()
