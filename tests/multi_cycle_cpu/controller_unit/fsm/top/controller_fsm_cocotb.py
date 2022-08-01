import os

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, Timer

from tests.common import check_value
from tests.multi_cycle_cpu.models import fsm as model_fsm
from tests.multi_cycle_cpu.models import output_logic


def read_vars():
    op = int(os.getenv("op"))
    reset = int(os.getenv("reset"))

    print("op {}\nreset {}".format(op, reset))

    return op, reset


async def assign_vars(dut, op, reset):
    dut.op.value = op
    dut.reset.value = reset
    await Timer(1, units="ns")


@cocotb.test()
async def test_controller_fsm(dut, period_ns=1):

    op, reset = read_vars()

    await assign_vars(dut, op, reset)

    cocotb.start_soon(Clock(dut.clk, period_ns, units="ns").start())

    for fsm_state in model_fsm(op, reset):
        await RisingEdge(dut.clk)
        await Timer(1, units="ns")

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
        ) = output_logic(fsm_state)

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
