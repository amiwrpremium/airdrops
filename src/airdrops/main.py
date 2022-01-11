import sys
import os
import time

from xrpy import create_wallet, Wallet, JsonRpcClient

from constants import XRP_TESTNET_URL
from csv_func import WalletCSV


XRP_TEST_CLIENT = JsonRpcClient(XRP_TESTNET_URL)

wallet_csv = WalletCSV('wallets.csv')


def clear():
    if os.name == 'posix':
        os.system('clear')
    elif os.name == 'nt':
        os.system('cls')
    else:
        pass


def mass_wallet_creator(count: int = 10, debug: bool = False, sleep_time: int = 0):
    print(f'{count=} | {debug=} | {sleep_time=}')

    if count == -1:
        count = sys.maxsize

    for i in range(count):
        try:
            if debug:
                print(f'Trying To Create Wallet: [{i+1}/{count}]')

            wallet = create_wallet(XRP_TEST_CLIENT)
            wallet_csv.insert_to_csv(wallet)

            if debug:
                print(f'Created wallet: {wallet.classic_address} | [{i+1}/{count}]')

            time.sleep(sleep_time)

        except KeyboardInterrupt:
            return

        except Exception as e:
            print(e)


mass_wallet_creator(count=-1, debug=True)
