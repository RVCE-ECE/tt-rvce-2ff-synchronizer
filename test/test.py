# SPDX-FileCopyrightText: © 2026 Punyashloka, Purnendu, Rahil, Ronak, Shylashree N (RVCE)
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, FallingEdge

# uo_out bit positions
RISE = 4
FALL = 5
TOGGLE = 6
PULSE = 7


def bit(value, n):
    return (int(value) >> n) & 1


async def reset(dut):
    clock = Clock(dut.clk, 10, unit="us")
    cocotb.start_soon(clock.start())
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 5)
    await FallingEdge(dut.clk)
    dut.rst_n.value = 1
    await FallingEdge(dut.clk)


@cocotb.test()
async def test_two_flop_latency(dut):
    """Each input appears on the output exactly two clock edges later."""
    await reset(dut)

    assert int(dut.uo_out.value) == 0
    assert int(dut.uio_oe.value) == 0xFF

    dut.ui_in.value = 0b1010
    await FallingEdge(dut.clk)  # first flop has captured the input
    assert int(dut.uo_out.value) & 0xF == 0, "output must not change after one flop"
    await FallingEdge(dut.clk)  # second flop has captured it
    assert int(dut.uo_out.value) & 0xF == 0b1010

    dut.ui_in.value = 0b0101
    await FallingEdge(dut.clk)
    assert int(dut.uo_out.value) & 0xF == 0b1010
    await FallingEdge(dut.clk)
    assert int(dut.uo_out.value) & 0xF == 0b0101


@cocotb.test()
async def test_edge_detect_and_counter(dut):
    """Rising/falling edges of ui_in[0] give one-clock pulses, a toggle and a count."""
    await reset(dut)
    dut.ui_in.value = 0  # ui_in[5] = 0 -> rise counter on uio_out

    for n in range(1, 4):
        dut.ui_in.value = 1
        await FallingEdge(dut.clk)
        await FallingEdge(dut.clk)
        out = dut.uo_out.value
        assert bit(out, RISE) == 1, "rising-edge pulse expected"
        assert bit(out, FALL) == 0
        await FallingEdge(dut.clk)
        assert bit(dut.uo_out.value, RISE) == 0, "pulse must last one clock"
        assert bit(dut.uo_out.value, TOGGLE) == n % 2
        assert int(dut.uio_out.value) == n

        dut.ui_in.value = 0
        await FallingEdge(dut.clk)
        await FallingEdge(dut.clk)
        assert bit(dut.uo_out.value, FALL) == 1, "falling-edge pulse expected"
        await FallingEdge(dut.clk)
        assert bit(dut.uo_out.value, FALL) == 0
        assert int(dut.uio_out.value) == n


@cocotb.test()
async def test_toggle_pulse_synchronizer(dut):
    """Every change of ui_in[4] gives one pulse on uo_out[7] and is counted."""
    await reset(dut)
    sel = 1 << 5  # show pulse counter on uio_out
    level = 0
    dut.ui_in.value = sel

    for n in range(1, 6):
        level ^= 1
        dut.ui_in.value = sel | (level << 4)
        await FallingEdge(dut.clk)
        assert bit(dut.uo_out.value, PULSE) == 0
        await FallingEdge(dut.clk)
        assert bit(dut.uo_out.value, PULSE) == 1, "pulse expected after two flops"
        await FallingEdge(dut.clk)
        assert bit(dut.uo_out.value, PULSE) == 0, "pulse must last one clock"
        assert int(dut.uio_out.value) == n
        await ClockCycles(dut.clk, 3)
        await FallingEdge(dut.clk)

    # ui_in[5] = 0 selects the rising-edge counter, which never counted here
    dut.ui_in.value = level << 4
    await FallingEdge(dut.clk)
    assert int(dut.uio_out.value) == 0
