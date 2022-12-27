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