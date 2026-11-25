<!---

This file is used to generate your project datasheet. Please fill in the information below and delete any unused
sections.

You can also include images in this folder and reference them in the markdown. Each image must be less than
512 kb in size, and the combined size of all images must be less than 1 MB.
-->

## How it works

A signal that comes from outside the chip (a switch, a button, or logic running on a different clock) can change at
any moment, including right at a clock edge. A flip-flop that samples it can become *metastable*. The classic fix is
the **two flip-flop (2-FF) synchronizer**: the first flip-flop may go metastable, but it gets one full clock period to
settle before the second flip-flop samples it, so the rest of the design only sees a clean, synchronized signal.

This project demonstrates the common clock-domain-crossing (CDC) building blocks:

1. **2-FF level synchronizers**: `ui[3:0]` are four independent asynchronous inputs. Each passes through two
   flip-flops and appears on `uo[3:0]` two clock cycles later.
2. **Edge detector**: a third flip-flop holds the previous synchronized value of `ui[0]`. Comparing the two gives a
   one-clock pulse on `uo[4]` for a rising edge and on `uo[5]` for a falling edge.
3. **Toggle flip-flop**: `uo[6]` changes state on every synchronized rising edge of `ui[0]`.
4. **Toggle (pulse) synchronizer**: the sending domain flips `ui[4]` once per event. After synchronization, an XOR
   of the current and previous values gives exactly one clock pulse on `uo[7]` per event. This is how single-cycle
   events are passed safely between clock domains.
5. **Event counters**: two 8-bit counters count the rising edges of `ui[0]` and the pulses from `ui[4]`. `ui[5]`
   selects which counter drives `uio[7:0]` (0 = rising-edge count, 1 = pulse count).

All flip-flops reset synchronously when `rst_n` is low.

## How to test

1. Set the clock (for example 10 MHz) and reset the design.
2. Change `ui[0]`..`ui[3]`. The same values appear on `uo[0]`..`uo[3]` two clock cycles later.
3. Switch `ui[0]` from 0 to 1. `uo[4]` pulses high for one clock, `uo[6]` toggles, and the counter on `uio[7:0]`
   (with `ui[5]` = 0) increases by one. Switching `ui[0]` back to 0 gives a one-clock pulse on `uo[5]`.
4. Set `ui[5]` = 1 and flip `ui[4]` several times. Each change gives one pulse on `uo[7]` and the counter on
   `uio[7:0]` counts the changes.

With a slow clock, the pulses can be seen on LEDs. With a fast clock, use a logic analyzer or watch the counters.

## External hardware

None required. Switches or buttons on the inputs and LEDs on the outputs (for example on the Tiny Tapeout demo board)
are enough. A logic analyzer is useful to see the one-clock pulses.

## Credits

We gratefully acknowledge the Center of Excellence (CoE) in Integrated Circuits and Systems (ICAS) and the Department
of Electronics and Communication Engineering (ECE) for providing the necessary resources and guidance.

Special thanks to Dr. H V Ravish Aradhya (HoD - ECE), Dr. K R Usha Rani (Associate Dean - PG), Dr. K. S. Geetha
(Vice Principal) and Dr. K. N. Subramanya (Principal) for their constant encouragement and support in facilitating
this Tiny Tapeout SKY26E submission.
