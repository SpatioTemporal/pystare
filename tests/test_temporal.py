import numpy 
import pystare 
import unittest

datetime = numpy.array(['1970-01-01T00:00:00', 
                        '2000-01-01T00:00:00', 
                        '2002-02-03T13:56:03.172', 
                        '2016-01-05T17:26:00.172'], dtype=numpy.datetime64)

class MainTest(unittest.TestCase):
    
    def test_fromutc_a(self):
        index = pystare.from_utc(datetime.astype(numpy.int64), 6)
        expected = numpy.array([34656606509596698, 35184372097220634, 35220842678627354, 35466003203795994])
        numpy.testing.assert_array_equal(index, expected)
    
    def test_fromutc_b(self):
        index = pystare.from_utc(datetime.astype(numpy.int64), 27)
        expected = numpy.array([34656606509596782, 35184372097220718, 35220842678627438, 35466003203796078])
        numpy.testing.assert_array_equal(index, expected)
        
    def test_toutc(self):
        index = numpy.array([34656606509596782, 35184372097220718, 35220842678627438, 35466003203796078])
        datetime_x = pystare.to_utc_approximate(index)
        datetime_r = numpy.array(datetime_x, dtype='datetime64[ms]')
        numpy.testing.assert_array_equal(datetime, datetime_r)
        
    def test_utc_roundtrip(self):
        index = pystare.from_utc(datetime.astype(numpy.int64), 27)
        datetime_x = pystare.to_utc_approximate(index)
        datetime_r = numpy.array(datetime_x, dtype='datetime64[ms]')
        numpy.testing.assert_array_equal(datetime, datetime_r)
        
    def test_epoch(self):
        datetime_x1 = datetime.astype(numpy.int64)
        index = pystare.from_utc(datetime_x1, 27)
        datetime_x2 = pystare.to_utc_approximate(index)
        numpy.testing.assert_array_equal(datetime_x1, datetime_x2)
        
        
        
