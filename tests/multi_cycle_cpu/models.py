from bitstring import Bits

from tests.multi_cycle_cpu.defs import XDEF, ALUControl, ImmSrc, Op, States


def state_register(state_next, reset):
    if reset:
        return States.S_FETCH

    return state_next


def next_state(state, op):

    print("model state {}".format(state))
    if state == States.S_FETCH:
        return States.S_DECODE

    elif state == States.S_DECODE:
        if op == Op.lw or op == Op.sw:
            return States.S_MEMADR

        elif op == Op.r_type:
            return States.S_EXECUTER

        elif op == Op.i_type:
            return States.S_EXECUTEL

        elif op == Op.jal:
            return States.S_JAL

        elif op == Op.beq:
            return States.S_BEQ

        else:
            return States.S_FETCH

    elif state == States.S_MEMADR:
        if op == Op.lw:
            return States.S_MEMREAD

        elif op == Op.sw:
            return States.S_MEMWRITE

        else:
            return States.S_FETCH

    elif (
        state == States.S_EXECUTER
        or state == States.S_EXECUTEL
        or state == States.S_JAL
    ):
        return States.S_ALUWB

    elif state == States.S_BEQ or state == States.S_MEMWRITE or state == States.S_ALUWB:
        return States.S_FETCH

    elif state == States.S_MEMREAD:
        return States.S_MEMWB

    else:
        return States.S_FETCH


def output_logic(state):
    if state == States.S_FETCH:
        ALUSrcA = 0b00
        ALUSrcB = 0b10
        ResultSrc = 0b10
        AdrSrc = 0b0
        IRWrite = 0b1
        aluOP = 0b00
        PCUpdate = 0b1

        RegWrite = 0b0
        MemWrite = 0b0
        Branch = 0b0

    elif state == States.S_DECODE:
        ALUSrcA = 0b01
        ALUSrcB = 0b01
        aluOP = 0b00

        ResultSrc = 0b00
        AdrSrc = 0b0
        IRWrite = 0b0

        RegWrite = 0b0
        MemWrite = 0b0
        Branch = 0b0
        PCUpdate = 0b0

    elif state == States.S_MEMADR:
        ALUSrcA = 0b10
        ALUSrcB = 0b01
        aluOP = 0b00

        ResultSrc = 0b00
        AdrSrc = 0b0
        IRWrite = 0b0

        RegWrite = 0b0
        MemWrite = 0b0
        Branch = 0b0
        PCUpdate = 0b0

    elif state == States.S_MEMREAD:
        ResultSrc = 0b00
        AdrSrc = 0b1

        ALUSrcA = 0b00
        ALUSrcB = 0b00
        IRWrite = 0b0

        RegWrite = 0b0
        MemWrite = 0b0
        aluOP = 0b00
        Branch = 0b0
        PCUpdate = 0b0

    elif state == States.S_MEMWB:
        ResultSrc = 0b01
        RegWrite = 0b1

        ALUSrcA = 0b00
        ALUSrcB = 0b00
        AdrSrc = 0b0
        IRWrite = 0b0

        MemWrite = 0b0
        aluOP = 0b00
        Branch = 0b0
        PCUpdate = 0b0

    elif state == States.S_MEMWRITE:
        ResultSrc = 0b00
        AdrSrc = 0b1
        MemWrite = 0b1

        ALUSrcA = 0b00
        ALUSrcB = 0b00
        IRWrite = 0b0

        RegWrite = 0b0
        aluOP = 0b00
        Branch = 0b0
        PCUpdate = 0b0

    elif state == States.S_EXECUTER:

        ALUSrcA = 0b10
        ALUSrcB = 0b00
        aluOP = 0b10

        ResultSrc = 0b00
        AdrSrc = 0b0
        IRWrite = 0b0

        RegWrite = 0b0
        MemWrite = 0b0
        Branch = 0b0
        PCUpdate = 0b0

    elif state == States.S_EXECUTEL:
        ALUSrcA = 0b10
        ALUSrcB = 0b01
        aluOP = 0b10

        ResultSrc = 0b00
        AdrSrc = 0b0
        IRWrite = 0b0

        RegWrite = 0b0
        MemWrite = 0b0
        Branch = 0b0
        PCUpdate = 0b0

    elif state == States.S_ALUWB:
        ResultSrc = 0b00
        RegWrite = 0b1

        ALUSrcA = 0b00
        ALUSrcB = 0b00
        AdrSrc = 0b0
        IRWrite = 0b0

        MemWrite = 0b0
        aluOP = 0b00
        Branch = 0b0
        PCUpdate = 0b0

    elif state == States.S_BEQ:
        ALUSrcA = 0b10
        ALUSrcB = 0b00
        aluOP = 0b01
        ResultSrc = 0b00
        Branch = 0b1

        AdrSrc = 0b0
        IRWrite = 0b0

        RegWrite = 0b0
        MemWrite = 0b0
        PCUpdate = 0b0

    elif state == States.S_JAL:
        ALUSrcA = 0b01
        ALUSrcB = 0b10
        ResultSrc = 0b00
        aluOP = 0b00
        PCUpdate = 0b1

        AdrSrc = 0b0
        IRWrite = 0b0

        RegWrite = 0b0
        MemWrite = 0b0
        Branch = 0b0

    else:
        ALUSrcA = 0b0
        ALUSrcB = 0b0
        ResultSrc = 0b0
        aluOP = 0b0
        PCUpdate = 0b0

        AdrSrc = 0b0
        IRWrite = 0b0

        RegWrite = 0b0
        MemWrite = 0b0
        Branch = 0b0

    return (
        ALUSrcA,
        ALUSrcB,
        ResultSrc,
        aluOP,
        PCUpdate,
        AdrSrc,
        IRWrite,
        RegWrite,
        MemWrite,
        Branch,
    )


def fsm(op, reset):

    states_base = [States.S_FETCH, States.S_DECODE]
    states_op = []
    states = []
    outputs = []

    if reset:
        states = [States.S_FETCH]

    elif op == Op.lw:
        states_op = [States.S_MEMADR, States.S_MEMREAD, States.S_MEMWB]

    elif op == Op.sw:
        states_op = [States.S_MEMADR, States.S_MEMWRITE]

    elif op == Op.r_type:
        states_op = [States.S_EXECUTER, States.S_ALUWB]

    elif op == Op.i_type:
        states_op = [States.S_EXECUTEL, States.S_ALUWB]

    elif op == Op.jal:
        states_op = [States.S_JAL, States.S_ALUWB]

    elif op == Op.beq:
        states_op = [States.S_BEQ]

    if not reset:
        states = states_base + states_op

    for state in states:
        outputs.append(output_logic(state))

    return states


def alu_control(opb5, funct3, funct7b5, ALUOp):

    if ALUOp == 0:
        return ALUControl.ADD

    elif ALUOp == 1:
        return ALUControl.SUB

    elif ALUOp == 2:
        if funct3 == 0:
            if (
                (opb5 == 0 and funct7b5 == 0)
                or (opb5 == 0 and funct7b5 == 1)
                or (opb5 == 1 and funct7b5 == 0)
            ):
                return ALUControl.ADD

            elif opb5 == 1 and funct7b5 == 1:
                return ALUControl.SUB

        elif funct3 == 1:
            return ALUControl.SLL

        elif funct3 == 2:
            return ALUControl.SLT

        elif funct3 == 6:
            return ALUControl.OR

        elif funct3 == 7:
            return ALUControl.AND

    return ALUControl.X


def pc_write(Zero, Branch, PCUpdate):
    return (Zero & Branch) | PCUpdate


def opb5(op):
    return int(Bits(uint=op, length=7)[1])


def extend(immsrc, instruction, length=32):
    instruction_b = Bits(uint=instruction, length=length)

    if immsrc == 0:
        # i type
        return (Bits(bin=str(int(instruction_b[0])) * 20) + instruction_b[:-20]).uint

    elif immsrc == 1:
        # s type
        return (
            Bits(bin=str(int(instruction_b[0])) * 20)
            + instruction_b[:-25]
            + instruction_b[-12:-7]
        ).uint

    elif immsrc == 2:
        # b type

        return (
            Bits(bin=str(int(instruction_b[0])) * 20)
            + Bits(bin=str(int(instruction_b[-8])))
            + instruction_b[-31:-25]
            + instruction_b[-12:-8]
            + Bits(bin="0")
        ).uint

    elif immsrc == 3:
        # j type
        return (
            Bits(bin=str(int(instruction_b[0])) * 12)
            + instruction_b[-20:-12]
            + Bits(bin=str(int(instruction_b[-21])))
            + instruction_b[-31:-21]
            + Bits(bin="0")
        ).uint

    else:
        return XDEF


def instruction_immext_i(bit_31: int, bits_30_20: int):
    op = Bits(bin=str(0) * 7)
    # bit31_b = Bits(bin=str(bit31) * 20)
    bits_31_20_b = Bits(bin=str(bit_31)) + Bits(bin=str(bits_30_20) * 11)

    # dont cares
    bits_19_7_op = Bits(bin=str(0) * 20)

    instruction = bits_31_20_b + bits_19_7_op
    assert instruction.length == 32

    return instruction.uint


def instruction_immext_s(bit_31: int, bits_30_25: int, bits_11_7: int):
    bits_31_25_b = Bits(bin=str(bit_31)) + Bits(bin=str(bits_30_25) * 6)
    bits_11_7_b = Bits(bin=str(bits_11_7) * 5)

    # dont cares
    op = Bits(bin=str(0) * 7)
    bits_24_12 = Bits(bin=str(0) * 13)

    instruction = bits_31_25_b + bits_24_12 + bits_11_7_b + op
    assert instruction.length == 32

    return instruction.uint


def instruction_immext_b(bit_31: int, bits_30_25: int, bit_7: int, bits_11_8: int):

    bit_31_b = Bits(bin=str(bit_31))
    bits_30_25_b = Bits(bin=str(bits_30_25) * 6)

    bits_11_8_b = Bits(bin=str(bits_11_8) * 4)
    bit_7_b = Bits(bin=str(bit_7))

    # dont cares
    bits_13_24_b = Bits(bin=str(0) * 12)
    op = Bits(bin=str(0) * 7)

    instruction = (
        bit_31_b
        + bits_30_25_b
        + bits_13_24_b
        + Bits(bin=str("0"))
        + bits_11_8_b
        + bit_7_b
        + op
    )
    assert instruction.length == 32

    return instruction.uint


def instruction_immext_j(bit_31: int, bits_30_21: int, bit_20: int, bits_19_12: int):
    bit31_b = Bits(bin=str(bit_31))
    bits_19_12_b = Bits(bin=str(bits_19_12) * 8)

    bit_20_b = Bits(bin=str(bit_20))
    bits_30_21_b = Bits(bin=str(bits_30_21) * 10)

    # dont cares
    bits_11_7_op = Bits(bin=str(0) * 12)

    instruction = bit31_b + bits_30_21_b + bit_20_b + bits_19_12_b + bits_11_7_op
    assert instruction.length == 32

    return instruction.uint


def bitwise_not(value, N):
    return value ^ int("0b" + "1" * N, 2)


def alu(a: int, b: int, alucontrol: ALUControl, N=32):
    zero = 0
    result = 0

    if alucontrol == ALUControl.ADD:
        result = a + b

    elif alucontrol == ALUControl.SUB:
        # subtraction is addition with a and not b and a carry in of 1
        result = int(bin(a + bitwise_not(b, N) + 1), 2)

    elif alucontrol == ALUControl.AND:
        result = a & b

    elif alucontrol == ALUControl.OR:
        result = a | b

    elif alucontrol == ALUControl.SLT:
        result = a < b

    elif alucontrol == ALUControl.SLL:
        result = a << Bits(uint=b, length=N)[-4:].uint

    length = Bits(bin=bin(result)).length
    result = Bits(bin=bin(result))[length - N :].uint

    if result == 0:
        zero = 1

    # cut off overflows : bits in result which are at the N + ith position are ignored
    return result, zero


def flopr(d, reset, init_state=False):
    if init_state:
        if reset == 1:
            return 0

        return XDEF

    else:
        if reset == 1:
            return 0

        else:
            return d


def flopenr(d, en, reset, init_state=False):
    if init_state:
        if reset == 1:
            return 0

        return XDEF

    else:
        if reset == 1:
            return 0

        if en == 0:
            return XDEF
        else:
            return d


def flop(d, init_state=False):
    if init_state:
        return XDEF

    else:
        return d


def mux2(d0, d1, s):
    if s == 0:
        return d0

    elif s == 1:
        return d1

    return XDEF


def mux3(d0, d1, d2, s):
    if s == 0:
        return d0

    elif s == 1:
        return d1

    elif s == 2:
        return d2

    return XDEF


class RegisterFile:
    def __init__(self, size=32):
        self._memory = [0 for i in range(size)]
        self._written_addresses = []
        self._we = 0

    def write(self, a3, data, we):
        self._we = we

        if self._we == 1:
            self._memory[a3] = data
            self._written_addresses.append(a3)

    def _read_address(self, a):

        # hardwired to 0 if a == 0, so a must be a > 0
        if a > 0 and a in self._written_addresses:
            rd = self._memory[a]

        # default value
        else:
            rd = 0

        return rd

    def read_addresses(self, a1, a2):

        rd1 = self._read_address(a1)
        rd2 = self._read_address(a2)

        return rd1, rd2


def get_rs1(instruction):
    return Bits(uint=instruction, length=32)[-20:-15].uint


def get_rs2(instruction):
    return Bits(uint=instruction, length=32)[-25:-20].uint


def get_rd(instruction):
    return Bits(uint=instruction, length=32)[-12:-7].uint


def get_extend_instruction(instruction):
    return Bits(uint=instruction, length=32)[:-7].uint


def get_op(instruction):
    return Bits(uint=instruction, length=32)[-7:].uint


def get_funct3(instruction, N=32):
    return Bits(uint=instruction, length=N)[-15:-12].uint


def get_funct7(instruction, N=32):
    funct7 = Bits(uint=instruction, length=N)[:-25]

    assert funct7.length == 7

    return funct7.uint


def get_funct7b5(instruction, N=32):
    funct7 = get_funct7(instruction, N=N)

    return int(Bits(uint=funct7, length=7)[1])


def instruction_decoder(op):

    if op == Op.lw:
        return ImmSrc.lw

    elif op == Op.sw:
        return ImmSrc.sw

    elif op == Op.r_type:
        return ImmSrc.r_type

    elif op == Op.beq:
        return ImmSrc.beq

    elif op == Op.i_type:
        return ImmSrc.i_type

    elif op == Op.jal:
        return ImmSrc.jal

    else:
        return XDEF


def signExtend(value, length=32):
    return Bits(uint=value, length=length).int
