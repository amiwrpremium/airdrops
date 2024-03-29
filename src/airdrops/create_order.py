import sys
import os
import time

import math

import argparse
import traceback

from typing import Union

from random import randint, uniform

from colorama import init as colorama_init
from termcolor import colored


from xrpy import Wallet, XRPY


if __name__ == '__main__':
    from constants import CREATE_ORDER_TEXT, DONATION_TEXT, DONATION_REQ, WALLETS
    from csv_func import WalletCSV
    from utils import Report
else:
    from .constants import CREATE_ORDER_TEXT, DONATION_TEXT, DONATION_REQ, WALLETS
    from .csv_func import WalletCSV
    from .utils import Report


parser = argparse.ArgumentParser(description='Set trustline for airdrop wallets')
parser.add_argument('--debug', '-D', dest='debug', help='Debug mode', action='store_true')
args = parser.parse_args()
debug = True if args.debug else False


colorama_init()
xrpy = XRPY()
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


def random_round_point(num: float) -> int:
    min_rand = abs(int(math.log10(abs(num)))) + 1
    max_rand = 6
    return randint(min_rand, max_rand)


def get_trustline_balance(address: str, currency: str) -> Union[float, int]:
    all_trust_lines = xrpy.get_account_trustlines(address)
    lines = all_trust_lines.result.get('lines')

    for line in lines:
        if line.get('currency') == currency:
            return float(line.get('balance'))
        else:
            continue

    return 0


def mass_create_order_buy(
        path_to_csv: str, min_taker_gets_xrp: Union[int, float], max_taker_gets_xrp: Union[int, float],
        taker_pays_currency: str, taker_pays_value: str, taker_pays_issuer: str, side: str,
        min_sleep_time: int = 0, max_sleep_time: int = 0, __debug: bool = False
):
    print(
        colored(
            text=f'{path_to_csv=}\n'
                 f'{min_taker_gets_xrp=}\n'
                 f'{max_taker_gets_xrp=}\n'
                 f'{taker_pays_currency=}\n'
                 f'{taker_pays_value=}\n'
                 f'{taker_pays_issuer=}\n'
                 f'{side=}\n'
                 f'{min_sleep_time=}\n'
                 f'{max_sleep_time=}\n\n',
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
            if debug or __debug:
                print(colored(text=f'Traceback: {traceback.format_exc()}', color='red'))
            continue

        taker_gets_xrp = round(uniform(min_taker_gets_xrp, max_taker_gets_xrp), random_round_point(min_taker_gets_xrp))
        print(colored(text=f'{taker_gets_xrp=}', color='cyan'))

        try:
            _create_offer = xrpy.create_buy_offer(
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

                sleep_time = randint(min_sleep_time, max_sleep_time)
                print(colored(text=f"Sleeping for {sleep_time} seconds", color='blue'))
                time.sleep(sleep_time)

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


def mass_create_order_sell(
        path_to_csv: str, min_taker_pays_xrp: Union[int, float], max_taker_pays_xrp: Union[int, float],
        taker_gets_currency: str, taker_gets_value: Union[int, float], percentage: Union[int, float],
        taker_gets_issuer: str, side: str, min_sleep_time: int = 0, max_sleep_time: int = 0, __debug: bool = False
):

    print(
        colored(
            text=f'{path_to_csv=}\n'
                 f'{min_taker_pays_xrp=}\n'
                 f'{max_taker_pays_xrp=}\n'
                 f'{taker_gets_currency=}\n'
                 f'{taker_gets_value=}\n'
                 f'{percentage=}\n'
                 f'{taker_gets_issuer=}\n'
                 f'{side=}\n'
                 f'{min_sleep_time=}\n'
                 f'{max_sleep_time=}\n\n',
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
            if debug or __debug:
                print(colored(text=f'Traceback: {traceback.format_exc()}', color='red'))
            continue

        try:
            balance = get_trustline_balance(wallet.classic_address, taker_gets_currency)
            print(colored(text=f'{balance=}', color='cyan'))
        except Exception as e:
            report.add_failed()
            print(colored(text=f'Error: {e}', color='red'))
            if debug or __debug:
                print(colored(text=f'Traceback: {traceback.format_exc()}', color='red'))
            continue

        taker_pays_xrp = round(uniform(min_taker_pays_xrp, max_taker_pays_xrp), random_round_point(min_taker_pays_xrp))
        print(colored(text=f'{taker_pays_xrp=}', color='cyan'))

        if taker_gets_value == -1:
            __taker_gets_value = float(balance * (percentage / 100))
        else:
            __taker_gets_value = taker_gets_value
        print(colored(text=f'{__taker_gets_value=}', color='cyan'))

        try:
            if balance and balance > 0:
                _create_offer = xrpy.create_sell_offer(
                    wallet,
                    taker_pays_xrp,
                    taker_gets_currency,
                    str(__taker_gets_value),
                    taker_gets_issuer,
                    'market'
                )

                if _create_offer and (_create_offer.result.get("meta").get("TransactionResult")) == 'tesSUCCESS':
                    report.add_success()

                    print(colored(
                        text=f'Status: Success',
                        color='green'
                    ))

                    sleep_time = randint(min_sleep_time, max_sleep_time)
                    print(colored(text=f"Sleeping for {sleep_time} seconds. zZz...", color='blue'))
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
            if debug or __debug:
                print(colored(text=f'Traceback: {traceback.format_exc()}', color='red'))
            continue

    try_again = input(colored(text='\n\nTry again? (y/n) ', color='cyan'))
    if try_again.lower() == 'y':
        clear()
        mass_create_order_sell(
            path_to_csv,
            min_taker_pays_xrp,
            max_taker_pays_xrp,
            taker_gets_currency,
            taker_gets_value,
            percentage,
            taker_gets_issuer,
            side,
            min_sleep_time,
            max_sleep_time,
            __debug
        )


def enter(__debug: bool = False):
    if debug or __debug:
        print(colored(text=f'DEBUG MODE\n\n', color='red', attrs=['blink', 'bold']))

    print(colored(text=CREATE_ORDER_TEXT, color='cyan'))

    path_to_csv = input('Enter path to csv file: ').strip()

    side = input('Enter side (buy/sell): ')

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

    if side.lower() == 'buy':
        try:
            min_taker_gets_xrp = float(input('Enter min taker gets XRP: '))
            max_taker_gets_xrp = float(input('Enter max taker gets XRP: '))
        except ValueError:
            print(colored(text='\n\ntaker gets XRP must be an float', color='red'))
            sys.exit()

        taker_pays_currency = input('Enter taker pays currency: ')
        taker_pays_value = input('Enter taker pays value: ')
        taker_pays_issuer = input('Enter taker pays issuer: ')

        clear()

        try:
            mass_create_order_buy(
                path_to_csv,
                min_taker_gets_xrp,
                max_taker_gets_xrp,
                taker_pays_currency,
                taker_pays_value,
                taker_pays_issuer,
                side,
                min_sleep_time,
                max_sleep_time,
                debug or __debug
            )
            print_end_report()

        except KeyboardInterrupt:
            print_end_report()

    elif side.lower() == 'sell':
        try:
            min_taker_pays_xrp = float(input('Enter min taker pays XRP: '))
            max_taker_pays_xrp = float(input('Enter max taker pays XRP: '))
        except ValueError:
            print(colored(text='\n\nError: taker gets XRP must be an float', color='red'))
            sys.exit()

        taker_gets_currency = input('Enter taker gets currency: ')
        taker_gets_issuer = input('Enter taker gets issuer: ')
        taker_gets_decider = input('Enter taker gets decider (yolo/fixed): ')

        if taker_gets_decider.lower().strip() == 'yolo':
            try:
                percentage = float(input('Enter percentage (0-100): '))
                if percentage < 0 or percentage > 100:
                    print(colored(text='\n\nPercentage must be between 0 and 100', color='red'))
                    sys.exit()
            except ValueError:
                print(colored(text='\n\npercentage must be a float', color='red'))
                sys.exit()

            taker_gets_value = -1

        elif taker_gets_decider.lower().strip() == 'fixed':
            percentage = 100
            try:
                taker_gets_value = float(input('Enter taker gets value: '))
            except ValueError:
                print(colored(text='\n\ntaker pays value must be an float', color='red'))
                sys.exit()

        else:
            print(colored(text='\n\nInvalid taker pays decider', color='red'))
            sys.exit()

        clear()

        try:
            mass_create_order_sell(
                path_to_csv,
                min_taker_pays_xrp,
                max_taker_pays_xrp,
                taker_gets_currency,
                taker_gets_value,
                percentage,
                taker_gets_issuer,
                side,
                min_sleep_time,
                max_sleep_time,
                debug or __debug
            )
            print_end_report()

        except KeyboardInterrupt:
            print_end_report()

    else:
        print(colored(text='\n\nInvalid side', color='red'))
        sys.exit()


if __name__ == '__main__':
    clear()
    try:
        enter()
    except KeyboardInterrupt:
        print(colored(text='\n\nExiting...', color='red'))
        sys.exit()
