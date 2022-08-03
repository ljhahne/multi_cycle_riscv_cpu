import os
import random

import pytest

from tests.multi_cycle_cpu.defs import ALUControl, ALUop
from tests.setup_tests import Config, init_waveforms, run_simulation

config = Config(
    HDLFILES=["src/multi_cycle_cpu/controller/alu_decoder.sv"],
    TOPLEVEL="alu_decoder",
    WORK_DIR="src/multi_cycle_cpu/controller/",
    TEST_DIR="tests/multi_cycle_cpu/controller_unit/alu_decoder",
)

init_waveforms(config)


def set_signals(request, instruction):
    return {
        "ALUOp": str(request.param[0]),
        "funct3": str(request.param[1]),
        "opb5": str(request.param[2]),
        "funct7b5": str(request.param[3]),
        "instruction": str(instruction),
    }


@pytest.fixture(
    params=[(ALUop.U, random.randint(0, 7), random.randint(0, 1), random.randint(0, 1))]
)
def signals_lui(request):
    return set_signals(request, ALUControl.LUI)


@pytest.fixture(
    params=[
        (ALUop.ADD, random.randint(0, 7), random.randint(0, 1), random.randint(0, 1)),
        (2, 0, 0, 0),
        (2, 0, 0, 1),
        (2, 0, 1, 0),
    ]
)
def signals_add(request):
    return set_signals(request, ALUControl.ADD)


@pytest.fixture(
    params=[
        (ALUop.SUB, random.randint(0, 7), random.randint(0, 1), random.randint(0, 1)),
        (2, 0, 1, 1),
    ]
)
def signals_sub(request):
    return set_signals(request, ALUControl.SUB)


@pytest.fixture(params=[(ALUop.RI_TYPE, 7, random.randint(0, 1), random.randint(0, 1))])
def signals_and(request):
    return set_signals(request, ALUControl.AND)


@pytest.fixture(params=[(ALUop.RI_TYPE, 6, random.randint(0, 1), random.randint(0, 1))])
def signals_or(request):
    return set_signals(request, ALUControl.OR)


@pytest.fixture(params=[(ALUop.RI_TYPE, 2, random.randint(0, 1), random.randint(0, 1))])
def signals_slt(request):
    return set_signals(request, ALUControl.SLT)


@pytest.fixture(params=[(ALUop.RI_TYPE, 1, random.randint(0, 1), random.randint(0, 1))])
def signals_sll(request):
    return set_signals(request, ALUControl.SLL)


waveform_file = "ALUOp_{}_funct3_{}opb5_{}_funct7b5_{}_instruction_{}.vcd"


def test_aludecoder_sll(signals_sll):
    run_simulation(config, "test_aludecoder", waveform_file, signals_sll)


def test_aludecoder_add(signals_add):
    run_simulation(config, "test_aludecoder", waveform_file, signals_add)


def test_aludecoder_sub(signals_sub):
    run_simulation(config, "test_aludecoder", waveform_file, signals_sub)


def test_aludecoder_and(signals_and):
    run_simulation(config, "test_aludecoder", waveform_file, signals_and)


def test_aludecoder_or(signals_or):
    run_simulation(config, "test_aludecoder", waveform_file, signals_or)


def test_aludecoder_slt(signals_slt):
    run_simulation(config, "test_aludecoder", waveform_file, signals_slt)


def test_aludecoder_lui(signals_lui):
    run_simulation(config, "test_aludecoder", waveform_file, signals_lui)
