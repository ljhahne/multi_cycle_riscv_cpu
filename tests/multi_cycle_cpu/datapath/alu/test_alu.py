import os
import random

import pytest
from bitstring import Bits

from tests.instructions import *
from tests.multi_cycle_cpu.defs import ALUControl
from tests.setup_tests import Config, init_waveforms, run_simulation

config = Config(
    HDLFILES=[
        "src/multi_cycle_cpu/datapath/alu.sv",
        "src/multi_cycle_cpu/datapath/aluflags.sv",
    ],
    TOPLEVEL="alu",
    WORK_DIR="src/multi_cycle_cpu/datapath/",
    TEST_DIR="tests/multi_cycle_cpu/datapath/alu",
)

init_waveforms(config)

waveform_file = "alu_a_{}_b_{}_alucontrol_{}.vcd"


def set_signals(a, b, alucontrol):

    return {"a": str(a), "b": str(b), "alucontrol": str(alucontrol)}


# overflow, underflow, -1 + 1, -1 + -1, 1 + 1
@pytest.mark.parametrize(
    "a, b",
    [
        (0b01111111111111111111111111111111, 0b1),
        (0b10000000000000000000000000000000, 0b11111111111111111111111111111111),
        (0b11111111111111111111111111111111, 0b1),
        (0b11111111111111111111111111111111, 0b11111111111111111111111111111111),
        (0b1, 0b1),
    ],
)
def test_add(a, b):
    run_simulation(config, "test_alu", waveform_file, set_signals(a, b, ALUControl.ADD))


# overflow, underflow, -1 - 1, -1 - -1, 1 - 1
@pytest.mark.parametrize(
    "a, b",
    [
        (0b01111111111111111111111111111111, 0b11111111111111111111111111111111),
        (0b10000000000000000000000000000000, 0b1),
        (0b1, 0b11111111111111111111111111111111),
        (0b11111111111111111111111111111111, 0b11111111111111111111111111111111),
        (0b1, 0b1),
    ],
)
def test_sub(a, b):
    run_simulation(config, "test_alu", waveform_file, set_signals(a, b, ALUControl.SUB))


@pytest.mark.parametrize("a", [0, 0b11111111111111111111111111111111])
@pytest.mark.parametrize("b", [0, 0b11111111111111111111111111111111])
def test_and(a, b):
    run_simulation(config, "test_alu", waveform_file, set_signals(a, b, ALUControl.AND))


@pytest.mark.parametrize("a", [0, 0b11111111111111111111111111111111])
@pytest.mark.parametrize("b", [0, 0b11111111111111111111111111111111])
def test_or(a, b):
    run_simulation(config, "test_alu", waveform_file, set_signals(a, b, ALUControl.OR))


@pytest.mark.parametrize("a,b", [(0, 1), (1, 0)])
def test_or(a, b):
    run_simulation(config, "test_alu", waveform_file, set_signals(a, b, ALUControl.SLT))


@pytest.mark.parametrize(
    "a,b", [(1, 0b1111), (1, 0), (0b11110000000000000000000000000000, 0b1111)]
)
def test_sll(a, b):
    run_simulation(config, "test_alu", waveform_file, set_signals(a, b, ALUControl.SLL))


@pytest.mark.parametrize("op", [ALUControl.ADD])
@pytest.mark.parametrize(
    "a,b",
    [
        (0b11111111111111111111111111111111, 0b1),
        (0b01111111111111111111111111111111, 0b1),
    ],
)
def test_C(a, b, op):
    run_simulation(config, "test_aluflags_C", waveform_file, set_signals(a, b, op))


@pytest.mark.parametrize("op", [ALUControl.ADD])
@pytest.mark.parametrize("a", [0b11111111111111111111111111111111, 0b1])
@pytest.mark.parametrize("b", [0b11111111111111111111111111111111, 0b1])
def test_V(a, b, op):
    run_simulation(config, "test_aluflags_V", waveform_file, set_signals(a, b, op))


@pytest.mark.parametrize("op", [ALUControl.ADD])
@pytest.mark.parametrize(
    "a, b",
    [
        (0b01111111111111111111111111111111, 0b1),
        (0b01111111111111111111111111111110, 0b1),
    ],
)
def test_N(a, b, op):
    run_simulation(config, "test_aluflags_N", waveform_file, set_signals(a, b, op))


@pytest.mark.parametrize("a, b", [(0b1, 0b1), (0b1, 0b10), (0b10, 0b1)])
def test_Z(a, b):
    run_simulation(
        config, "test_aluflags_Z", waveform_file, set_signals(a, b, ALUControl.SUB)
    )
