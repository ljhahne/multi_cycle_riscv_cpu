import os

from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, Timer

import cocotb
from tests.common import check_value
from tests.multi_cycle_cpu.models import RegisterFile as Model


def read_vars():

    we = int(os.getenv("we"))
    a1 = int(os.getenv("a1"))
    a2 = int(os.getenv("a2"))
    a3 = int(os.getenv("a3"))
    wd3 = int(os.getenv("wd3"))

    print("we {}\na1 {}\na2 {}\na3 {}\nwd3 {}".format(we, a1, a2, a3, wd3))

    return we, a1, a2, a3, wd3


async def assign_vars(dut, we, a1, a2, a3, wd3):

    dut.we3.value = we
    dut.a1.value = a1
    dut.a2.value = a2
    dut.a3.value = a3
    dut.wd3.value = wd3

    await Timer(1, units="ns")


@cocotb.test()
async def test_registerfile(dut, period_ns=1):
    model = Model()

    we, a1, a2, a3, wd3 = read_vars()

    await assign_vars(dut, we, a1, a2, a3, wd3)
    model.write(a3, wd3, we)

    cocotb.start_soon(Clock(dut.clk, period_ns, units="ns").start())

    await RisingEdge(dut.clk)
    await Timer(1, units="ns")

    rd1, rd2 = model.read_addresses(a1, a2)
    print("dut.rd1 {}".format(dut.rd1.value))
    print("dut.rd2 {}".format(dut.rd2.value))

    check_value(dut.rd1, rd1)
    check_value(dut.rd2, rd2)
