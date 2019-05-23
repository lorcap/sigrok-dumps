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

from .ft8xx import HOST, Ft8xx
from .param import *

class Ft8xxCoProcCommand (Ft8xx):
    '''Writer of FT8xx's Co-Processor Commands in VCD format.

    For command references, see:
    - Document Reference No.: BRT_000031
    - Document Title: FT81x Series Programmers Guide
    - Version: 1.1
    - Date: 2016-09-19
    - Chapter: 5 - Co-Processor Engine
    - Pages: 161-251
    '''

    def __init__ (self, file, *, write_addr=None, read_addr=None):
        super().__init__(file)
        self._cmd_write_addr = write_addr
        self._cmd_read_addr  = read_addr

    def __enter__ (self):
        super().__enter__()
        if self._cmd_write_addr != None:
            self.mem_write(self._cmd_write_addr)
        elif self._cmd_read_addr != None:
            self.mem_read(self._cmd_read_addr)
        return self

    def __exit__ (self, exc_type, exc_val, exc_tb):
        self.mem_end()
        super().__exit__(exc_type, exc_val, exc_tb)

    def _cmd (self, cmd, *params):
        '''Write out a read/write command and its parameters to co-processor.'''
        assert self._host in (HOST.MEM_WRITE, HOST.MEM_READ)
        mosi = (*int32(cmd),)
        for p in params:
            mosi += (*p,)
        rem = len(mosi) % 4
        if rem:
            mosi += (0,) * (4 - rem)
        self.write(mosi)

    def cmd_dlstart (self):
        self._cmd(0xffffff00)

    def cmd_swap (self):
        self._cmd(0xffffff01)

    def cmd_coldstart (self):
        self._cmd(0xffffff32)

    def cmd_interrupt (self, ms):
        self._cmd(0xffffff02, int32(ms))

    def cmd_append (self, ptr, num):
        self._cmd(0xffffff1e, int32(ptr, num))

    def cmd_regread (self, ptr, result=0):
        self._cmd(0xffffff19, int32(ptr, result))

    def cmd_memwrite (self, ptr, *bytes_):
        self._cmd(0xffffff1a, int32(ptr, len(bytes_)), int8(*bytes_))

    def cmd_inflate (self, ptr, *bytes_):
        self._cmd(0xffffff22, int32(ptr), int8(*bytes_))

    def cmd_loadimage (self, ptr, options, *bytes_):
        self._cmd(0xffffff24, int32(ptr, options), int8(*bytes_))

    def cmd_mediafifo (self, ptr, size):
        self._cmd(0xffffff39, int32(ptr, size))

    def cmd_playvideo (self, opts, *bytes_):
        self._cmd(0xffffff3a, int32(opts), int8(*bytes_))

    def cmd_videostart (self):
        self._cmd(0xffffff40)

    def cmd_videoframe (self, dst, ptr):
        self._cmd(0xffffff41, int32(dst, ptr))

    def cmd_memcrc (self, ptr, num, result=0):
        self._cmd(0xffffff18, int32(ptr, num, result))

    def cmd_memzero (self, ptr, num):
        self._cmd(0xffffff1c, int32(ptr, num))

    def cmd_memset (self, ptr, value, num):
        self._cmd(0xffffff1b, int32(ptr, value, num))

    def cmd_memcpy (self, dest, src, num):
        self._cmd(0xffffff1d, int32(dest, src, num))

    def cmd_button (self, x, y, w, h, font, options, s):
        self._cmd(0xffffff1d, int16(x, y, w, h, font, options), char(s))

    def cmd_clock (self, x, y, r, options, h, m, s, ms):
        self._cmd(0xffffff14, int16(x, y, r, options, h, m, s, ms))

    def cmd_fgcolor (self, c):
        self._cmd(0xffffff0a, int32(bit(c, 24, 0)))

    def cmd_bgcolor (self, c):
        self._cmd(0xffffff09, int32(bit(c, 24, 0)))

    def cmd_gradcolor (self, c):
        self._cmd(0xffffff34, int32(bit(c, 24, 0)))

    def cmd_gauge (self, x, y, r, options, major, minor, val, range_):
        self._cmd(0xffffff13, int16(x, y, r, options, major, minor, val, range_))

    def cmd_gradient (self, x0, y0, rgb0, x1, y1, rgb1):
        self._cmd(0xffffff0b, int16(x0, y0), int32(bit(rgb0, 24, 0)),
                              int16(x1, y1), int32(bit(rgb1, 24, 0)))

    def cmd_keys (self, x, y, w, h, font, options, s):
        self._cmd(0xffffff0e, int16(x, y, w, h, font, options), char(s))

    def cmd_progress (self, x, y, w, h, options, val, range_):
        self._cmd(0xffffff0f, int16(x, y, w, h, options, val, range_))

    def cmd_scrollbar (self, x, y, w, h, options, val, size, range_):
        self._cmd(0xffffff11, int16(x, y, w, h, options, val, size, range_))

    def cmd_slider (self, x, y, w, h, options, val, range_):
        self._cmd(0xffffff10, int16(x, y, w, h, options, val, range_))

    def cmd_dial (self, x, y, r, options, val):
        self._cmd(0xffffff2d, int16(x, y, r, options, val))

    def cmd_toggle (self, x, y, w, font, options, state, s):
        self._cmd(0xffffff12, int16(x, y, w, font, options, state), char(s))

    def cmd_text (self, x, y, font, options, s):
        self._cmd(0xffffff0c, int16(x, y, font, options), char(s))

    def cmd_setbase (self, b):
        self._cmd(0xffffff38, int32(b))

    def cmd_number (self, x, y, font, options, n):
        self._cmd(0xffffff2e, int16(x, y, font, options), int32(n));

    def cmd_loadidentity (self):
        self._cmd(0xffffff26)

    def cmd_setmatrix (self):
        self._cmd(0xffffff2a)

    def cmd_getmatrix (self, a=0, b=0, c=0, d=0, e=0, f=0):
        self._cmd(0xffffff33, int32(a, b, c, d, e, f))

    def cmd_getptr (self, result=0):
        self._cmd(0xffffff23, int32(result))

    def cmd_getprops (self, ptr=0, width=0, height=0):
        self._cmd(0xffffff25, int32(ptr, width, height))

    def cmd_scale (self, sx, sy):
        self._cmd(0xffffff28, int32(sx, sy))

    def cmd_rotate (self, a):
        self._cmd(0xffffff29, int32(a))

    def cmd_translate (self, tx, ty):
        self._cmd(0xffffff27, int32(tx, ty))

    def cmd_calibrate (self, result=0):
        self._cmd(0xffffff15, int32(result))

    def cmd_setrotate (self, r):
        self._cmd(0xffffff36, int32(r))

    def cmd_spinner (self, x, y, style, scale):
        self._cmd(0xffffff16, int16(x, y, style, scale))

    def cmd_screensaver (self):
        self._cmd(0xffffff2f)

    def cmd_sketch (self, x, y, w, h, ptr, format):
        self._cmd(0xffffff30, int16(x, y, w, h), int32(ptr), int16(format))

    def cmd_stop (self):
        self._cmd(0xffffff17)

    def cmd_setfont (self, font, ptr):
        self._cmd(0xffffff2b, int32(font, ptr))

    def cmd_setfont2 (self, font, ptr, firstchar):
        self._cmd(0xffffff3b, int32(font, ptr, firstchar))

    def cmd_setscratch (self, handle):
        self._cmd(0xffffff3c, int32(handle))

    def cmd_romfont (self, font, romslot):
        self._cmd(0xffffff3f, int32(font, romslot))

    def cmd_track (self, x, y, w, h, tag):
        self._cmd(0xffffff2c, int16(x, y, w, h, tag))

    def cmd_snapshot (self, ptr):
        self._cmd(0xffffff1f, int32(ptr))

    def cmd_snapshot2 (self, fmt, ptr, x, y, w, h):
        self._cmd(0xffffff37, int32(fmt, ptr), int16(x, y, w, h))

    def cmd_setbitmap (self, addr, fmt, width, height):
        self._cmd(0xffffff43, int32(addr), int16(fmt, width, height))

    def cmd_logo (self):
        self._cmd(0xffffff31)

    def cmd_csketch (self, x, y, w, h, ptr, format, freq):
        self._cmd(0xffffff35, int16(x, y, w, h), int32(ptr), int16(format, freq))

