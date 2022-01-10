import sys
import time

from uuid import uuid4

from xrpy import create_wallet, Wallet, JsonRpcClient


from src.airdrops.db_func import WalletDB
from src.airdrops.constants import XRP_TESTNET_URL


wallet_db = WalletDB(database_name='xrp', host="185.235.42.31", port=5432, user="amiwrpremium", password="0024444103")

XRP_TEST_CLIENT = JsonRpcClient(XRP_TESTNET_URL)


def insert_created_wallet(wallet: Wallet, label: str = None):
    wallet_db.insert_wallet(
        label if label else str(uuid4()),
        wallet.classic_address,
        wallet.get_xaddress(),
        wallet.private_key,
        wallet.public_key,
        wallet.seed,
        wallet.sequence,
    )


def mass_wallet_creator(count: int = 10, debug: bool = False, sleep_time: int = 0):
    if count == -1:
        count = sys.maxsize

    if debug:
        print(f'Created wallet 0/{count}', end='\r', flush=True)

    for i in range(count):
        try:
            wallet = create_wallet(XRP_TEST_CLIENT)
            insert_created_wallet(wallet)

            if debug:
                print(f'Created wallet {i+1}/{count}', end='\r', flush=True)

            time.sleep(sleep_time)

        except KeyboardInterrupt:
            return

        except Exception as e:
            print(e)
