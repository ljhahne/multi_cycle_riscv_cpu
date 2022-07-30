# __all__ = ["i_instruction", "r_instruction", "sb_instruction", "uj_instruction"]

from tests.instructions.i_instruction import IInstruction
from tests.instructions.interface import InstructionType
from tests.instructions.r_instruction import RInstruction
from tests.instructions.sb_instruction import BInstruction, SInstruction
from tests.instructions import sb_instruction
from tests.instructions.uj_instruction import JInstruction


b_instructions = [   sb_instruction.BEQop,
                    sb_instruction.BNEop,
                    sb_instruction.BLTop,
                    sb_instruction.BGEop,
                    sb_instruction.BLTUop,
                    sb_instruction.BGEUop
                    ]

s_instructions = [  sb_instruction.SWop,
                    ]