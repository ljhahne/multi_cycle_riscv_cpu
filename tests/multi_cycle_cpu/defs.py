from dataclasses import dataclass

XDEF = -1


@dataclass(frozen=True)
class Op:
    r_type = 0b0110011
    i_type = 0b0010011
    lw = 0b0000011
    sw = 0b0100011
    beq = 0b1100011
    jal = 0b1101111
    # default requires only to be different than ops above
    default = 0b1111111

    def get_all(self):
        return [
            self.r_type,
            self.i_type,
            self.lw,
            self.sw,
            self.beq,
            self.jal,
            self.default,
        ]


@dataclass(frozen=True)
class ImmSrc:
    i_type = 0b00
    lw = 0b00
    sw = 0b01
    beq = 0b10
    jal = 0b11
    default = XDEF
    r_type = XDEF


@dataclass(frozen=True)
class States:
    S_FETCH = 0
    S_DECODE = 1
    S_MEMADR = 2
    S_MEMREAD = 3
    S_MEMWB = 4
    S_MEMWRITE = 5
    S_EXECUTER = 6
    S_EXECUTEL = 7
    S_ALUWB = 8
    S_BEQ = 9
    S_JAL = 10

    def get_all(self):
        return [
            self.S_FETCH,
            self.S_DECODE,
            self.S_MEMADR,
            self.S_MEMREAD,
            self.S_MEMWB,
            self.S_MEMWRITE,
            self.S_EXECUTER,
            self.S_EXECUTEL,
            self.S_ALUWB,
            self.S_BEQ,
            self.S_JAL,
        ]


@dataclass(frozen=True)
class ALUControl:
    ADD = 0
    SUB = 1
    AND = 2
    OR = 3
    SLT = 5
    SLL = 6
    X = XDEF
