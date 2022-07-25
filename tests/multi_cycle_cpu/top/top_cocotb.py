import operator
import os

from bitstring import Bits
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, Timer

import cocotb
from tests.common import check_value
from tests.multi_cycle_cpu.common import datapath_tests, memory_tests, register_tests
from tests.multi_cycle_cpu.common.dut import reset_dut
from tests.multi_cycle_cpu.defs import Op
from tests.multi_cycle_cpu.models import (
    get_op,
    get_rd,
    get_rs1,
    get_rs2,
    instruction_decoder,
    signExtend,
)


def read_vars():
    op = int(os.getenv("op"))

    funct3 = int(os.getenv("funct3"))

    funct7b5 = int(os.getenv("funct7b5"))

    ImmSrc = int(os.getenv("ImmSrc"))

    instruction = int(os.getenv("instruction"))

    return op, funct3, funct7b5, ImmSrc, instruction


def read_rd1_rd2():
    rd1 = int(os.getenv("rd1"))
    rd2 = int(os.getenv("rd2"))

    return rd1, rd2


async def assign_vars(
    dut,
    reset,
    ImmSrc,
    ALUSrcA,
    ALUSrcB,
    ResultSrc,
    AdrSrc,
    ALUControl,
    IRWrite,
    PCWrite,
    RegWrite,
    instruction,
):

    dut.reset.value = reset
    dut.ImmSrc.value = ImmSrc
    dut.ALUSrcA.value = ALUSrcA
    dut.ALUSrcB.value = ALUSrcB
    dut.ResultSrc.value = ResultSrc
    dut.AdrSrc.value = AdrSrc
    dut.ALUControl.value = ALUControl
    dut.IRWrite.value = IRWrite
    dut.PCWrite.value = PCWrite
    dut.RegWrite.value = RegWrite
    dut.ReadData.value = instruction
    dut.instructionReg.d1.value = instruction

    await Timer(1, units="ns")


def test_fetch(dut, instruction, pc=0, oldPC=0):
    datapath = dut.rvmulti.dp
    control_unit = dut.rvmulti.riscvcontroller

    # control unit
    check_value(control_unit.AdrSrc, 0)
    check_value(control_unit.IRWrite, 1)
    check_value(control_unit.ALUSrcA, 0)
    check_value(control_unit.ALUSrcB, 0b10)
    check_value(control_unit.aluOP, 0)
    check_value(control_unit.ResultSrc, 0b10)
    check_value(control_unit.PCUpdate, 1)

    # datapath
    datapath_tests.test_fetch(datapath, instruction, pc=pc, oldPC=oldPC)


def test_decode(dut, instruction, pc=0, oldPC=0):
    datapath = dut.rvmulti.dp
    control_unit = dut.rvmulti.riscvcontroller

    ImmSrc = instruction_decoder(get_op(instruction))

    # control unit
    check_value(control_unit.ALUSrcA, 1)
    check_value(control_unit.ALUSrcB, 1)
    check_value(control_unit.aluOP, 0)
    check_value(control_unit.ImmSrc, ImmSrc)

    # datapath
    # check_value(datapath.pcReg.q, pc)
    # check_value(datapath.instructionReg.q2, oldPC)
    # check_value(datapath.SrcAmux.y, oldPC)
    #
    # if ImmSrc != XDEF:
    #     immext = extend(ImmSrc, instruction)
    #     check_value(datapath.ext.instr, get_extend_instruction(instruction))
    #     check_value(datapath.ext.immext, immext)
    #     check_value(datapath.SrcBmux.y, immext)
    #
    # # # register file
    # check_value(datapath.registerFile.a1, get_rs1(instruction))
    # check_value(datapath.registerFile.a2, get_rs2(instruction))
    # check_value(datapath.registerFile.a3, get_rd(instruction))
    #
    # # alu
    # if immext != XDEF:
    #     alu_result = oldPC + immext
    #     check_value(datapath.alu.result, alu_result)
    #     check_value(datapath.aluOutReg.d, alu_result)

    immext, alu_result = datapath_tests.test_decode(
        datapath, instruction, ImmSrc, pc=pc, oldPC=oldPC
    )

    return immext, alu_result


def test_ExecuteI(dut, immext, rd1=0):
    datapath = dut.rvmulti.dp
    control_unit = dut.rvmulti.riscvcontroller

    # control unit
    check_value(control_unit.ALUSrcA, 0b10)
    check_value(control_unit.ALUSrcB, 1)
    check_value(control_unit.aluOP, 0b10)

    # datapath

    # test_ExecuteI(datapath, rd1, immext)
    #
    # check_value(datapath.SrcAmux.y, rd1)
    # check_value(datapath.SrcBmux.y, immext)
    #
    # # cast from uint to int
    # immext = Bits(uint=immext, length=32).int
    #
    # rd1_immext = rd1 + immext
    #
    # # alu
    # check_value(datapath.alu.result, rd1_immext)
    # check_value(datapath.aluOutReg.d, rd1_immext)

    rd1_immext = datapath_tests.test_ExecuteI(datapath, rd1, immext)

    return rd1_immext


def test_aluwb(dut, value, instruction, registerfile):
    datapath = dut.rvmulti.dp
    control_unit = dut.rvmulti.riscvcontroller

    # control unit
    check_value(control_unit.ResultSrc, 0)
    check_value(control_unit.RegWrite, 1)

    datapath_tests.test_aluwb(datapath, value, instruction, registerfile=registerfile)


def read_instructions():
    with open("riscvtest.txt", "r") as file:
        instructions = [int(line.splitlines()[0], 16) for line in file.readlines()]

    return instructions


async def test_fetch_decode(dut, pc, instruction):
    oldPC = pc

    test_fetch(dut, instruction, pc=pc, oldPC=oldPC)

    await RisingEdge(dut.clk)
    await Timer(1, units="ns")

    # pc update
    pc += 4

    immext, alu_result = test_decode(dut, instruction, pc=pc, oldPC=oldPC)

    await RisingEdge(dut.clk)
    await Timer(1, units="ns")

    return immext, alu_result


async def test_i_type(dut, instruction, registerfile, immext):
    rd1 = registerfile[get_rs1(instruction)]

    rd1_immext = test_ExecuteI(dut, immext, rd1=rd1)

    await RisingEdge(dut.clk)
    await Timer(1, units="ns")

    test_aluwb(dut, rd1_immext, instruction, registerfile)

    await RisingEdge(dut.clk)
    await Timer(1, units="ns")


def test_ExecuteR(dut, rd1=0, rd2=0):
    datapath = dut.rvmulti.dp
    control_unit = dut.rvmulti.riscvcontroller

    # control unit
    check_value(control_unit.ALUSrcA, 0b10)
    check_value(control_unit.ALUSrcB, 0)
    check_value(control_unit.aluOP, 0b10)

    # datapath
    datapath_tests.test_ExecuteR(datapath, rd1=rd1, rd2=rd2)


async def test_r_type(dut, instruction, registerfile):
    rd1 = registerfile[get_rs1(instruction)]
    rd2 = registerfile[get_rs2(instruction)]

    test_ExecuteR(dut, rd1, rd2)

    await RisingEdge(dut.clk)
    await Timer(1, units="ns")

    result = datapath_tests.test_ExecuteR_post_edge(
        dut.rvmulti.dp, instruction, rd1, rd2
    )
    test_aluwb(dut, result, instruction, registerfile)

    await RisingEdge(dut.clk)
    await Timer(1, units="ns")


def test_beq_state(dut, branch_target_address, rd1, rd2):
    control_unit = dut.rvmulti.riscvcontroller
    datapath = dut.rvmulti.dp

    # control unit
    check_value(control_unit.ALUSrcA, 0b10)
    check_value(control_unit.ALUSrcB, 0)
    check_value(control_unit.aluOP, 1)
    check_value(control_unit.ResultSrc, 0)
    check_value(control_unit.Branch, 1)

    # datapath
    zero = datapath_tests.test_beq(datapath, branch_target_address, rd1, rd2)

    return zero


def test_memadr(dut, immext, rd1):
    control_unit = dut.rvmulti.riscvcontroller
    datapath = dut.rvmulti.dp

    # control unit
    check_value(control_unit.ALUSrcA, 0b10)
    check_value(control_unit.ALUSrcB, 1)
    check_value(control_unit.aluOP, 0)

    immext = signExtend(immext)

    # datapath
    check_value(datapath.alu.a, rd1)
    check_value(datapath.alu.b, immext)

    datapath_tests.test_memadr(datapath, immext, rd1)

    return rd1 + immext


def test_memwrite(dut, DataAdr, rd2):
    control_unit = dut.rvmulti.riscvcontroller

    # control unit
    check_value(control_unit.ResultSrc, 0)
    check_value(control_unit.AdrSrc, 1)
    check_value(control_unit.MemWrite, 1)

    # memory
    assert DataAdr % 4 == 0
    check_value(dut.memory.a, DataAdr)
    check_value(dut.memory.wd, rd2)


async def test_sw(dut, instruction, registerfile, memory, immext):
    rd1 = registerfile[get_rs1(instruction)]
    rd2 = registerfile[get_rs2(instruction)]

    DataAdr = test_memadr(dut, immext, rd1)

    await RisingEdge(dut.clk)
    await Timer(1, units="ns")

    test_memwrite(dut, DataAdr, rd2)
    memory[DataAdr] = rd2

    await RisingEdge(dut.clk)
    await Timer(1, units="ns")


async def test_beq(dut, instruction, registerfile, alu_result):
    rd1 = registerfile[get_rs1(instruction)]
    rd2 = registerfile[get_rs2(instruction)]

    zero = test_beq_state(dut, alu_result, rd1, rd2)

    await RisingEdge(dut.clk)
    await Timer(1, units="ns")

    return alu_result, zero


def test_memread(dut, memory_model, DataAdr):
    control_unit = dut.rvmulti.riscvcontroller
    datapath = dut.rvmulti.dp
    memory = dut.memory

    # control unit
    check_value(control_unit.ResultSrc, 0)
    check_value(control_unit.AdrSrc, 1)

    # if DataAdr in list(memory_model.keys()):
    #     rd = memory_model[DataAdr]
    #
    # else:
    #     rd = 0

    rd = memory_tests.get_rd_from_memory_model(memory_model, DataAdr)

    # memory
    memory_tests.test_memread(memory, rd)

    # datapath
    datapath_tests.test_memread(datapath, rd)

    return rd


def test_memwb(dut, registerfile, instruction, rd):
    control_unit = dut.rvmulti.riscvcontroller
    datapath = dut.rvmulti.dp

    # control unit
    check_value(control_unit.ResultSrc, 1)
    check_value(control_unit.RegWrite, 1)

    # datapath
    datapath_tests.test_memwb(datapath, rd)

    registerfile[get_rd(instruction)] = rd


async def test_lw(dut, instruction, registerfile, memory, immext):
    rd1 = registerfile[get_rs1(instruction)]

    DataAdr = test_memadr(dut, immext, rd1)

    await RisingEdge(dut.clk)
    await Timer(1, units="ns")

    rd = test_memread(dut, memory, DataAdr)

    await RisingEdge(dut.clk)
    await Timer(1, units="ns")

    test_memwb(dut, registerfile, instruction, rd)

    await RisingEdge(dut.clk)
    await Timer(1, units="ns")


def test_jal_state(dut, pc, alu_result):
    control_unit = dut.rvmulti.riscvcontroller
    datapath = dut.rvmulti.dp

    # control unit
    check_value(control_unit.ALUSrcA, 1)
    check_value(control_unit.ALUSrcB, 0b10)
    check_value(control_unit.aluOP, 0)
    check_value(control_unit.ResultSrc, 0)
    check_value(control_unit.PCUpdate, 1)

    # datapath
    datapath_tests.test_jal(datapath, pc, alu_result)


async def test_jal(dut, pc, instruction, registerfile, alu_result):

    test_jal_state(dut, pc, alu_result)

    await RisingEdge(dut.clk)
    await Timer(1, units="ns")

    test_aluwb(dut, pc + 4, instruction, registerfile)

    await RisingEdge(dut.clk)
    await Timer(1, units="ns")

    return alu_result


@cocotb.test()
async def test_cpu(dut, period_ns=1):

    # TODO BEFORE EACH FETCH CHECK REGISTER

    registerfile = [0 for i in range(32)]

    instructions = read_instructions()

    cocotb.start_soon(Clock(dut.clk, period_ns, units="ns").start())

    pc = 0

    await reset_dut(dut)

    bta = 0
    zero = 0
    jadr = 0

    memory = {}

    for i in range(30):

        # make sure cpu is byte addressable
        assert pc % 4 == 0

        instruction = instructions[int(pc / 4)]
        print("pc {} instruction {} : {}".format(hex(pc), i + 1, hex(instruction)))
        op = get_op(instruction)
        register_tests.test_register_file(dut.rvmulti.dp, registerfile)
        memory_tests.test_memory(dut, memory)

        immext, alu_result = await test_fetch_decode(dut, pc, instruction)

        if op == Op.r_type:
            await test_r_type(dut, instruction, registerfile)

        elif op == Op.sw:
            await test_sw(dut, instruction, registerfile, memory, immext)

        elif op == Op.beq:
            bta, zero = await test_beq(dut, instruction, registerfile, alu_result)

        elif op == Op.i_type:
            await test_i_type(dut, instruction, registerfile, immext)

        elif op == Op.jal:
            jadr = await test_jal(dut, pc, instruction, registerfile, alu_result)

        if op == Op.lw:
            await test_lw(dut, instruction, registerfile, memory, immext)

        # uodate pc
        if op == Op.beq and zero:
            pc = bta

        elif op == Op.jal:
            pc = jadr

        else:
            pc += 4

        i += 1
