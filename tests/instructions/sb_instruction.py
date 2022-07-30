from abc import abstractmethod

from bitstring import Bits

from tests.instructions.components import FUNCT3, IMM, OP, RS1, RS2
from tests.instructions.interface import InstructionType


class SBInstructionBase(InstructionType):
    def __init__(self, op, funct3, rs1, rs2, imm):
        super().__init__()

        self._op = OP(op)
        self._funct3 = FUNCT3(funct3)
        self._rs1 = RS1(rs1)
        self._rs2 = RS2(rs2)

        # only check length
        IMM(imm, 13)

        self._imm1, self._imm2 = self.set_imm_values(imm)

    @abstractmethod
    def set_imm_values(self, imm):
        pass

    def _get_binary_string(self):
        return (
            self._imm2.get_string()
            + self._rs2.get_string()
            + self._rs1.get_string()
            + self._funct3.get_string()
            + self._imm1.get_string()
            + self._op.get_string()
        )

    def get_funct3(self):
        return self._funct3.get_value()

    def get_funct7(self):
        return 0

    def get_funct7b5(self):
        return 0


class SInstruction(SBInstructionBase):
    def __init__(self, op, funct3, rs1, rs2, imm):
        super().__init__(op, funct3, rs1, rs2, imm)

    def set_imm_values(self, imm):

        imm_bits = Bits(uint=imm, length=13)

        # idx 4:0
        imm1 = IMM(imm_bits[-5:].uint, length=5, signed=False)
        # idx 11:5
        imm2 = IMM(imm_bits[-12:-5].uint, length=7, signed=False)

        return imm1, imm2


class BInstruction(SBInstructionBase):
    def __init__(self, op, funct3, rs1, rs2, imm):
        super().__init__(op, funct3, rs1, rs2, imm)

    def set_imm_values(self, imm):

        imm_bits = Bits(uint=imm, length=13)

        # idx 4:1, 11
        imm1 = IMM((imm_bits[-5:-1] + bin(imm_bits[-12])).uint, length=5, signed=False)
        # idx 12 10:5
        imm2 = IMM((bin(imm_bits[-13]) + imm_bits[-11:-5]).uint, length=7, signed=False)

        return imm1, imm2


class SWop(SInstruction):
    def __init__(self, rs2, imm, rs1):
        super().__init__(0b0100011, 0b010, rs1, rs2, imm)

        # memory[register_file[rs1] + imm] = rs2


class BEQop(BInstruction):
    def __init__(self, rs1, rs2, imm, pc=0):
        super().__init__(op=0b1100011, funct3=0b000, rs1=rs1, rs2=rs2, imm=imm)

        # if register_file[rs1] == register_file[rs2]:
        #     pc += imm


class BNEop(BInstruction):
    def __init__(self, rs1, rs2, imm, pc=0):
        super().__init__(op=0b1100011, funct3=0b001, rs1=rs1, rs2=rs2, imm=imm)


class BLTop(BInstruction):
    def __init__(self, rs1, rs2, imm, pc=0):
        super().__init__(op=0b1100011, funct3=0b100, rs1=rs1, rs2=rs2, imm=imm)


class BGEop(BInstruction):
    def __init__(self, rs1, rs2, imm, pc=0):
        super().__init__(op=0b1100011, funct3=0b101, rs1=rs1, rs2=rs2, imm=imm)


class BLTUop(BInstruction):
    def __init__(self, rs1, rs2, imm, pc=0):
        super().__init__(op=0b1100011, funct3=0b110, rs1=rs1, rs2=rs2, imm=imm)


class BGEUop(BInstruction):
    def __init__(self, rs1, rs2, imm, pc=0):
        super().__init__(op=0b1100011, funct3=0b111, rs1=rs1, rs2=rs2, imm=imm)
