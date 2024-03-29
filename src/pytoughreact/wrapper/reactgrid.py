'''
MIT License

Copyright (c) [2022] [Temitope Ajayi]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

'''

from t2grids import t2grid
from pytoughreact.wrapper.reactzone import t2zone
from pytoughreact.wrapper.reactblock import t2block
from t2data import rocktype


class t2reactgrid(t2grid):
    def __init__(self):
        self.empty()
        super().__init__()

    def get_num_zones(self):
        return len(self.zonelist)
    num_zones = property(get_num_zones)

    def fromgeo(self, geo, blockmap={}):
        """Converts a MULgraph grid to a TOUGH2 grid. The blockmap parameter
        applies an optional mapping to the block names from the geometry.
        """
        self.empty()
        self.add_rocktype(rocktype())  # add default rock type
        self.add_blocks(geo, blockmap)
        self.add_connections(geo, blockmap)
        return self

    def __add__(self, other):
        """Adds two grids together."""
        result = t2reactgrid()
        for grid in [self, other]:
            for rt in grid.rocktypelist:
                result.add_rocktype(rt)
            for blk in grid.blocklist:
                result.add_block(blk)
            for con in grid.connectionlist:
                result.add_connection(con)
        return result

    def empty(self):
        """Empties a TOUGH2 grid"""
        self.rocktypelist = []
        self.blocklist = []
        self.connectionlist = []
        self.rocktype = {}
        self.block = {}
        self.connection = {}
        self.zone = {}
        self.zonelist = []

    def add_block(self, newblock=None):
        """Adds a block to the grid"""
        if newblock is None:
            newblock = t2block()
        if newblock.name in self.block:
            i = self.blocklist.index(self.block[newblock.name])
            self.blocklist[i] = newblock
        else:
            self.blocklist.append(newblock)
        self.block[newblock.name] = newblock

    def add_zone(self, newzone=None):
        """Adds a rock type to the grid.  Any existing rocktype of the same name is replaced."""
        if newzone is None:
            newzone = t2zone()
        if newzone.name in self.zone:
            i = self.zonelist.index(self.zone[newzone.name])
            self.zonelist[i] = newzone
        else:
            self.zonelist.append(newzone)
        self.zone[newzone.name] = newzone

    def __repr__(self):
        return str(self.num_rocktypes) + ' rock types; ' + str(self.num_zones) + ' zones; ' + str(self.num_blocks) + ' blocks; ' + str(self.num_connections) + ' connections'
