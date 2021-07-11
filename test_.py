

import numpy as np
import pystare

if __name__ == '__main__':
    print('hello world')
    tivs = pystare.from_tai_iso_strings([
        "2003-02-13T12:00:00.000 (12 12) (1)"
        ,"2004-02-13T12:00:00.000 (12 12) (1)"
        ,"2004-03-13T12:00:00.000"
        ,"2004-04-13T12:00:00"
        ])
    print('tivs:      ',[hex(i) for i in tivs])
    print('type tivs: ',type(tivs))
    tais=pystare.to_tai_iso_strings(tivs)
    print('tais:      ',tais)
    # print('list tais: ',list(tais))
    t_triple = pystare.to_temporal_triple_tai(tivs)
    print('t_triple: ',t_triple,type(t_triple))
    for i in range(len(t_triple[0])):
        print(     hex(t_triple[0][i])
                  ,hex(t_triple[1][i])
                  ,hex(t_triple[2][i])
                  )

    del tivs
    tivs = pystare.from_tai_iso_strings([
        "2003-02-13T12:00:00.000 (12 12) (1)"
        ,"2004-02-13T12:00:00.000 (12 12) (1)"
        ,"2004-03-13T12:00:00.000"
        ,"2004-04-13T12:00:00"
        ])
    
    for i in range(len(t_triple[0])):
        print(t_triple[1][i],tivs[i])
        print(type(t_triple[1][i]),type(tivs[i]))
        # a = np.array([t_triple[0][i]],dtype=np.int64)
        a = np.array([tivs[i]],dtype=np.int64)
        print(a)
        print(type(a))
        res = pystare.to_tai_iso_strings(tivs)
        print(res)

    triple0 = pystare.from_tai_iso_strings(["2004-04-12T12:00:00","2004-04-13T12:00:00","2004-04-14T12:00:00"])
    print('triple0: ',triple0)
    print('    :    ',pystare.to_tai_iso_strings(triple0))
    tiv0    = pystare.from_temporal_triple(triple0)
    print('tiv0:    ',tiv0,type(tiv0),tiv0.shape)
    print('    :    ',pystare.to_tai_iso_strings(tiv0))
    try: del tmp
    except: pass
    tmp = np.array(pystare.to_temporal_triple_tai(tiv0),dtype=np.int64).flatten()
    print('    :     ',tmp)
    print('    :    ',pystare.to_tai_iso_strings(tmp))
    # print('    :    ',pystare.to_tai_iso_strings(pystare.to_temporal_triple_tai(tiv0).flatten()))
    
    triple1 = pystare.from_tai_iso_strings(["2004-04-13T00:00:00","2004-04-14T00:00:00","2004-04-15T00:00:00"])
    print('triple1: ',triple1)
    print('    :    ',pystare.to_tai_iso_strings(triple1))
    
    tiv1    = pystare.from_temporal_triple(triple1)
    print('tiv1:    ',tiv1)
    print('    :    ',pystare.to_tai_iso_strings(tiv1))
    # print('    :    ',pystare.to_tai_iso_strings(pystare.to_temporal_triple_tai(tiv1)))
    try: del tmp
    except: pass
    tmp = np.array(pystare.to_temporal_triple_tai(tiv1),dtype=np.int64).flatten()
    print('    :     ',tmp)
    print('    :    ',pystare.to_tai_iso_strings(tmp))
    
    union01     = pystare.temporalValueUnionIfOverlap(tiv0,tiv1)
    print('u01: ',union01)
    
    intersect01 = pystare.temporalValueIntersectionIfOverlap(tiv0,tiv1)
    print('i01: ',intersect01)



    
