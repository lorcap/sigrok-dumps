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

from .ft8xx import Ft8xx
from .param import *

class Ft8xxRamReg (Ft8xx):
    '''Writer of FT8xx's Register commands in VCD format.

    For command references, see:
    - Document Reference No.: BRT_000220
    - Document Title: BT81X (815/6) Advanced Embedded Video Engine Datasheet
    - Version: 1.0
    - Date:
    - Chapter: 5.1 - Registers
    - Pages: 42-47

    - Document Reference No.: BRT_000002
    - Document Title: FT81x (Advanced Embedded Video Engine)
    - Version: 1.4
    - Date:
    - Chapter: 5.1 - Registers
    - Pages: 41-46

    - Document Reference No.: BRT_000039
    - Document Title: FT800 (Embedded Video Engine)
    - Version: 1.3
    - Date:
    - Chapter: 5.1 - FT800 Registers
    - Pages: 34-37
    '''

    def __enter__ (self):
        return self

    def __exit__ (self, exc_type, exc_val, exc_tb):
        self.mem_end()
        super().__exit__(exc_type, exc_val, exc_tb)

    def _reg (self, addr, bits, write, read):
        assert 0x302000 <= addr <= 0x302fff
        if write != None:
            self.mem_write(addr)
            val = bit(write, bits - 1, 0)
            mosi = tuple(int32(val))
            self.data(mosi)
        elif read != None:
            self.mem_read(addr)
            val = bit(read, bits - 1, 0)
            mosi = tuple(int32(-1))
            miso = tuple(int32(val))
            self.data(mosi, miso)
        else:
            assert False, 'cannot neither write nor read'

    def reg_id (self, *, read=0x7c):
        self._reg(0x302000, 8, None, read)

    def reg_frames (self, *, read=0):
        self._reg(0x302004, 32, None, read)

    def reg_clock (self, *, read=0):
        self._reg(0x302008, 32, None, read)

    def reg_frequency (self, write=None, read=60000000):
        self._reg(0x30200c, 28, write, read)

    def reg_rendermode (self, write=None, read=0):
        self._reg(0x302010, 1, write, read)

    def reg_snapy (self, write=None, read=0):
        self._reg(0x302014, 11, write, read)

    def reg_snapshot (self, write=None, read=0):
        self._reg(0x302018, 1, write, read)

    def reg_snapformat (self, write=None, read=0x20):
        self._reg(0x30201c, 6, write, read)

    def reg_cpureset (self, write=None, read=2):
        self._reg(0x302020, 3, write, read)

    def reg_tap_crc (self, *, read=0):
        self._reg(0x302024, 32, None, read)

    def reg_tap_mask (self, write=None, read=0xffffffff):
        self._reg(0x302028, 32, write, read)

    def reg_hcycle (self, write=None, read=0x224):
        self._reg(0x30202c, 12, write, read)

    def reg_hoffset (self, write=None, read=0x02b):
        self._reg(0x302030, 12, write, read)

    def reg_hsize (self, write=None, read=0x1e0):
        self._reg(0x302034, 12, write, read)

    def reg_hsync0 (self, write=None, read=0x000):
        self._reg(0x302038, 12, write, read)

    def reg_hsync1 (self, write=None, read=0x029):
        self._reg(0x30203c, 12, write, read)

    def reg_vcycle (self, write=None, read=0x124):
        self._reg(0x302040, 12, write, read)

    def reg_voffset (self, write=None, read=0x00c):
        self._reg(0x302044, 12, write, read)

    def reg_vsize (self, write=None, read=0x110):
        self._reg(0x302048, 12, write, read)

    def reg_vsync0 (self, write=None, read=0x000):
        self._reg(0x30204c, 10, write, read)

    def reg_vsync1 (self, write=None, read=0x00a):
        self._reg(0x302050, 10, write, read)

    def reg_dlswap (self, write=None, read=0):
        self._reg(0x302054, 2, write, read)

    def reg_rotate (self, write=None, read=0):
        self._reg(0x302058, 3, write, read)

    def reg_outbits (self, write=None, read=0x1b6):
        self._reg(0x30205c, 9, write, read)

    def reg_dither (self, write=None, read=1):
        self._reg(0x302060, 1, write, read)

    def reg_swizzle (self, write=None, read=0):
        self._reg(0x302064, 4, write, read)

    def reg_cspread (self, write=None, read=1):
        self._reg(0x302068, 1, write, read)

    def reg_pclk_pol (self, write=None, read=1):
        self._reg(0x30206c, 1, write, read)

    def reg_pclk (self, write=None, read=0):
        self._reg(0x302070, 8, write, read)

    def reg_tag_x (self, write=None, read=0):
        self._reg(0x302074, 11, write, read)

    def reg_tag_y (self, write=None, read=0):
        self._reg(0x302078, 11, write, read)

    def reg_tag (self, *, read=0):
        self._reg(0x30207c, 8, None, read)

    def reg_vol_pb (self, write=None, read=0xff):
        self._reg(0x302080, 8, write, read)

    def reg_vol_sound (self, write=None, read=0xff):
        self._reg(0x302084, 8, write, read)

    def reg_sound (self, write=None, read=0):
        self._reg(0x302088, 16, write, read)

    def reg_play (self, write=None, read=0):
        self._reg(0x30208c, 1, write, read)

    def reg_gpio_dir (self, write=None, read=0x80):
        self._reg(0x302090, 8, write, read)

    def reg_gpio (self, write=None, read=0):
        self._reg(0x302094, 8, write, read)

    def reg_gpiox_dir (self, write=None, read=0x8000):
        self._reg(0x302098, 16, write, read)

    def reg_gpiox (self, write=None, read=0x0080):
        self._reg(0x30209c, 16, write, read)

    def reg_int_flags (self, *, read=0x00):
        self._reg(0x3020a8, 8, None, read)

    def reg_int_en (self, write=None, read=0):
        self._reg(0x3020ac, 1, write, read)

    def reg_int_mask (self, write=None, read=0xff):
        self._reg(0x3020b0, 8, write, read)

    def reg_playback_start (self, write=None, read=0):
        self._reg(0x3020b4, 20, write, read)

    def reg_playback_length (self, write=None, read=0):
        self._reg(0x3020b8, 20, write, read)

    def reg_playback_readptr (self, *, read=0):
        self._reg(0x3020bc, 20, None, read)

    def reg_playback_freq (self, write=None, read=8000):
        self._reg(0x3020c0, 16, write, read)

    def reg_playback_format (self, write=None, read=0):
        self._reg(0x3020c4, 2, write, read)

    def reg_playback_loop (self, write=None, read=0):
        self._reg(0x3020c8, 1, write, read)

    def reg_playback_play (self, write=None, read=0):
        self._reg(0x3020cc, 1, write, read)

    def reg_pwm_hz (self, write=None, read=250):
        self._reg(0x3020d0, 14, write, read)

    def reg_pwm_duty (self, write=None, read=128):
        self._reg(0x3020d4, 8, write, read)

    def reg_macro_0 (self, write=None, read=0):
        self._reg(0x3020d8, 32, write, read)

    def reg_macro_1 (self, write=None, read=0):
        self._reg(0x3020dc, 32, write, read)

    def reg_cmd_read (self, write=None, read=0):
        self._reg(0x3020f8, 12, write, read)

    def reg_cmd_write (self, *, read=0):
        self._reg(0x3020fc, 12, None, read)

    def reg_cmd_dl (self, write=None, read=0):
        self._reg(0x302100, 13, write, read)

    def reg_touch_mode (self, write=None, read=3):
        self._reg(0x302104, 2, write, read)

    def reg_touch_adc_mode (self, write=None, read=1):
        self._reg(0x302108, 1, write, read)

    reg_ctouch_extended = reg_touch_adc_mode

    def reg_touch_charge (self, write=None, read=9000):
        self._reg(0x30210c, 16, write, read)

    reg_ehost_touch_x = reg_touch_charge

    def reg_touch_settle (self, write=None, read=3):
        self._reg(0x302110, 4, write, read)

    def reg_touch_oversample (self, write=None, read=7):
        self._reg(0x302114, 4, write, read)

    reg_ehost_touch_id = reg_touch_oversample

    def reg_touch_rzthresh (self, write=None, read=0xffff):
        self._reg(0x302118, 16, write, read)

    reg_ehost_touch_y = reg_touch_rzthresh

    def reg_touch_raw_xy (self, *, read=0):
        self._reg(0x30211c, 32, None, read)

    reg_ctouch_touch1_xy = reg_touch_raw_xy

    def reg_touch_rz (self, *, read=0):
        self._reg(0x302120, 16, None, read)

    reg_ctouch_touch4_y = reg_touch_rz

    def reg_touch_screen_xy (self, *, read=0):
        self._reg(0x302124, 32, None, read)

    reg_ctouch_touch0_xy = reg_touch_screen_xy

    def reg_touch_tag_xy (self, *, read=0):
        self._reg(0x302128, 32, None, read)

    def reg_touch_tag (self, *, read=0):
        self._reg(0x30212c, 8, None, read)

    def reg_touch_tag1_xy (self, *, read=0):
        self._reg(0x302130, 32, None, read)

    def reg_touch_tag1 (self, *, read=0):
        self._reg(0x302134, 8, None, read)

    def reg_touch_tag2_xy (self, *, read=0):
        self._reg(0x302138, 32, None, read)

    def reg_touch_tag2 (self, *, read=0):
        self._reg(0x30213c, 8, None, read)

    def reg_touch_tag3_xy (self, *, read=0):
        self._reg(0x302140, 32, None, read)

    def reg_touch_tag3 (self, *, read=0):
        self._reg(0x302144, 8, None, read)

    def reg_touch_tag4_xy (self, *, read=0):
        self._reg(0x302148, 32, None, read)

    def reg_touch_tag4 (self, *, read=0):
        self._reg(0x30214c, 8, None, read)

    def reg_touch_transform_a (self, write=None, read=0x00010000):
        self._reg(0x302150, 32, write, read)

    def reg_touch_transform_b (self, write=None, read=0x00000000):
        self._reg(0x302154, 32, write, read)

    def reg_touch_transform_c (self, write=None, read=0x00000000):
        self._reg(0x302158, 32, write, read)

    def reg_touch_transform_d (self, write=None, read=0x00000000):
        self._reg(0x30215c, 32, write, read)

    def reg_touch_transform_e (self, write=None, read=0x00010000):
        self._reg(0x302160, 32, write, read)

    def reg_touch_transform_f (self, write=None, read=0x00000000):
        self._reg(0x302164, 32, write, read)

    def reg_touch_config (self, write=None, read=0x0381):
        self._reg(0x302168, 16, write, read)

    def reg_ctouch_touch4_x (self, *, read=0):
        self._reg(0x30216c, 16, None, read)

    def reg_bist_en (self, write=None, read=0):
        self._reg(0x302174, 1, write, read)

    def reg_trim (self, write=None, read=0):
        self._reg(0x302180, 5, write, read)

    def reg_ana_comp (self, write=None, read=0):
        self._reg(0x302184, 8, write, read)

    def reg_spi_width (self, write=None, read=0):
        self._reg(0x302188, 3, write, read)

    def reg_touch_direct_xy (self, *, read=0):
        self._reg(0x30218c, 32, None, read)

    reg_ctouch_touch2_xy = reg_touch_direct_xy

    def reg_touch_direct_z1z2 (self, *, read=0):
        self._reg(0x302190, 32, None, read)

    reg_ctouch_touch3_xy = reg_touch_direct_z1z2

    def reg_datestamp (self, *, read=4*(0,)):
        for i in range(int(128/32)):
            self._reg(0x302564 + 4*i, 32, None, read[i])

    def reg_cmdb_space (self, write=None, read=0xffc):
        self._reg(0x302574, 12, write, read)

    def reg_cmdb_write (self, write=None):
        self._reg(0x302578, 32, write, None)

    def reg_adaptive_framerate (self, write=None, read=1):
        self._reg(0x30257c, 1, write, read)

    def reg_playback_pause (self, write=None, read=0):
        self._reg(0x3025ec, 1, write, read)

    def reg_flash_status (self, write=None, read=0):
        self._reg(0x3025f0, 2, write, read)

