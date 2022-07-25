from bitstring import Bits

from tests.common import check_value


def test_memory(dut, memory, N=32):
    for DataAdr in list(memory.keys()):
        check_value(
            dut.memory.RAM[Bits(uint=DataAdr, length=N)[:-2].uint], memory[DataAdr]
        )


def test_memread(memory, rd):
    check_value(memory.rd, rd)


def get_rd_from_memory_model(memory_model, DataAdr):
    if DataAdr in list(memory_model.keys()):
        rd = memory_model[DataAdr]

    else:
        rd = 0

    return rd
