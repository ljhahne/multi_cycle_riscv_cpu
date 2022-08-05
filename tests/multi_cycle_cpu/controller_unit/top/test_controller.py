import os

print(os.listdir("/opt/project/tests/multi_cycle_cpu/controller_unit/top/"))
import pytest

from tests import instructions
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
from tests.instructions.sb_instruction import BInstruction, SInstruction
from tests.instructions.uj_instruction import JALop, LUIop
from tests.multi_cycle_cpu.defs import ImmSrc
from tests.setup_tests import Config, init_waveforms, run_simulation

toplevel = "controller"
hdl_file = toplevel
test_dir = hdl_file


config = Config(
    INCLUDES=["src/multi_cycle_cpu/include/"],
    HDLFILES=[
        "src/multi_cycle_cpu/controller/controller.sv",
        "src/multi_cycle_cpu/controller/controller_fsm.sv",
        "src/multi_cycle_cpu/controller/alu_decoder.sv",
        "src/multi_cycle_cpu/controller/instruction_decoder.sv",
        "src/multi_cycle_cpu/controller/pc_write.sv",
    ],
    TOPLEVEL=toplevel,
    WORK_DIR="src/multi_cycle_cpu/controller/",
    TEST_DIR="tests/multi_cycle_cpu/controller_unit/top",
)

init_waveforms(config)


def set_signals(reset, instruction, immsrc, N=0, Z=0, C=0, V=0):
    return {
        "reset": str(reset),
        "op": str(instruction.get_op()),
        "funct3": str(instruction.get_funct3()),
        "funct7b5": str(instruction.get_funct7b5()),
        "Z": str(Z),
        "N": str(N),
        "C": str(C),
        "V": str(V),
        "ImmSrc": str(immsrc),
    }


waveform_file = "controller_reset_{}_op_{}_funct3_{}_funct7b5_{}_Z_{}.vcd"


@pytest.mark.parametrize("reset", [0])
@pytest.mark.parametrize("Instruction", [ORop, ANDop, SLTop, ADDop, SUBop, SLLop])
def test_r_instructions(reset, Instruction):
    run_simulation(
        config,
        "test_{}".format(toplevel),
        waveform_file,
        set_signals(reset, Instruction(0, 0, 0), ImmSrc.r_type),
    )


@pytest.mark.parametrize("reset", [0])
@pytest.mark.parametrize("Instruction", [ADDIop, LWop])
def test_i_instructions(reset, Instruction):
    run_simulation(
        config,
        "test_{}".format(toplevel),
        waveform_file,
        set_signals(reset, Instruction(0, 0, 0), ImmSrc.i_type),
    )


@pytest.mark.parametrize("reset", [0])
@pytest.mark.parametrize("Instruction", [JALop])
def test_j_instructions(reset, Instruction):
    run_simulation(
        config,
        "test_{}".format(toplevel),
        waveform_file,
        set_signals(reset, Instruction(0, 0, 0), ImmSrc.jal),
    )


@pytest.mark.parametrize("reset", [0])
@pytest.mark.parametrize("Instruction", [LUIop])
def test_u_instructions(reset, Instruction):
    run_simulation(
        config,
        "test_{}".format(toplevel),
        waveform_file,
        set_signals(reset, Instruction(1, 0), ImmSrc.u_type),
    )


@pytest.mark.parametrize("N", [0, 1])
@pytest.mark.parametrize("Z", [0, 1])
@pytest.mark.parametrize("C", [0, 1])
@pytest.mark.parametrize("V", [0, 1])
@pytest.mark.parametrize("reset", [0])
@pytest.mark.parametrize("Instruction", [*instructions.s_instructions])
def test_s_instructions(reset, Instruction, N, Z, C, V):
    run_simulation(
        config,
        "test_{}".format(toplevel),
        waveform_file,
        set_signals(reset, Instruction(0, 0, 0), ImmSrc.sw, N, Z, C, V),
    )


@pytest.mark.parametrize("N", [0, 1])
@pytest.mark.parametrize("Z", [0, 1])
@pytest.mark.parametrize("C", [0, 1])
@pytest.mark.parametrize("V", [0, 1])
@pytest.mark.parametrize("reset", [0])
@pytest.mark.parametrize("Instruction", [*instructions.b_instructions])
def test_b_instructions(reset, Instruction, N, Z, C, V):
    run_simulation(
        config,
        "test_{}".format(toplevel),
        waveform_file,
        set_signals(reset, Instruction(0, 0, 0), ImmSrc.beq, N, Z, C, V),
    )
