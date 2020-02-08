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

def bit (val, msb, lsb = None):
    '''Mask integer `val` from bit `msb` to bit `lsb` inclusive (counting from 0).'''
    if lsb == None:
        lsb = msb
    mask = 2**(msb + 1 - lsb) - 1
    return (val & mask) << lsb

def bit2int (*bit_list):
    '''Calculate an integer by or-ing a list of (val, msb, lsb).'''
    ret = 0
    for b in bit_list:
        ret += bit(*b)
    return ret

def _byte (val, range_):
    '''Generate a byte sequence in `range_` order out of integer `val`.'''
    if val != None:
        size = len(range_)
        val = int(val) & 2**(8*size) - 1
        byte = bytes.fromhex(f'{val:0{2*size}x}')
        for i in range_:
            yield byte[i]

def char (string):
    '''Generate a null-terminated sequence of chars.'''
    for c in bytes(string, 'utf8'):
        yield c
    yield 0

def addr (val):
    '''Generate a 3-byte memory address out of integer `val`.'''
    yield from _byte(val, range(3))

def int8 (*val):
    '''Generate a 1-byte sequence for each integer in `val`.'''
    for v in val:
        yield from _byte(v, range(0, -1, -1))

def int16 (*val):
    '''Generate a 2-byte sequence for each integer in `val`.'''
    for v in val:
        yield from _byte(v, range(1, -1, -1))

def int32 (*val):
    '''Generate a 4-byte sequence for each integer in `val`.'''
    for v in val:
        yield from _byte(v, range(3, -1, -1))

