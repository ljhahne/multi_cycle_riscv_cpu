import operator

from bitstring import Bits

from tests.common import check_value
from tests.multi_cycle_cpu.defs import XDEF, ALUControl
from tests.multi_cycle_cpu.models import alu_control as alu_decoder
from tests.multi_cycle_cpu.models import (
    extend,
    get_extend_instruction,
    get_funct3,
    get_funct7b5,
    get_op,
    get_rd,
    get_rs1,
    get_rs2,
    opb5,
)


def test_fetch(datapath, instruction, pc=0, oldPC=0):
    check_value(datapath.pcReg.q, pc)
    check_value(datapath.pcReg.d, pc + 4)
    check_value(datapath.pcReg.en, 1)

    check_value(datapath.instructionReg.d1, instruction)
    check_value(datapath.instructionReg.d2, oldPC)
    check_value(datapath.instructionReg.en, 1)

    check_value(datapath.alu.result, pc + 4)

    check_value(datapath.SrcAmux.y, pc)
    check_value(datapath.SrcBmux.y, 4)


def test_decode(datapath, instruction, ImmSrc, pc=0, oldPC=0):
    immext = XDEF
    alu_result = XDEF

    check_value(datapath.pcReg.en, 0)
    check_value(datapath.instructionReg.en, 0)

    check_value(datapath.pcReg.q, pc)
    check_value(datapath.instructionReg.q2, oldPC)
    check_value(datapath.SrcAmux.y, oldPC)

    if ImmSrc != XDEF:
        immext = extend(ImmSrc, instruction)
        check_value(datapath.ext.instr, get_extend_instruction(instruction))
        check_value(datapath.ext.immext, immext)
        check_value(datapath.SrcBmux.y, immext)

    # # register file
    check_value(datapath.registerFile.a1, get_rs1(instruction))
    check_value(datapath.registerFile.a2, get_rs2(instruction))
    check_value(datapath.registerFile.a3, get_rd(instruction))

    # alu
    if immext != XDEF:
        alu_result = oldPC + immext
        check_value(datapath.alu.result, alu_result)
        check_value(datapath.aluOutReg.d, alu_result)

    return immext, alu_result


def test_ExecuteI(datapath, rd1, immext):
    check_value(datapath.SrcAmux.y, rd1)
    check_value(datapath.SrcBmux.y, immext)

    # cast from uint to int
    immext = Bits(uint=immext, length=32).int

    rd1_immext = rd1 + immext

    # alu
    check_value(datapath.alu.result, rd1_immext)
    check_value(datapath.aluOutReg.d, rd1_immext)

    return rd1_immext


def test_aluwb(datapath, value, instruction, registerfile=None):

    check_value(datapath.aluOutReg.q, value)
    check_value(datapath.registerFile.wd3, value)

    if registerfile is not None:
        registerfile[get_rd(instruction)] = value


def test_memadr(datapath, immext, rd1):
    check_value(datapath.alu.a, rd1)
    check_value(datapath.alu.b, immext)


def test_memwrite(datapath, DataAdr, rd2):
    check_value(datapath.DataAdr, DataAdr)
    check_value(datapath.WriteData, rd2)


def test_ExecuteR(datapath, rd1=0, rd2=0):
    check_value(datapath.registerFile.rd1, rd1)
    check_value(datapath.registerFile.rd2, rd2)

    check_value(datapath.rd1rd2Reg.d1, rd1)
    check_value(datapath.rd1rd2Reg.d2, rd2)


def test_ExecuteR_post_edge(datapath, instruction, rd1, rd2):

    # rtype
    aluOP = 0b10

    op = get_op(instruction)
    funct3 = get_funct3(instruction)
    funct7b5 = get_funct7b5(instruction)

    alu_control = alu_decoder(opb5(op), funct3, funct7b5, aluOP)

    if alu_control == ALUControl.ADD:
        op = operator.add

    elif alu_control == ALUControl.SUB:
        op = operator.sub

    elif alu_control == ALUControl.AND:
        op = operator.and_

    elif alu_control == ALUControl.OR:
        op = operator.or_

    elif alu_control == ALUControl.SLT:
        op = operator.lt

    elif alu_control == ALUControl.SLL:
        # use only first 5 bits of b
        op = operator.lshift

    result = op(rd1, rd2)

    check_value(datapath.aluOutReg.q, result)

    return result


def test_jal(datapath, pc, alu_result):
    check_value(datapath.alu.a, pc)
    check_value(datapath.alu.b, 4)
    check_value(datapath.aluOutReg.q, alu_result)


def test_beq(datapath, branch_target_address, rd1, rd2):
    Z = 1 if rd1 - rd2 == 0 else 0
    check_value(datapath.pcReg.d, branch_target_address)
    check_value(datapath.alu.Z, Z)

    return Z


def test_memread(datapath, rd):
    check_value(datapath.dataReg.d, rd)


def test_memwb(datapath, rd):
    check_value(datapath.dataReg.q, rd)
    check_value(datapath.registerFile.wd3, rd)
