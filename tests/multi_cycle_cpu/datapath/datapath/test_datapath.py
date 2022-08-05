import pytest

from tests import instructions
from tests.instructions.i_instruction import ADDIop, LWop
from tests.instructions.r_instruction import ORop
from tests.instructions.uj_instruction import JALop
from tests.multi_cycle_cpu.defs import ImmSrc
from tests.setup_tests import Config, init_waveforms, run_simulation

config = Config(
    INCLUDES=["src/multi_cycle_cpu/include/"],
    HDLFILES=[
        "src/multi_cycle_cpu/datapath/datapath.sv",
        "src/multi_cycle_cpu/datapath/alu.sv",
        "src/multi_cycle_cpu/datapath/aluflags.sv",
        "src/multi_cycle_cpu/datapath/extend.sv",
        "src/multi_cycle_cpu/datapath/flop.sv",
        "src/multi_cycle_cpu/datapath/flopdual.sv",
        "src/multi_cycle_cpu/datapath/flopenr.sv",
        "src/multi_cycle_cpu/datapath/flopenrdual.sv",
        "src/multi_cycle_cpu/datapath/flopr.sv",
        "src/multi_cycle_cpu/datapath/mux2.sv",
        "src/multi_cycle_cpu/datapath/mux3.sv",
        "src/multi_cycle_cpu/datapath/registerfile.sv",
    ],
    TOPLEVEL="datapath",
    WORK_DIR="src/multi_cycle_cpu/datapath/",
    TEST_DIR="tests/multi_cycle_cpu/datapath/datapath",
)

init_waveforms(config)

waveform_file = config.TOPLEVEL + "_instruction_{}.vcd"


def set_signals(instruction, immsrc, rd1=0, rd2=0):

    signals = {
        "op": str(instruction.get_op()),
        "funct3": str(instruction.get_funct3()),
        "funct7b5": str(instruction.get_funct7b5()),
        "ImmSrc": str(immsrc),
        "instruction": str(instruction.machine_code()),
        "rd1": str(rd1),
        "rd2": str(rd2),
    }

    return signals


@pytest.mark.parametrize("Instruction", [ADDIop])
def test_i_instructions(Instruction):

    instruction = Instruction(rd=4, rs1=6, imm=10)

    run_simulation(
        config,
        "test_i_instruction",
        waveform_file,
        set_signals(instruction, ImmSrc.i_type, rd1=4, rd2=0),
    )


@pytest.mark.parametrize("Instruction", [*instructions.s_instructions])
def test_sw_instructions(Instruction):
    instruction = Instruction(rs2=2, imm=10, rs1=4)

    run_simulation(
        config,
        "test_sw_instruction",
        waveform_file,
        set_signals(instruction, ImmSrc.sw, rd1=1, rd2=2),
    )


@pytest.mark.parametrize("Instruction", [ORop])
def test_r_instructions(Instruction):
    instruction = Instruction(rd=4, rs1=1, rs2=2)

    run_simulation(
        config,
        "test_r_instruction",
        waveform_file,
        set_signals(instruction, ImmSrc.r_type, rd1=1, rd2=2),
    )


@pytest.mark.parametrize("Instruction", [JALop])
def test_j_instructions(Instruction):
    instruction = Instruction(rd=20, imm=12)

    run_simulation(
        config,
        "test_j_instruction",
        waveform_file,
        set_signals(instruction, ImmSrc.jal),
    )


@pytest.mark.parametrize("Instruction", [*instructions.b_instructions])
@pytest.mark.parametrize("rd1", [1, -1])
@pytest.mark.parametrize("rd2", [1, -1])
def test_b_instructions(Instruction, rd1, rd2):
    instruction = Instruction(rs1=2, rs2=1, imm=12)

    run_simulation(
        config,
        "test_b_instruction",
        waveform_file,
        set_signals(instruction, ImmSrc.beq, rd1=rd1, rd2=rd2),
    )


@pytest.mark.parametrize("Instruction", [LWop])
def test_lw_instruction(Instruction):
    instruction = Instruction(rd=1, imm=2, rs1=4)

    run_simulation(
        config,
        "test_lw_instruction",
        waveform_file,
        set_signals(instruction, ImmSrc.lw, rd1=4),
    )


@pytest.mark.parametrize(
    "imm", [0b0, 0b11111111111111111111, 0b11111111111111111110, 0b01111111111111111111]
)
def test_lui_instruction(imm):
    instruction = instructions.uj_instruction.LUIop(rd=1, imm=imm)

    run_simulation(
        config,
        "test_lui_instruction",
        waveform_file,
        set_signals(instruction, ImmSrc.u_type, rd1=4),
    )
