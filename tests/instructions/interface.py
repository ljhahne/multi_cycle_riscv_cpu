from abc import ABC, abstractmethod

# X : dont care value
X = 0


class InstructionType(ABC):
    def __init__(self):
        self._length = 32
        self._op = None
        self._funct3 = None

    @abstractmethod
    def _get_binary_string(self):
        pass

    def machine_code(self):
        binary_str = self._get_binary_string()
        return int(binary_str, 2)

    def print_machine_code(self):
        binary_str = self._get_binary_string()
        print("{:x}".format(int(binary_str, 2)).zfill(8))

    def get_op(self):
        return self._op.get_value()

    @abstractmethod
    def get_funct3(self):
        pass

    @abstractmethod
    def get_funct7(self):
        pass

    @abstractmethod
    def get_funct7b5(self):
        pass
