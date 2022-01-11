import csv
from xrpy import Wallet
from uuid import uuid4
from datetime import datetime


class WalletCSV:
    def __init__(self, csv_file: str):
        self.csv_file = csv_file.lower()
        self.headers = [
            'date', 'label', 'classic_address', 'x_address', 'private_key', 'public_key', 'seed', 'sequence'
        ]

        self.write_headers()

    def write_headers(self):
        with open(self.csv_file, 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(self.headers)

    def insert_to_csv(self, wallet: Wallet, label: str = None):
        with open(self.csv_file, 'a', encoding='UTF8', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(
                [
                    str(datetime.utcnow()),
                    label if label else str(uuid4()).split('-')[0],
                    wallet.classic_address,
                    wallet.get_xaddress(),
                    wallet.private_key,
                    wallet.public_key,
                    wallet.seed,
                    wallet.sequence
                ]
            )
