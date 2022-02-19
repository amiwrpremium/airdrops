from typing import Dict, Union


from colorama import init as colorama_init
from termcolor import colored

from prettytable import PrettyTable


colorama_init()


class Report:
    def __init__(self):
        self.success = 0
        self.failed = 0
        self.total = 0

    def add_success(self):
        self.success += 1
        self.total += 1

    def add_failed(self):
        self.failed += 1
        self.total += 1

    def get_success(self):
        return self.success

    def get_failed(self):
        return self.failed

    def get_total(self):
        return self.total

    def get_success_rate(self):
        return str(round((self.success / self.total * 100), 2)) + '%'

    def get_failure_rate(self):
        return str(round((self.failed / self.total * 100), 2)) + '%'

    def get_report(self):
        return {
            'success': self.success,
            'failed': self.failed,
            'total': self.total,
            'success-rate': self.get_success_rate(),
            'failure-rate': self.get_failure_rate()
        }

    def get_pretty_report(self):
        table = PrettyTable()
        table.title = colored(f"Result", "magenta")
        table.field_names = ["Data", "Value"]
        table.add_row(["Success", colored(text=self.success, color='green')])
        table.add_row(["Failed", colored(text=self.failed, color='red')])
        table.add_row(["Total", colored(text=self.total, color='yellow')])
        table.add_row(["Success Rate", colored(text=self.get_success_rate(), color='blue')])
        table.add_row(["Failure Rate", colored(text=self.get_failure_rate(), color='blue')])

        return table

    def __str__(self):
        return f'Success: {self.success}\n' \
               f'Failed: {self.failed}\n' \
               f'Total: {self.total}\n' \
               f'Success Rate: {self.get_success_rate()}\n' \
               f'Failure Rate: {self.get_failure_rate()}'

    def __repr__(self):
        return self.__str__()


class Balance:
    def __init__(self):
        self.free = 0
        self.reserved = 0
        self.total = 0

    def add_free(self, amount: Union[float, int]):
        self.free += amount

    def add_reserved(self, amount: Union[float, int]):
        self.reserved += amount

    def add_total(self, amount: Union[float, int]):
        self.total += amount

    def get_free(self) -> Union[float, int]:
        return round(self.free, 2)

    def get_reserved(self) -> Union[float, int]:
        return round(self.reserved, 2)

    def get_total(self) -> Union[float, int]:
        return round(self.total, 2)

    def add_from_dict(self, data: Dict):
        self.add_free(data['free'])
        self.add_reserved(data['reserved'])
        self.add_total(data['total'])

    def get_report(self):
        return {
            'free': self.get_free(),
            'reserved': self.get_reserved(),
            'total': self.get_total(),
        }

    def get_pretty_report(self):
        table = PrettyTable()
        table.title = colored(f"Result", "magenta")
        table.field_names = ["Data", "Value"]
        table.add_row(["Free", colored(text=self.get_free(), color='green')])
        table.add_row(["Reserved", colored(text=self.get_reserved(), color='red')])
        table.add_row(["Total", colored(text=self.get_total(), color='yellow')])

        return table

    def __str__(self):
        return f'Free: {self.get_free()}\n' \
               f'Reserved: {self.get_reserved()}\n' \
               f'Total: {self.get_total()}'

    def __repr__(self):
        return self.__str__()
