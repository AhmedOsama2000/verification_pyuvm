from random import randint
from base_tester import BaseTester

# provide max values for A, B buses
class MaxTester(BaseTester):
    def get_operands(self):
        return 0xFF, 0xFF