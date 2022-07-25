import os

from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, Timer

import cocotb
from tests.common import check_value
from tests.multi_cycle_cpu.models import alu_control as model_alu_control
from tests.multi_cycle_cpu.models import fsm as model_fsm
from tests.multi_cycle_cpu.models import opb5, output_logic
from tests.multi_cycle_cpu.models import pc_write as model_pc_write


def read_vars():
    op = int(os.getenv("op"))
    reset = int(os.getenv("reset"))

    funct3 = int(os.getenv("funct3"))

    funct7b5 = int(os.getenv("funct7b5"))

    Zero = int(os.getenv("Zero"))
    ImmSrc = int(os.getenv("ImmSrc"))

    print(
        "op {}\nreset {}\nfunct3 {}\nfunct7b5 {}\nZero {}\nImmSrc {}".format(
            op, reset, funct3, funct7b5, Zero, ImmSrc
        )
    )

    return op, reset, funct3, funct7b5, Zero, ImmSrc


async def assign_vars(dut, op, reset, funct3, funct7b5, Zero):
    dut.reset.value = reset
    dut.op.value = op
    dut.funct3.value = funct3
    dut.funct7b5.value = funct7b5
    dut.Zero.value = Zero

    await Timer(1, units="ns")


@cocotb.test()
async def test_controller(dut, period_ns=1):

    op, reset, funct3, funct7b5, Zero, ImmSrc = read_vars()
    await assign_vars(dut, op, reset, funct3, funct7b5, Zero)

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

        alu_control = model_alu_control(opb5(op), funct3, funct7b5, aluOP)
        pc_write = model_pc_write(Zero, Branch, PCUpdate)

        check_value(dut.ImmSrc, ImmSrc)
        check_value(dut.ALUSrcA, ALUSrcA)
        check_value(dut.ALUSrcB, ALUSrcB)
        check_value(dut.ResultSrc, ResultSrc)
        check_value(dut.AdrSrc, AdrSrc)
        check_value(dut.ALUControl, alu_control)
        check_value(dut.IRWrite, IRWrite)
        check_value(dut.PCWrite, pc_write)
        check_value(dut.RegWrite, RegWrite)
        check_value(dut.MemWrite, MemWrite)
