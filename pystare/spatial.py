import warnings
import pystare.core
import numpy


def from_latlon(lat, lon, level):
    """ Converts latitudes and longitudes to SIDs at the given level.

    Latitudes and longitudes have to be array-like.

    Parameters
    -----------
    lat: 1D array-like
        latitudes. Has to have same length as lon
    lon: 1D array-like
        longitudes. Has to have same length as lat
    level: int (0<=level<=27)
        level/resolution of the SIDs

    Returns
    --------
    sids: numpy 1D array
        stare index values

    Examples
    ----------
    >>> import pystare
    >>> lats = [34.4]
    >>> lons = [-119.7]
    >>> pystare.from_latlon(lat=lats, lon=lons, level=7)
    array([3331783833575763399])
    """
    if level < 0 or level > 27:
        raise pystare.exceptions.PyStareLevelError()
    sids = pystare.core._from_latlon(lat, lon, level)
    return sids


def from_lonlat(lon, lat, level):
    """ Converts longitudes and latitudes to SIDs at the given level.
    (c.f. :func:`~from_latlon`).

    Examples
    ----------
    >>> lats = [34.4]
    >>> lons = [-119.7]
    >>> pystare.from_lonlat(lon=lons, lat=lats, level=7)
    array([3331783833575763399])
    """
    sids = from_latlon(lat, lon, level)
    return sids


def from_latlon_2d(lat, lon, level=None, adapt_level=False, fill_value_in=None, fill_value_out=None):
    """Coverts latitudes and longitudes to SIDs.
    In contrary to :func:`~from_latlon`, this function accepts 2D arrays as latitude and longitude inputs.
    This is e.g. convenient to convert the geolocation of Level1/2 swath granules to SIDs.
    Additionally, this function allows to adapt the stare level of each generated SID to match the resolution of
    the geolocations.

    Parameters
    ------------
    lat: 2D array-like
        latitudes. Has to have same length as lon
    lon: 2D array-like
        longitudes. Has to have same length as lat
    level: int (0<=level<=27)
        level of the SIDs. If not set, level will me automatically adapted.
        If set, adapt_level will be set to false.
    adapt_level: bool
        if True, level will adapted to match resolution of lat/lon. Will overwrite level.
    fill_value_in: STARE indices are not calculated for lat/lon of this value
    fill_value_out: set indices to this value where lat/lon is fill_value_in

    Returns
    ---------
    sids: 2D numpy array
        stare index values

    Examples
    -----------
    >>> lats = numpy.array([[53.20177841, 53.20317078, 53.20351791], \
                            [53.29219437, 53.29222107, 53.29125977], \
                            [53.28958893, 53.29105759, 53.29147339]])
    >>> lons = numpy.array([[-15.9339962 , -16.2881012 , -16.62910461], \
                            [-15.93274784, -16.28762245, -16.62934113], \
                            [-15.93699169, -16.29188538, -16.63365936]])
    >>> pystare.from_latlon_2d(lats, lons, adapt_level=True)
    array([[4298473764500464809, 4298458168380511209, 4297394569014717897],
           [4298462872969244297, 4298459225563237225, 4297297422977447753],
           [4298462873435275369, 4298459227962358473, 4297297429637206121]])

    >>> pystare.from_latlon_2d(lats, lons, level=20, adapt_level=False)
    array([[4298473764500464820, 4298458168380511220, 4297394569014717908],
           [4298462872969244308, 4298459225563237236, 4297297422977447764],
           [4298462873435275380, 4298459227962358484, 4297297429637206132]])
    """
    if level is None:
        adapt_level = True
    elif level < 0 or level > 27:
        raise pystare.exceptions.PyStareLevelError()
    elif adapt_level is True:
        raise pystare.exceptions.PyStareError('Cannot set level AND adapt level. (level,adapt_level) = (%s,%s)'%(level,adapt_level))
    else:
        adapt_level = False

    if fill_value_in is not None:
        fill_value_enabled = True
        if fill_value_out is None:
            raise ValueError('fill_value_out must be specified if fill_value_in is specified.')
    else:
        fill_value_enabled = False
        fill_value_in  = -999.0
        fill_value_out = -999
        
    if adapt_level:
        level = 27
    sids = numpy.full(lon.shape, -1, dtype=numpy.int64)

    pystare.core._from_latlon2D(lat, lon, sids, level, adapt_level,
                                fill_value_enabled, fill_value_in, fill_value_out)
    return sids


def to_latlon(sids):
    """ Converts SIDs to latitudes and longitudes

    Parameters
    -----------
    sids: 1D array-like
        SIDs to convert to latitutdes and longitudes

    Returns
    --------
    lats: 1D numpy array
        latitudes
    lons: 1D numpy array
        longitudes

    Examples
    ---------
    >>> import pystare
    >>> import numpy
    >>> sids = numpy.array([4151504989081014894, 4161865161846704590, 3643626718498217166])
    >>> pystare.to_latlon(sids)
    (array([30.00000012, 45.00000003, 59.99999986]),
    array([44.99999991, 60.00000013,  9.9999999 ]))
    """

    lats, lons = pystare.core._to_latlon(sids)
    return lats, lons


def to_latlonlevel(sids):
    """ Converts SIDs to latitudes, longitudes and levels

    Parameters
    -----------
    sids: 1D array-like
        SIDs to convert to latitutdes, longitudes and levels

    Returns
    --------
    lats: 1D numpy array
        latitudes
    lons: 1D numpy array
        longitudes
    levels: 1D numpy arrau
        stare levels of the sids

    Examples
    ---------
    >>> import pystare
    >>> import numpy
    >>> sids = numpy.array([4151504989081014894, 4161865161846704590, 3643626718498217166])
    >>> pystare.to_latlonlevel(sids)
    (array([30.00000012, 45.00000003, 59.99999986]),
    array([44.99999991, 60.00000013,  9.9999999 ]),
    array([14, 14, 14], dtype=int32))
    """
    lats, lons, levels = pystare.core._to_latlonlevel(sids)
    return lats, lons, levels


def to_level(sids):
    """ Converts SIDs to levels

    Parameters
    -----------
    sids: 1D array-like
        SIDs to convert to levels

    Returns
    --------
    levels: 1D numpy arrau
        stare levels of the sids

    Examples
    ---------
    >>> import pystare
    >>> import numpy
    >>> sids = numpy.array([4151504989081014894, 4161865161846704590, 3643626718498217166])
    >>> pystare.to_level(sids)
    array([14, 14, 14], dtype=int32)
    """
    return pystare.core._to_level(sids)


def to_area(sids):
    """ Returns areas of trixels of SIDs in sterdians.

    Parameters
    -----------
    sids: 1D array-like
        SIDs to convert to areas

    Returns
    --------
    area: 1D numpy arrau
        areas of trixels of sids

    Examples
    ---------
    >>> import math
    >>> sids = numpy.array([4151504989081014894, 4161865161846704590, 3643626718498217166])
    >>> pystare.to_area(sids)
    array([5.41567334e-09, 5.46741649e-09, 4.98636938e-09])

    >>> level = 8
    >>> n = 8 * (4 ** level)
    >>> level_increment = pystare.spatial_increment_from_level(level)
    >>> sivs = [s+level for s in range(0, n*level_increment, level_increment)]
    >>> area = sum(pystare.to_area(sivs))
    >>> area/(4.0*math.pi)
    1.000000000000014
    """
    return pystare.core._to_area(sids)


def from_intervals(intervals):
    """

    Parameters
    -----------

    Returns
    --------

    Examples
    --------

    """
    return pystare.core._from_intervals(intervals)


def to_neighbors(sids):
    """

    Parameters
    -----------

    Returns
    --------

    Examples
    --------

    """
    result = pystare.core._to_neighbors(sids)
    range_indices = numpy.full([result.get_size_as_values()], -1, dtype=numpy.int64)
    result.copy_as_values(range_indices)
    return range_indices


def to_compressed_range(sids):
    """

    Parameters
    -----------

    Returns
    --------

    Examples
    --------

    """
    out_length = len(sids)
    range_indices = numpy.full([out_length], -1, dtype=numpy.int64)
    pystare.core._to_compressed_range(sids, range_indices)
    end_arg = 0
    while (end_arg < out_length) and (range_indices[end_arg] >= 0):
        end_arg = end_arg + 1
    range_indices = range_indices[:end_arg]
    return range_indices


def expand_intervals(intervals, level, multi_resolution=False):
    """
    Expand intervals

    Parameters
    -----------
    intervals: array-like
        intervals to expand
    level: int
        level to expand intervals to
    multi_resolution: bool
        allow multiresolution

    Returns
    --------


    """
    if level < -1 or level > 27:
        # Expand understands -1 to mean to use the level embedded in the index value.
        raise pystare.exceptions.PyStareLevelError()
    result = pystare.core._expand_intervals(intervals, level, multi_resolution)
    expanded_intervals = numpy.zeros([result.get_size_as_intervals()], dtype=numpy.int64)
    result.copy_as_values(expanded_intervals)
    return expanded_intervals


def adapt_resolution_to_proximity(sids):
    """
    Adapts the resolution of SIDs to match the geographical distanc between the SIDs.

    Parameters
    -----------
    sids: 1D array-like
        SIDs to adapt the resolution

    Returns
    --------
    adapted_sids: 1D numpy array
        SIDs with adapted resolution

    Examples
    --------
    >>> sids = numpy.array([4298473764500464820, 4298458168380511220, 4297394569014717908])
    >>> pystare.to_level(sids)
    array([20, 20, 20], dtype=int32)
    >>> sids = pystare.adapt_resolution_to_proximity(sids)
    >>> sids
    array([4298473764500464809, 4298458168380511209, 4297394569014717897])
    >>> pystare.to_level(sids)
    array([9, 9, 9], dtype=int32)
    """
    adapted_sids = numpy.copy(sids)
    pystare.core._adapt_resolution_to_proximity(sids, adapted_sids)
    return adapted_sids


def to_hull_range(indices, level):
    """

    Parameters
    -----------

    Returns
    --------

    Examples
    --------

    """
    if level < 0 or level > 27:
        raise pystare.exceptions.PyStareLevelError()

    result = pystare.core._to_hull_range(indices, level)
    range_indices = numpy.full([result.get_size_as_intervals()], -1, dtype=numpy.int64)
    result.copy_as_intervals(range_indices)
    return range_indices


def to_hull_range_from_latlon(lat, lon, level):
    warnings.warn('to_hull_range_from_latlon() is depreciated and will be removed in the future'
                  'Use cover_from_hull() instead', DeprecationWarning)
    return cover_from_hull(lat, lon, level)


def cover_from_hull(lat, lon, level):
    """ Converts a set of hull vertices to a trixel cover.

    Interprets a set of latitudes and longitudes as ring vertices.
    Then converts the ring into a convex hull.
    The ordering of the vertices thus is irrelevant.
    Then tesselates the ring with trixels and returns the according SIDs.

    Parameters
    -----------
    lat: 1D array-like
        latitudes of hull vertices. Has to be same length as lon
    lon: 1D array-like
        longitudes of hull vertices. Has to be same length as lat
    level: int
        Maximum level of trixels of the cover.

    Returns
    ----------
    range_indices: 1D array-like
        SIDs of trixel cover of the hull

    See Also
    -----------


    Examples
    ----------
    >>> import pystare
    >>> lat = [53.75702912049104, 54.98310415304803, 53.69393219666267, 50.128051662794235, 49.01778351500333, \
               47.62058197691181, 47.467645575544, 50.266337795607285, 51.10667409932158, 53.75702912049104]
    >>> lon = [14.119686313542559, 9.921906365609118, 7.100424838905269, 6.043073357781111, 8.099278598674744, \
                7.466759067422231, 12.932626987365948, 12.240111118222558, 15.01699588385867, 14.119686313542559]
    >>> pystare.cover_from_hull(lat, lon, 3)
    array([4251398048237748227, 4269412446747230211, 4278419646001971203,
           4539628424389459971, 4548635623644200963, 4566650022153682947])
    """
    if level < 0 or level > 27:
        raise pystare.exceptions.PyStareLevelError()

    result = pystare.core._to_hull_range_from_latlon(lat, lon, level)
    range_indices = numpy.full([result.get_size_as_intervals()], -1, dtype=numpy.int64)
    result.copy_as_intervals(range_indices)
    return range_indices


def to_nonconvex_hull_range_from_latlon(lat, lon, level):
    """
    Depreciated alias to :func:`~cover_from_ring()` .
    """
    warnings.warn('Use cover_from_hull() instead', DeprecationWarning)
    return cover_from_ring(lat, lon, level)


def cover_from_ring(lat, lon, level):
    """ Converts ring vertices to a trixel cover.

    Interprets a set of latitudes and longitudes as ring vertices.
    Then tesselates the ring with trixels and returns the according SIDs.
    The ordering of the vertices is relevant and has to be counterclockwise!
    However, the ring does not have to be closed and will impicitly be closed.

    Parameters
    -----------
    lat: 1D array-like
        latitudes of ring vertices. Has to be same length as lon
    lon: 1D array-like
        longitudes of ring vertices. Has to be same length as lat
    level: int
        Maximum level of trixels of the cover.

    Returns
    ----------
    range_indices: 1D array-like
        SIDs of trixel cover of the ring

    See Also
    -----------


    Examples
    ----------
    >>> lat = [53.75702912049104, 54.98310415304803, 53.69393219666267, 50.128051662794235, 49.01778351500333, \
               47.62058197691181, 47.467645575544, 50.266337795607285, 51.10667409932158, 53.75702912049104]
    >>> lon = [14.119686313542559, 9.921906365609118, 7.100424838905269, 6.043073357781111, 8.099278598674744, \
               7.466759067422231, 12.932626987365948, 12.240111118222558, 15.01699588385867, 14.119686313542559]
    >>> pystare.cover_from_ring(lat, lon, 5)
    array([4254212798004854789, 4255901647865118725, 4256464597818540037,
           4257027547771961349, 4257590497725382661, 4258153447678803973,
           4271664246560915461, 4280671445815656453, 4281234395769077765,
           4282360295675920389, 4284049145536184325, 4285175045443026949,
           4541880224203145221, 4553139223271571461, 4571153621781053445])  """

    if level < 0 or level > 27:
        raise pystare.exceptions.PyStareLevelError()

    result = pystare.core._to_nonconvex_hull_range_from_latlon(lat, lon, level)
    out_length = result.get_size_as_intervals()
    range_indices = numpy.zeros([out_length], dtype=numpy.int64)
    result.copy_as_intervals(range_indices)
    return range_indices


def latlon2circular_cover(lat, lon, radius, level):
    """
    Creates a circular cover around  a lat/lon center

    Parameters
    -----------
    lat: float
        lat of center
    lon: float
        lon of center
    radius: float
        radius of the circular cover in degrees
    level: int
        cover stare resolution

    Returns
    --------
    stare_cover: 1D array
        the circular cover
    """
    if level < 0 or level > 27:
        raise pystare.exceptions.PyStareLevelError()

    result = pystare.core._to_circular_cover(lat, lon, radius, level)
    out_length = result.get_size_as_intervals()
    range_indices = numpy.zeros([out_length], dtype=numpy.int64)
    result.copy_as_intervals(range_indices)
    return range_indices


def sid2circular_cover(index, radius, level):
    """
    Creates a circular cover around  an SID center

    Parameters
    -----------
    index: int64
        SID of the center
    radius: float
        radius of the circular cover in degrees
    level: int

    Returns
    --------
    stare_cover: 1D array
        the circular cover
    """

    if level < 0 or level > 27:
        raise pystare.exceptions.PyStareLevelError()

    latsv, lonsv, lat_center, lon_center = to_vertices_latlon([index])
    return latlon2circular_cover(lat_center[0], lon_center[0], radius, level)


def to_box_cover_from_latlon(lat, lon, resolution):
    """ Constructs a numpy array of intervals covering a 4-corner box specified using lat and lon.

    Parameters
    -----------

    Returns
    --------

    Examples
    --------
    >>>
    """
    result = pystare.core._to_box_cover_from_latlon(lat, lon, resolution)
    range_indices = numpy.zeros([result.get_size_as_intervals()], dtype=numpy.int64)
    result.copy_as_intervals(range_indices)
    return range_indices


def to_vertices_latlon(sids):
    """ Converts SIDs into latitudes and longiutdes of the trixel vertices and the centers

    Parameters
    -----------
    sids: 1D array-like
        SIDs to convert to lat/lon of trixel vertices and centers

    Returns
    --------
    latsv: 1D numpy array
        serialized latitudes of trixel vertices. Same length as lonsv. Tripple the size of lat_centers and lon_centers
    latsv: 1D numpy array
        serialized longitudes of trixel vertices. Same length as latsv. Tripple the size of lat_centers and lon_centers
    lat_centers: 1D numpy array
        latitudes of trixel centers. Same length as lon_centers
    lon_centers: 1D numpy array
        longitudes of trixel centers. Same length as lat_centers

    Examples
    ---------
    >>> pystare.to_vertices_latlon([4254212798004854789])
    (array([53.89745687, 56.8965353 , 56.93769843]),
    array([ 9.22866958, 13.23186479,  8.07137938]),
    array([55.93005351]),
    array([10.15342841]))
    """

    out_length = len(sids)
    lats, lons = pystare.core._to_vertices_latlon(sids)
    latsv = numpy.zeros([3 * out_length], dtype=numpy.double)
    lonsv = numpy.zeros([3 * out_length], dtype=numpy.double)
    lat_centers = numpy.zeros([out_length], dtype=numpy.double)
    lon_centers = numpy.zeros([out_length], dtype=numpy.double)

    k = 0
    l = 0
    for i in range(out_length):
        latsv[l] = lats[k]
        lonsv[l] = lons[k]

        latsv[l + 1] = lats[k + 1]
        lonsv[l + 1] = lons[k + 1]

        latsv[l + 2] = lats[k + 2]
        lonsv[l + 2] = lons[k + 2]

        lat_centers[i] = lats[k + 3]
        lon_centers[i] = lons[k + 3]
        k = k + 4
        l = l + 3
    return latsv, lonsv, lat_centers, lon_centers


def cmp_spatial(sids1, sids2, flatten=True):
    """ Performs an n by m containment test between two sets of sids.

    A containment test is performed between each sid of sids1 and each sid of sids2.
    For each pair {-1,0,1} is returned depending on which, if either, element contains the other.

    Parameters
    -----------
    sids1: 1D array-like
        first set of SIDs
    sids2: 1D array-like
        second set of SIDs
    flatten: bool
        if true, flatten the results. If false, return an array of size [len(sids1), len(sids2)]

    Returns
    --------
    cmp: numpy array. If flatten is True, 1D, otherwise 2D.
        Spatial containment. -1 if sid1 is contained in sid2, 1 if sid2 is contained in sid1 and 0 otherwise.
    """
    out_length = len(sids1) * len(sids2)
    cmp = numpy.zeros([out_length], dtype=numpy.int64)
    pystare.core._cmp_spatial(sids1, sids2, cmp)
    if not flatten:
        cmp = cmp.reshape(len(sids1), len(sids2))
    return cmp


def intersects(cover, sids, method='binsearch'):
    """ Intersects tests between a cover and a collection of sids.

    Tests for each element of sids if it intersect with
    the cover.

    Parameters
    -----------
    cover: 1D array-like
        Collection of sids representing a cover
    sids: 1D array-like
        Collection of sids to test for intersection with cover
    method: string
        intersects method. Can be 'skiplist', 'binsearch', or 'nn'

    Returns
    --------
    does_intersect: 1D numpy array of same length as sids.
        True for all sids that intersect with the cover. False otherwise

    Examples
    ----------
    >>> cover = numpy.array([4251398048237748227, 4269412446747230211, 4278419646001971203])
    >>> sids = numpy.array([1251398048237748227, 4269412446747230210])
    >>> pystare.intersects(cover, sids, method='binsearch')
    array([False,  True])
    """

    if isinstance(method, str):
        method = {'skiplist': 0, 'binsearch': 1, 'nn': 2}[method]
    does_intersect = pystare.core._intersects(cover, sids, method).astype(bool)
    return does_intersect


def intersect(indices1, indices2, multi_resolution=True):
    """
    Depreciated alias to :func:`~intersection()`
    """

    warnings.warn('Use intersection() instead', DeprecationWarning)
    return intersection(indices1, indices2, multi_resolution)


def intersection(sids1, sids2, multi_resolution=True):
    """ Creates an intersection of sids1 and sids2

    Parameters
    -----------
    sids1: 1D array-like
        first collection of SIDs
    sids2: 1D array-like
        second collection of SIDs
    multi_resolution: bool
        if true, allow the intersection to be multi resolution.

    Returns
    ----------
    intersection: 1D numpy array
        SIDs representing the intersection of sids1 and sids2

    Examples
    -------------
    >>> sids1 = [4251398048237748227, 4269412446747230211, 4278419646001971203, 4539628424389459971]
    >>> sids2 = [4251398048237748228, 4255901647865118724, 4258153447678803972, 4539628424389459972]
    >>> pystare.intersection(sids1, sids2, multi_resolution=False)
    array([4251398048237748228, 4255901647865118724, 4258153447678803972, 4539628424389459972])
    """

    out_length = 2 * max(len(sids1), len(sids2))
    intersection = numpy.full([out_length], -1, dtype=numpy.int64)
    if multi_resolution:
        pystare.core._intersect_multiresolution(sids1, sids2, intersection)
    else:
        pystare.core._intersect(sids1, sids2, intersection)

    # Argmax returns 0 if intersection is non-negative, and not len(intersection)+1
    # It's supposed to be the first index of the max val, but if all false...
    end_arg = numpy.argmax(intersection < 0)
    if end_arg == 0:
        if intersection[0] >= 0:
            end_arg = len(intersection)
    intersection = intersection[:end_arg]
    return intersection


def int2bin(sids):
    """
    Converts 64 bit integer to binary

    Examples
    ----------
    >>> sids = numpy.array([3458764513820540928])
    >>> int2bin(sids)
     ['0011000000000000000000000000000000000000000000000000000000000000']
    """
    if hasattr(sids, "__len__"):
        return ['{0:064b}'.format(sid) for sid in sids]
    else:
        return '{0:064b}'.format(sids)


def int2hex(sids):
    """ Converts int sids to hex sids

    Parameters
    -----------
    sids: array-like or int64
        int representations of SIDs

    Returns
    --------
    sid: array-like or str
        hex representations of SIDs

    Examples
    -----------
    >>> sid = 3458764513820540928
    >>> pystare.int2hex(sid)
    '0x3000000000000000'
    """

    if hasattr(sids, "__len__"):
        return ["0x%016x" % sid for sid in sids]
    else:
        return "0x%016x" % sids


def hex2int(sids):
    """ Converts hex SIDs to int SIDs

    Parameters
    -----------
    sids: array-like or str
        hex representations of SIDs

    Returns
    ----------
    sid: array-like or int64
        int representation of SIDs


    Examples
    -----------
    >>> sid = '0x3000000000000000'
    >>> pystare.hex2int(sid)
    3458764513820540928

    >>> sid = ['0x3000000000000000']
    >>> pystare.hex2int(sid)
    [3458764513820540928]
    """

    if isinstance(sids, str):
        return int(sids, 16)
    else:
        return [int(sid, 16) for sid in sids]


def spatial_resolution(sids):
    """
    Returns the spatial resolution of an sid

    Parameters
    ------------
    sids: int or array-like
        STARE index value

    Returns
    ---------
    resolution: int
        Resolution of the SID

    Examples
    ---------
    >>> sid = pystare.hex2int('0x3000000000000004')
    >>> pystare.spatial_resolution(sid)
    4

    >>> sids = pystare.hex2int(['0x3000000000000004', '0x3000000000000005'])
    >>> pystare.spatial_resolution(sids)
    array([4, 5])

    >>> sid = numpy.array(sids)
    >>> pystare.spatial_resolution(sid)
    array([4, 5])
    """
    sids = numpy.array(sids)
    resolutions = sids & 31  # levelMaskSciDB
    return resolutions


def spatial_increment_from_level(level):
    if level < 0 or level > 27:
        raise pystare.exceptions.PyStareLevelError()
    return 1 << (59 - 2 * level)


def spatial_terminator_mask(levels):
    """ Creates a STARE mask for a given STARE resolution.

    Examples
    ---------
    >>> mask = pystare.spatial_terminator_mask(0)
    >>> '{0:064b}'.format(mask)
    '0000011111111111111111111111111111111111111111111111111111111111'

    >>> pystare.spatial_terminator_mask([0, 10])
     array([576460752303423487,       549755813887])

    """
    levels = numpy.array(levels)
    if (levels < 0).any() or (levels > 27).any():
        raise pystare.exceptions.PyStareLevelError()
    return (1 << (1 + 58 - 2 * levels)) - 1


def spatial_terminator(sid):
    return sid | ((1 << (1 + 58 - 2 * (sid & 31))) - 1)


def spatial_coerce_resolution(sid, resolution):
    return (sid & ~31) | resolution


def spatial_clear_to_resolution(sids):
    """
    Clears the SID location bits up to the encoded spatial resolution
    Clears the SID location bits up to the encoded spatial resolution

    Parameters
    -------------
    sid: int
        the spatial ID to be cleared

    Examples
    ----------
    >>> sid = 2299437706637111721
    >>> spatial_clear_to_resolution(sid)
    2299437254470270985

    >>> sids = pystare.hex2int(['0x097cf40fd3132507', '0x097cf40fd3132505'])
    >>> pystare.int2hex(spatial_clear_to_resolution(sids))
    ['0x097ce00000000007', '0x097c000000000005']
    """
    resolution = spatial_resolution(sids)
    mask = spatial_terminator_mask(resolution)
    return (sids & ~mask) + resolution


def lon_wrap_180(lon):
    """ Wrap angle in degrees to [-180 180]

    Wraps angles (in degrees) to the interval [–180, 180] such that

    - 90 maps to 90
    - –90 maps to –90
    - 360 maps to 0
    - 270 maps to -90

    Notes
    --------
    - 180 wraps to -180 but -180 to -180
    - lon_wrap_180() casts to floats
    - This method is not intended to correct illformated longitudes outside the interval [-180, 360]

    Examples
    -----------
    >>> lon_wrap_180(90.0)
    90.0
    >>> lon_wrap_180(-90.0)
    -90.0
    >>> lon_wrap_180(360.0)
    0.0
    >>> lon_wrap_180(270.0)
    -90.0
    >>> lon_wrap_180(180.0)
    -180.0
    >>> lon_wrap_180(-180.0)
    -180.0
    """
    return ((lon + 180.0) % 360.0) - 180.0


def spatial_resolution_from_km(km, return_int=True):
    if return_int:
        return 10 - numpy.log2(km / 10)
    else:
        return int(10 - numpy.log2(km / 10))


def spatial_scale_km(level):
    """ Returns a rough estimate for the length scale at level."
    """

    return 10 * (2.0 ** (10 - level))


def triangulate(lats, lons):
    """ Helps prepare data for matplotlib.tri.Triangulate.
    """
    intmat = []
    npts = int(len(lats) / 3)
    k = 0
    for i in range(npts):
        intmat.append([k, k + 1, k + 2])
        k = k + 3
    for i in range(len(lons)):
        lons[i] = lon_wrap_180(lons[i])
    return lons, lats, intmat


def triangulate_indices(indices):
    """
    Prepare data for matplotlib.tri.Triangulate.

    Examples
    --------
    >>> lons, lats, intmat = triangulate_indices(indices)   # doctest: +SKIP
    >>> triang = tri.Triangulation(lons,lats,intmat)        # doctest: +SKIP
    >>> plt.triplot(triang,'r-',transform=transform,lw=1,markersize=3) # doctest: +SKIP
    """

    latv, lonv, lat_center, lon_center = to_vertices_latlon(indices)
    lons, lats, intmat = triangulate(latv, lonv)
    return lons, lats, intmat


def speedy_subset(sids_left, sids_right, values_left=None):
    """ Fast subsetting of data

    We make use of multi-level nature of STARE with the following steps:

    - clamp the sids_left by the upper and lower bounds of sids_right.
    - determine the intersection level as the lower one of the highest level of left and right.
    - coerce the resolution of the left sids to the intersection level
    - get the unique sids of the coerced left sids
    - perform stare-based intersects pf the unique values and the right
    - map the intersects back to the original array indices.

    Parameters
    ------------
    sids_left: 1D numpy.array
        The sids of the left which we are subsetting
    sids_right: 1D numpy.array
        The sids we are subseting sids_left with
    values_left: ndarray
        optional. If set, we return the subsetted values rather than the left indices. `values_left` must have same length as sids_left. I.e. the fastest changing index must be of the same length as sids_left.

    Examples
    ---------
    >>> import numpy
    >>> values_left = numpy.array([1,2,3,4,5,6])
    >>> sids_left = numpy.array([3330891586388099091, 3330891586390196243, 3330891586392293395,\
                                 3330891586394390547, 3330891586396487699, 3330891586398584851])
    >>> sids_right = numpy.array([3330891586396487699, 3330891586398584851])
    >>> left_values = numpy.array([1,2,3,4,5,6,])
    >>> res = speedy_subset(sids_left=sids_left, sids_right=sids_right, values_left=values_left)
    >>> res
    array([5, 6])
    """

    if values_left is not None:
        if not len(sids_left) == len(values_left):
            print('sids_left must have same length as values_left')
            return

    # Filter by top / bottom bounds
    top_bound = pystare.spatial_clear_to_resolution(sids_right.max())
    level = pystare.spatial_resolution(top_bound)
    top_bound += pystare.spatial_increment_from_level(level)
    bottom_bound = sids_right.min()
    candidate_sids = sids_left[(sids_left >= bottom_bound) * (sids_left <= top_bound)]
    if values_left is not None:
        values = values_left[(sids_left >= bottom_bound) * (sids_left <= top_bound)]

    # Find intersection level
    left_min_level = pystare.spatial_resolution(candidate_sids).max()
    right_min_level = pystare.spatial_resolution(sids_right).max()
    intersecting_level = min(right_min_level, left_min_level)

    # Extract unique SIDs
    coerced_sids = pystare.spatial_coerce_resolution(candidate_sids, intersecting_level)
    cleared_sids = pystare.spatial_clear_to_resolution(coerced_sids)
    distinct_sids = numpy.unique(cleared_sids)

    # Subset by STARE
    intersects = pystare.intersects(sids_right, distinct_sids)
    intersecting_sids = distinct_sids[intersects]
    intersecting_idx = numpy.isin(cleared_sids, intersecting_sids)
    if values_left is not None:
        return values[intersecting_idx]
    else:
        original_sids = candidate_sids[intersecting_idx]
        return numpy.isin(sids_left, original_sids)
