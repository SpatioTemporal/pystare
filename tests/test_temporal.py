import numpy 
import pystare 
import unittest

datetime = numpy.array(['1970-01-01T00:00:00', 
                        '2000-01-01T00:00:00', 
                        '2002-02-03T13:56:03.172', 
                        '2016-01-05T17:26:00.172'], dtype=numpy.datetime64)

def hex16(i):
    return "0x%016x"%i

class MainTest(unittest.TestCase):
    
    def test_fromutc_a(self):
        index = pystare.from_utc(datetime.astype(numpy.int64), 6, 6)
        # print(list(map(hex16,index)))
        expected = numpy.array([0x1ec8000008000619, 0x1f40000020000619, 0x1f484ade232b0619, 0x1f800916a42b0619])
        numpy.testing.assert_array_equal(index, expected)
    
    def test_fromutc_b(self):
        index = pystare.from_utc(datetime.astype(numpy.int64), 27, 27)
        # print(list(map(hex16,index)))
        expected = numpy.array([0x1ec8000008001b6d, 0x1f40000020001b6d, 0x1f484ade232b1b6d, 0x1f800916a42b1b6d])
        numpy.testing.assert_array_equal(index, expected)
        
    def test_toutc(self):
        index = numpy.array([0x1ec8000008001b6d, 0x1f40000020001b6d, 0x1f484ade232b1b6d, 0x1f800916a42b1b6d])
        datetime_x = pystare.to_utc_approximate(index)
        datetime_r = numpy.array(datetime_x, dtype='datetime64[ms]')
        numpy.testing.assert_array_equal(datetime, datetime_r)
        
    def test_utc_roundtrip(self):
        index = pystare.from_utc(datetime.astype(numpy.int64), 27, 27)
        datetime_x = pystare.to_utc_approximate(index)
        datetime_r = numpy.array(datetime_x, dtype='datetime64[ms]')
        numpy.testing.assert_array_equal(datetime, datetime_r)
        
    def test_epoch(self):
        datetime_x1 = datetime.astype(numpy.int64)
        index = pystare.from_utc(datetime_x1, 27, 27)
        datetime_x2 = pystare.to_utc_approximate(index)
        numpy.testing.assert_array_equal(datetime_x1, datetime_x2)
        
        
if __name__ == "__main__":
    unittest.main()

    
