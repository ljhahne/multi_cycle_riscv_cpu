import os

from cocotb.triggers import Timer

import cocotb
from tests.common import check_value
from tests.multi_cycle_cpu.models import mux3 as model


def read_vars():
    d0 = int(os.getenv("d0"))
    d1 = int(os.getenv("d1"))
    d2 = int(os.getenv("d2"))
    s = int(os.getenv("s"))
    print("d0 {}\nd1 {}\nd2 {}\ns {}".format(d0, d1, d2, s))

    return d0, d1, d2, s


async def assign_vars(dut, d0, d1, d2, s):
    dut.d0.value = d0
    dut.d1.value = d1
    dut.d2.value = d2
    dut.s.value = s

    await Timer(1, units="ns")


@cocotb.test()
async def test_mux3(dut):
    d0, d1, d2, s = read_vars()
    await assign_vars(dut, d0, d1, d2, s)

    check_value(dut.y, model(d0, d1, d2, s))
