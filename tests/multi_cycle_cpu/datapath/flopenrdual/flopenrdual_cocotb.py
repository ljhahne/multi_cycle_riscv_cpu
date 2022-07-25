import os

from bitstring import Bits
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, Timer

import cocotb
from tests.common import check_value
from tests.multi_cycle_cpu.models import flopenr as model


def read_vars():
    d00 = int(os.getenv("d00"))
    d10 = int(os.getenv("d10"))

    d01 = int(os.getenv("d01"))
    d11 = int(os.getenv("d11"))

    en = int(os.getenv("en"))
    reset = int(os.getenv("reset"))
    print(
        "d00 {}\nd10 {}\nd01 {}\nd11{}\nen {}\nreset {}".format(
            d00, d10, d01, d11, en, reset
        )
    )

    return d00, d10, d01, d11, en, reset


async def assign_vars(dut, d1, d2, en, reset):
    dut.d1.value = d1
    dut.d2.value = d2
    dut.en.value = en
    dut.reset.value = reset

    await Timer(1, units="ns")


@cocotb.test()
async def test_flopenrdual(dut, period_ns=1):
    d00, d10, d01, d11, en, reset = read_vars()
    await assign_vars(dut, d00, d10, en, reset)

    # init state
    print(dut.q1.value)
    print(dut.q2.value)

    check_value(dut.q1, model(d00, en, reset, init_state=True))
    check_value(dut.q2, model(d10, en, reset, init_state=True))

    cocotb.start_soon(Clock(dut.clk, period_ns, units="ns").start())

    await RisingEdge(dut.clk)
    await Timer(1, units="ns")

    print(dut.q1.value)
    print(dut.q2.value)

    check_value(dut.q1, model(d00, en, reset))
    check_value(dut.q2, model(d10, en, reset))

    # change value
    await assign_vars(dut, d01, d11, en, reset)

    await RisingEdge(dut.clk)
    await Timer(1, units="ns")

    check_value(dut.q1, model(d01, en, reset))
    check_value(dut.q2, model(d11, en, reset))
