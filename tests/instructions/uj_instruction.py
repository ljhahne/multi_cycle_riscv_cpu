from abc import ABC, abstractmethod

from bitstring import Bits

from tests.instructions.components import IMM, OP, RD
from tests.instructions.interface import InstructionType


class UJInstructionBase(InstructionType):
    def __init__(self, op, rd, imm):
        super().__init__()

        self._op = OP(op)
        self._rd = RD(rd)

        # only check length
        IMM(imm, length=32)

        self._imm = self.set_imm(imm)

    @abstractmethod
    def set_imm(self, imm):
        pass

    def _get_binary_string(self):
        return self._imm.get_string() + self._rd.get_string() + self._op.get_string()

    def get_funct3(self):
        return 0

    def get_funct7(self):
        return 0

    def get_funct7b5(self):
        return 0


class JInstruction(UJInstructionBase):
    def __init__(self, op, rd, imm):
        super().__init__(op, rd, imm)

    def set_imm(self, imm):
        imm_bits = Bits(uint=imm, length=32)

        # idx 20, 10:1, 11, 19:12
        return IMM(
            (
                bin(imm_bits[-21])
                + imm_bits[-11:-1]
                + bin(imm_bits[-12])
                + imm_bits[-20:-12]
            ).uint,
            length=20,
            signed=False,
        )


class JALop(JInstruction):
    def __init__(self, rd, imm, pc=0):
        super().__init__(0b1101111, rd, imm)

        # TODO currently not byte addressed: change 1 to 4
        # register_file[rd] = pc + 1

        # TODO
        # pc += sign_extend(imm[-21:])
