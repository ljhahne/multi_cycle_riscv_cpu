import os
import random

import pytest

from tests.instructions import *
from tests.setup_tests import Config, init_waveforms, run_simulation

config = Config(
    HDLFILES=["src/multi_cycle_cpu/datapath/flopr.sv"],
    TOPLEVEL="flopr",
    WORK_DIR="src/multi_cycle_cpu/datapath/",
    TEST_DIR="tests/multi_cycle_cpu/datapath/flopr",
)

init_waveforms(config)

waveform_file = "flop_d0_{}_d1_{}_reset_{}.vcd"


def set_signals(d0, d1, reset):

    return {"d0": str(d0), "d1": str(d1), "reset": str(reset)}


@pytest.mark.parametrize("d0", [0, 1])
@pytest.mark.parametrize("d1", [0, 1])
@pytest.mark.parametrize("reset", [0, 1])
def test_flop(d0, d1, reset):
    run_simulation(config, "test_flopr", waveform_file, set_signals(d0, d1, reset))
