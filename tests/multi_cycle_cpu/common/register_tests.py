from bitstring import Bits

from tests.common import check_value


def test_register_file(datapath, registerfile, N=32):
    for i in range(N):
        check_value(
            datapath.registerFile.rf[i], Bits(int=registerfile[i], length=N).uint
        )
