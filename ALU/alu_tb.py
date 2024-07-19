# Importing the modules
import cocotb
from cocotb.clock import Clock
from cocotb.triggers import FallingEdge, ClockCycles
import random  # for randomize testing

correct_cases = 0
incorrect_cases = 0

def get_int(signal):
    try:
        ii = int(signal.value)
    except ValueError:
        ii = 0  # if the signal value is x or z

    return ii


def dut_init(dut):
    dut.rst_n.value = 0
    dut.en .value = 0
    dut.A.value = 0
    dut.B.value = 0
    dut.OP.value = 0



def scoreboard(A, B, op, dut_result):
    global correct_cases
    global incorrect_cases
    opcode = {
        0: A + B,
        1: A * B,
        2: A & B,
        3: A | B,
        4: A ^ B,
        5: ~A
    }

    expected_result = opcode[op]
    # convert the signed number to unsigned number
    if expected_result < 0:
        expected_result += 2**8

   
    print (f"A: {A} B: {B} opcode: {op} dut_result: {dut_result} expected_result: {expected_result}")
    if dut_result == expected_result:
        correct_cases += 1
        print("Test Pass")
    else:
        incorrect_cases += 1
        print("Test Fails")


@cocotb.test()
async def alu_test(dut):
    
    cocotb.start_soon(Clock(dut.CLK, 2, units="ns").start())
    # initialize the inputs of the dut
    await FallingEdge(dut.CLK)
    dut_init(dut)
    
    # start the stimulus 
    await FallingEdge(dut.CLK)
    dut.rst_n.value = 1
    dut.en.value = 1

    for ii in range(0, 50):
        await FallingEdge(dut.CLK)
        dut.A.value = random.randint(0, 255)
        dut.B.value = random.randint(0, 255)
        dut.OP.value = random.randint(0, 5)

        # get the result at the next clock cycle
        await FallingEdge(dut.CLK)
        a_i = get_int(dut.A)
        b_i = get_int(dut.B)
        op_i = get_int(dut.OP)
        result = get_int(dut.result)
        scoreboard(a_i, b_i, op_i, result)
        
    await FallingEdge(dut.CLK)
    dut.en.value = 0

    await ClockCycles(dut.CLK, 5)

    print(f"Correct Cases: {correct_cases}")
    print(f"Inorrect Cases: {incorrect_cases}")
    

