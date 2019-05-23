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

class Signal:
    '''1-bit signal.'''

    def __init__ (self, name, symbol):
        self._name = name
        self._symbol = symbol
        self._val = None
        self._old = None

    def __repr__ (self):
        return f'{self.val}{self.symbol}'

    def dump (self):
        if self._old != self._val:
            self._old = self._val
            return repr(self)
        else:
            return None

    @property
    def name (self):
        return self._name

    @property
    def symbol (self):
        return self._symbol

    @property
    def val (self):
        return '1' if self._val else '0'

    def change (self, val):
        self._val = val

