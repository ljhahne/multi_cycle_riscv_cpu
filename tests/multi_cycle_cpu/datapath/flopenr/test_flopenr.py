import os
import random

import pytest

from tests.instructions import *
from tests.setup_tests import Config, init_waveforms, run_simulation

config = Config(
    HDLFILES=["src/multi_cycle_cpu/datapath/flopenr.sv"],
    TOPLEVEL="flopenr",
    WORK_DIR="src/multi_cycle_cpu/datapath/",
    TEST_DIR="tests/multi_cycle_cpu/datapath/flopenr",
)

init_waveforms(config)

waveform_file = "flop_d0_{}_d1_{}_en_{}_reset_{}.vcd"


def set_signals(d0, d1, en, reset):

    return {"d0": str(d0), "d1": str(d1), "en": str(en), "reset": str(reset)}


@pytest.mark.parametrize("d0", [0, 1])
@pytest.mark.parametrize("d1", [0, 1])
@pytest.mark.parametrize("en", [0, 1])
@pytest.mark.parametrize("reset", [0, 1])
def test_flop(d0, d1, en, reset):
    run_simulation(
        config, "test_flopenr", waveform_file, set_signals(d0, d1, en, reset)
    )
