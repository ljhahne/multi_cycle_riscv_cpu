import os

import cocotb
from bitstring import Bits
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, Timer

from tests.common import check_value
from tests.multi_cycle_cpu.models import flopr as model


def read_vars():
    d0 = int(os.getenv("d0"))
    d1 = int(os.getenv("d1"))
    reset = int(os.getenv("reset"))
    print("d0 {}\nd1\nreset {}".format(d0, d1, reset))

    return d0, d1, reset


async def assign_vars(dut, d, reset):
    dut.d.value = d
    dut.reset.value = reset

    await Timer(1, units="ns")


@cocotb.test()
async def test_flopr(dut, period_ns=1):
    d0, d1, reset = read_vars()
    await assign_vars(dut, d0, reset)

    # init state
    print(dut.q.value)

    check_value(dut.q, model(d0, reset, init_state=True))

    cocotb.start_soon(Clock(dut.clk, period_ns, units="ns").start())

    await RisingEdge(dut.clk)
    await Timer(1, units="ns")

    print(dut.q.value)

    check_value(dut.q, model(d0, reset))

    # change value
    await assign_vars(dut, d1, reset)

    await RisingEdge(dut.clk)
    await Timer(1, units="ns")

    check_value(dut.q, model(d1, reset))
