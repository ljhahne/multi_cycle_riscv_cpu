import os

import pytest

from tests.setup_tests import Config, init_waveforms, run_simulation

toplevel = "pc_write"

config = Config(
    HDLFILES=["src/multi_cycle_cpu/controller/pc_write.sv"],
    TOPLEVEL=toplevel,
    WORK_DIR="src/multi_cycle_cpu/controller",
    TEST_DIR="tests/multi_cycle_cpu/controller_unit/pc_write",
)

init_waveforms(config)


def set_signals(Zero, Branch, PCUpdate):
    return {"Zero": str(Zero), "Branch": str(Branch), "PCUpdate": str(PCUpdate)}


waveform_file = "instruction_decoder_Zero_{}_Branch_{}_PCUpdate_{}.vcd"


@pytest.mark.parametrize("Zero", [0, 1])
@pytest.mark.parametrize("Branch", [0, 1])
@pytest.mark.parametrize("PCUpdate", [0, 1])
def test_lw(Zero, Branch, PCUpdate):
    run_simulation(
        config,
        "test_{}".format(toplevel),
        waveform_file,
        set_signals(Zero, Branch, PCUpdate),
    )
