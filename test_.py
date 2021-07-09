


import pystare

if __name__ == '__main__':
    print('hello world')
    tivs = pystare.from_tai_iso_strings([
        "2003-02-13T12:00:00.000 (12 12) (1)"
        ,"2004-02-13T12:00:00.000 (12 12) (1)"
        ,"2004-03-13T12:00:00.000"
        ,"2004-04-13T12:00:00"
        ])
    print('tivs: ',[hex(i) for i in tivs])
    
    tais=pystare.to_tai_iso_strings(tivs)
    print('tais:      ',tais)

    print('list tais: ',list(tais))
    
