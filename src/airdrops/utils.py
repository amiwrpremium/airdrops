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
        return self.success / self.total * 100

    def get_failure_rate(self):
        return self.failed / self.total * 100

    def get_report(self):
        return {
            'success': self.success,
            'failed': self.failed,
            'total': self.total,
            'success-rate': self.get_success_rate(),
            'failure-rate': self.get_failure_rate()
        }

    def __str__(self):
        return f'Success: {self.success}\n' \
               f'Failed: {self.failed}\n' \
               f'Total: {self.total}\n' \
               f'Success Rate: {self.get_success_rate()}\n' \
               f'Failure Rate: {self.get_failure_rate()}'

    def __repr__(self):
        return self.__str__()
