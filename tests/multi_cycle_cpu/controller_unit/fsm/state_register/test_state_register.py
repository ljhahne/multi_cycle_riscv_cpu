import os
import random

import pytest

from tests.multi_cycle_cpu.defs import States
from tests.setup_tests import Config, init_waveforms, run_simulation

toplevel = "state_register"
hdl_file = "controller_fsm"
test_dir = hdl_file

config = Config(
    HDLFILES=["src/multi_cycle_cpu/controller/controller_fsm.sv"],
    TOPLEVEL=toplevel,
    WORK_DIR="src/multi_cycle_cpu/controller",
    TEST_DIR="tests/multi_cycle_cpu/controller_unit/fsm/state_register",
)

init_waveforms(config)


def set_signals(state_next, reset):
    return {"state_next": str(state_next), "reset": str(reset)}


waveform_file = "state_register_state_next_{}_reset_{}.vcd"


@pytest.mark.parametrize("reset", [0, 1])
@pytest.mark.parametrize("state_next", States().get_all())
def test_state_register(state_next, reset):
    run_simulation(
        config,
        "test_{}".format(toplevel),
        waveform_file,
        set_signals(state_next, reset),
    )
