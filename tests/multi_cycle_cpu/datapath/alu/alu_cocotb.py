import os

from bitstring import Bits
from cocotb.triggers import Timer

import cocotb
from tests.common import check_value
from tests.multi_cycle_cpu.models import alu as model


def read_vars():
    a = int(os.getenv("a"))
    b = int(os.getenv("b"))
    alucontrol = int(os.getenv("alucontrol"))

    print(
        "a {}\nb {}\nalucontrol {}".format(
            Bits(uint=a, length=32).bin, Bits(uint=b, length=32).bin, alucontrol
        )
    )

    return a, b, alucontrol


async def assign_vars(dut, a, b, alucontrol):
    dut.a.value = a
    dut.b.value = b
    dut.alucontrol.value = alucontrol

    await Timer(1, units="ns")


@cocotb.test()
async def test_alu(dut):
    a, b, alucontrol = read_vars()
    await assign_vars(dut, a, b, alucontrol)

    result, zero = model(a, b, alucontrol)
    check_value(dut.result, result)
    check_value(dut.zero, zero)
