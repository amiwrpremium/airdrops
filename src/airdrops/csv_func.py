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
        self.date_index = 0
        self.label_index = 1
        self.classic_address_index = 2
        self.x_address_index = 3
        self.private_key_index = 4
        self.public_key_index = 5
        self.seed_index = 6
        self.sequence_index = 7

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

    def get_all_csv_info(self):
        with open(self.csv_file, 'r', encoding='UTF8') as csvfile:
            reader = csv.reader(csvfile)
            return list(reader)
