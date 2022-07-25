import os

from cocotb.triggers import Timer

import cocotb
from tests.multi_cycle_cpu.models import pc_write as model


def read_vars():
    Zero = int(os.getenv("Zero"))
    Branch = int(os.getenv("Branch"))
    PCUpdate = int(os.getenv("PCUpdate"))

    print("Zero {}\nBranch {}\nPCUpdate {}".format(Zero, Branch, PCUpdate))

    return Zero, Branch, PCUpdate


async def assign_vars(dut, Zero, Branch, PCUpdate):
    dut.Zero.value = Zero
    dut.Branch.value = Branch
    dut.PCUpdate.value = PCUpdate

    await Timer(1, units="ns")


@cocotb.test()
async def test_pc_write(dut):
    Zero, Branch, PCUpdate = read_vars()
    await assign_vars(dut, Zero, Branch, PCUpdate)

    assert dut.PCWrite.value == model(
        Zero, Branch, PCUpdate
    ), "dut.PCWrite.value {} expected {}".format(
        dut.PCWrite.value, model(Zero, Branch, PCUpdate)
    )
