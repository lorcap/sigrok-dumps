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

from .signal import Signal
from .writer import VCDWriter
from .param import *

class HOST:
    '''Transaction types.'''
    CMD, MEM_READ, MEM_WRITE = range(3)

class Ft8xx (VCDWriter):
    '''Writer of FT8xx's SPI protocol in VCD format.'''

    def __init__ (self, file):
        self.cs   = Signal('CS'  , 's')
        self.clk  = Signal('CLK' , 'c')
        self.mosi = Signal('MOSI', 'o')
        self.miso = Signal('MISO', 'i')
        super().__init__((self.cs, self.clk, self.mosi, self.miso), file)

        self._addr = None # current memory address
        self._host = None # transaction type

        self.cs  .change(1)
        self.clk .change(0)
        self.mosi.change(1)
        self.miso.change(1)
        self._dump()
        self.ts += self.CLK_T/2

    def write (self, mosi, miso = None):
        '''Write out a sequence of MISO/MOSI bytes.'''
        size = len(mosi)
        if miso == None:
            miso = (0xff,) * size
        else:
            assert size == len(miso)

        for i in range(size):
            for b in reversed(range(8)):
                self.clk.change(0)
                self.mosi.change(mosi[i] & 2**b)
                self.miso.change(miso[i] & 2**b)
                self.ts += self.CLK_T/2
                self.clk.change(1)
                self.ts += self.CLK_T/2

        self.mosi.change(1)
        self.miso.change(1)
        self.ts += self.CLK_T/2

    ### Memory read/write ####################################################

    def mem_read (self, addr):
        '''Begin reading memory.'''
        assert 0 <= addr <= 0x3fffff
        if self.mem_begin(read=addr):
            self.addr(addr)
            self.dummy()

    def mem_write (self, addr):
        '''Begin writing memory.'''
        assert 0 <= addr <= 0x3fffff
        if self.mem_begin(write=addr):
            self.addr(addr)

    def mem_begin (self, *, write=None, read=None):
        '''Begin a transaction if needed.'''
        if write != None:
            addr = write
            host = HOST.MEM_WRITE
        elif read != None:
            addr = read
            host = HOST.MEM_READ
        else:
            assert False

        if self._host == host and self._addr == addr:
            return False

        self.mem_end()
        self.cs.change(0)
        self._host = host
        self._addr = addr
        return True

    def mem_end (self):
        '''End a transaction.'''
        if self._host != None:
            self.cs  .change(1)
            self.clk .change(0)
            self.mosi.change(1)
            self.miso.change(1)
            self.ts += 2*self.CLK_T
            self._addr = None
            self._host = None

    def addr (self, addr_):
        '''Write out a memory address.'''
        if self._host == HOST.MEM_WRITE:
            addr_ |= 0x800000
        elif self._host == HOST.MEM_READ:
            pass
        else:
            assert False

        mosi = tuple(addr(addr_))
        miso = tuple(addr(0x004a43))
        self.write(mosi, miso)

    def dummy (self):
        '''Write out a dummy byte.'''
        mosi = tuple(int8(0xff))
        miso = tuple(int8(0x42))
        self.write(mosi, miso)

    def data (self, mosi, miso=None):
        '''Write out memory data.'''
        self.write(mosi, miso)
        if 0x308000 <= self._addr <= 0x308fff:
            # RAM_CMD
            self._addr = (self._addr + len(mosi)) & 0x308fff
        elif self._addr == 0x302578:
            # REG_CMDB_WRITE
            pass
        else:
            self._addr += len(mosi)

