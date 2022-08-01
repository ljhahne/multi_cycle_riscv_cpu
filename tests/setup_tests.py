import glob
import os
import shutil
from dataclasses import dataclass, field
from typing import List

from cocotb_test.simulator import run

waveform_file_template = """module waveform_dump();
initial begin
    string waveformfile;
    $value$plusargs("waveformfile=%s", waveformfile);
    $dumpfile(waveformfile);
    $dumpvars(0, {});
end
endmodule
"""
import random
import string

TESTDIR_PREFIX = "tests"


@dataclass
class Config:
    HDLFILES: List[str]
    TOPLEVEL: str
    WORK_DIR: str
    INCLUDES: List[str] = field(default_factory=list)
    SIM_BUILD: str = field(init=False)
    # THIS IS THE PATH TO THE HDL FILE OTHERWISE INCLUDES DO NOT WORK
    WAVEFORM_DIR: str = field(init=False)
    DUMPFILE_SRCDIR: str = field(init=False)
    DUMPFILE_DESTDIR: str = field(init=False)
    TEST_DIR: str = None
    COCOTBMODULE: str = None

    def __post_init__(self):
        for hdl_file in self.HDLFILES:
            assert os.path.exists(hdl_file), "hdl file {} does not exist".format(
                hdl_file
            )

        for path in [self.WORK_DIR, self.TEST_DIR]:
            assert os.path.exists(path), "path {} does not exist".format(path)

        if self.TEST_DIR is None:
            self.TEST_DIR = os.path.join(TESTDIR_PREFIX, self.WORK_DIR)
            # self.COCOTBMODULE = os.path.join(self.TEST_DIR).replace("/", ".")

        if self.COCOTBMODULE is None:
            self.COCOTBMODULE = "{}.{}_cocotb".format(
                self.TEST_DIR.replace("/", "."), self.TOPLEVEL
            )

        self.WORK_DIR = os.path.abspath(self.WORK_DIR)
        self.TEST_DIR = os.path.abspath(self.TEST_DIR)

        self.SIM_BUILD = os.path.join(self.TEST_DIR, "sim_build")
        self.WAVEFORM_DIR = os.path.join(self.TEST_DIR, "waveforms")
        self.DUMPFILE_SRCDIR = os.path.join(self.TEST_DIR, "{}.vcd")
        self.DUMPFILE_DESTDIR = os.path.join(self.WAVEFORM_DIR, "{}.vcd")


def init_waveforms(config: Config) -> None:
    # if os.path.exists(config.SIM_BUILD):
    #     shutil.rmtree(config.SIM_BUILD)

    if not os.path.exists(config.WAVEFORM_DIR):
        os.mkdir(config.WAVEFORM_DIR)

    # clean dumped waveforms from previous run
    else:
        for file in glob.glob(
            os.path.join(config.WAVEFORM_DIR, "*.vcd"), recursive=False
        ):
            os.remove(file)

    waveform_path = os.path.join(config.WAVEFORM_DIR, "waveform_dump.sv")
    with open(waveform_path, "w") as file:
        file.write(waveform_file_template.format(config.TOPLEVEL))

    config.HDLFILES.append(waveform_path)


def default_run_vars(config: Config, testcase, N=10):
    return {
        "includes": config.INCLUDES,
        "verilog_sources": config.HDLFILES,
        "toplevel": config.TOPLEVEL,
        "module": config.COCOTBMODULE,
        "testcase": testcase,
        "sim_build": "{}_{}".format(
            config.SIM_BUILD,
            "".join(
                [
                    random.choice(string.ascii_uppercase + string.digits)
                    for _ in range(N)
                ]
            ),
        ),
        "work_dir": config.WORK_DIR,
        "force_compile": True,
        "compile_args": ["-s", "waveform_dump"],
    }


def init_waveformfile(config, filename_template, *args, **kwargs):
    if "prefix" in list(kwargs.keys()):
        prefix = kwargs["prefix"]

    else:
        prefix = config.TOPLEVEL

    return "+waveformfile={}".format(
        os.path.join(
            config.WAVEFORM_DIR,
            ("{}_" + filename_template).format(prefix, *kwargs["signals"]),
        )
    )


def run_simulation(config, testcase, waveformfile_template, signals):
    waveform = init_waveformfile(config, waveformfile_template, signals=signals)

    vars = default_run_vars(config, testcase)

    try:
        run(**vars, extra_env=signals, plus_args=[waveform])

    finally:
        shutil.rmtree(vars["sim_build"])
