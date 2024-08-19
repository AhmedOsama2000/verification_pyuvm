from random import randint
from base_tester import BaseTester


class RandomTester(BaseTester):
    def get_operands(self):
        return randint(0, 255), randint(0, 255)