import os
import random

import pytest

from tests.multi_cycle_cpu.defs import Op, States
from tests.setup_tests import Config, init_waveforms, run_simulation

toplevel = "next_state_logic"


config = Config(
    INCLUDES=["src/multi_cycle_cpu/include/"],
    HDLFILES=["src/multi_cycle_cpu/controller/controller_fsm.sv"],
    TOPLEVEL=toplevel,
    WORK_DIR="src/multi_cycle_cpu/controller",
    TEST_DIR="tests/multi_cycle_cpu/controller_unit/fsm/next_state_logic",
)

init_waveforms(config)


def set_signals(state, op):
    return {"state": str(state), "op": str(op)}


waveform_file = "state_register_op_{}_state_{}.vcd"


@pytest.mark.parametrize("op", Op().get_all())
@pytest.mark.parametrize("state", States().get_all())
def test_next_state_logic(state, op):
    run_simulation(
        config, "test_{}".format(toplevel), waveform_file, set_signals(state, op)
    )
