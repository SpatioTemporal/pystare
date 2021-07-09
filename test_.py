

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
    print('t_triple: ',t_triple)
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

