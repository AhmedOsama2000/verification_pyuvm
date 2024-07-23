import cocotb
from cocotb.clock import Clock
from cocotb.queue import Queue, QueueEmpty
from cocotb.triggers import FallingEdge
import pyuvm

class AluBfm(metaclass=pyuvm.Singleton):
    def __init__(self):
        self.dut = cocotb.top  # cocotb.dut contains the handle of the dut, same handle that cocotb.test() got
        self.cmd_driver_queue = Queue(maxsize=1)  # handles only ooen operation
        self.cmd_mon_queue = Queue(maxsize=0)  # set the size to very large
        self.result_mon_queue = Queue(maxsize=0)


    async def gen_clk(self):
        cocotb.start_soon(Clock(self.dut.CLK, 2, units="ns").start())

    # adding a reset() coroutine
    async def reset(self):
        await FallingEdge(self.dut.CLK)
        self.dut.rst_n.value = 0
        self.dut.en.value = 0
        self.dut.A.value = 0
        self.dut.B.value = 0
        self.dut.OP.value = 0
        await FallingEdge(self.dut.CLK)
        self.dut.rst_n.value = 1
        await FallingEdge(self.dut.CLK)

    # monitor the result
    async def result_mon(self):
        while True:
            await FallingEdge(self.dut.CLK)
            if self.dut.done.value == 1:
                result = int(self.dut.result.value)
                self.result_mon_queue.put_nowait(result)

    
    # monitor the command (e.g. for coverage purpose)
    async def cmd_mon(self):
        while True:
            await FallingEdge(self.dut.CLK)
            # check if the alu is enabled to capture the inputs
            cmd_tuple = (
                int(self.dut.A.value),
                int(self.dut.B.value),
                int(self.dut.OP.value)
            )
            self.cmd_mon_queue.put_nowait(cmd_tuple)


    # drive the alu with stimulus
    async def cmd_driver(self):
        while True:
            await FallingEdge(self.dut.CLK)
            # get the data fromt driver queue which's taken from send_op coroutine
            try:
                (aa, bb, op) = self.cmd_driver_queue.get_nowait()
                self.dut.A.value = aa
                self.dut.B.value = bb
                self.dut.OP.value = op
                self.dut.en.value = 1

            except QueueEmpty:
                continue

            

    # read/send data to the dut
    async def get_cmd(self):
        cmd = await self.cmd_mon_queue.get()
        return cmd
    

    async def get_result(self):
        result = await self.result_mon_queue.get()
        return result
    

    async def send_op(self, aa, bb, op):
        command_tuple = (aa, bb, op)
        print("send a command")
        await self.cmd_driver_queue.put(command_tuple)


    # start the coroutines of the BFM, note that start_soon is a function so this function defined as def not async def
    def start_task(self):
        cocotb.start_soon(self.cmd_driver())
        cocotb.start_soon(self.cmd_mon())
        cocotb.start_soon(self.result_mon())