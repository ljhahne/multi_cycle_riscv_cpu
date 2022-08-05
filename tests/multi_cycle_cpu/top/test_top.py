from tests.setup_tests import Config, init_waveforms, run_simulation

config = Config(
    INCLUDES=["src/multi_cycle_cpu/include/"],
    HDLFILES=[
        "src/multi_cycle_cpu/top/top.sv",
        "src/multi_cycle_cpu/top/mem.sv",
        "src/multi_cycle_cpu/top/riscvmulti.sv",
        "src/multi_cycle_cpu/datapath/datapath.sv",
        "src/multi_cycle_cpu/datapath/alu.sv",
        "src/multi_cycle_cpu/datapath/aluflags.sv",
        "src/multi_cycle_cpu/datapath/extend.sv",
        "src/multi_cycle_cpu/datapath/flop.sv",
        "src/multi_cycle_cpu/datapath/flopdual.sv",
        "src/multi_cycle_cpu/datapath/flopenr.sv",
        "src/multi_cycle_cpu/datapath/flopenrdual.sv",
        "src/multi_cycle_cpu/datapath/flopr.sv",
        "src/multi_cycle_cpu/datapath/mux2.sv",
        "src/multi_cycle_cpu/datapath/mux3.sv",
        "src/multi_cycle_cpu/datapath/registerfile.sv",
        "src/multi_cycle_cpu/controller/controller.sv",
        "src/multi_cycle_cpu/controller/controller_fsm.sv",
        "src/multi_cycle_cpu/controller/alu_decoder.sv",
        "src/multi_cycle_cpu/controller/instruction_decoder.sv",
        "src/multi_cycle_cpu/controller/pc_write.sv",
    ],
    COCOTBMODULE="tests.multi_cycle_cpu.top.top_cocotb",
    TOPLEVEL="top",
    WORK_DIR="src/multi_cycle_cpu/top/",
    TEST_DIR="tests/multi_cycle_cpu/top/",
)

init_waveforms(config)

waveform_file = config.TOPLEVEL + ".vcd"


def test_cpu():

    # TODO read riscvtest.txt here. Use symlink or custom verilog header file to pass test instruction to hw design

    run_simulation(
        config,
        "test_cpu",
        waveform_file,
        {},
    )
