from cocotb.triggers import ClockCycles
from alu_bfm import AluBfm

opcodes = [0, 1, 2, 3, 4, 5]

class BaseTester():
    async def execute(self):
        self.bfm = AluBfm()
        for op in opcodes:
            aa, bb = self.get_operands()
            await self.bfm.send_op(aa, bb, op)
            # send two dummy operations
            # to allow last real operation to complete
            await self.bfm.send_op(0 ,0 ,1)
            await self.bfm.send_op(0 ,0 ,1)
        await ClockCycles(self.bfm.dut.CLK, 2)
        