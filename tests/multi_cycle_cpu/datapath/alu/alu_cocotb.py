import os

import cocotb
from bitstring import Bits
from cocotb.triggers import Timer

from tests.common import check_value
from tests.multi_cycle_cpu.models import alu, alu_flags


def read_vars():
    a = int(os.getenv("a"))
    b = int(os.getenv("b"))
    alucontrol = int(os.getenv("alucontrol"))

    print(
        "a {}\nb {}\nalucontrol {}".format(
            Bits(uint=a, length=32).bin, Bits(uint=b, length=32).bin, alucontrol
        )
    )

    return a, b, alucontrol


async def assign_vars(dut, a, b, alucontrol):
    dut.a.value = a
    dut.b.value = b
    dut.alucontrol.value = alucontrol

    await Timer(1, units="ns")


@cocotb.test()
async def test_alu(dut):
    a, b, alucontrol = read_vars()
    await assign_vars(dut, a, b, alucontrol)

    result, Z = alu(a, b, alucontrol)
    check_value(dut.result, result)
    check_value(dut.Z, Z)


@cocotb.test()
async def test_aluflags_C(dut):
    a, b, alucontrol = read_vars()
    await assign_vars(dut, a, b, alucontrol)

    N, Z, C, V = alu_flags(a, b, alucontrol)

    check_value(dut.C, C)


@cocotb.test()
async def test_aluflags_V(dut):
    a, b, alucontrol = read_vars()
    await assign_vars(dut, a, b, alucontrol)

    N, Z, C, V = alu_flags(a, b, alucontrol)

    check_value(dut.V, V)


@cocotb.test()
async def test_aluflags_N(dut):
    a, b, alucontrol = read_vars()
    await assign_vars(dut, a, b, alucontrol)

    N, Z, C, V = alu_flags(a, b, alucontrol)

    check_value(dut.N, N)


@cocotb.test()
async def test_aluflags_Z(dut):
    a, b, alucontrol = read_vars()
    await assign_vars(dut, a, b, alucontrol)

    N, Z, C, V = alu_flags(a, b, alucontrol)

    check_value(dut.Z, Z)
