from bitstring import Bits


class InstructionComponent:
    def __init__(self, value, length, name, signed=False):
        self._value = value
        self._length = length
        self._name = name
        self.__signed = signed

        self._check_length()

    def get_value(self):
        return self._value

    def get_length(self):
        return self._length

    def get_string(self):
        if self.__signed:
            bits = Bits(int=self._value, length=self._length)
        else:
            bits = Bits(uint=self._value, length=self._length)

        return bits.bin

    def _check_length(self):
        assert self._value.bit_length() <= self._length


class OP(InstructionComponent):
    def __init__(self, value):
        super().__init__(value, length=7, name="op")


class RD(InstructionComponent):
    def __init__(self, value):
        super().__init__(value, length=5, name="rd")


class FUNCT3(InstructionComponent):
    def __init__(self, value):
        super().__init__(value, length=3, name="funct3")


class RS1(InstructionComponent):
    def __init__(self, value):
        super().__init__(value, length=5, name="rs1")


class RS2(InstructionComponent):
    def __init__(self, value):
        super().__init__(value, length=5, name="rs2")


class FUNCT7(InstructionComponent):
    def __init__(self, value):
        super().__init__(value, length=7, name="funct7")


class IMM(InstructionComponent):
    def __init__(self, value, length, signed=True):
        super().__init__(value, length=length, name="imm", signed=signed)
