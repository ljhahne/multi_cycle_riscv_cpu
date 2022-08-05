import os
import random

import pytest
from bitstring import Bits

from tests import instructions
from tests.instructions import *
from tests.multi_cycle_cpu.defs import ImmSrc
from tests.multi_cycle_cpu.models import (
    instruction_immext_b,
    instruction_immext_i,
    instruction_immext_j,
    instruction_immext_s,
)
from tests.setup_tests import Config, init_waveforms, run_simulation

config = Config(
    INCLUDES=["src/multi_cycle_cpu/include/"],
    HDLFILES=["src/multi_cycle_cpu/datapath/extend.sv"],
    TOPLEVEL="extend",
    WORK_DIR="src/multi_cycle_cpu/datapath/",
    TEST_DIR="tests/multi_cycle_cpu/datapath/extend",
)

init_waveforms(config)

waveform_file = "extend_ImmSrc_{}_instruction_{}.vcd"


def set_signals(instruction, immsrc):

    return {
        "ImmSrc": str(immsrc),
        "instruction": str(instruction),
    }


@pytest.mark.parametrize("bit_31", [0, 1])
@pytest.mark.parametrize("bits_30_20", [0, 1])
def test_i_type(bit_31, bits_30_20):
    instruction = instruction_immext_i(bit_31, bits_30_20)

    run_simulation(
        config, "test_extend", waveform_file, set_signals(instruction, ImmSrc.i_type)
    )


@pytest.mark.parametrize("bit_31", [0, 1])
@pytest.mark.parametrize("bits_30_25", [0, 1])
@pytest.mark.parametrize("bits_11_7", [0, 1])
def test_s_type(bit_31, bits_30_25, bits_11_7):
    instruction = instruction_immext_s(bit_31, bits_30_25, bits_11_7)
    run_simulation(
        config, "test_extend", waveform_file, set_signals(instruction, ImmSrc.sw)
    )


@pytest.mark.parametrize("bit_31", [0, 1])
@pytest.mark.parametrize("bits_30_25", [0, 1])
@pytest.mark.parametrize("bit_7", [0, 1])
@pytest.mark.parametrize("bits_11_8", [0, 1])
def test_b_type(bit_31, bits_30_25, bit_7, bits_11_8):
    instruction = instruction_immext_b(bit_31, bits_30_25, bit_7, bits_11_8)
    run_simulation(
        config, "test_extend", waveform_file, set_signals(instruction, ImmSrc.beq)
    )


@pytest.mark.parametrize("bit_31", [0, 1])
@pytest.mark.parametrize("bits_19_12", [0, 1])
@pytest.mark.parametrize("bit_20", [0, 1])
@pytest.mark.parametrize("bits_30_21", [0, 1])
def test_j_type(bit_31, bits_19_12, bit_20, bits_30_21):
    instruction = instruction_immext_j(bit_31, bits_30_21, bit_20, bits_19_12)

    run_simulation(
        config, "test_extend", waveform_file, set_signals(instruction, ImmSrc.jal)
    )


@pytest.mark.parametrize(
    "imm", [0b0, 0b11111111111111111111, 0b11111111111111111110, 0b01111111111111111111]
)
def test_lui_instruction(imm):
    # rd dont'care
    instruction = instructions.uj_instruction.LUIop(
        rd=0, imm=Bits(uint=imm, length=20).uint
    ).machine_code()

    run_simulation(
        config, "test_extend", waveform_file, set_signals(instruction, ImmSrc.u_type)
    )
