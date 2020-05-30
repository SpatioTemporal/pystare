import numpy 
import pystare 
import unittest

lat = numpy.array([30,45,60], dtype=numpy.double)
lon = numpy.array([45,60,10], dtype=numpy.double)

class MainTest(unittest.TestCase):
    
    def test__intersect(self):        
        indices = pystare.from_latlon(lat, lon, 12)
        intersected = numpy.zeros([3], dtype=numpy.int64)
        pystare._intersect(indices, indices, intersected)
        expected = numpy.array([3643626709468577804, 4151504977312874508, 4161865159985332236])
        numpy.testing.assert_array_equal(intersected, expected)
        
    def test_intersect(self):
        indices = pystare.from_latlon(lat, lon, 12)
        intersected = pystare.intersect(indices, indices)        
        expected = numpy.array([3643626709468577804, 4151504977312874508, 4161865159985332236])
        numpy.testing.assert_array_equal(intersected, expected)
        
    def test_intersect_multires(self):
        indices = pystare.from_latlon(lat, lon, 12)
        intersected = pystare.intersect(indices, indices, multiresolution=True)
        expected = numpy.array([3643626709468577804, 4151504977312874508, 4161865159985332236])
        numpy.testing.assert_array_equal(intersected, expected)

    def test_intersect_multires2(self):
        indices1 = pystare.from_latlon(lat, lon, 12)
        indices2 = numpy.array([indices1[1]], dtype=numpy.int64)
        intersected = pystare.intersect(indices1, indices2, multiresolution=True)
        expected = numpy.array([4161865159985332236])
        numpy.testing.assert_array_equal(intersected, expected)
        
    def test_intersect_multires3(self):
        indices1 = pystare.from_latlon(lat, lon, 12)
        indices2 = numpy.array([0x100000000000000c], dtype=numpy.int64)
        intersected = pystare.intersect(indices1, indices2, multiresolution=True)
        numpy.testing.assert_array_equal(intersected, numpy.array([], dtype=numpy.int64))
        
    def test_intersect_single_res(self):
        resolution = 6
        resolution0 = resolution
        lat0 = numpy.array([ 10, 5, 60,70], dtype=numpy.double)
        lon0 = numpy.array([-30,-20,60,10], dtype=numpy.double)
        hull0 = pystare.to_hull_range_from_latlon(lat0, lon0, resolution0)
                                              
        resolution1 = 6
        lat1 = numpy.array([10,  20, 30, 20 ], dtype=numpy.double)
        lon1 = numpy.array([-60, 60, 60, -60], dtype=numpy.double)
        hull1 = pystare.to_hull_range_from_latlon(lat1, lon1, resolution1)

        intersectedFalse = pystare.intersect(hull0, hull1, multiresolution=False)
        intersectedTrue  = pystare.intersect(hull0, hull1, multiresolution=True)

        # See examples/test_intersect_single_res.py
        self.assertEqual(328, len(intersectedFalse))
        self.assertEqual(172, len(intersectedTrue))
        
    def test_intersect_repetition(self):
        a = [4114022797720682508, 4505997421712506892, 4505997834029367308, 4505997868389105676, 4505998418144919564]
        b = [4528191461944221900, 4505997456072245260]
        for i in range(1, 10000):        
            pystare.intersect(a, b)
        self.assertTrue(True)

    def test_intersect_range_single_res(self):
        resolution = 6
        resolution0 = resolution
        lat0 = numpy.array([ 10, 5, 60,70], dtype=numpy.double)
        lon0 = numpy.array([-30,-20,60,10], dtype=numpy.double)
        hull0 = pystare.to_hull_range_from_latlon(lat0, lon0, resolution0)
                                              
        resolution1 = 6
        lat1 = numpy.array([10,  20, 30, 20 ], dtype=numpy.double)
        lon1 = numpy.array([-60, 60, 60, -60], dtype=numpy.double)
        hull1 = pystare.to_hull_range_from_latlon(lat1, lon1, resolution1)

        r0 = pystare.srange()
        r0.add_intervals(hull0)

        r1 = pystare.srange()
        r1.add_intervals(hull1)

        r01 = pystare.srange()
        r01.add_intersect(r0,r1,False)
        n01 = r01.get_size_as_values()

        self.assertEqual(328, n01)
        intersected = numpy.zeros([n01],dtype=numpy.int64)
        r01.copy_values(intersected)
        # See examples/test_intersect_single_res.py
        self.assertEqual(328, len(intersected))

        r01.purge()
        n01 = r01.get_size_as_values()
        self.assertEqual(0, n01)

        r01.reset()
        r01.add_intersect(r0,r1,True)
        n01 = r01.get_size_as_values()
        self.assertEqual(172, n01)
        
        intersected = numpy.zeros([n01],dtype=numpy.int64)
        r01.copy_values(intersected)
        # See examples/test_intersect_single_res.py
        self.assertEqual(172, len(intersected))

        iv = intersected[3]
        self.assertEqual(True,r01.contains(int(iv)))

        iv_max_plus = 4584664420663164934 + 100000000000000000
        self.assertEqual(False,r01.contains(int(iv_max_plus)))

        for i in range(int(len(intersected)/2)):
            intersected[int(2*i)] = int(4584664420663164934 + ( 100000000000000000 + 1000000 * i ))
        intersected1 = numpy.zeros(intersected.shape,dtype=numpy.int64)
        r0.acontains(intersected,intersected1,-1)
        for i in range(len(intersected)):
            # print(i,'i',intersected[i],intersected1[i])
            if i % 2 == 0:
                self.assertEqual(-1,intersected1[i])
            else:
                self.assertEqual(intersected[i],intersected1[i])
            

        # print('max intersected ',numpy.amax(intersected))
