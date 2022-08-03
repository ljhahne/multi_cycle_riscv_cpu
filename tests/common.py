from tests.instructions.i_instruction import IInstruction, LWop
from tests.instructions.r_instruction import RInstruction
from tests.instructions.sb_instruction import BEQop, SWop
from tests.instructions.uj_instruction import JALop
from tests.multi_cycle_cpu.defs import XDEF, ImmSrc


def check_value(value_model, value_expected):
    if not value_model.value.is_resolvable:
        assert value_expected == XDEF, "dut x model {}".format(value_expected)

    else:
        assert value_model.value.integer == value_expected, "dut  {} model {}".format(
            value_model.value.integer, value_expected
        )


def get_immsrc_from_instruction_type(Instruction):
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

    return immsrc
