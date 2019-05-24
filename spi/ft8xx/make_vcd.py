#!/usr/bin/env python
##
## This file is part of the libsigrokdecode project.
##
## Copyright (C) 2018 Lorenzo Cappelletti <lorenzo.cappelletti@gmail.com>
##
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program; if not, see <http://www.gnu.org/licenses/>.
##

from vcd import Ft8xxCoProc, Ft8xxDispList,\
                Ft8xxHostCmd, Ft8xxRamReg

'''PNG data of a 1-red-pixel image.'''
RED_DOT_PNG = (137,  80,  78,  71,  13,  10,  26,  10,
                 0,   0,   0,  13,  73,  72,  68,  82,
                 0,   0,   0,   1,   0,   0,   0,   1,
                 8,   2,   0,   0,   0, 144, 119,  83,
               222,   0,   0,   0,  12,  73,  68,  65,
                84, 120, 156,  99, 248, 247, 227,   7,
                 0,   5, 230,   2, 239, 238, 216, 252,
                77,   0,   0,   0,   0,  73,  69,  78,
                68, 174,  66,  96, 130               )

'''Zlib compress data of a 1-red-pixel image.'''
RED_DOT_ZLIB = (120,156,187,255,31,0,2,191,1,223)

def host_cmd (filename):
    '''Generate a VCD file with all Host Commands.'''
    with Ft8xxHostCmd(open(filename, 'w')) as ft:
        ft.active()
        ft.standby()
        ft.sleep()
        ft.pwrdown()
        ft.pwrdown2()
        ft.pd_roms(0x05)
        ft.clkext()
        ft.clkint()
        ft.clksel(0, 0)
        ft.clksel2(1, 4)
        ft.rst_pulse()
        ft.pindrive(0x0a, 1)
        ft.pin_pd_state(0x10, 2)

def host_err (filename):
    '''Generate a VCD file with errors in Host Commands.'''
    with Ft8xxHostCmd(open(filename, 'w')) as ft:
        ft.clksel(0, 1)
        ft.clksel(0, 4)
        ft.cmd(0x44, 0x01)
        ft.cmd(0x44, 0x00, byte3=0x01)

        # trailing data
        ft.cs.change(0)
        ft.write((0x44, 0x00, 0x00, 0x01, 0x02))
        ft.cs.change(1)
        ft.ts += 2*ft.CLK_T

def coproc_cmd (filename):
    '''Generate a VCD file with all co-processor commands.'''
    with Ft8xxCoProc(file=open(filename, 'w'), write_addr=0x308000) as ft:
        ft.cmd_dlstart()
        ft.cmd_swap()
        ft.cmd_coldstart()
        ft.cmd_interrupt(500)
        ft.cmd_append(0, 40)
        ft.cmd_regread(0x302008, 0)
        ft.cmd_memwrite(0x3020d4, 0, 0, 0, 100)
        ft.cmd_inflate(0x8000, *RED_DOT_ZLIB)
        ft.cmd_loadimage(0, 0, *RED_DOT_PNG)
        ft.cmd_mediafifo(0x100000 - 65536, 65536)
        #ft.cmd_playvideo(8|4, data?)
        ft.cmd_videostart()
        ft.cmd_videoframe(4, 0)
        ft.cmd_memcrc(0, 1024, 0)
        ft.cmd_memzero(0, 1024)
        ft.cmd_memset(0, 0xff, 1024)
        ft.cmd_memcpy(0x8000, 0, 1024)
        ft.cmd_button(10, 10, 140, 100, 31, 0, 'Press!')
        ft.cmd_clock(80, 60, 50, 0, 8, 15, 0, 0)
        ft.cmd_fgcolor(0x703800)
        ft.cmd_bgcolor(0x402000)
        ft.cmd_gradcolor(0xff0000)
        ft.cmd_gauge(80, 60, 50, 0, 5, 4, 30, 100)
        ft.cmd_gradient(0, 0, 0x0000ff, 160, 0, 0xff0000)
        ft.cmd_keys(10, 10, 140, 30, 26, 0, '12345')
        ft.cmd_progress(20, 50, 120, 12, 0, 50, 100)
        ft.cmd_scrollbar(20, 50, 120, 8, 0, 10, 40, 100)
        ft.cmd_slider(20, 50, 120, 8, 0, 50, 100)
        ft.cmd_dial(80, 60, 55, 0, 0x8000)
        ft.cmd_toggle(60, 20, 33, 27, 0, 0, 'no\xffyes')
        ft.cmd_text(0, 0, 31, 0, 'Text!')
        ft.cmd_setbase(16)
        ft.cmd_number(20, 60, 31, 0, 42)
        ft.cmd_loadidentity()
        ft.cmd_setmatrix()
        ft.cmd_getmatrix()
        ft.cmd_getptr(0)
        ft.cmd_getprops()
        ft.cmd_scale(2*65536, 2*65536)
        ft.cmd_rotate(10*65536/360)
        ft.cmd_translate(20*65536, 0)
        ft.cmd_calibrate()
        ft.cmd_setrotate(2)
        ft.cmd_spinner(80, 60, 0, 0)
        ft.cmd_screensaver()
        ft.cmd_sketch(0, 0, 480, 272, 0, 1) # L1
        ft.cmd_stop()
        ft.cmd_setfont(7, 1000)
        ft.cmd_setfont2(20, 100000, 32)
        ft.cmd_setscratch(31)
        ft.cmd_romfont(1, 31)
        ft.cmd_track(60*16, 50*16, 40, 12, 1)
        ft.cmd_snapshot(0)
        ft.cmd_snapshot2(7, 0, 0, 0, 32, 32)
        ft.cmd_setbitmap(0, 7, 32, 32)
        ft.cmd_logo()
        ft.cmd_csketch(100, 100, 24, 48, 0, 1, 0)

def displist_cmd (filename):
    '''Generate a VCD file with all Display List commands.'''
    with Ft8xxDispList(file=open(filename, 'w'), write_addr=0x301020) as ft:
        ft.alpha_func(1, 10)
        ft.begin(3)
        ft.bitmap_handle(4)
        ft.bitmap_layout(2, 32, 32)
        ft.bitmap_layout_h(1, 1)
        ft.bitmap_size(1, 1, 1, 100, 100)
        ft.bitmap_size_h(1, 1)
        ft.bitmap_source(0x1234)
        ft.bitmap_swizzle(0, 1, 2, 3)
        ft.bitmap_transform_a(0, 0x1000)
        ft.bitmap_transform_b(1, 0x1000)
        ft.bitmap_transform_c(0x100000)
        ft.bitmap_transform_d(0, 0x1020)
        ft.bitmap_transform_e(1, 0x1020)
        ft.bitmap_transform_f(0x102030)
        ft.blend_func(1, 2)
        ft.call(0x1234)
        ft.cell(12)
        ft.clear(1, 0, 0)
        ft.clear_color_a(0xaa)
        ft.clear_color_rgb(0x11, 0x22, 0x33)
        ft.clear_stencil(0x55)
        ft.clear_tag(0xaa)
        ft.color_a(0xaa)
        ft.color_mask(1, 0, 1, 0)
        ft.color_rgb(0x11, 0x22, 0x33)
        ft.display()
        ft.end()
        ft.jump(0x308030)
        ft.line_width(16)
        ft.macro(1)
        ft.nop()
        ft.palette_source(0x1234)
        ft.point_size(30)
        ft.restore_context()
        ft.return_()
        ft.save_context()
        ft.scissor_size(20, 30)
        ft.scissor_xy(100, 200)
        ft.stencil_func(1, 2, 3)
        ft.stencil_mask(123)
        ft.stencil_op(1, 2)
        ft.tag(100)
        ft.tag_mask(1)
        ft.vertex2f(0x1100, 0x2200)
        ft.vertex2ii(100, 200, 3, 4)
        ft.vertex_format(1)
        ft.vertex_translate_x(100)
        ft.vertex_translate_y(100)

def ramreg_cmd (filename):
    '''Generate a VCD file with all register writings.'''
    with Ft8xxRamReg(open(filename, 'w')) as ft:
        ft.reg_id()
        ft.reg_frames()
        ft.reg_clock()
        ft.reg_frequency(10000000)
        ft.reg_rendermode(1)
        ft.reg_snapy(4)
        ft.reg_snapshot(1)
        ft.reg_snapformat(10)
        ft.reg_cpureset(4)
        ft.reg_tap_crc()
        ft.reg_tap_mask(0x0fffffff)
        ft.reg_hcycle(0x224)
        ft.reg_hoffset(0x02b)
        ft.reg_hsize(0x1e0)
        ft.reg_hsync0(0x000)
        ft.reg_hsync1(0x029)
        ft.reg_vcycle(0x124)
        ft.reg_voffset(0x00c)
        ft.reg_vsize(0x110)
        ft.reg_vsync0(0x000)
        ft.reg_vsync1(0x00a)
        ft.reg_dlswap(0x00)
        ft.reg_rotate(0)
        ft.reg_outbits(0)
        ft.reg_dither(1)
        ft.reg_swizzle(0)
        ft.reg_cspread(1)
        ft.reg_pclk_pol(0)
        ft.reg_pclk(0)
        ft.reg_tag_x(0)
        ft.reg_tag_y(0)
        ft.reg_tag()
        ft.reg_vol_pb(0xff)
        ft.reg_vol_sound(0xff)
        ft.reg_sound(0)
        ft.reg_play(0)
        ft.reg_gpio_dir(0x80)
        ft.reg_gpio(0)
        ft.reg_gpiox_dir(0x8000)
        ft.reg_gpiox(0x0080)
        ft.reg_int_flags()
        ft.reg_int_en(0)
        ft.reg_int_mask(0xff)
        ft.reg_playback_start(0)
        ft.reg_playback_length(0)
        ft.reg_playback_readptr()
        ft.reg_playback_freq(8000)
        ft.reg_playback_format(0)
        ft.reg_playback_loop(1)
        ft.reg_playback_play(1)
        ft.reg_pwm_hz(250)
        ft.reg_pwm_duty(128)
        ft.reg_macro_0(0)
        ft.reg_macro_1(0)
        ft.reg_cmd_read(0)
        ft.reg_cmd_write()
        ft.reg_cmd_dl(0)
        ft.reg_touch_mode(3)
        ft.reg_touch_adc_mode(1)
        ft.reg_ctouch_extended(1)
        ft.reg_touch_charge(9000)
        ft.reg_touch_settle(3)
        ft.reg_touch_oversample(7)
        ft.reg_touch_rzthresh(0xffff)
        ft.reg_touch_raw_xy()
        ft.reg_ctouch_touch1_xy()
        ft.reg_touch_rz()
        ft.reg_ctouch_touch4_y()
        ft.reg_touch_screen_xy()
        ft.reg_ctouch_touch0_xy()
        ft.reg_touch_tag_xy()
        ft.reg_touch_tag()
        ft.reg_touch_tag1_xy()
        ft.reg_touch_tag1()
        ft.reg_touch_tag2_xy()
        ft.reg_touch_tag2()
        ft.reg_touch_tag3_xy()
        ft.reg_touch_tag3()
        ft.reg_touch_tag4_xy()
        ft.reg_touch_tag4()
        ft.reg_touch_transform_a(0x00010000)
        ft.reg_touch_transform_b(0x00000000)
        ft.reg_touch_transform_c(0x00000000)
        ft.reg_touch_transform_d(0x00000000)
        ft.reg_touch_transform_e(0x00010000)
        ft.reg_touch_transform_f(0x00000000)
        ft.reg_touch_config(0x0381)
        ft.reg_ctouch_touch4_x()
        ft.reg_bist_en(0)
        ft.reg_trim(0)
        ft.reg_ana_comp(0)
        ft.reg_spi_width(0)
        ft.reg_touch_direct_xy()
        ft.reg_ctouch_touch2_xy()
        ft.reg_touch_direct_z1z2()
        ft.reg_ctouch_touch3_xy()
        ft.reg_datestamp(read=(0x01234567, 0x89abcdef, 0x01234567, 0x89abcdef))
        ft.reg_cmdb_space(0xffc)
        ft.reg_cmdb_write(0)
        ft.reg_adaptive_framerate(1)
        ft.reg_playback_pause(0)
        ft.reg_flash_status(2)

if __name__ == '__main__':
    import sys

    host_cmd('hostcmd.vcd')
    host_err('hostcmd_err.vcd')
    coproc_cmd('coproc.vcd')
    displist_cmd('displist.vcd')
    ramreg_cmd('ramreg.vcd')

