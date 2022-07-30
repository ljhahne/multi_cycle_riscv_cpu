import os

import cocotb
from cocotb.triggers import Timer

from tests.common import check_value


def read_vars():
    op = int(os.getenv("op"))
    ImmSrc = int(os.getenv("ImmSrc"))

    print("op {}\nImmSrc {}".format(op, ImmSrc))

    return op, ImmSrc


async def assign_vars(dut, op):
    dut.op.value = op

    await Timer(1, units="ns")


@cocotb.test()
async def test_instruction_decoder(dut):
    op, ImmSrc = read_vars()
    await assign_vars(dut, op)

    check_value(dut.ImmSrc, ImmSrc)
