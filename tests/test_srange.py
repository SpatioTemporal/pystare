import numpy 
import pystare 
import unittest


class MainTest(unittest.TestCase):
    
    def test_make_srange1000(self):
        from tests.sids import sids
        sids = sids[0:1000]
        srange = pystare.srange(sids)
        
    def test_make_srange10000(self):
        from tests.sids import sids
        sids = sids[0:10000]
        srange = pystare.srange(sids)
        
    def test_collapse1(self):
        # parent with 4 children 
        sids = numpy.array([0x300a300000000009,
                            0x300a30000000000a,
                            0x300a30800000000a,
                            0x300a31000000000a,
                            0x300a31800000000a])
        ivs = pystare.to_compressed_range(sids.flatten())
        #indices = numpy.zeros([srange.get_size_as_values()], dtype=numpy.int64)
        #srange.copy_values(indices)
        with self.subTest():
            self.assertEqual(ivs.size, 1)
        with self.subTest():    
            self.assertEqual(hex(ivs[0]), '0x300a300000000009')
        
    def test_collapse2(self):
        # parent with same ancestor
        sids = numpy.array([0x300a30000000000a,
                            0x300a30800000000a,
                            0x300a31000000000a,
                            0x300a31800000000a])
        ivs = pystare.to_compressed_range(sids.flatten())
        #indices = numpy.zeros([srange.get_size_as_values()], dtype=numpy.int64)
        #srange.copy_values(indices)
        with self.subTest():
            self.assertEqual(ivs.size, 1)
        with self.subTest():    
            self.assertEqual(hex(ivs[0]), '0x300a300000000009')
            
    def test_multires_intersect1(self):
        # Earth are the 8 initial trixels
        earth = numpy.array([0x0000000000000000, 0x0800000000000000, 0x1000000000000000, 
                             0x1800000000000000, 0x2000000000000000, 0x2800000000000000,
                             0x3000000000000000, 0x3800000000000000])
        sids = numpy.array([0x300a30000000000a, 0x300a30800000000a, 0x300a31000000000a, 0x300a31800000000a])
        indices = pystare.intersect(earth, sids, multiresolution=True)
        ivs = indices
        with self.subTest():
            self.assertEqual(ivs.size, 1)
        with self.subTest():    
            self.assertEqual(hex(ivs[0]), '0x300a300000000009')
            
    def test_multires_intersect2(self):
        sids = numpy.array([0x300a30000000000a, 0x300a30800000000a, 0x300a31000000000a, 0x300a31800000000a])
        parent = pystare.expand_intervals(sids, resolution=9)
        indices = pystare.intersect(parent, sids)
        ivs = indices
        with self.subTest():
            self.assertEqual(ivs.size, 1)
        with self.subTest():    
            self.assertEqual(hex(ivs[0]), '0x300a300000000009')
        
