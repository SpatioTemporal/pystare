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

    def test_contains(self):
        datetime1 = numpy.array(['1970-01-01T00:00:00', 
                                 '2000-01-01T00:00:00', 
                                 '2002-02-03T13:56:03.172', 
                                 '2016-01-05T17:26:00.172'], dtype=numpy.datetime64)
        index1 = pystare.from_utc(datetime1.astype(numpy.int64), 20, 30)
        
        datetime2 = numpy.array(['1970-01-01T00:00:00', 
                                 '2000-01-01T00:00:00', 
                                 '2004-02-03T13:56:03.172', 
                                 '2000-01-05T17:26:00.172'], dtype=numpy.datetime64)
        index2 = pystare.from_utc(datetime2.astype(numpy.int64), 35, 35)

        cmp = numpy.zeros(index2.shape,dtype=numpy.int64)
        cmp[:] = pystare.temporalContainsInstant(index1,index2)
        # print('cmp: ',cmp)
        
        numpy.testing.assert_array_equal(numpy.array([1,1,0,0],dtype=numpy.int64),cmp)

    def test_variable_res(self):

        index = pystare.from_tai_iso_strings([
            "2003-02-13T12:00:00.000 (12 12) (1)"
            ,"2004-02-13T12:00:00.000 (12 12) (1)"
            ,"2004-03-13T12:00:00.000"
            ,"2004-04-13T12:00:00"
            ])
        
        ### print("index sh:   ",index.shape)
        ### index_with_variable_res = numpy.zeros(index.shape,dtype=numpy.int64)
        ### print("index:      ",index)
        ### print("index size: ",len(index))
        ### print("     :      ",pystare.to_tai_iso_strings(index))
        ### 
        ### i_varres_str = []
        ### ni = len(index)
        ### for i in range(ni):
        ###     tm = -1 if i-1 < 0 else index[i-1]
        ###     t0 = index[i]
        ###     tp = -1 if i+1 >= ni else index[i+1]
        ###     triple=[tm,t0,tp]
        ###     i_varres     = pystare.from_temporal_triple(triple,include_bounds=True)
        ###     i_varres_str = i_varres_str + [pystare.to_tai_iso_strings( numpy.concatenate(pystare.to_temporal_triple_tai(i_varres)))]
        ###     print(i,'index:    ',pystare.to_tai_iso_strings(index[i:i+1]))
        ###     print(i,'i_varres: ',pystare.to_temporal_triple_tai(i_varres))
        ###     print(i,'triple: %16x %16x %16x'%tuple(triple),pystare.to_tai_iso_strings(i_varres)[0]
        ###           ,' [ '
        ###           ,pystare.to_tai_iso_strings( numpy.concatenate(pystare.to_temporal_triple_tai(i_varres) ))
        ###           ,' ] '
        ###           )
        ### 
        ###     index_with_variable_res[i]=pystare.from_temporal_triple(triple,include_bounds=True)[0]
        ### del index_with_variable_res

        index_with_variable_res = pystare.set_temporal_resolutions_from_sorted(index)
        ### print(index_with_variable_res)
        ### for i in range(4):
        ###     print('--')
        ###     print(pystare.to_temporal_triple_tai(index[i:i+1]))
        ###     print(pystare.to_temporal_triple_tai(index_with_variable_res[i:i+1]))
        ###     print(pystare.to_tai_iso_strings( numpy.concatenate(pystare.to_temporal_triple_tai(index_with_variable_res[i:i+1]) )))
        ### print('//')
        i_varres_str = []
        ni = len(index)
        for i in range(ni):
             i_varres_str = i_varres_str + [pystare.to_tai_iso_strings( numpy.concatenate(pystare.to_temporal_triple_tai(index_with_variable_res[i:i+1]) ))]

        expected = [
            ['2003-02-13T11:59:59.999 (00 63) (1)', '2003-02-13T12:00:00.000 (12 48) (1)', '2004-02-13T12:00:00.000 (63 63) (1)']
            ,['2003-02-13T12:00:00.000 (00 63) (1)', '2004-02-13T12:00:00.000 (15 12) (1)', '2004-04-09T12:00:00.000 (63 63) (1)']
            ,['2004-01-17T12:00:00.000 (00 63) (1)', '2004-03-13T12:00:00.000 (15 15) (1)', '2004-05-08T12:00:00.000 (63 63) (1)']
            ,['2004-02-17T12:00:00.000 (00 63) (1)', '2004-04-13T12:00:00.000 (48 15) (1)', '2004-04-13T12:00:00.001 (63 63) (1)']
        ]
        self.assertEqual(ni,len(expected))
        for i in range(ni):
            for j in range(3):
                self.assertEqual(expected[i][j],i_varres_str[i][j])

if __name__ == "__main__":
    unittest.main()

    
