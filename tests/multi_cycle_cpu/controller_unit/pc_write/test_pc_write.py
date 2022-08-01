import os

import pytest

from tests import instructions
from tests.setup_tests import Config, init_waveforms, run_simulation

toplevel = "pc_write"

config = Config(
    HDLFILES=["src/multi_cycle_cpu/controller/pc_write.sv"],
    TOPLEVEL=toplevel,
    WORK_DIR="src/multi_cycle_cpu/controller",
    TEST_DIR="tests/multi_cycle_cpu/controller_unit/pc_write",
)

init_waveforms(config)


def set_signals(Op, N, Z, C, V, Branch, PCUpdate):

    if not isinstance(Op, int):
        op = Op(0, 0, 0)
        funct3 = op.get_funct3()

    else:
        # only for illegal state
        funct3 = Op

    return {
        "funct3": str(funct3),
        "N": str(N),
        "Z": str(Z),
        "V": str(V),
        "C": str(C),
        "Branch": str(Branch),
        "PCUpdate": str(PCUpdate),
    }


waveform_file = "instruction_decoder_op_{}_Z_{}_C_{}_V_{}_Branch_{}_PCUpdate_{}.vcd"


# funct3 = 0b11 does not exist for b type instructions
@pytest.mark.parametrize("op", [*instructions.b_instructions, 0b11])
@pytest.mark.parametrize("N", [0, 1])
@pytest.mark.parametrize("Z", [0, 1])
@pytest.mark.parametrize("C", [0, 1])
@pytest.mark.parametrize("V", [0, 1])
@pytest.mark.parametrize("Branch", [1])
@pytest.mark.parametrize("PCUpdate", [0])
def test_alu_branch(op, N, Z, C, V, Branch, PCUpdate):
    run_simulation(
        config,
        "test_{}".format(toplevel),
        waveform_file,
        set_signals(op, N, Z, C, V, Branch, PCUpdate),
    )


@pytest.mark.parametrize("Branch", [0, 1])
@pytest.mark.parametrize("PCUpdate", [0, 1])
def test_branch_pcupdate(Branch, PCUpdate):
    run_simulation(
        config,
        "test_{}".format(toplevel),
        waveform_file,
        set_signals(
            Op=instructions.sb_instruction.BEQop,
            N=0,
            Z=1,
            C=0,
            V=0,
            Branch=Branch,
            PCUpdate=PCUpdate,
        ),
    )
