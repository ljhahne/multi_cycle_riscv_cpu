
# Self-Implementation of a Multi Cycle RISC-V RS32I CPU
- Implemented in SystemVerilog
- Based on the [Digital Design and Computer Architecture: RISC-V Edition](http://pages.hmc.edu/harris/ddca/ddcarv.html) textbook and the corresponding [edX Course](https://www.edx.org/course/computer-architecture?index=product&queryID=ca158da1df6c2a04c6b56864aed4fc51&position=3&linked_from=autocomplete).
- Work in progress: Instruction set is not yet complete. This will be fixed soon.
- Verification of the design is achieved with [cocotb](https://github.com/cocotb/cocotb/) and [icarus verilog](http://iverilog.icarus.com/)  

To test the design build the docker container in `docker/cocotb` and run

```bash
SIM=icarus python3 -m pytest -o log_cli=True tests/
```
