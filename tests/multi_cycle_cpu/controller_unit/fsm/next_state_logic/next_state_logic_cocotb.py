import os

import cocotb
from cocotb.triggers import Timer

from tests.common import check_value
from tests.multi_cycle_cpu.models import next_state as model


def read_vars():
    state = int(os.getenv("state"))
    op = int(os.getenv("op"))

    print("state {}\nop {}".format(state, op))

    return state, op


async def assign_vars(dut, state, op):
    dut.state.value = state
    dut.op.value = op

    await Timer(1, units="ns")


@cocotb.test()
async def test_next_state_logic(dut):
    state, op = read_vars()
    await assign_vars(dut, state, op)

    state_next = model(state, op)

    check_value(dut.state_next, state_next)
