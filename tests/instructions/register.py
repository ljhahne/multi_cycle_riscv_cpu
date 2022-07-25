from dataclasses import dataclass


@dataclass()
class RegisterFile:
    def __init__(self, size):
        self.register_file = np.zeros(size, dtype=int)

    def __getitem__(self, i):
        return self.register_file[i]

    def __len__(self):
        return len(register_file)

    def __setitem__(self, i, value):
        self.register_file[i] = value

    def __repr__(self):
        repr_str = "Register File\n"

        for i in range(len(self.register_file)):
            repr_str += "0x{}\t{}\n".format(i, self.register_file[i])

        return repr_str[:-1]
