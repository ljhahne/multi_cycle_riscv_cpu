import operator
import os

import cocotb
from bitstring import Bits
from cocotb.clock import Clock
from cocotb.triggers import Timer

from tests.common import check_value
from tests.multi_cycle_cpu import models
from tests.multi_cycle_cpu.defs import Loadtype


def read_vars():
    ReadData = int(os.getenv("ReadData"))

    return ReadData


async def assign_vars(dut, ReadData, LoadType):
    dut.ReadData.value = ReadData
    dut.loadtype.value = LoadType

    await Timer(1, units="ns")


@cocotb.test()
async def test_lb(dut):
    ReadData = read_vars()
    loadtype = Loadtype.lb
    await assign_vars(dut, ReadData, LoadType=loadtype)

    Data = models.load_extend(ReadData, loadtype)
    check_value(dut.Data, Data)


@cocotb.test()
async def test_lh(dut):
    ReadData = read_vars()
    loadtype = Loadtype.lh
    await assign_vars(dut, ReadData, LoadType=loadtype)

    Data = models.load_extend(ReadData, loadtype)

    check_value(dut.Data, Data)


@cocotb.test()
async def test_lbu(dut):
    ReadData = read_vars()

    loadtype = Loadtype.lbu

    await assign_vars(dut, ReadData, LoadType=loadtype)

    Data = models.load_extend(ReadData, loadtype)

    check_value(dut.Data, Data)


@cocotb.test()
async def test_lhu(dut):
    ReadData = read_vars()
    loadtype = Loadtype.lhu

    await assign_vars(dut, ReadData, LoadType=loadtype)

    Data = models.load_extend(ReadData, loadtype)

    check_value(dut.Data, Data)


@cocotb.test()
async def test_lw(dut):
    ReadData = read_vars()
    loadtype = Loadtype.lw
    await assign_vars(dut, ReadData, LoadType=loadtype)

    Data = models.load_extend(ReadData, loadtype)

    check_value(dut.Data, Data)
