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

import datetime

class VCDWriter:
    '''Write a VCD file.'''

    CLK_T = 2 # clock period

    def __init__ (self, signals, file):
        self._ofile = file
        self._signals = signals
        self._timestamp = 0

        date = str(datetime.datetime.now())
        self._print(f'$date {date} $end',
                    f'$timescale 1 ns $end',
                    f'$scope module spi $end')
        for s in signals:
            self._print(f'$var wire 1 {s.symbol} {s.name} $end')
        self._print(f'$upscope $end',
                    f'$enddefinitions $end')

    @property
    def timestamp (self):
        return self._timestamp

    @timestamp.setter
    def timestamp (self, val):
        val = int(val)
        assert val >= self._timestamp

        if val > self._timestamp:
            self._dump()
            self._timestamp = val

    @property
    def ts (self):
        return self.timestamp

    @ts.setter
    def ts (self, val):
        self.timestamp = val

    def _print (self, *lines):
        '''Print lines to output file.'''
        print(*lines, sep='\n', file=self._ofile)

    def _change (self, signal, timestamp, val):
        '''Record a signal change (if any).'''
        assert timestamp >= self._timestamp

        if timestamp > self._timestamp:
            self._dump()
            self._timestamp = timestamp

        val_str = signal.change(val)
        if val_str:
            self._changes.append(val_str)

    def _dump (self):
        '''Dump accumulated changes.'''
        changes = []
        for s in self._signals:
            d = s.dump()
            if d:
                changes.append(d)

        changes = ' '.join(changes)
        if changes:
            self._print(f'#{self._timestamp} {changes}')

    def __enter__ (self):
        return self

    def __exit__ (self, exc_type, exc_val, exc_tb):
        self.close()

    def close (self):
        self._dump()
        self.ts += 2*self.CLK_T
        self._print(f'#{self._timestamp}')
        self._ofile.flush()

