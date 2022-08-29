import pytest

from tests import instructions
from tests.instructions.i_instruction import LBop, LBUop, LHop, LHUop, LWop
from tests.instructions.r_instruction import ORop
from tests.instructions.uj_instruction import JALop
from tests.multi_cycle_cpu.defs import ImmSrc
from tests.setup_tests import Config, init_waveforms, run_simulation

config = Config(
    INCLUDES=["src/multi_cycle_cpu/include/"],
    HDLFILES=[
        "src/multi_cycle_cpu/datapath/load_extend.sv",
    ],
    TOPLEVEL="load_extend",
    WORK_DIR="src/multi_cycle_cpu/datapath/",
    TEST_DIR="tests/multi_cycle_cpu/datapath/load_extend",
)

init_waveforms(config)

waveform_file = config.TOPLEVEL + "_load_extend_{}.vcd"

# we don't care about rd, rs1 and imm in these tests


# def set_signals(instruction, immsrc):
#
#     signals = {
#         "op": str(instruction.get_op()),
#         "funct3": str(instruction.get_funct3()),
#         "funct7b5": str(instruction.get_funct7b5()),
#         "ImmSrc": str(immsrc),
#         "instruction": str(instruction.machine_code()),
#         "rd": str(instruction.get_rd()),
#         "rs1": str(instruction.get_rs1()),
#         "imm": str(instruction.get_imm)
#     }
#
#     return signals


@pytest.mark.parametrize("Instruction", [LBop, LHop, LWop, LBUop, LHUop])
def test_lb(Instruction):

    signals = dict(Instruction(rd=4, rs1=6, imm=10))
    signals["ImmSrc"] = str(ImmSrc.i_type)

    run_simulation(
        config,
        "test_lb",
        waveform_file,
        signals,
    )


@pytest.mark.parametrize("ReadData", [0b11111111, 0b01111111, 0b101111111])
def test_lb(ReadData):

    signals = {"ReadData": str(ReadData)}

    run_simulation(
        config,
        "test_lb",
        waveform_file,
        signals,
    )


@pytest.mark.parametrize(
    "ReadData", [0b1111111111111111, 0b0111111111111111, 0b10111111111111111]
)
def test_lh(ReadData):

    signals = {"ReadData": str(ReadData)}

    run_simulation(
        config,
        "test_lh",
        waveform_file,
        signals,
    )


@pytest.mark.parametrize("ReadData", [0b11111111, 0b01111111, 0b101111111])
def test_lbu(ReadData):

    signals = {"ReadData": str(ReadData)}

    run_simulation(
        config,
        "test_lbu",
        waveform_file,
        signals,
    )


@pytest.mark.parametrize(
    "ReadData", [0b1111111111111111, 0b0111111111111111, 0b10111111111111111]
)
def test_lhu(ReadData):

    signals = {"ReadData": str(ReadData)}

    run_simulation(
        config,
        "test_lhu",
        waveform_file,
        signals,
    )


@pytest.mark.parametrize("ReadData", [0b1])
def test_lw(ReadData):

    signals = {"ReadData": str(ReadData)}

    run_simulation(
        config,
        "test_lw",
        waveform_file,
        signals,
    )
