import os
import random

import pytest

from tests.multi_cycle_cpu.defs import States
from tests.setup_tests import Config, init_waveforms, run_simulation

toplevel = "output_logic"

config = Config(
    HDLFILES=["src/multi_cycle_cpu/controller/controller_fsm.sv"],
    TOPLEVEL=toplevel,
    WORK_DIR="src/multi_cycle_cpu/controller",
    TEST_DIR="tests/multi_cycle_cpu/controller_unit/fsm/output_logic",
)

init_waveforms(config)


def set_signals(state):
    return {"state": str(state)}


waveform_file = "state_register_state_{}.vcd"


@pytest.mark.parametrize("state", States().get_all())
def test_output_logic(state):
    run_simulation(
        config, "test_{}".format(toplevel), waveform_file, set_signals(state)
    )
