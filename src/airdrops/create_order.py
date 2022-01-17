import sys
import os
import time

from typing import Union

from colorama import init as colorama_init
from termcolor import colored


from xrpy import Wallet, JsonRpcClient, create_offer_buy, create_offer_sell, get_account_trustlines

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


def get_trustline_balance(client: JsonRpcClient, address: str, currency: str) -> Union[float, int]:
    all_trust_lines = get_account_trustlines(client, address)
    lines = all_trust_lines.result.get('lines')

    for line in lines:
        if line.get('currency') == currency:
            return float(line.get('balance'))
        else:
            continue

    return 0


def mass_create_order_buy(path_to_csv: str, taker_gets_xrp: Union[int, float], taker_pays_currency: str,
                          taker_pays_value: str, taker_pays_issuer: str, side: str,
                          sleep_time: int = 0):

    print(
        colored(
            text=f'{path_to_csv=}\n'
                 f'{taker_gets_xrp=}\n'
                 f'{taker_pays_currency=}\n'
                 f'{taker_pays_value=}\n'
                 f'{taker_pays_issuer=}\n'
                 f'{side=}\n'
                 f'{sleep_time=}\n\n',
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
            _create_offer = create_offer_buy(
                XRP_MAIN_CLIENT,
                wallet,
                taker_gets_xrp,
                taker_pays_currency,
                taker_pays_value,
                taker_pays_issuer,
                'market'
            )

            result = _create_offer.result.get("meta").get("TransactionResult")

            if _create_offer and result == 'tesSUCCESS':
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
            continue


def mass_create_order_sell(path_to_csv: str, taker_pays_xrp: Union[int, float], taker_gets_currency: str,
                           taker_gets_value: str, taker_gets_issuer: str, side: str,
                           sleep_time: int = 0):

    print(
        colored(
            text=f'{path_to_csv=}\n'
                 f'{taker_pays_xrp=}\n'
                 f'{taker_gets_currency=}\n'
                 f'{taker_gets_value=}\n'
                 f'{taker_gets_issuer=}\n'
                 f'{side=}\n'
                 f'{sleep_time=}\n\n',
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
            balance = get_trustline_balance(XRP_MAIN_CLIENT, wallet.classic_address, taker_gets_currency)
        except Exception as e:
            print(colored(text=f'Error: {e}', color='red'))
            report.add_failed()
            continue

        try:
            if balance and balance > 0:
                _create_offer = create_offer_sell(
                    XRP_MAIN_CLIENT,
                    wallet,
                    taker_pays_xrp,
                    taker_gets_currency,
                    taker_gets_value,
                    taker_gets_issuer,
                    'market'
                )

                if _create_offer and (_create_offer.result.get("meta").get("TransactionResult")) == 'tesSUCCESS':
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
            else:
                report.add_failed()
                print(colored(text=f'Failed: [Insufficient Balance]', color='red'))
                continue

        except Exception as e:
            report.add_failed()
            print(colored(text=f'Error: {e}', color='red'))
            continue


def enter():
    path_to_csv = input('Enter path to csv file: ')

    side = input('Enter side (buy/sell): ')

    try:
        sleep_time = int(input('Enter sleep time: '))
    except ValueError:
        sys.exit('Sleep time must be an integer')

    if sleep_time < 0:
        sys.exit('Invalid sleep time')

    if side.lower() == 'buy':
        try:
            taker_gets_xrp = float(input('Enter taker gets XRP: '))
        except ValueError:
            sys.exit('Error: taker gets XRP must be an integer')

        taker_pays_currency = input('Enter taker pays currency: ')
        taker_pays_value = input('Enter taker pays value: ')
        taker_pays_issuer = input('Enter taker pays issuer: ')

        clear()

        mass_create_order_buy(
            path_to_csv,
            taker_gets_xrp,
            taker_pays_currency,
            taker_pays_value,
            taker_pays_issuer,
            side,
            sleep_time,
        )

    elif side.lower() == 'sell':
        try:
            taker_pays_xrp = float(input('Enter taker pays XRP: '))
        except ValueError:
            sys.exit('Error: taker gets XRP must be an integer')

        taker_gets_currency = input('Enter taker gets currency: ')
        taker_gets_value = input('Enter taker gets value: ')
        taker_gets_issuer = input('Enter taker gets issuer: ')

        clear()

        mass_create_order_sell(
            path_to_csv,
            taker_pays_xrp,
            taker_gets_currency,
            taker_gets_value,
            taker_gets_issuer,
            side,
            sleep_time,
        )

        print('\n\n')
        print(colored(text=report.get_report(), color='cyan'))

    else:
        sys.exit('Invalid side')


if __name__ == '__main__':
    enter()
