import numpy as np
import pystare
import unittest


def print_(x,flag=False):
    if flag:
        print(x)


class MainTest(unittest.TestCase):

    def test_a(self):

        print_(('hello world'))
        index1 = pystare.from_stare_timestrings([
            "2003-02-13T12:00:00.000 (12 12) (1)",
            "2004-02-13T12:00:00.000 (12 12) (1)"
             ])

        index2 = pystare.from_iso_strings([
            "2004-03-13T12:00:00.000",
            "2004-04-13T12:00:00.0"
            ])

        tivs = np.append(index1, index2)

        print_(('tivs:      ',[hex(i) for i in tivs]))
        print_(('type tivs: ',type(tivs)))
        tais = pystare.to_stare_timestring(tivs)
        print_(('tais:      ',tais))
        # print_(('list tais: ',list(tais)))
        t_triple = pystare.to_temporal_triple_tai(tivs)
        print_(('t_triple: ',t_triple,type(t_triple)))
        for i in range(len(t_triple[0])):
            print_((     hex(t_triple[0][i])
                      ,hex(t_triple[1][i])
                      ,hex(t_triple[2][i])
                      ))
    
        del tivs
        index1 = pystare.from_stare_timestrings([
            "2003-02-13T12:00:00.000 (12 12) (1)",
            "2004-02-13T12:00:00.000 (12 12) (1)"
             ])

        index2 = pystare.from_iso_strings([
            "2004-03-13T12:00:00.000",
            "2004-04-13T12:00:00.0"
            ])

        tivs = np.append(index1, index2)
        
        for i in range(len(t_triple[0])):
            print_((t_triple[1][i],tivs[i]))
            print_((type(t_triple[1][i]),type(tivs[i])))
            # a = np.array([t_triple[0][i]],dtype=np.int64)
            a = np.array([tivs[i]],dtype=np.int64)
            print_((a))
            print_((type(a)))
            res = pystare.to_stare_timestring(tivs)
            print_((res))
    
        print_(())
        tiv = 2256562898056779093
        tiv_lb_ms = pystare.lower_bound_ms(np.array([tiv], dtype=np.int64))
        tiv_lb_tai = pystare.lower_bound_tai(np.array([tiv], dtype=np.int64))


        print_(('tiv type: ',type(tiv)))
        print_(('lb type ms:  ',type(tiv_lb_ms)))

        print_(('tiv:    ',hex(tiv)))    
        print_(('lb ms:  ',list(map(hex,tiv_lb_ms))))    
        print_(('lb tai: ',list(map(hex,tiv_lb_tai))))    
        print_(('tiv:    ',pystare.to_stare_timestring([tiv])))
        print_(('lb ms:  ',pystare.to_stare_timestring(tiv_lb_ms)))
        print_(('lb tai: ',pystare.to_stare_timestring(tiv_lb_tai)))
        triple = pystare.to_temporal_triple_tai(np.array([tiv],dtype=np.int64))
        print_(('trp:  ',triple))    
        print_(('   :  ',list(map(lambda x: hex(x[0]),triple))))    
        print_((' iso: ',list(map(pystare.to_stare_timestring, triple))))
        print_((' iso: ',pystare.to_stare_timestring(np.array(triple).flatten())))
    
        triple0 = pystare.from_iso_strings(["2004-04-12T12:00:00", "2004-04-13T12:00:00", "2004-04-14T12:00:00"])
        print_(())    
        print_(('triple0: ',triple0))
        print_(('    :    ',pystare.to_stare_timestring(triple0)))
        tiv0    = pystare.from_temporal_triple(triple0)
        print_(('tiv0:    ',tiv0,type(tiv0),tiv0.shape))
        print_(('    :    ',pystare.to_stare_timestring(tiv0)))

        tmp = np.array(pystare.to_temporal_triple_tai(tiv0),dtype=np.int64).flatten()
        print_(('    :     ',tmp))
        print_(('    :    ',pystare.to_stare_timestring(tmp)))
        # print_(('    :    ',pystare.to_tai_iso_strings(pystare.to_temporal_triple_tai(tiv0).flatten()))
        
        triple1 = pystare.from_iso_strings(["2004-04-13T00:00:00", "2004-04-14T00:00:00", "2004-04-15T00:00:00"])
        print_(())
        print_(('triple1: ',triple1))
        print_(('    :    ',pystare.to_stare_timestring(triple1)))
        
        tiv1    = pystare.from_temporal_triple(triple1)
        print_(('tiv1:    ',tiv1))
        print_(('    :    ',pystare.to_stare_timestring(tiv1)))
        # print_(('    :    ',pystare.to_tai_iso_strings(pystare.to_temporal_triple_tai(tiv1))))
        try: del tmp
        except: pass
        tmp = np.array(pystare.to_temporal_triple_tai(tiv1),dtype=np.int64).flatten()
        print_(('    :     ',tmp))
        print_(('    :    ',pystare.to_stare_timestring(tmp)))
    
        print_(())
        overlap     = pystare.temporal_overlap(tiv0, tiv1)
        print_(('overlap:  ',overlap))
    
        union01     = pystare.temporal_value_union_if_overlap(tiv0, tiv1)
        print_(())
        print_(('u01: ',union01))
        print_(('u01: ',pystare.to_stare_timestring(union01)))
        
        intersect01 = pystare.temporal_value_intersection_if_overlap(tiv0, tiv1)
        print_(())
        print_(('i01: ',intersect01))
        print_(('i01: ',pystare.to_stare_timestring(intersect01)))
    
        datetime = np.array(['1970-01-01T00:00:00', 
                                 '2000-01-01T00:00:00', 
                                 '2002-02-03T13:56:03.172', 
                                 '2016-01-05T17:26:00.172'], dtype=np.datetime64)
    
        forward_res = np.array([21,
                                       21,
                                       21,
                                       21], dtype=np.int64)
    
        reverse_res = np.array([22,
                                       22,
                                       22,
                                       22], dtype=np.int64)
    
        global_flag = False # True
        del tivs
        tivs = pystare.from_utc_variable(datetime.astype(np.int64),forward_res,reverse_res)
        print_(('tivs iso:    ',pystare.to_stare_timestring(tivs)), flag=global_flag)
        dt_utc = np.array(pystare.to_ms_since_epoch_utc(tivs), dtype='datetime64[ms]')
        print_(('dt_utc:      ',dt_utc.tolist()),flag=global_flag)
        print_(('dt_utc:      ',[np.datetime_as_string(i) for i in dt_utc]),flag=global_flag)
        print_(('dt_utc orig: ',[np.datetime_as_string(i) for i in datetime]),flag=global_flag)
        print_(('tivs tai:    ',[i[0:-12] for i in pystare.to_stare_timestring(tivs)]), flag=global_flag)
    
        for s in zip([np.datetime_as_string(i) for i in datetime],[np.datetime_as_string(i) for i in dt_utc]):
            self.assertEqual(s[0],s[1])

        # Regression
        for s in zip(['1970-01-01T00:00:08.000', '2000-01-01T00:00:32.000', '2002-02-03T13:56:35.172', '2016-01-05T17:26:36.172'],
                     pystare.to_stare_timestring(tivs)):
            self.assertEqual(s[0],s[1][0:-12])
            
if __name__ == '__main__':
    unittest.main()
