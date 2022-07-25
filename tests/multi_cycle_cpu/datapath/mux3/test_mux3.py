import os
import random

import pytest

from tests.instructions import *
from tests.setup_tests import Config, init_waveforms, run_simulation

config = Config(
    HDLFILES=["src/multi_cycle_cpu/datapath/mux3.sv"],
    TOPLEVEL="mux3",
    WORK_DIR="src/multi_cycle_cpu/datapath/",
    TEST_DIR="tests/multi_cycle_cpu/datapath/mux3",
)

init_waveforms(config)

waveform_file = config.TOPLEVEL + "_d0_{}_d1_{}_d2{}_s_{}.vcd"


def set_signals(d0, d1, d2, s):

    return {"d0": str(d0), "d1": str(d1), "d2": str(d2), "s": str(s)}


@pytest.mark.parametrize("d0", [0, 1])
@pytest.mark.parametrize("d1", [0, 1])
@pytest.mark.parametrize("d2", [0, 1])
@pytest.mark.parametrize("s", [0, 1])
def test_flop(d0, d1, d2, s):
    run_simulation(config, "test_mux3", waveform_file, set_signals(d0, d1, d2, s))
