import os
import random

import pytest

from tests.instructions import *
from tests.setup_tests import Config, init_waveforms, run_simulation

config = Config(
    HDLFILES=[
        "src/multi_cycle_cpu/datapath/flopdual.sv",
        "src/multi_cycle_cpu/datapath/flop.sv",
    ],
    TOPLEVEL="flopdual",
    WORK_DIR="src/multi_cycle_cpu/datapath/",
    TEST_DIR="tests/multi_cycle_cpu/datapath/flopdual",
)

init_waveforms(config)

waveform_file = "flopenrdual_d00_{}_d10_{}_d01_{}_d11.vcd"


def set_signals(d00, d10, d01, d11):

    return {"d00": str(d00), "d10": str(d10), "d01": str(d01), "d11": str(d11)}


@pytest.mark.parametrize("d00", [0, 1])
@pytest.mark.parametrize("d10", [0, 1])
@pytest.mark.parametrize("d01", [0, 1])
@pytest.mark.parametrize("d11", [0, 1])
def test_flopdual(d00, d10, d01, d11):
    run_simulation(
        config, "test_flopdual", waveform_file, set_signals(d00, d10, d01, d11)
    )
