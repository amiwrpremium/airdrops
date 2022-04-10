import sys
import os

import argparse
import traceback


from colorama import init as colorama_init
from termcolor import colored

from xrpy import Wallet, XRPY
from xrpl import XRPLException


XRPLException


if __name__ == '__main__':
    from constants import DELETE_WALLET_TEXT, DONATION_TEXT, DONATION_REQ, WALLETS
    from csv_func import WalletCSV
    from utils import Report
else:
    from .constants import DELETE_WALLET_TEXT, DONATION_TEXT, DONATION_REQ, WALLETS
    from .csv_func import WalletCSV
    from .utils import Report

parser = argparse.ArgumentParser(description='Set trustline for airdrop wallets')
parser.add_argument('--debug', '-D', dest='debug', help='Debug mode', action='store_true')
args = parser.parse_args()
debug = True if args.debug else False

colorama_init()
xrpy = XRPY('https://s2.ripple.com:51234/')
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


def is_trustline_set(address: str, currency: str) -> bool:
    all_trust_lines = xrpy.get_account_trustlines(address)
    lines = all_trust_lines.result.get('lines')

    for line in lines:
        if line.get('currency') == currency:
            return True
        else:
            continue

    return False


def mass_delete_account(path_to_csv: str, destination: str, destination_tag: int,
                        threaded: bool, max_workers: int, __debug: bool = False):
    print(
        colored(
            text=f'{path_to_csv=}\n'
                 f'{destination=}\n'
                 f'{destination_tag=}\n'
                 f'{threaded=}\n'
                 f'{max_workers=}\n\n',
            color='cyan'
        )
    )

    wallet_csv_write = WalletCSV(f'NO-{os.path.basename(path_to_csv)}')
    wallet_csv_write.write_headers()

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
            if debug or __debug:
                print(colored(text=f'Traceback: {traceback.format_exc()}', color='red'))
            continue

        try:
            delete = xrpy.advanced_delete_account(wallet, destination, destination_tag, threaded, max_workers)
            result = delete.get('DeleteAccount').result.get("meta").get("TransactionResult")

            if delete and result == 'tesSUCCESS':
                report.add_success()

                print(colored(
                    text=f'Status: Success',
                    color='green'
                ))
            else:
                report.add_failed()
                print(colored(text=f'Failed: [Unknown Error] | [{result}]', color='red'))
                __wallet = Wallet(data[wallet_csv_write.seed_index], data[wallet_csv_write.sequence_index])
                wallet_csv_write.insert_to_csv(__wallet)
                continue

        except Exception as e:
            report.add_failed()
            print(colored(text=f'Error: {e}', color='red'))

            __wallet = Wallet(data[wallet_csv_write.seed_index], data[wallet_csv_write.sequence_index])
            wallet_csv_write.insert_to_csv(__wallet)

            if debug or __debug:
                print(colored(text=f'Traceback: {traceback.format_exc()}', color='red'))

            continue

    try_again = input(colored(text='\n\nTry again? (y/n) ', color='cyan'))
    if try_again.lower() == 'y':
        clear()
        mass_delete_account(
            path_to_csv,
            destination,
            destination_tag,
            threaded,
            max_workers,
            __debug
        )


def enter(__debug: bool = False):
    if debug or __debug:
        print(colored(text=f'DEBUG MODE\n\n', color='red', attrs=['blink', 'bold']))

    print(colored(text=DELETE_WALLET_TEXT, color='cyan'))

    path_to_csv = input('Enter path to csv file: ').strip()

    destination = input('Enter destination wallet address: ')
    destination_tag = input('Enter destination tag / wallet memo (leave blank if None): ')

    if destination_tag == '':
        destination_tag = None
    else:
        try:
            destination_tag = int(destination_tag)
        except ValueError:
            print(colored(text='\n\nDestination Tag must be an integer', color='red'))
            sys.exit()

    threaded = input('Threaded? (y/n) ')

    if threaded.lower() == 'y':
        threaded = True
    else:
        threaded = False

    max_worker = input('Max workers (leave blank if None): ')

    if max_worker == '':
        max_worker = None
    else:
        try:
            max_worker = int(max_worker)
        except ValueError:
            print(colored(text='\n\nMax worker must be an integer', color='red'))
            sys.exit()

    clear()

    try:
        mass_delete_account(path_to_csv, destination, destination_tag,
                            threaded, max_worker, debug or __debug)
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
