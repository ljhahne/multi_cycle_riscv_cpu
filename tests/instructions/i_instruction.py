from tests.instructions.components import FUNCT3, IMM, OP, RD, RS1
from tests.instructions.interface import InstructionType


class IInstruction(InstructionType):
    def __init__(self, op, rd, funct3, rs1, imm):
        super().__init__()

        self._op = OP(op)
        self._rd = RD(rd)
        self._funct3 = FUNCT3(funct3)
        self._rs1 = RS1(rs1)
        self._imm = IMM(imm, 12)

    def _get_binary_string(self):
        return (
            self._imm.get_string()
            + self._rs1.get_string()
            + self._funct3.get_string()
            + self._rd.get_string()
            + self._op.get_string()
        )

    def get_funct3(self):
        return self._funct3.get_value()

    def get_funct7(self):
        return 0

    def get_funct7b5(self):
        return 0


class ADDIop(IInstruction):
    def __init__(self, rd, rs1, imm):
        super().__init__(op=0b0010011, rd=rd, funct3=0b000, rs1=rs1, imm=imm)

        # register_file[rd] = register_file[rs1] + imm


class LWop(IInstruction):
    def __init__(self, rd, imm, rs1):
        super().__init__(op=0b0000011, rd=rd, funct3=0b010, rs1=rs1, imm=imm)

        # register_file[rd] = memory[register_file[rs1] + imm]
