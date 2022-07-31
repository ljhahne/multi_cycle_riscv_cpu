
# Self-Implementation of a Multi Cycle RISC-V RV32I CPU
- Implemented in SystemVerilog
- Based on the [Digital Design and Computer Architecture: RISC-V Edition](http://pages.hmc.edu/harris/ddca/ddcarv.html) textbook and the corresponding [edX Course](https://www.edx.org/course/computer-architecture?index=product&queryID=ca158da1df6c2a04c6b56864aed4fc51&position=3&linked_from=autocomplete).
- Work in progress: Instruction set is not yet complete. This will be fixed soon.
- Verification of the design is achieved with [cocotb](https://github.com/cocotb/cocotb/) and [icarus verilog](http://iverilog.icarus.com/)  

To test the design, build the docker container

```
cd docker/cocotb
docker build -t cocotb .
```

In the root directory of the project, run

```bash
docker run --rm -it -v $(pwd):/opt/project cocotb bash -c "cd /opt/project ; SIM=icarus python3 -m pytest -o log_cli=True -n auto tests/"
```
