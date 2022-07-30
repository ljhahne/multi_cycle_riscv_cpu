import os

import cocotb
from cocotb.triggers import Timer

from tests.common import check_value
from tests.multi_cycle_cpu.models import pc_write


def read_vars():

    funct3 = int(os.getenv("funct3"))
    N = int(os.getenv("N"))
    Z = int(os.getenv("Z"))
    V = int(os.getenv("V"))
    C = int(os.getenv("C"))

    Branch = int(os.getenv("Branch"))
    PCUpdate = int(os.getenv("PCUpdate"))

    print(
        "funct3 {}\nN {}\nZ {}\nV {}\nC {}\nBranch {}\nPCUpdate {}".format(
            funct3, N, Z, V, C, Branch, PCUpdate
        )
    )

    return funct3, N, Z, V, C, Branch, PCUpdate


async def assign_vars(dut, funct3, N, Z, V, C, Branch, PCUpdate):
    dut.funct3.value = funct3
    dut.N.value = N
    dut.Z.value = Z
    dut.V.value = V
    dut.C.value = C
    dut.Branch.value = Branch
    dut.PCUpdate.value = PCUpdate

    await Timer(1, units="ns")


@cocotb.test()
async def test_pc_write(dut):
    funct3, N, Z, V, C, Branch, PCUpdate = read_vars()
    await assign_vars(dut, funct3, N, Z, V, C, Branch, PCUpdate)

    PCWrite = pc_write(funct3, N, Z, C, V, Branch, PCUpdate)

    print("dut.PCWrite {}".format(dut.PCWrite.value))
    check_value(dut.PCWrite, PCWrite)
