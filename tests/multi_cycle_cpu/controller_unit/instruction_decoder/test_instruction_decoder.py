import os
import random

import pytest

from tests.multi_cycle_cpu.defs import ImmSrc, Op
from tests.setup_tests import Config, init_waveforms, run_simulation

toplevel = "instruction_decoder"

config = Config(
    HDLFILES=[
        "src/multi_cycle_cpu/controller/instruction_decoder.sv",
        "src/multi_cycle_cpu/controller/riscv.vh",
    ],
    TOPLEVEL=toplevel,
    WORK_DIR="src/multi_cycle_cpu/controller/",
    TEST_DIR="tests/multi_cycle_cpu/controller_unit/instruction_decoder",
)

init_waveforms(config)


def set_signals(op, ImmSrc):
    return {"op": str(op), "ImmSrc": str(ImmSrc)}


waveform_file = "instruction_decoder_op_{}ImmSrc_{}.vcd"


@pytest.mark.parametrize(
    "op, immSrc",
    [
        (Op.lw, ImmSrc.lw),
        (Op.sw, ImmSrc.sw),
        (Op.r_type, ImmSrc.r_type),
        (Op.beq, ImmSrc.beq),
        (Op.i_type, ImmSrc.i_type),
        (Op.jal, ImmSrc.jal),
        (Op.u_type, ImmSrc.u_type),
        (Op.default, ImmSrc.default),
    ],
)
def test_instruction_decoder(op, immSrc):
    run_simulation(
        config, "test_instruction_decoder", waveform_file, set_signals(op, immSrc)
    )
