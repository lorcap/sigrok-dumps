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

class Ft8xxHostCmd (Ft8xx):
    '''Writer of FT8xx's Host Commands in VCD format.

    For command references, see:
    - Document Reference No.: BRT_000220
    - Document Title: BT81X (815/6) Advanced Embedded Video Engine Datasheet
    - Version: 1.0
    - Date:
    - Chapter: 4.1.5 - Host Command
    - Pages: 15-18

    - Document Reference No.: BRT_000002
    - Document Title: FT81x (Advanced Embedded Video Engine)
    - Version: 1.4
    - Date:
    - Chapter: 4.1.5 - Host Command
    - Pages: 16-20

    - Document Reference No.: BRT_000039
    - Document Title: FT800 (Embedded Video Engine)
    - Version: 1.3
    - Date:
    - Chapter: 4.1.6 - Host Command
    - Pages: 14-15
    '''

    def cmd (self, byte1, *byte2, byte3=0x00):
        '''Write out a host command.'''
        if len(byte2) == 1 and isinstance(byte2[0], int):
            byte2 = ((byte2[0], 7, 0),)
        self.cs.change(0)
        mosi = (byte1, bit2int(*byte2), byte3)
        self.write(mosi)
        self.cs.change(1)
        self.ts += 2*self.CLK_T

    def active (self):
        self.cmd(0x00)

    def standby (self):
        self.cmd(0x41)

    def sleep (self):
        self.cmd(0x42)

    def pwrdown (self):
        self.cmd(0x43)

    def pwrdown2 (self):
        self.cmd(0x50)

    def pd_roms (self, roms):
        self.cmd(0x49, (roms, 7, 3))

    def clkext (self):
        self.cmd(0x44)

    def clkint (self):
        self.cmd(0x48)

    def clksel (self, pll, freq):
        self.cmd(0x61, (pll, 7, 6), (freq, 5, 0))

    def clksel2 (self, pll, freq):
        self.cmd(0x62, (pll, 7, 6), (freq, 5, 0))

    def rst_pulse (self):
        self.cmd(0x68)

    def pindrive (self, pin, strength):
        self.cmd(0x70, (pin, 7, 2), (strength, 1, 0))

    def pin_pd_state (self, pin, setting):
        self.cmd(0x71, (pin, 7, 2), (setting, 1, 0))

