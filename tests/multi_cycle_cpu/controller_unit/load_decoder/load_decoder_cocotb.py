import os

import cocotb
from cocotb.triggers import Timer

from tests.common import check_value
from tests.multi_cycle_cpu.models import load_decoder


def read_vars():
    funct3 = int(os.getenv("funct3"))

    print("funct3 {}".format(funct3))

    return funct3


async def assign_vars(dut, funct3):
    dut.funct3.value = funct3
    await Timer(1, units="ns")


@cocotb.test()
async def test_load_decoder(dut):
    funct3 = read_vars()
    await assign_vars(dut, funct3)

    check_value(dut.loadtype, load_decoder(funct3))
