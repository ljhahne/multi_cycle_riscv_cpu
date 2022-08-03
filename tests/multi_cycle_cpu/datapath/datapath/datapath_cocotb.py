import operator
import os

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, Timer

from tests.common import check_value
from tests.multi_cycle_cpu.common import datapath_tests, memory_tests, register_tests
from tests.multi_cycle_cpu.common.dut import reset_dut
from tests.multi_cycle_cpu.defs import XDEF, Op, States
from tests.multi_cycle_cpu.models import alu_control as model_alu_control
from tests.multi_cycle_cpu.models import fsm as model_fsm
from tests.multi_cycle_cpu.models import get_rd, get_rs1, get_rs2, opb5, output_logic
from tests.multi_cycle_cpu.models import pc_write as model_pc_write
from tests.multi_cycle_cpu.models import signExtend


async def assign_dut_state(
    dut,
    fsm_state,
    reset,
    op,
    funct3,
    funct7b5,
    ImmSrc,
    ReadData,
    read_data_override=None,
):
    (
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
    ) = output_logic(fsm_state)

    ALUControl = model_alu_control(opb5(op), funct3, funct7b5, aluOP)

    PCWrite = model_pc_write(
        funct3=funct3, N=0, Z=0, C=0, V=0, Branch=Branch, PCUpdate=PCUpdate
    )

    if read_data_override is not None:
        ReadData = read_data_override

    await assign_vars(
        dut,
        reset=0,
        ImmSrc=ImmSrc,
        ALUSrcA=ALUSrcA,
        ALUSrcB=ALUSrcB,
        ResultSrc=ResultSrc,
        AdrSrc=AdrSrc,
        ALUControl=ALUControl,
        IRWrite=IRWrite,
        PCWrite=PCWrite,
        RegWrite=RegWrite,
        ReadData=ReadData,
        propagate=False if reset and fsm_state == States.S_FETCH else True,
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
    ReadData,
    propagate=True,
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
    dut.ReadData.value = ReadData
    # dut.instructionReg.d1.value = instruction

    # if we reset the device first we are already in the fetch state. if we would propagate for an additional t_prop = 1 ns,
    # we would be in an incorrect state

    if propagate:
        await Timer(1, units="ns")


def test_fetch(dut, instruction, pc=0, oldPC=0):
    datapath_tests.test_fetch(dut, instruction, pc=pc, oldPC=oldPC)


def test_decode(dut, ImmSrc, instruction, pc=0, oldPC=0):
    immext, alu_result = datapath_tests.test_decode(
        dut, instruction, ImmSrc, pc=pc, oldPC=oldPC
    )

    return immext, alu_result


def test_memwb(dut, rd):
    datapath_tests.test_memwb(dut, rd)


def test_memadr(dut, immext, rd1=0):
    immext = signExtend(immext)

    datapath_tests.test_memadr(dut, immext, rd1)

    return rd1 + immext


def test_fetch_decode(dut, fsm_state, instruction, ImmSrc, rd1=0, rd2=0, pc=0):

    immext = XDEF
    alu_result = XDEF

    if fsm_state == States.S_FETCH:
        test_fetch(dut, instruction, pc=pc)

    # decode
    elif fsm_state == States.S_DECODE:
        oldPC = pc
        pc += 4
        immext, alu_result = test_decode(dut, ImmSrc, instruction, pc=pc, oldPC=oldPC)

    return immext, alu_result


def test_memread(dut, memory, DataAdr):
    rd = memory_tests.get_rd_from_memory_model(memory, DataAdr)

    # datapath
    datapath_tests.test_memread(dut, rd)

    return rd


def test_beq(dut, branch_target_address, zero):
    check_value(dut.pcReg.q, branch_target_address if zero else 4)
    check_value(dut.alu.zero, zero)


def set_register_content(dut, registerfile, instruction, rd1, rd2):
    dut.registerFile.rf[get_rs1(instruction)].value = rd1
    dut.registerFile.rf[get_rs2(instruction)].value = rd2

    registerfile[get_rs1(instruction)] = rd1
    registerfile[get_rs2(instruction)] = rd2


async def setup_init_state(dut, op, funct3, funct7b5, ImmSrc, instruction):

    # sets control unit to fetch state and performs a reset
    (
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
    ) = output_logic(States.S_FETCH)

    PCWrite = model_pc_write(
        funct3=0, N=0, Z=0, C=0, V=0, Branch=Branch, PCUpdate=PCUpdate
    )
    ALUControl = model_alu_control(opb5(op), funct3, funct7b5, aluOP)

    await assign_vars(
        dut,
        reset=0,
        ImmSrc=ImmSrc,
        ALUSrcA=ALUSrcA,
        ALUSrcB=ALUSrcB,
        ResultSrc=ResultSrc,
        AdrSrc=AdrSrc,
        ALUControl=ALUControl,
        IRWrite=IRWrite,
        PCWrite=PCWrite,
        RegWrite=RegWrite,
        ReadData=instruction,
    )

    await reset_dut(dut)


async def setup_test(dut, period_ns):
    op, funct3, funct7b5, ImmSrc, instruction = read_vars()
    rd1, rd2 = read_rd1_rd2()

    registerfile = [0 for i in range(32)]

    memory = {}
    memory_tests.test_memory(dut, memory)

    set_register_content(dut, registerfile, instruction, rd1, rd2)

    cocotb.start_soon(Clock(dut.clk, period_ns, units="ns").start())

    await setup_init_state(dut, op, funct3, funct7b5, ImmSrc, instruction)

    register_tests.test_register_file(dut, registerfile)

    fsm_states = model_fsm(op=op, reset=0)

    pc = 0
    reset = True

    return (
        op,
        funct3,
        funct7b5,
        ImmSrc,
        instruction,
        registerfile,
        memory,
        fsm_states,
        pc,
        reset,
    )


@cocotb.test()
async def test_j_instruction(dut, period_ns=1):
    (
        op,
        funct3,
        funct7b5,
        ImmSrc,
        instruction,
        registerfile,
        memory,
        fsm_states,
        pc,
        reset,
    ) = await setup_test(dut, period_ns)

    alu_result = XDEF

    for fsm_state in fsm_states:
        await assign_dut_state(
            dut, fsm_state, reset, op, funct3, funct7b5, ImmSrc, instruction
        )

        if fsm_state == States.S_FETCH or fsm_state == States.S_DECODE:
            _, alu_result = test_fetch_decode(
                dut, fsm_state, instruction, ImmSrc, pc=pc
            )

        elif fsm_state == States.S_JAL:
            datapath_tests.test_jal(dut, pc, alu_result)

        # # aluwb
        elif fsm_state == States.S_ALUWB:
            datapath_tests.test_aluwb(dut, pc + 4, instruction, registerfile)

        await RisingEdge(dut.clk)
        await Timer(1, units="ns")


@cocotb.test()
async def test_lui_instruction(dut, period_ns=1):
    (
        op,
        funct3,
        funct7b5,
        ImmSrc,
        instruction,
        registerfile,
        memory,
        fsm_states,
        pc,
        reset,
    ) = await setup_test(dut, period_ns)

    immext = XDEF

    for fsm_state in fsm_states:
        await assign_dut_state(
            dut, fsm_state, reset, op, funct3, funct7b5, ImmSrc, instruction
        )

        if fsm_state == States.S_FETCH or fsm_state == States.S_DECODE:
            print("DEBUG immsrc {}".format(ImmSrc))
            immext, _ = test_fetch_decode(dut, fsm_state, instruction, ImmSrc, pc=pc)

        elif fsm_state == States.S_U:

            datapath_tests.test_lui(dut, immext)

        # aluwb
        elif fsm_state == States.S_ALUWB:
            datapath_tests.test_aluwb(dut, immext, instruction, registerfile)

        await RisingEdge(dut.clk)
        await Timer(1, units="ns")


@cocotb.test()
async def test_r_instruction(dut, period_ns=1):
    (
        op,
        funct3,
        funct7b5,
        ImmSrc,
        instruction,
        registerfile,
        memory,
        fsm_states,
        pc,
        reset,
    ) = await setup_test(dut, period_ns)

    rd1 = registerfile[get_rs1(instruction)]
    rd2 = registerfile[get_rs2(instruction)]

    for fsm_state in fsm_states:
        await assign_dut_state(
            dut, fsm_state, reset, op, funct3, funct7b5, ImmSrc, instruction
        )

        if fsm_state == States.S_FETCH or fsm_state == States.S_DECODE:
            immext, _ = test_fetch_decode(
                dut, fsm_state, instruction, ImmSrc, rd1=rd1, pc=pc
            )

        elif fsm_state == States.S_EXECUTER:
            datapath_tests.test_ExecuteR(dut, rd1=rd1, rd2=rd2)

        elif fsm_state == States.S_ALUWB:
            result = datapath_tests.test_ExecuteR_post_edge(dut, instruction, rd1, rd2)
            datapath_tests.test_aluwb(dut, result, instruction)

        await RisingEdge(dut.clk)
        await Timer(1, units="ns")


@cocotb.test()
async def test_lw_instruction(dut, period_ns=1):
    (
        op,
        funct3,
        funct7b5,
        ImmSrc,
        instruction,
        registerfile,
        memory,
        fsm_states,
        pc,
        reset,
    ) = await setup_test(dut, period_ns)

    rd1 = registerfile[get_rs1(instruction)]

    immext = XDEF
    DataAdr = XDEF
    rd = XDEF

    for fsm_state in fsm_states:

        if fsm_state == States.S_MEMREAD:
            # cannot be tested. Read from dummy memory instead
            if DataAdr in list(memory.keys()):
                rd = memory[DataAdr]
            else:
                rd = 0

        await assign_dut_state(
            dut,
            fsm_state,
            reset,
            op,
            funct3,
            funct7b5,
            ImmSrc,
            rd
            if fsm_state == States.S_MEMREAD or fsm_state == States.S_MEMWB
            else instruction,
        )

        if fsm_state == States.S_FETCH or fsm_state == States.S_DECODE:
            immext, _ = test_fetch_decode(
                dut, fsm_state, instruction, ImmSrc, rd1=rd1, pc=pc
            )

        elif fsm_state == States.S_MEMADR:
            DataAdr = test_memadr(dut, immext, rd1)

        elif fsm_state == States.S_MEMREAD:
            datapath_tests.test_memread(dut, rd)

        elif fsm_state == States.S_MEMWB:
            test_memwb(dut, rd)
            registerfile[get_rd(instruction)] = rd

        await RisingEdge(dut.clk)
        await Timer(1, units="ns")


@cocotb.test()
async def test_sw_instruction(dut, period_ns=1):
    (
        op,
        funct3,
        funct7b5,
        ImmSrc,
        instruction,
        registerfile,
        memory,
        fsm_states,
        pc,
        reset,
    ) = await setup_test(dut, period_ns)

    rd1 = registerfile[get_rs1(instruction)]
    rd2 = registerfile[get_rs2(instruction)]

    immext = XDEF
    DataAdr = XDEF

    for fsm_state in fsm_states:

        await assign_dut_state(
            dut, fsm_state, reset, op, funct3, funct7b5, ImmSrc, instruction
        )

        if fsm_state == States.S_FETCH or fsm_state == States.S_DECODE:
            immext, _ = test_fetch_decode(
                dut, fsm_state, instruction, ImmSrc, rd1=rd1, pc=pc
            )

        elif fsm_state == States.S_MEMADR:
            DataAdr = test_memadr(dut, immext, rd1=rd1)

        elif fsm_state == States.S_MEMWRITE:
            datapath_tests.test_memwrite(dut, DataAdr, rd2)
            memory[DataAdr] = rd2

        await RisingEdge(dut.clk)
        await Timer(1, units="ns")


@cocotb.test()
async def test_b_instruction(dut, period_ns=1):
    (
        op,
        funct3,
        funct7b5,
        ImmSrc,
        instruction,
        registerfile,
        memory,
        fsm_states,
        pc,
        reset,
    ) = await setup_test(dut, period_ns)

    rd1 = registerfile[get_rs1(instruction)]
    rd2 = registerfile[get_rs2(instruction)]

    alu_result = XDEF

    for fsm_state in fsm_states:

        await assign_dut_state(
            dut,
            fsm_state,
            reset,
            op,
            funct3,
            funct7b5,
            ImmSrc,
            instruction,
        )

        if fsm_state == States.S_FETCH or fsm_state == States.S_DECODE:
            _, alu_result = test_fetch_decode(
                dut, fsm_state, instruction, ImmSrc, rd1=rd1, pc=pc
            )

        elif fsm_state == States.S_BEQ:
            datapath_tests.test_b_instructions(dut, alu_result, rd1, rd2)

        await RisingEdge(dut.clk)
        await Timer(1, units="ns")


@cocotb.test()
async def test_i_instruction(dut, period_ns=1):
    (
        op,
        funct3,
        funct7b5,
        ImmSrc,
        instruction,
        registerfile,
        memory,
        fsm_states,
        pc,
        reset,
    ) = await setup_test(dut, period_ns)
    rd1 = registerfile[get_rs1(instruction)]

    immext = XDEF
    rd1_immext = XDEF

    for fsm_state in fsm_states:

        await assign_dut_state(
            dut, fsm_state, reset, op, funct3, funct7b5, ImmSrc, instruction
        )

        if fsm_state == States.S_FETCH or fsm_state == States.S_DECODE:
            immext, _ = test_fetch_decode(
                dut, fsm_state, instruction, ImmSrc, rd1=rd1, pc=pc
            )

        elif fsm_state == States.S_EXECUTEL:
            print("rd1 {}".format(rd1))
            rd1_immext = datapath_tests.test_ExecuteI(dut, rd1, immext)

        elif fsm_state == States.S_ALUWB:
            datapath_tests.test_aluwb(dut, rd1_immext, instruction)

        await RisingEdge(dut.clk)
        await Timer(1, units="ns")
