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

class Ft8xxDispList (Ft8xx):
    '''Writer of FT8xx/BT81x's Display List commands in VCD format.

    For command references, see:
    - Document Reference No.: BRT_000225
    - Document Title: Application Note - BRT_AN_033 - BT81X Series Programming Guide
    - Version: 1.0
    - Date: 2018-08-14
    - Chapter: 4 - Display List Commands
    - Pages: 65-107

    - Document Reference No.: BRT_000031
    - Document Title: FT81x Series Programmers Guide
    - Version: 1.2
    - Date: 2018-10-02
    - Chapter: 4 - Display List Commands
    - Pages: 89-149

    - Document Reference No.: BRT_000030
    - Document Title: FT800 Series Programmer Guide
    - Version: 2.1
    - Date: 2016-09-19
    - Chapter: 4 - Display List Commands
    - Pages: 81-143
    '''

    def __init__ (self, file, *, write_addr=None, read_addr=None):
        super().__init__(file)
        self._dl_write_addr = write_addr
        self._dl_read_addr  = read_addr

    def __enter__ (self):
        super().__enter__()
        if self._dl_write_addr != None:
            self.mem_write(self._dl_write_addr)
        elif self._dl_read_addr != None:
            self.mem_read(self._dl_read_addr)
        return self

    def __exit__ (self, exc_type, exc_val, exc_tb):
        self.mem_end()
        super().__exit__(exc_type, exc_val, exc_tb)

    def _dl (self, cmd, *params):
        '''Write out a display list command.'''
        assert self._host in (HOST.MEM_WRITE, HOST.MEM_READ)
        mosi = tuple(int32(bit2int((cmd, 31, 24), *params)))
        self.write(mosi)

    def alpha_func (self, func, ref):
        self._dl(0x09, (func, 10, 8), (ref, 7, 0))

    def begin (self, prim):
        self._dl(0x1f, (prim, 3, 0))

    def bitmap_handle (self, handle):
        self._dl(0x05, (handle, 4, 0))

    def bitmap_layout (self, format, linestride, height):
        self._dl(0x07, (format, 23, 19), (linestride, 18, 9), (height, 8, 0))

    def bitmap_layout_h (self, linestride, height):
        self._dl(0x28, (linestride, 3, 2), (height, 1, 0))

    def bitmap_size (self, filter, wrapx, wrapy, width, height):
        self._dl(0x08, (filter, 20), (wrapx, 19), (wrapy, 18),
                       (width, 17, 9), (height, 8, 0))

    def bitmap_size_h (self, width, height):
        self._dl(0x29, (width, 3, 2), (height, 1, 0))

    def bitmap_source (self, addr):
        self._dl(0x01, (addr, 21, 0))

    def bitmap_swizzle (self, r, g, b, a):
        self._dl(0x2f, (r, 11, 9), (g, 8, 6), (b, 5, 3), (a, 2, 0))

    def bitmap_transform_a (self, p, v):
        self._dl(0x15, (p, 17), (v, 16, 0))

    def bitmap_transform_b (self, p, v):
        self._dl(0x16, (p, 17), (v, 16, 0))

    def bitmap_transform_c (self, c):
        self._dl(0x17, (c, 23, 0))

    def bitmap_transform_d (self, p, v):
        self._dl(0x18, (p, 17), (v, 16, 0))

    def bitmap_transform_e (self, p, v):
        self._dl(0x19, (p, 17), (v, 16, 0))

    def bitmap_transform_f (self, f):
        self._dl(0x1a, (f, 23, 0))

    def blend_func (self, src, dst):
        self._dl(0x0b, (src, 5, 3), (dst, 2, 0))

    def call (self, dest):
        self._dl(0x1d, (dest, 15, 0))

    def cell (self, cell):
        self._dl(0x06, (cell, 6, 0))

    def clear (self, c, s, t):
        self._dl(0x26, (c, 2), (s, 1), (t, 0))

    def clear_color_a (self, alpha):
        self._dl(0x0f, (alpha, 7, 0))

    def clear_color_rgb (self, red, blue, green):
        self._dl(0x02, (red, 23, 16), (blue, 15, 8), (green, 7, 0))

    def clear_stencil (self, s):
        self._dl(0x11, (s, 7, 0))

    def clear_tag (self, t):
        self._dl(0x12, (t, 7, 0))

    def color_a (self, alpha):
        self._dl(0x10, (alpha, 7, 0))

    def color_mask (self, r, g, b, a):
        self._dl(0x20, (r, 3), (g, 2), (b, 1), (a, 0))

    def color_rgb (self, red, blue, green):
        self._dl(0x04, (red, 23, 16), (blue, 15, 8), (green, 7, 0))

    def display (self):
        self._dl(0x00)

    def end (self):
        self._dl(0x21)

    def jump (self, dest):
        self._dl(0x1e, (dest, 15, 0))

    def line_width (self, width):
        self._dl(0x0e, (width, 11, 0))

    def macro (self, m):
        self._dl(0x25, (m, 0))

    def nop (self):
        self._dl(0x2d)

    def palette_source (self, addr):
        self._dl(0x2a, (addr, 21, 0))

    def point_size (self, size):
        self._dl(0x0d, (size, 12, 0))

    def restore_context (self):
        self._dl(0x23)

    def return_ (self):
        self._dl(0x24)

    def save_context (self):
        self._dl(0x22)

    def scissor_size (self, width, height):
        self._dl(0x1c, (width, 23, 12), (height, 11, 0))

    def scissor_xy (self, x, y):
        self._dl(0x1b, (x, 21, 11), (y, 10, 0))

    def stencil_func (self, func, ref, mask):
        self._dl(0x0a, (func, 19, 16), (ref, 15, 8), (mask, 7, 0))

    def stencil_mask (self, mask):
        self._dl(0x13, (mask, 7, 0))

    def stencil_op (self, sfail, spass):
        self._dl(0x0c, (sfail, 5, 3), (spass, 2, 0))

    def tag (self, s):
        self._dl(0x03, (s, 7, 0))

    def tag_mask (self, mask):
        self._dl(0x14, (mask, 0))

    def vertex2f (self, x, y):
        self._dl(0x01, (x, 29, 15), (y, 14, 0))

    def vertex2ii (self, x, y, handle, cell):
        self._dl(0x02, (x, 29, 21), (y, 20, 12), (handle, 11, 7), (cell, 6, 0))

    def vertex_format (self, frac):
        self._dl(0x27, (frac, 2, 0))

    def vertex_translate_x (self, x):
        self._dl(0x2b, (x, 16, 0))

    def vertex_translate_y (self, y):
        self._dl(0x2b, (y, 16, 0))

