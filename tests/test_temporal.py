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

    def test_from_julian_tai(self):
        datetime_x1 = datetime.astype(numpy.int64)
        index = pystare.from_utc(datetime_x1, 27, 27)
        numpy.testing.assert_array_equal(index,numpy.array([0x1ec8000008001b6d, 0x1f40000020001b6d, 0x1f484ade232b1b6d, 0x1f800916a42b1b6d],dtype=numpy.int64))
        j_tai1,j_tai2 = pystare.to_JulianTAI(index)
        # [2440587.5 2451544.5 2452275.5 2457388.5]
        # [9.25925926e-05 3.70370370e-04 3.35809626e+01 4.72680755e+00]        
        index1 = pystare.from_JulianTAI(j_tai1,j_tai2)
        numpy.testing.assert_array_equal(index1,numpy.array([0x1ec8000008000001, 0x1f40000020000001, 0x1f484ade232b0001, 0x1f800916a42b0001],dtype=numpy.int64))

    def test_from_julian_utc(self):
        datetime_x1 = datetime.astype(numpy.int64)
        index = pystare.from_utc(datetime_x1, 27, 27)
        numpy.testing.assert_array_equal(index,numpy.array([0x1ec8000008001b6d, 0x1f40000020001b6d, 0x1f484ade232b1b6d, 0x1f800916a42b1b6d],dtype=numpy.int64))
        j_utc1,j_utc2 = pystare.to_JulianUTC(index)
        # [2440587.5 2451544.5 2452275.5 2457388.5]
        # [-9.49073951e-10  1.61546124e-17  3.35805923e+01  4.72639088e+00]
        index1 = pystare.from_JulianUTC(j_utc1,j_utc2)
        numpy.testing.assert_array_equal(index1,numpy.array([0x1ec8000008000001, 0x1f40000020000001, 0x1f484ade232b0001, 0x1f800916a42b0001],dtype=numpy.int64))

    def test_resolutions(self):
        datetime_x1 = datetime.astype(numpy.int64)
        index = pystare.from_utc(datetime_x1, 20, 30)
        res_r = numpy.zeros(index.shape,dtype=numpy.int64)
        res_r[:] = pystare.reverse_resolution(index)
        numpy.testing.assert_array_equal(res_r,numpy.array([30,30,30,30],dtype=numpy.int64))
        res_f = numpy.zeros(index.shape,dtype=numpy.int64)
        res_f[:] = pystare.forward_resolution(index)
        numpy.testing.assert_array_equal(res_f,numpy.array([20,20,20,20],dtype=numpy.int64))
        # print('res_f: ',res_f)

        res_r[:] = pystare.set_reverse_resolution(index,numpy.array([1,2,3,4],dtype=numpy.int64))
        numpy.testing.assert_array_equal(pystare.reverse_resolution(res_r),numpy.array([ 1, 2, 3, 4],dtype=numpy.int64))
        numpy.testing.assert_array_equal(pystare.forward_resolution(res_r),numpy.array([20,20,20,20],dtype=numpy.int64))
        
        # print('res r: ',pystare.reverse_resolution(res_r))
        # print('res f: ',pystare.forward_resolution(res_r))

        res_f[:] = pystare.set_forward_resolution(index,numpy.array([4,3,2,1],dtype=numpy.int64))
        numpy.testing.assert_array_equal(pystare.reverse_resolution(res_f),numpy.array([30,30,30,30],dtype=numpy.int64))
        numpy.testing.assert_array_equal(pystare.forward_resolution(res_f),numpy.array([ 4, 3, 2, 1],dtype=numpy.int64))

        # print('res r: ',pystare.reverse_resolution(res_f))
        # print('res f: ',pystare.forward_resolution(res_f))
        
if __name__ == "__main__":
    unittest.main()

    
