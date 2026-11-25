/*
 * Copyright (c) 2026 Punyashloka, Purnendu, Rahil, Ronak, Shylashree N (RV College of Engineering)
 * SPDX-License-Identifier: Apache-2.0
 *
 * 2-FF Synchronizer / Clock-Domain-Crossing (CDC) demo
 *
 * ui_in[3:0] : four asynchronous level inputs, each passed through a 2-FF synchronizer
 * ui_in[4]   : asynchronous "toggle" input for the toggle-based pulse synchronizer
 * ui_in[5]   : selects which counter is shown on uio_out (0 = rising-edge count, 1 = pulse count)
 *
 * uo_out[3:0]: synchronized copies of ui_in[3:0]
 * uo_out[4]  : one-clock pulse on a rising edge of synchronized ui_in[0]
 * uo_out[5]  : one-clock pulse on a falling edge of synchronized ui_in[0]
 * uo_out[6]  : toggles on every rising edge of synchronized ui_in[0]
 * uo_out[7]  : one-clock pulse for every change of ui_in[4] (pulse synchronizer output)
 * uio_out    : 8-bit event counter (selected by ui_in[5])
 */

`default_nettype none

module tt_um_rvce_2ff_sync (
    input  wire [7:0] ui_in,    // Dedicated inputs
    output wire [7:0] uo_out,   // Dedicated outputs
    input  wire [7:0] uio_in,   // IOs: Input path
    output wire [7:0] uio_out,  // IOs: Output path
    output wire [7:0] uio_oe,   // IOs: Enable path (active high: 0=input, 1=output)
    input  wire       ena,      // always 1 when the design is powered, so you can ignore it
    input  wire       clk,      // clock
    input  wire       rst_n     // reset_n - low to reset
);

  // Stage 1 (may go metastable), stage 2 (synchronized), stage 3 (previous value for edge detection)
  reg [4:0] sync_ff1;
  reg [4:0] sync_ff2;
  reg [4:0] sync_prev;

  reg       toggle_q;
  reg [7:0] rise_count;
  reg [7:0] pulse_count;

  wire rise_pulse   = sync_ff2[0] & ~sync_prev[0];
  wire fall_pulse   = ~sync_ff2[0] & sync_prev[0];
  wire toggle_pulse = sync_ff2[4] ^ sync_prev[4];

  always @(posedge clk) begin
    if (!rst_n) begin
      sync_ff1    <= 5'b0;
      sync_ff2    <= 5'b0;
      sync_prev   <= 5'b0;
      toggle_q    <= 1'b0;
      rise_count  <= 8'b0;
      pulse_count <= 8'b0;
    end else begin
      sync_ff1  <= ui_in[4:0];
      sync_ff2  <= sync_ff1;
      sync_prev <= sync_ff2;

      if (rise_pulse) begin
        toggle_q   <= ~toggle_q;
        rise_count <= rise_count + 8'd1;
      end

      if (toggle_pulse) begin
        pulse_count <= pulse_count + 8'd1;
      end
    end
  end

  assign uo_out  = {toggle_pulse, toggle_q, fall_pulse, rise_pulse, sync_ff2[3:0]};
  assign uio_out = ui_in[5] ? pulse_count : rise_count;
  assign uio_oe  = 8'hFF;

  // List all unused inputs to prevent warnings
  wire _unused = &{ena, ui_in[7:6], uio_in, 1'b0};

endmodule
