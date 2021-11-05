import pystare
import numpy


def test_issue84():
    lon = numpy.array([130.78000366004676, 130.78000485358513, 130.78000735893113])
    lat = numpy.array([42.220007813203225, 42.22001036108258, 42.22000722916885])
    # The following segfault
    pystare.cover_from_hull(lon, lat, level=5)
