import cocotb
from alu_bfm import AluBfm

correct_cases = 0
incorrect_cases = 0

class Scoreboard():
    def __init__(self):
        self.bfm = AluBfm()
        self.cmds = []
        self.results = []
        # self.cvg = set()

    async def get_cmd(self):
        while True:
            cmd = await self.bfm.get_cmd()
            self.cmds.append(cmd)

    async def get_result(self):
        while True:
            result = await self.bfm.get_result()
            self.results.append(result)
    
    def expected_result(self, aa, bb, op):
        opcode = {
            0: aa + bb,
            1: aa * bb,
            2: aa & bb,
            3: aa | bb,
            4: aa ^ bb,
            5: ~aa
        }

        return opcode[op]

    def check_results(self):
        passed = True
        global correct_cases
        global incorrect_cases

        for cmd in self.cmds:
            aa_dut, bb_dut, op_dut = cmd

            try:
                actual = self.results.pop(0)
            except IndexError:
                print("list is empty for now!")

            expected_result = self.expected_result(aa_dut, bb_dut, op_dut)
            print(expected_result)
            # convert the signed number to unsigned number
            if expected_result < 0:
                expected_result += 2**8

            print (f"A: {aa_dut} B: {bb_dut} opcode: {op_dut} dut_result: {actual} expected_result: {expected_result}")
            if actual == expected_result:
                correct_cases += 1
                passed = True
            else:
                incorrect_cases += 1
                print("Test Fails")
                passed =  False

        return passed

    def start_tasks(self):
        cocotb.start_soon(self.get_cmd())
        cocotb.start_soon(self.get_result())