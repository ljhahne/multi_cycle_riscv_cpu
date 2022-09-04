import os
import random

import pytest

from tests.multi_cycle_cpu.defs import ALUControl, ALUop, Loadtype
from tests.setup_tests import Config, init_waveforms, run_simulation

config = Config(
    INCLUDES=["src/multi_cycle_cpu/include/"],
    HDLFILES=["src/multi_cycle_cpu/controller/load_decoder.sv"],
    TOPLEVEL="load_decoder",
    WORK_DIR="src/multi_cycle_cpu/controller/",
    TEST_DIR="tests/multi_cycle_cpu/controller_unit/load_decoder",
)

init_waveforms(config)

waveform_file = "alu_decoder_funct3_{}.vcd"


@pytest.mark.parametrize(
    "load_type", [Loadtype.lb, Loadtype.lh, Loadtype.lw, Loadtype.lbu, Loadtype.lhu]
)
def test_load_decoder(load_type):
    run_simulation(
        config, "test_load_decoder", waveform_file, {"funct3": str(load_type)}
    )
