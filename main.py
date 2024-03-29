import sys
import os
import argparse

from colorama import init as colorama_init
from termcolor import colored

from src.airdrops import create_wallet_entrance
from src.airdrops import set_trustline_entrance
from src.airdrops import create_order_entrance
from src.airdrops import cancel_order_entrance
from src.airdrops import gid_validator_entrance
from src.airdrops import wallet_agg_entrance
from src.airdrops import wallet_balance_entrance
from src.airdrops import delete_wallet_entrance


parser = argparse.ArgumentParser(description='Set trustline for airdrop wallets')
parser.add_argument('--debug', '-D', dest='debug', help='Debug mode', action='store_true')
args = parser.parse_args()
main_debug = True if args.debug else False


colorama_init()


def clear():
    if os.name == 'posix':
        os.system('clear')
    elif os.name == 'nt':
        os.system('cls')
    else:
        pass


def decide(option: int):
    if option == 1:
        create_wallet_entrance.enter(main_debug)
    elif option == 2:
        set_trustline_entrance.enter(main_debug)
    elif option == 3:
        create_order_entrance.enter(main_debug)
    elif option == 4:
        cancel_order_entrance.enter(main_debug)
    elif option == 5:
        gid_validator_entrance.enter(main_debug)
    elif option == 6:
        wallet_agg_entrance.enter(main_debug)
    elif option == 7:
        wallet_balance_entrance.enter(main_debug)
    elif option == 8:
        delete_wallet_entrance.enter(main_debug)
    elif option == 0:
        sys.exit()


def enter():
    print(
        "[01] \t [Create Wallet]\n"
        "[02] \t [Set Trustline]\n"
        "[03] \t [Create Order]\n"
        "[04] \t [Cancel Order]\n"
        "[05] \t [Validate GID]\n"
        "[06] \t [Wallet Aggregator]\n"
        "[07] \t [Wallet Balance]\n"
        "[08] \t [Delete Wallet]\n"
        "[00] \t [Exit]\n"
    )
    option = int(input("Enter option: "))
    clear()
    decide(option)


if __name__ == "__main__":
    clear()
    try:
        enter()
    except KeyboardInterrupt:
        print(colored(text='\n\nExiting...', color='red'))
        sys.exit()
