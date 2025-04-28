import pystare
import numpy


def test_intersect_single_res():
    resolution = 6
    resolution0 = resolution
    lat0 = numpy.array([10, 5, 60, 70], dtype=numpy.double)
    lon0 = numpy.array([-30, -20, 60, 10], dtype=numpy.double)
    hull0 = pystare.cover_from_hull(lat0, lon0, resolution0)

    resolution1 = 6
    lat1 = numpy.array([10, 20, 30, 20], dtype=numpy.double)
    lon1 = numpy.array([-60, 60, 60, -60], dtype=numpy.double)
    hull1 = pystare.cover_from_hull(lat1, lon1, resolution1)

    r0 = pystare.core.srange()
    r0.add_intervals(hull0)

    r1 = pystare.core.srange()
    r1.add_intervals(hull1)

    r01 = pystare.core.srange()
    r01.add_intersect(r0, r1, False)
    n01 = r01.get_size_as_values()

    assert n01 == 77

    intersected = numpy.zeros([n01], dtype=numpy.int64)
    r01.copy_values(intersected)

    assert len(intersected) == 77

    r01.purge()
    n01 = r01.get_size_as_values()

    assert 0 == n01

    r01.reset()
    r01.add_intersect(r0, r1, True)

    n01 = r01.get_size_as_values()
    assert n01 == 79
