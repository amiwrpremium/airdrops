import sys
import os

import argparse
import traceback

from typing import List


from colorama import init as colorama_init
from termcolor import colored


from xrpy import Wallet, JsonRpcClient, get_account_offers, cancel_offer


if __name__ == '__main__':
    from constants import XRPL_FOUNDATION, CANCEL_ORDER_TEXT
    from csv_func import WalletCSV
    from utils import Report
else:
    from .constants import XRPL_FOUNDATION, CANCEL_ORDER_TEXT
    from .csv_func import WalletCSV
    from .utils import Report


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


def get_sequences(address: str) -> List[int]:
    data = []

    account_offers = get_account_offers(XRP_MAIN_CLIENT, address)
    offers = account_offers.result.get('offers')

    if offers and len(offers) > 0:
        for offer in offers:
            sequence = offer.get('seq')
            data.append(sequence)

    return data


def cancel_all_orders(path_to_csv: str, __debug: bool = False):
    print(
        colored(
            text=f"{path_to_csv=}",
            color='cyan',
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
            if debug or __debug:
                print(colored(text=f'Traceback: {traceback.format_exc()}', color='red'))
            continue

        try:
            all_sequences = get_sequences(wallet.classic_address)
        except Exception as e:
            report.add_failed()
            print(colored(text=f'Error: {e}', color='red'))
            if debug or __debug:
                print(colored(text=f'Traceback: {traceback.format_exc()}', color='red'))
            continue

        if all_sequences and len(all_sequences) > 0:
            for sequence in all_sequences:
                try:
                    cancel = cancel_offer(XRP_MAIN_CLIENT, wallet, sequence)
                    result = cancel.result.get("meta").get("TransactionResult")
                    if cancel and result == 'tesSUCCESS':
                        report.add_success()
                        print(colored(
                            text=f'Status: Success',
                            color='green'
                        ))
                        continue
                    else:
                        report.add_failed()
                        print(colored(text=f'Failed: [Unknown Error] | [{result}]', color='red'))
                        continue

                except Exception as e:
                    report.add_failed()
                    print(colored(text=f'Error: {e}', color='red'))
                    if debug or __debug:
                        print(colored(text=f'Traceback: {traceback.format_exc()}', color='red'))
                    continue
        else:
            print(f'No offers found for {wallet.classic_address}')
            continue


def enter(__debug: bool = False):
    if debug or __debug:
        print(colored(text=f'DEBUG MODE\n\n', color='red', attrs=['blink', 'bold']))

    print(colored(text=CANCEL_ORDER_TEXT, color='cyan'))

    path_to_csv = input('Enter path to csv file: ').strip()

    clear()

    cancel_all_orders(path_to_csv, __debug)


if __name__ == '__main__':
    clear()
    try:
        enter()
    except KeyboardInterrupt:
        print(colored(text='\n\nExiting...', color='red'))
        sys.exit()
