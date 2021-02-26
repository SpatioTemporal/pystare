import numpy 
import pystare 
import unittest

from sids import sids

class MainTest(unittest.TestCase):
    
    def test_make_srange1000(self):
        sids = sids[0:1000]
        srange = pystare.srange(sids)
        
    def test_make_srange10000(self)
        sids = sids[0:1000]
        srange = pystare.srange(sids)
        
    def test_collapse1(self):
        # parent with 4 children 
        sids = numpy.array([0x300a300000000009,
                            0x300a30000000000a,
                            0x300a30800000000a,
                            0x300a31000000000a,
                            0x300a31800000000a])
        ivs = pystare.to_compressed_range(sids.flatten())
        indices = numpy.zeros([srange.get_size_as_values()], dtype=numpy.int64)
        srange.copy_values(indices)
        self.assertEqual()
