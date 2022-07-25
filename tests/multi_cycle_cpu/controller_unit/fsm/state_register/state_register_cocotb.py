import os

from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, Timer

import cocotb
from tests.common import check_value
from tests.multi_cycle_cpu.models import state_register as model


def read_vars():
    state_next = int(os.getenv("state_next"))
    reset = int(os.getenv("reset"))

    print("state_next {}\nreset {}".format(state_next, reset))

    return state_next, reset


async def assign_vars(dut, state_next, reset):
    dut.state_next.value = state_next
    dut.reset.value = reset

    await Timer(1, units="ns")


@cocotb.test()
async def test_state_register(dut, period_ns=1):
    state_next, reset = read_vars()
    await assign_vars(dut, state_next, reset)

    cocotb.start_soon(Clock(dut.clk, period_ns, units="ns").start())
    await RisingEdge(dut.clk)
    await Timer(1, units="ns")

    state = model(state_next, reset)

    check_value(dut.state, state)
