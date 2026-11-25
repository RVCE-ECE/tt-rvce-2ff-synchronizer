![](../../workflows/gds/badge.svg) ![](../../workflows/docs/badge.svg) ![](../../workflows/test/badge.svg) ![](../../workflows/fpga/badge.svg)

# 2-FF Synchronizer / Clock-Domain-Crossing Demo

A Tiny Tapeout (SKY130, shuttle SKY26E) project from RV College of Engineering that shows how asynchronous signals
are brought safely into a clock domain.

- [Datasheet / project documentation](docs/info.md)
- Top module: `tt_um_rvce_2ff_sync` in [src/project.v](src/project.v)
- Testbench: [test/test.py](test/test.py) (cocotb)

## What it does

| Block | Inputs | Outputs |
|---|---|---|
| Four 2-FF level synchronizers | `ui[3:0]` | `uo[3:0]` (two clock cycles later) |
| Rising / falling edge detector on synchronized `ui[0]` | `ui[0]` | `uo[4]` rise pulse, `uo[5]` fall pulse |
| Toggle flip-flop | `ui[0]` | `uo[6]` |
| Toggle (pulse) synchronizer | `ui[4]` | `uo[7]`, one pulse per change |
| 8-bit event counters | `ui[5]` selects | `uio[7:0]` |

Why two flip-flops: the first flip-flop may go metastable when the input changes near a clock edge. It is given a
full clock period to settle before the second flip-flop samples it, so the rest of the logic only sees a clean signal.

## Running the tests

```sh
cd test
make -B
```

This needs Icarus Verilog and cocotb (see [test/README.md](test/README.md)). The same tests run automatically in the
GitHub Actions `test` workflow.

## Team

Punyashloka, Purnendu, Rahil, Ronak and Shylashree N, RV College of Engineering.

## Credits

We gratefully acknowledge the Center of Excellence (CoE) in Integrated Circuits and Systems (ICAS) and the Department
of Electronics and Communication Engineering (ECE), RVCE, for providing the necessary resources and guidance.

Special thanks to Dr. H V Ravish Aradhya (HoD - ECE), Dr. K R Usha Rani (Associate Dean - PG), Dr. K. S. Geetha
(Vice Principal) and Dr. K. N. Subramanya (Principal) for their constant encouragement and support.

Built from the [Tiny Tapeout Verilog template](https://github.com/TinyTapeout/ttsky-verilog-template).
Learn more at [tinytapeout.com](https://tinytapeout.com).
