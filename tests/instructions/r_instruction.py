from bitstring import Bits

from tests.instructions.components import FUNCT3, FUNCT7, OP, RD, RS1, RS2
from tests.instructions.interface import InstructionType


class RInstruction(InstructionType):
    def __init__(self, op, rd, funct3, rs1, rs2, funct7):
        super().__init__()

        self._op = OP(op)
        self._rd = RD(rd)
        self._funct3 = FUNCT3(funct3)
        self._rs1 = RS1(rs1)
        self._rs2 = RS2(rs2)
        self._funct7 = FUNCT7(funct7)

    def _get_binary_string(self):
        return (
            self._funct7.get_string()
            + self._rs2.get_string()
            + self._rs1.get_string()
            + self._funct3.get_string()
            + self._rd.get_string()
            + self._op.get_string()
        )

    def get_funct3(self):
        return self._funct3.get_value()

    def get_funct7(self):
        return self._funct7

    def get_funct7b5(self):
        return int(
            Bits(uint=self._funct7.get_value(), length=self._funct7.get_length())[1]
        )


class ORop(RInstruction):
    def __init__(self, rd, rs1, rs2):
        super().__init__(0b0110011, rd, 0b110, rs1, rs2, 0b0000000)

        # register_file[rd] = register_file[rs1] | register_file[rs2]


class ANDop(RInstruction):
    def __init__(self, rd, rs1, rs2):
        super().__init__(0b0110011, rd, 0b111, rs1, rs2, 0b0000000)

        # register_file[rd] = register_file[rs1] & register_file[rs2]


class SLTop(RInstruction):
    def __init__(self, rd, rs1, rs2):
        super().__init__(0b0110011, rd, 0b010, rs1, rs2, 0b0000000)

        # register_file[rd] = register_file[rs1] << register_file[rs2]


class ADDop(RInstruction):
    def __init__(self, rd, rs1, rs2):
        super().__init__(0b0110011, rd, 0b000, rs1, rs2, 0b0000000)

        # register_file[rd] = register_file[rs1] + register_file[rs2]


class SUBop(RInstruction):
    def __init__(self, rd, rs1, rs2):
        super().__init__(0b0110011, rd, 0b000, rs1, rs2, 0b0100000)

        # register_file[rd] = register_file[rs1] - register_file[rs2]


class SLLop(RInstruction):
    def __init__(self, rd, rs1, rs2):
        super().__init__(0b0110011, rd, 0b001, rs1, rs2, 0b0000000)

        # register_file[rd] = register_file[rs1] - register_file[rs2]
