import os

import cocotb
from bitstring import Bits
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, Timer

from tests.common import check_value
from tests.multi_cycle_cpu.models import flop as model


def read_vars():
    d00 = int(os.getenv("d00"))
    d10 = int(os.getenv("d10"))

    d01 = int(os.getenv("d01"))
    d11 = int(os.getenv("d11"))

    print("d00 {}\nd10 {}\nd01 {}\nd11{}".format(d00, d10, d01, d11))

    return d00, d10, d01, d11


async def assign_vars(dut, d1, d2):
    dut.d1.value = d1
    dut.d2.value = d2

    await Timer(1, units="ns")


@cocotb.test()
async def test_flopdual(dut, period_ns=1):
    d00, d10, d01, d11 = read_vars()
    await assign_vars(dut, d00, d10)

    # init state
    print(dut.q1.value)
    print(dut.q2.value)

    check_value(dut.q1, model(d00, init_state=True))
    check_value(dut.q2, model(d10, init_state=True))

    cocotb.start_soon(Clock(dut.clk, period_ns, units="ns").start())

    await RisingEdge(dut.clk)
    await Timer(1, units="ns")

    print(dut.q1.value)
    print(dut.q2.value)

    check_value(dut.q1, model(d00))
    check_value(dut.q2, model(d10))

    # change value
    await assign_vars(dut, d01, d11)

    await RisingEdge(dut.clk)
    await Timer(1, units="ns")

    check_value(dut.q1, model(d01))
    check_value(dut.q2, model(d11))
