import numpy
import pystare

lat = numpy.array([30, 45, 60], dtype=numpy.double)
lon = numpy.array([45, 60, 10], dtype=numpy.double)
indices1 = pystare.from_latlon(lat, lon, 12)
indices2 = numpy.array([0x100000000000000c], dtype=numpy.int64)


def test_issue79a():
    # This segfaults
    intersected = pystare.intersection(indices1, indices2, multi_resolution=True)


def test_issue79b():
    # This segfaults
    intersected = pystare.intersection(indices1, indices2, multi_resolution=False)


def test_issue79c():
    # This segfaults
    out_length = 2 * max(len(indices1), len(indices2))
    intersection = numpy.full([out_length], -1, dtype=numpy.int64)
    pystare.core._intersect_multiresolution(indices1, indices2, intersection)


def test_issue79d():
    # This segfaults
    out_length = 2 * max(len(indices1), len(indices2))
    intersection = numpy.full([out_length], -1, dtype=numpy.int64)
    pystare.core._intersect(indices1, indices2, intersection)


