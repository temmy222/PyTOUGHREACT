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

class t2block(object):
    """Grid block"""
    def __init__(self, name='     ', volume=1.0, blockrocktype=None, blockzone=None,
                 centre=None, atmosphere=False, ahtx=None, pmx=None,
                 nseq=None, nadd=None):
        self.zone = blockzone
        if blockrocktype is None: blockrocktype = rocktype()
        self.name = name
        self.volume = volume
        self.rocktype = blockrocktype
        if isinstance(centre, list): centre = np.array(centre)
        self.centre = centre
        self.atmosphere = atmosphere
        self.ahtx = ahtx
        self.pmx = pmx
        self.nseq, self.nadd = nseq, nadd
        self.connection_name = set([])