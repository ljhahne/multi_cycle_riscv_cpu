import numpy as np


class Memory:
    def __init__(self, size):
        self.memory = np.zeros(size, dtype=int)

    def __getitem__(self, i):
        return self.memory[i]

    def __len__(self):
        return len(memory)

    def __setitem__(self, i, value):
        self.memory[i] = value

    def __repr__(self):
        repr_str = "Memory Map\n"

        for i in range(len(self.memory)):
            repr_str += "0x{}\t{}\n".format(i, self.memory[i])

        return repr_str[:-1]
