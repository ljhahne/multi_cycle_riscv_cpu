import os
import random

import pytest

from tests.instructions import *
from tests.setup_tests import Config, init_waveforms, run_simulation

config = Config(
    HDLFILES=["src/multi_cycle_cpu/datapath/registerfile.sv"],
    TOPLEVEL="registerfile",
    WORK_DIR="src/multi_cycle_cpu/datapath/",
    TEST_DIR="tests/multi_cycle_cpu/datapath/registerfile",
)

init_waveforms(config)

waveform_file = config.TOPLEVEL + "_d0_{}_d1_{}.vcd"


def set_signals(we, a1, a2, a3, wd3):

    return {
        "we": str(we),
        "a1": str(a1),
        "a2": str(a2),
        "a3": str(a3),
        "wd3": str(wd3),
    }


@pytest.mark.parametrize("we", [0, 1])
@pytest.mark.parametrize("a1", [0, 1])
@pytest.mark.parametrize("a2", [0, 1])
@pytest.mark.parametrize("a3", [0, 1])
@pytest.mark.parametrize("wd3", [0, 1])
def test_registerfile(we, a1, a2, a3, wd3):
    run_simulation(
        config, "test_registerfile", waveform_file, set_signals(we, a1, a2, a3, wd3)
    )
