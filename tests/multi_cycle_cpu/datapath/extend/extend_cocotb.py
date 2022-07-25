import os

from bitstring import Bits
from cocotb.triggers import Timer

import cocotb
from tests.common import check_value
from tests.multi_cycle_cpu.models import extend as model


def read_vars():
    ImmSrc = int(os.getenv("ImmSrc"))
    instruction = int(os.getenv("instruction"))

    print("ImmSrc {}\ninstruction {}".format(ImmSrc, instruction))

    return ImmSrc, instruction


async def assign_vars(dut, ImmSrc, instruction):
    dut.immsrc.value = ImmSrc
    dut.instr.value = Bits(uint=instruction, length=32)[:-7].uint

    await Timer(1, units="ns")


@cocotb.test()
async def test_extend(dut):
    ImmSrc, instruction = read_vars()
    await assign_vars(dut, ImmSrc, instruction)

    immext = model(ImmSrc, instruction)
    print("instruction {}".format(instruction))
    check_value(dut.immext, immext)
