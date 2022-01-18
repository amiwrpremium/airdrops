import sys
import os
import time

import argparse
import traceback

from colorama import init as colorama_init
from termcolor import colored

from xrpy import Wallet, JsonRpcClient, set_trust_line, get_account_trustlines

from constants import XRPL_FOUNDATION
from csv_func import WalletCSV
from utils import Report


parser = argparse.ArgumentParser(description='Set trustline for airdrop wallets')
parser.add_argument('--debug', '-D', dest='debug', help='Debug mode', action='store_true')
args = parser.parse_args()
debug = True if args.debug else False


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


def is_trustline_set(client: JsonRpcClient, address: str, currency: str) -> bool:
    all_trust_lines = get_account_trustlines(client, address)
    lines = all_trust_lines.result.get('lines')

    for line in lines:
        if line.get('currency') == currency:
            return True
        else:
            continue

    return False


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

        try:
            wallet = Wallet(data[wallet_csv.seed_index], data[wallet_csv.sequence_index])
        except Exception as e:
            report.add_failed()
            print(colored(text=f'Error: {e}', color='red'))
            if debug:
                print(colored(text=f'Traceback: {traceback.format_exc()}', color='red'))
            continue

        try:
            _is_set = is_trustline_set(client=XRP_MAIN_CLIENT, address=wallet.classic_address, currency=currency)
        except Exception as e:
            report.add_failed()
            print(colored(text=f'Error: {e}', color='red'))
            if debug:
                print(colored(text=f'Traceback: {traceback.format_exc()}', color='red'))
            continue

        if (_is_set and value == 0) or (not _is_set and value > 0):
            try:
                _trust_line = set_trust_line(XRP_MAIN_CLIENT, wallet, currency, str(value), issuer)
                result = _trust_line.result.get("meta").get("TransactionResult")

                if _trust_line and result == 'tesSUCCESS':
                    report.add_success()

                    print(colored(
                        text=f'Status: Success',
                        color='green'
                    ))

                    time.sleep(sleep_time)
                else:
                    report.add_failed()
                    print(colored(text=f'Failed: [Unknown Error] | [{result}]', color='red'))
                    continue

            except Exception as e:
                report.add_failed()
                print(colored(text=f'Error: {e}', color='red'))
                if debug:
                    print(colored(text=f'Traceback: {traceback.format_exc()}', color='red'))
                continue
        else:
            report.add_failed()
            print(colored(text=f'Failed: [Trustline already set]', color='red'))
            continue


def enter():
    if debug:
        print(colored(text=f'DEBUG MODE\n\n', color='red', attrs=['blink', 'bold']))

    path_to_csv = input('Enter path to csv file: ')

    currency = input('Enter currency: ')

    try:
        value = int(input('Enter value: '))
    except ValueError:
        print(colored(text='\n\nValue must be an integer', color='red'))
        sys.exit()

    issuer = input('Enter issuer: ')

    try:
        sleep_time = int(input('Enter sleep time: '))
    except ValueError:
        print(colored(text='\n\nSleep time must be an integer', color='red'))
        sys.exit()

    if sleep_time < 0:
        print(colored(text='\n\nInvalid sleep time', color='red'))
        sys.exit()

    clear()

    mass_trust_line(path_to_csv, currency, value, issuer, sleep_time)

    print('\n\n')
    print(report.get_report())


if __name__ == '__main__':
    clear()
    try:
        enter()
    except KeyboardInterrupt:
        print(colored(text='\n\nExiting...', color='red'))
        sys.exit()
