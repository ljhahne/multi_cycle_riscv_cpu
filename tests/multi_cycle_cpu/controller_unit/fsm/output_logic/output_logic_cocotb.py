import os

from cocotb.triggers import Timer

import cocotb
from tests.common import check_value
from tests.multi_cycle_cpu.models import output_logic as model


def read_vars():
    state = int(os.getenv("state"))

    print("state {}".format(state))

    return state


async def assign_vars(dut, state):
    dut.state.value = state
    await Timer(1, units="ns")


@cocotb.test()
async def test_output_logic(dut):
    state = read_vars()
    await assign_vars(dut, state)

    (
        ALUSrcA,
        ALUSrcB,
        ResultSrc,
        aluOP,
        PCUpdate,
        AdrSrc,
        IRWrite,
        RegWrite,
        MemWrite,
        Branch,
    ) = model(state)

    check_value(dut.ALUSrcA, ALUSrcA)
    check_value(dut.ALUSrcB, ALUSrcB)
    check_value(dut.ResultSrc, ResultSrc)
    check_value(dut.aluOP, aluOP)
    check_value(dut.PCUpdate, PCUpdate)
    check_value(dut.AdrSrc, AdrSrc)
    check_value(dut.IRWrite, IRWrite)
    check_value(dut.RegWrite, RegWrite)
    check_value(dut.MemWrite, MemWrite)
    check_value(dut.Branch, Branch)
