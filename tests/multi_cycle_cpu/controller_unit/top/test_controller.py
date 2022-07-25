import os

import pytest

from tests.instructions.i_instruction import ADDIop, IInstruction, LWop
from tests.instructions.r_instruction import (
    ADDop,
    ANDop,
    ORop,
    RInstruction,
    SLLop,
    SLTop,
    SUBop,
)
from tests.instructions.sb_instruction import BEQop, SWop
from tests.instructions.uj_instruction import JALop
from tests.multi_cycle_cpu.defs import ImmSrc
from tests.setup_tests import Config, init_waveforms, run_simulation

toplevel = "controller"
hdl_file = toplevel
test_dir = hdl_file


config = Config(
    HDLFILES=[
        "src/multi_cycle_cpu/controller/controller.sv",
        "src/multi_cycle_cpu/controller/controller_fsm.sv",
        "src/multi_cycle_cpu/controller/alu_decoder.sv",
        "src/multi_cycle_cpu/controller/instruction_decoder.sv",
        "src/multi_cycle_cpu/controller/pc_write.sv",
        "src/multi_cycle_cpu/controller/riscv.vh",
    ],
    TOPLEVEL=toplevel,
    WORK_DIR="src/multi_cycle_cpu/controller/",
    TEST_DIR="tests/multi_cycle_cpu/controller_unit/top",
)

init_waveforms(config)


def set_signals(reset, Instruction, Zero):
    if issubclass(Instruction, IInstruction):
        immsrc = ImmSrc.i_type

    elif issubclass(Instruction, LWop):
        immsrc = ImmSrc.lw

    elif issubclass(Instruction, SWop):
        immsrc = ImmSrc.sw

    elif issubclass(Instruction, BEQop):
        immsrc = ImmSrc.beq

    elif issubclass(Instruction, JALop):
        immsrc = ImmSrc.jal

    elif issubclass(Instruction, RInstruction):
        immsrc = ImmSrc.r_type

    else:
        immsrc = ImmSrc.default

    instruction = Instruction(0, 0, 0)

    return {
        "reset": str(reset),
        "op": str(instruction.get_op()),
        "funct3": str(instruction.get_funct3()),
        "funct7b5": str(instruction.get_funct7b5()),
        "Zero": str(Zero),
        "ImmSrc": str(immsrc),
    }


waveform_file = "controller_reset_{}_op_{}_funct3_{}_funct7b5_{}_Zero_{}.vcd"


@pytest.mark.parametrize("Zero", [0, 1])
@pytest.mark.parametrize("reset", [0])
@pytest.mark.parametrize("instruction", [ORop, ANDop, SLTop, ADDop, SUBop, SLLop])
def test_r_instructions(reset, instruction, Zero):
    run_simulation(
        config,
        "test_{}".format(toplevel),
        waveform_file,
        set_signals(reset, instruction, Zero),
    )


@pytest.mark.parametrize("Zero", [0, 1])
@pytest.mark.parametrize("reset", [0])
@pytest.mark.parametrize("instruction", [ADDIop, LWop])
def test_i_instructions(reset, instruction, Zero):
    run_simulation(
        config,
        "test_{}".format(toplevel),
        waveform_file,
        set_signals(reset, instruction, Zero),
    )


@pytest.mark.parametrize("Zero", [0, 1])
@pytest.mark.parametrize("reset", [0])
@pytest.mark.parametrize("instruction", [JALop])
def test_ju_instructions(reset, instruction, Zero):
    run_simulation(
        config,
        "test_{}".format(toplevel),
        waveform_file,
        set_signals(reset, instruction, Zero),
    )


@pytest.mark.parametrize("Zero", [0, 1])
@pytest.mark.parametrize("reset", [0])
@pytest.mark.parametrize("instruction", [SWop, BEQop])
def test_sb_instructions(reset, instruction, Zero):
    run_simulation(
        config,
        "test_{}".format(toplevel),
        waveform_file,
        set_signals(reset, instruction, Zero),
    )
