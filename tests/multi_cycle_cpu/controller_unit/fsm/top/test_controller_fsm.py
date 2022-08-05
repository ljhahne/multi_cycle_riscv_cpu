import os

import pytest

from tests.multi_cycle_cpu.defs import Op
from tests.setup_tests import Config, init_waveforms, run_simulation

toplevel = "controller_fsm"

config = Config(
    INCLUDES=["src/multi_cycle_cpu/include/"],
    HDLFILES=[
        "src/multi_cycle_cpu/controller/controller_fsm.sv",
    ],
    TOPLEVEL=toplevel,
    WORK_DIR="src/multi_cycle_cpu/controller/",
    TEST_DIR="tests/multi_cycle_cpu/controller_unit/fsm/top",
)

init_waveforms(config)


def set_signals(op, reset):
    return {"op": str(op), "reset": str(reset)}


waveform_file = "fsm_op_{}_reset_{}.vcd"


@pytest.mark.parametrize("reset", [0])
@pytest.mark.parametrize("op", Op().get_all())
def test_fetch(op, reset):
    run_simulation(
        config, "test_{}".format(toplevel), waveform_file, set_signals(op, reset)
    )
