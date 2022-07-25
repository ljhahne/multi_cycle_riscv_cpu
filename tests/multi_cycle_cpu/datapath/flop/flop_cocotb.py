import os

from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, Timer

import cocotb
from tests.common import check_value


def read_vars():
    d0 = int(os.getenv("d0"))
    d1 = int(os.getenv("d1"))
    print("d0 {}\nd1 {}".format(d0, d1))

    return d0, d1


async def assign_vars(dut, d):
    dut.d.value = d

    await Timer(1, units="ns")


@cocotb.test()
async def test_flop(dut, period_ns=1):
    d0, d1 = read_vars()
    await assign_vars(dut, d0)

    # init state
    print(dut.q.value)

    assert dut.q.value.is_resolvable == False

    cocotb.start_soon(Clock(dut.clk, period_ns, units="ns").start())

    await RisingEdge(dut.clk)
    await Timer(1, units="ns")

    check_value(dut.q, d0)

    # change value
    await assign_vars(dut, d1)

    await RisingEdge(dut.clk)
    await Timer(1, units="ns")

    check_value(dut.q, d1)
    # immext = model(ImmSrc, instruction)
    # print("instruction {}".format(instruction))
    # check_value(dut.immext, immext)
