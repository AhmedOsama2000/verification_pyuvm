# Importing the modules
import cocotb

# importing BFM class
from alu_bfm import AluBfm
from random_tester import RandomTester
from max_tester import MaxTester
from scoreboard import Scoreboard

##starts the tasks
async def execute_test(tester_class):
    bfm = AluBfm()
    await bfm.gen_clk()
    await bfm.reset()
    scoreboard = Scoreboard()
    bfm.start_task()
    scoreboard.start_tasks()
    tester = tester_class()
    await tester.execute()
    passed = scoreboard.check_results()
    return passed

@cocotb.test()
async def random_test(_):
    """random operands"""
    passed = await execute_test(RandomTester)
    assert passed
    
@cocotb.test()    
async def max_test(_):
    """Maximums operands"""
    passed = await execute_test(MaxTester)
    assert passed
    


    

