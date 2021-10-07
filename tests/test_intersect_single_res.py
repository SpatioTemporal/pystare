# Visualize test_intersect_single_res seen in test_intersections.py

import pystare
import matplotlib.tri
import numpy


def test_intersect_single_res():
    resolution = 6
    resolution0 = resolution
    lat0 = numpy.array([10, 5, 60, 70], dtype=numpy.double)
    lon0 = numpy.array([-30, -20, 60, 10], dtype=numpy.double)
    hull0 = pystare.cover_from_hull(lat0, lon0, resolution0)

    lons0, lats0, intmat0 = pystare.triangulate_indices(hull0)
    triang0 = matplotlib.tri.Triangulation(lons0, lats0, intmat0)

    resolution1 = 6
    lat1 = numpy.array([10, 20, 30, 20], dtype=numpy.double)
    lon1 = numpy.array([-60, 60, 60, -60], dtype=numpy.double)
    hull1 = pystare.cover_from_hull(lat1, lon1, resolution1)

    lons1, lats1, intmat1 = pystare.triangulate_indices(hull1)
    triang1 = matplotlib.tri.Triangulation(lons1, lats1, intmat1)

    intersectedFalse = pystare.intersection(hull0, hull1, multi_resolution=False)
    intersectedTrue = pystare.intersection(hull0, hull1, multi_resolution=True)

    lonsF, latsF, intmatF = pystare.triangulate_indices(intersectedFalse)
    triangF = matplotlib.tri.Triangulation(lonsF, latsF, intmatF)

    lonsT, latsT, intmatT = pystare.triangulate_indices(intersectedTrue)
    triangT = matplotlib.tri.Triangulation(lonsT, latsT, intmatT)

    if True:
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
        # See examples/test_intersect_single_res.py

        assert len(intersected) == 77

        r01.purge()
        n01 = r01.get_size_as_values()

        assert 0 == n01

        r01.reset()
        r01.add_intersect(r0, r1, True)

        n01 = r01.get_size_as_values()
        assert n01 == 79

        intersected = numpy.zeros([n01], dtype=numpy.int64)
        r01.copy_values(intersected)

        lonsRT, latsRT, intmatRT = pystare.triangulate_indices(intersected)
        triangRT = matplotlib.tri.Triangulation(lonsRT, latsRT, intmatRT)


        lonsRT_, latsRT_, intmatRT_ = pystare.triangulate_indices(intersected[51:55])
        triangRT_ = matplotlib.tri.Triangulation(lonsRT_, latsRT_, intmatRT_)






