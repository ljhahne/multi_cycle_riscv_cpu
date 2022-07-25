import os

from cocotb.triggers import Timer

import cocotb
from tests.common import check_value
from tests.multi_cycle_cpu.models import alu_control as model


def read_vars():
    opb5 = int(os.getenv("opb5"))
    funct3 = int(os.getenv("funct3"))
    funct7b5 = int(os.getenv("funct7b5"))
    ALUOp = int(os.getenv("ALUOp"))

    print(
        "ALUOp {}\nfunct3 {}\nopb5 {}\nfunct7b5 {}".format(
            ALUOp, funct3, opb5, funct7b5
        )
    )

    return opb5, funct3, funct7b5, ALUOp


async def assign_vars(dut, opb5, funct3, funct7b5, ALUOp):
    dut.opb5.value = opb5
    dut.funct3.value = funct3
    dut.funct7b5.value = funct7b5
    dut.ALUOp.value = ALUOp

    await Timer(1, units="ns")


@cocotb.test()
async def test_aludecoder(dut):
    opb5, funct3, funct7b5, ALUOp = read_vars()
    await assign_vars(dut, opb5, funct3, funct7b5, ALUOp)

    alu_control = model(opb5, funct3, funct7b5, ALUOp)

    check_value(dut.ALUControl, alu_control)
