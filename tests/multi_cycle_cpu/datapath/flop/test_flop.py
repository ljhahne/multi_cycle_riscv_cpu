import os
import random

import pytest

from tests.instructions import *
from tests.setup_tests import Config, init_waveforms, run_simulation

config = Config(
    HDLFILES=["src/multi_cycle_cpu/datapath/flop.sv"],
    TOPLEVEL="flop",
    WORK_DIR="src/multi_cycle_cpu/datapath/",
    TEST_DIR="tests/multi_cycle_cpu/datapath/flop",
)

init_waveforms(config)

waveform_file = "flop_d0_{}_d1_{}.vcd"


def set_signals(d0, d1):

    return {
        "d0": str(d0),
        "d1": str(d1),
    }


@pytest.mark.parametrize("d0, d1", [(0, 1), (1, 0)])
def test_flop(d0, d1):
    run_simulation(config, "test_flop", waveform_file, set_signals(d0, d1))
