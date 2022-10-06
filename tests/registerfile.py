from bitstring import Bits


class RegisterFile:
    def __init__(self, size=32):
        self.__size = size
        self.__data = [0] * self.__size

    def set(self, address, data):
        self.__data[address] = data

    def __len__(self):
        return self.__size

    def __getitem__(self, i):
        if i == 0:
            return 0

        return Bits(int=self.__data[i], length=self.__size).uint
