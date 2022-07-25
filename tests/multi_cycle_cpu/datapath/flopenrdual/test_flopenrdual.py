import os
import random

import pytest

from tests.instructions import *
from tests.setup_tests import Config, init_waveforms, run_simulation

config = Config(
    HDLFILES=[
        "src/multi_cycle_cpu/datapath/flopenrdual.sv",
        "src/multi_cycle_cpu/datapath/flopenr.sv",
    ],
    TOPLEVEL="flopenrdual",
    WORK_DIR="src/multi_cycle_cpu/datapath/",
    TEST_DIR="tests/multi_cycle_cpu/datapath/flopenrdual",
)

init_waveforms(config)

waveform_file = "flopenrdual_d00_{}_d10_{}_d01_{}_d11_{}_en_{}_reset_{}.vcd"


def set_signals(d00, d10, d01, d11, en, reset):

    return {
        "d00": str(d00),
        "d10": str(d10),
        "d01": str(d01),
        "d11": str(d11),
        "en": str(en),
        "reset": str(reset),
    }


@pytest.mark.parametrize("d00", [0, 1])
@pytest.mark.parametrize("d10", [0, 1])
@pytest.mark.parametrize("d01", [0, 1])
@pytest.mark.parametrize("d11", [0, 1])
@pytest.mark.parametrize("en", [0, 1])
@pytest.mark.parametrize("reset", [0, 1])
def test_flopenrdual(d00, d10, d01, d11, en, reset):
    run_simulation(
        config,
        "test_flopenrdual",
        waveform_file,
        set_signals(d00, d10, d01, d11, en, reset),
    )
