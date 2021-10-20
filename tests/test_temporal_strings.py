import pystare
from astropy import time  # doctest: +SKIP


def test_temporal():
    timestamps = ['2021-09-26T17:16:46.426092', '2020-09-26T17:16:46.426092']
    t = time.Time(timestamps, format='isot')

    tivs = pystare.from_julian_date(t.jd1, t.jd2, scale='tai')

    jds = pystare.to_julian_date(tivs, scale='tai')
    t = time.Time(jds[0], jds[1], format='jd', scale='tai')


