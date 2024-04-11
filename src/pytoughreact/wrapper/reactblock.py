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
from t2data import rocktype
import numpy as np


class T2Block(object):
    """Grid block"""
    def __init__(self, name='     ', volume=1.0, blockrocktype=None, blockzone=None,
                 centre=None, atmosphere=False, ahtx=None, pmx=None,
                 nseq=None, nadd=None):
        """ Initialization of parameters

        Parameters
        -----------
        name : string
            Name of the block
        volume : float
            Volume associated with the block
        blockrocktype : rocktype
            Rock type of the block
        blockzone : t2zone
            Zone the block is associated with
        centre : float
            Center of the block
        atmosphere: boolean
            If atmosphere present in block or not
        ahtx: float
            Interface area (m2) for linear heat exchange with semi-infinite confining
            bed
        pmx : float
            Block-by-block permeability modification coefficient
        nseq : int
            Number of additional elements having the same volume and belonging to
            the same reservoir domain
        nadd : int
            Increment between the code numbers of two successive elements

        Returns
        --------

        """
        self.zone = blockzone
        if blockrocktype is None:
            blockrocktype = rocktype()
        self.name = name
        self.volume = volume
        self.rocktype = blockrocktype
        if isinstance(centre, list):
            centre = np.array(centre)
        self.centre = centre
        self.atmosphere = atmosphere
        self.ahtx = ahtx
        self.pmx = pmx
        self.nseq, self.nadd = nseq, nadd
        self.connection_name = set([])
