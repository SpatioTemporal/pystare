import datetime
import numpy
import pystare.core
import pystare.exceptions
import re


def from_ms_since_epoch_utc(ms_since_epoch_utc, forward_res=48, reverse_res=48):
    """ Converts an integer of milliseconds since unix epoch in UTC to TIV.

    Parameters
    -----------
    ms_since_epoch_utc: array-like of ints
        milliseconds since unix epoch in UTC
    forward_res: int. Valid range is 0..48
        The forward resolution (c.f :func:`~coarsest_resolution_finer_or_equal_ms()`)
    reverse_res: int. Valid range is 0..48
        The reverse resolution (c.f. :func:`~coarsest_resolution_finer_or_equal_ms()`

    Returns
    --------
    tivs: numpy array
        temporal index values

    Examples
    ----------
    >>> import numpy
    >>> import pystare
    >>> timestamps = numpy.array(['2021-01-03'], dtype='datetime64[ms]')
    >>> ms_since_epoch = timestamps.astype(numpy.int64)
    >>> pystare.from_ms_since_epoch_utc(ms_since_epoch_utc=ms_since_epoch, forward_res=48, reverse_res=48)
    array([2275448110396223681])

    See Also
    --------

    """
    tivs = pystare.core._from_utc(ms_since_epoch_utc, forward_res, reverse_res)
    return tivs


def to_ms_since_epoch_utc(tivs):
    """
    Converts TIVs into milliseconds since epoch in UTC

    Parameters
    -----------
    tivs: array-like of ints
        Temporal index values to convert

    Returns
    ---------
    ms_since_epoch_utc: numpy array of ints
        milliseconds since epoch in UTC

    Examples
    ---------
    >>> import numpy
    >>> import pystare
    >>> tivs = [2275448110396223681]
    >>> ts = pystare.to_ms_since_epoch_utc(tivs).astype('datetime64[ms]')
    >>> numpy.datetime_as_string(ts)
    array(['2021-01-03T00:00:00.000'], dtype='<U42')
    """
    ms_since_epoch_utc = pystare.core._to_utc_approximate(tivs)
    return ms_since_epoch_utc


def from_utc_variable(datetime, forward_resolution, reverse_resolution):
    """
    This function takes an array of datetimes and constructs temporal index values from them
    with forward and reverse resolutions as given in the arrays passed in.
    """
    return pystare.core._from_utc_variable(datetime, forward_resolution, reverse_resolution)


def now(forward_res=48, reverse_res=48):
    """Get a tiv representing current point in time.

    Parameters
    ------------
    forward_res: int. Valid range is 0..48
        The forward resolution (c.f :func:`~coarsest_resolution_finer_or_equal_ms()`)
    reverse_res: int. Valid range is 0..48
        The reverse resolution (c.f. :func:`~coarsest_resolution_finer_or_equal_ms()`

    Examples
    ---------
    >>> import pystare
    >>> now = pystare.now()
    """
    now = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    now = numpy.array([now], dtype='datetime64[ms]')
    now = now.astype(numpy.int64)
    tiv = pystare.from_ms_since_epoch_utc(now, forward_res, reverse_res)[0]
    return tiv


def coarsest_resolution_finer_or_equal_ms(ms):
    """ Converts milliseconds to finer or equal STARE temporal resolution.

    Resolutions go from 0 being coarsest to 48 being the finest.
    Bits are numbered in the opposite direction.
    The biggest year bit is bit 62. The smallest millisecond bit is at bit 14. So we have:

    .. tabularcolumns:: |R|R|R|R|R|R|
    +----------+-------------+-------+-----+------+----------------------------+
    |Field     | Resolutions | Start | End | Size | Unit                       |
    +==========+=============+=======+=====+======+============================+
    |0         | -           |  0    |  1  |  2   | Calendar or Scaleindicator |
    +----------+-------------+-------+-----+------+----------------------------+
    |1         | -           |  2    |  7  |  6   | Reverse Neighborhood       |
    +----------+-------------+-------+-----+------+----------------------------+
    |2         | -           |  8    | 13  |  6   | Forward Neighborhood       |
    +----------+-------------+-------+-----+------+----------------------------+
    |3         | 48-39       | 14    | 23  | 10   | Millisecond                |
    +----------+-------------+-------+-----+------+----------------------------+
    |4         | 38-33       | 24    | 29  |  6   | Second                     |
    +----------+-------------+-------+-----+------+----------------------------+
    |5         | 32-27       | 30    | 35  |  6   | Minute                     |
    +----------+-------------+-------+-----+------+----------------------------+
    |6         | 26-22       | 36    | 40  |  5   | Hour                       |
    +----------+-------------+-------+-----+------+----------------------------+
    |7         | 21-19       | 41    | 43  |  3   | Day-of-week                |
    +----------+-------------+-------+-----+------+----------------------------+
    |8         | 18-17       | 44    | 45  |  2   | Week-of-month              |
    +----------+-------------+-------+-----+------+----------------------------+
    |9         | 16-13       | 46    | 49  |  4   | Month-of-year              |
    +----------+-------------+-------+-----+------+----------------------------+
    |10        | 12-00       | 50    | 62  | 13   | Year                       |
    +----------+-------------+-------+-----+------+----------------------------+
    |11        | -           | -     | -   |  1   | Before/After Epoch         |
    +----------+-------------+-------+-----+------+----------------------------+

    Parameters
    ----------
    ms: 1D array of ints
        resolution in milliseconds

    Returns
    ---------
    resolutions: 1D numpy array of ints
        STARE temporal resolutrions corresponding to ms

    Examples
    ---------
    >>> import pystare
    >>> millisecond  = 1
    >>> second = 1000 * millisecond
    >>> minute = 60 * second
    >>> hour = 60 * minute
    >>> day = 86400 * second
    >>> year = 365 * day
    >>> times = numpy.array([millisecond, second, minute, hour, day, year], dtype=numpy.int64)
    >>> pystare.coarsest_resolution_finer_or_equal_ms(times)
    array([48, 38, 32, 26, 21, 12])

    """
    resolutions = pystare.core._coarsest_resolution_finer_or_equal_milliseconds(ms)
    return resolutions


def milliseconds_at_resolution(resolution):
    """ Returns milliseconds for a given resolution.
    Inverse of :func:`~coarsest_resolution_finer_or_equal_ms()`

    Parameters
    ----------
    resolution: int between 0 and 48
        resolution to look milliseconds up fpr

    Returns
    -----------
    milliseconds: int
        the size of the resolution in milliseconds

    Examples
    ---------
    >>> ms = 5 * 60 * 1000 # 5 mintes
    >>> resolution = coarsest_resolution_finer_or_equal_ms([ms])
    >>> resolution
    array([30])
    >>> pystare.milliseconds_at_resolution(resolution) / 60 / 1000 # Back to minutes
    array([4.])
    """
    return pystare.core._milliseconds_at_resolution(resolution)


def cmp_temporal(tivs1, tivs2, flatten=True):
    """Intersects tests between temporal index values.

    Returns 1 for when two temporal index values overlap and 0 if they don't

    Parameters
    -----------
    tivs1: 1D array-like
        first set of temporal index values to compare
    tivs2: 1D array-like
        second set of temporal index values to compare
    flatten: bool
        if true, flatten the results. If false, return an array of size [len(tivs1), len(tivs2)]

    Returns
    --------
    cmp: numpy.array. If flatten is True, 1D, otherwise 2D.
        Temporal containment. -1 if tiv1 is contained in tiv2. 0 otherwise.

    Examples
    -----------
    >>> ts1 = numpy.array(['2021-01-03T01', '1985-01-03T01'], dtype='datetime64[ms]').astype(numpy.int64)
    >>> ts2 = numpy.array(['2021-05-01T10', '1986-10-01'], dtype='datetime64[ms]').astype(numpy.int64)
    >>> tiv1 = pystare.from_ms_since_epoch_utc(ts1, 10, 10)
    >>> tiv2 = pystare.from_ms_since_epoch_utc(ts2, 10, 10)
    >>> pystare.cmp_temporal(tiv1, tiv2, flatten=False)
    array([[1, 0],
           [0, 1]])
    """
    out_length = len(tivs1) * len(tivs2)
    cmp = numpy.zeros([out_length], dtype=numpy.int64)
    pystare.core._cmp_temporal(tivs1, tivs2, cmp)
    if not flatten:
        cmp = cmp.reshape(len(tivs1), len(tivs2))
    return cmp


def validate_iso8601_string(iso_string, has_ms=None, has_tz=None):
    """
    Test if string is ISO 8601 timestring.
    Also verify if string includes milliseconds and timezone
    https://en.wikipedia.org/wiki/ISO_8601

    Parameters
    -----------
    iso_string: str
        A formated timestring
    has_ms: bool
        Test if string includes milliseconds
    has_tz: bool
        Test if string includes timezone

    Returns
    --------
    valid: Bool or str
        Returns True if timestring is of shape %Y-%m-%dT%H:%M:%S.%ms.
        Else False

    Examples
    -----------
    >>> validate_iso8601_string('2021-01-09T17:47:56.154564', has_ms=True, has_tz=False) # ISO8601 w/o timezone and with ms
    True
    >>> validate_iso8601_string('2021-01-09T17:47:56.154564', has_ms=False) # ISO8601 w/o timezone and with ms
    False
    >>> validate_iso8601_string('2021-01-09T17:47:56', has_ms=True) # No ms
    False
    >>> validate_iso8601_string('2021-01-09T17:47:56', has_ms=False) # No ms
    True
    >>> validate_iso8601_string('2021-01-09T17:47:56.2435+05:00', has_tz=True) # includes timezone
    True
    >>> validate_iso8601_string('2021-01-09T17:47:56.2435+05:00', has_tz=False) # includes timezone
    False
    >>> validate_iso8601_string('2021-01-09T17:47:56.154564 (45 12) (1)') # STARE timestring
    False
    >>> validate_iso8601_string('Wolfgang') # Not a timestamp
    False
    """
    regex_iso8601 = r'^(-?(?:[1-9][0-9]*)?[0-9]{4})-(1[0-2]|0[1-9])-(3[01]|0[1-9]|[12][0-9])' \
                    r'T(2[0-3]|[01][0-9]):([0-5][0-9]):([0-5][0-9])(\.[0-9]+)' \
                    r'?(Z|[+-](?:2[0-3]|[01][0-9]):[0-5][0-9])?$'
    match_iso8601 = re.compile(regex_iso8601).match

    match = match_iso8601(iso_string)
    if match is None:
        return False
    else:
        groups = match.groups()
        if has_tz is not None and has_tz == (groups[7] is None):
            return False
        elif has_ms is not None and has_ms == (groups[6] is None):
            return False
        else:
            return True


def analyze_iso8601_string(iso_string):
    """
    Returns 'has_tz' if timestring contains timezone
    Returns 'no_ms' if timestring does not contain milliseconds
    Returns 'nat' if timestring is not a ISO8601 timestring
    Returns 'good' if timestring contains ms but no tz

    Examples
    ---------
    >>> analyze_iso8601_string('2021-01-09T17:47:56') # No ms
    'no_ms'
    >>> analyze_iso8601_string('2021-01-09T17:47:56.2435+05:00') # includes timezone
    'has_tz'
    """
    regex_iso8601 = r'^(-?(?:[1-9][0-9]*)?[0-9]{4})-(1[0-2]|0[1-9])-(3[01]|0[1-9]|[12][0-9])' \
                    r'T(2[0-3]|[01][0-9]):([0-5][0-9]):([0-5][0-9])(\.[0-9]+)' \
                    r'?(Z|[+-](?:2[0-3]|[01][0-9]):[0-5][0-9])?$'
    match_iso8601 = re.compile(regex_iso8601).match

    match = match_iso8601(iso_string)
    if match is None:
        return 'nat'
    elif match.groups()[7] is not None:
        return 'has_tz'
    elif match.groups()[6] is None:
        return 'no_ms'
    else:
        return 'good'


def validate_iso8601_strings(time_strings, has_ms=None, has_tz=None):
    """Validate if collection of strings all are ISO8601.
     Also verify if timestamps includes milliseconds and  timezone.

    Parameters
    ----------
    time_strings: 1D array-like of strings
        collection of timestrings to be validated
    has_ms: bool
        Test if strings include milliseconds
    has_tz: bool
        Test if strings include timezone

    Returns
    ---------
    are_valid: bool
        True if all strings in collection are ISO8601 timestamps including ms and excluding timezone. False otherwise

    Examples
    ----------
    >>> time_strings = ['2021-01-09T17:47:56.154564', '2021-05-09T17:47:56.13']
    >>> pystare.validate_iso8601_strings(time_strings, has_ms=True, has_tz=False)
    True
    >>> time_strings = ['2021-01-09T17:47:56.154564', '2021-05-09T17:47:51']
    >>> pystare.validate_iso8601_strings(time_strings, has_ms=True, has_tz=False)
    False

    See Also
    ---------
    validate_iso8601_string

    """
    for time_string in time_strings:
        if validate_iso8601_string(time_string, has_ms, has_tz) is not True:
            return False
    return True


def validate_stare_timestring(timestrings):
    """ Tests if timestring has shape of STARE timestring,

    STARE timestrings are of the form "%Y-%m-%dT%H:%M:%S.%ms (f_res, b_res) (type)"

    Examples
    ----------
    >>> pystare.validate_stare_timestring('2021-01-09T17:47:56.154 (45 12) (1)')
    True
    >>> pystare.validate_stare_timestring('2021-01-09T17:47:56.15 (45 12) (1)')
    False
    >>> pystare.validate_stare_timestring('2021-01-09T17:47:56.15345345 (45 12) (1)')
    False
    >>> pystare.validate_stare_timestring('2021-01-09T17:47:56 (45 12) (1)')
    False
    >>> pystare.validate_stare_timestring('2021-01-09T17:47:56.154564')
    False
    """
    regex_stare = r'^(-?(?:[1-9][0-9]*)?[0-9]{4})-(1[0-2]|0[1-9])-(3[01]|0[1-9]|[12][0-9])' \
                  r'T(2[0-3]|[01][0-9]):([0-5][0-9]):([0-5][0-9])\.([0-9]{3})' \
                  r'?(\s\(([0-9]+)\s([0-9]+)\)\s\(([0-9])\))$'
    match_stare = re.compile(regex_stare).match

    if match_stare(timestrings) is not None:
        return True
    else:
        return False


def validate_stare_timestrings(timestrings):
    """ Validate if collection of strings are STARE timestrings.
    STARE timestrings are of the form "%Y-%m-%dT%H:%M:%S.%ms (f_res, r_res) (type)"

    Examples
    ---------
    >>> stare_ts = ['2021-01-09T17:47:56.154 (45 12) (1)']
    >>> validate_stare_timestrings(stare_ts)
    True

    See Also
    ---------
    validate_stare_timestring

    """
    for timestring in timestrings:
        if validate_stare_timestring(timestring) is False:
            return False
    return True


def force_3ms(timestamp):
    """ Forces 3 digits for the millisecods in an ISO timestamp.

    Examples
    ---------
    >>> pystare.force_3ms('2021-08-26T17:03:56.6')
    '2021-08-26T17:03:56.600'
    >>> pystare.force_3ms('2021-08-26T17:03:56.643365456345')
    '2021-08-26T17:03:56.643'
    """
    regex_iso8601 = r'^(-?(?:[1-9][0-9]*)?[0-9]{4})-(1[0-2]|0[1-9])-(3[01]|0[1-9]|[12][0-9])' \
                    r'T(2[0-3]|[01][0-9]):([0-5][0-9]):([0-5][0-9])(\.[0-9]+)' \
                    r'?(Z|[+-](?:2[0-3]|[01][0-9]):[0-5][0-9])?$'
    match_iso8601 = re.compile(regex_iso8601).match

    ms = match_iso8601(timestamp).groups()[6]
    ms3 = ms.ljust(4, '0')[0:4]
    timestamp = timestamp.replace(ms, ms3)
    return timestamp


def iso_to_stare_timestrings(iso_strings, forward_res, reverse_res, stare_type):
    """ Converts an ISO 8601 timestring to a STARE timestring.

    The ISO 8601 timestring has to contain exactly 3 digits for milliseconds but no timezone.
    I.e. it is of the form "%Y-%m-%dT%H:%M:%S.%ms"
    The stare timestring is of the form "%Y-%m-%dT%H:%M:%S.%ms (f_res, b_res) (stare_type)"


    Parameters
    -----------
    iso_strings: array-like of iso timestrings
        iso 8601 timestring
    forward_res: int. Valid range is 0..48
        The forward resolution (c.f :func:`~coarsest_resolution_finer_or_equal_ms()`)
    reverse_res: int. Valid range is 0..48
        The reverse resolution (c.f. :func:`~coarsest_resolution_finer_or_equal_ms()`
    stare_type: str
        #TODO what is the stare_type?

    Returns
    ----------
    stare_strings: list of strings
        list of STARE timestrings

    Examples
    ---------
    >>> iso_timestring = ['2021-01-09T17:47:56.154564']
    >>> pystare.iso_to_stare_timestrings(iso_timestring, forward_res=45, reverse_res=12, stare_type=1)
    ['2021-01-09T17:47:56.154 (45 12) (1)']
    """
    
    if validate_iso8601_strings(iso_strings, has_tz=True):
        raise ValueError('malformatted. '
                         'Iso strings should be of shape: "%Y-%m-%dT%H:%M:%S.%ms" and should not contain TZ')

    suffix = ' ({f_res} {b_res}) ({type})'.format(f_res=forward_res, b_res=reverse_res, type=stare_type)
    stare_strings = []
    for iso_string in iso_strings:
        if validate_iso8601_string(iso_string, has_ms=False):
            iso_string += '.0'
        stare_string = force_3ms(iso_string)
        stare_string = stare_string + suffix
        stare_strings.append(stare_string)
    return stare_strings


def from_iso_strings(iso_strings, forward_res=48, reverse_res=48, scale='TAI', stare_type=1):
    """ Converts an iso strings to STARE temporal index values

    Parameters
    -----------
    iso_strings: array-like of iso timestrings
        iso 8601 timestring
    forward_res: int. Valid range is 0..48
        The forward resolution (c.f :func:`~coarsest_resolution_finer_or_equal_ms()`)
    reverse_res: int. Valid range is 0..48
        The reverse resolution (c.f. :func:`~coarsest_resolution_finer_or_equal_ms()`
    scale: str
        time scale. Currently only TAI
    stare_type: str
        #TODO what is the stare_type?

    Returns
    --------
    tiv: 1D numpy array of ints
        STARE temporal index values

    Examples
    ----------
    >>> time_strings = ['2021-08-26T17:03:56.6']
    >>> pystare.from_iso_strings(time_strings, forward_res=20, reverse_res=18, scale='TAI')
    array([2276038620409631817])
    """
    stare_timestrings = iso_to_stare_timestrings(iso_strings, forward_res, reverse_res, stare_type)
    tivs = from_stare_timestrings(stare_timestrings, scale)
    return tivs


def from_stare_timestrings(stare_timestrings, scale='TAI'):
    """ Converts a STARE timestring to a STARE temporal index value
    The stare timestring is of the form "%Y-%m-%dT%H:%M:%S.%ms (f_res, b_res) (stare_type)
    
    Parameters
    -----------
    stare_timestrings: array-like of iso timestrings
        STARE timestring
    scale: str
        time scale. Currently only 'TAI'

    Examples
    ---------
    >>> stare_ts = ['2021-01-09T17:47:56.154 (45 12) (1)']
    >>> pystare.from_stare_timestrings(stare_ts, scale='TAI')
    array([2275464722577272113])
    """

    if not validate_stare_timestrings(stare_timestrings):
        raise pystare.exceptions.PyStareError()
    
    out_length = len(stare_timestrings)
    tivs = numpy.zeros([out_length], dtype=numpy.int64)
    if scale == 'TAI':
        pystare.core._from_tai_iso_strings(stare_timestrings, tivs)
        return tivs
    else:
        raise pystare.exceptions.PyStareError('only TAI is implemented')


def to_stare_timestring(tivs, scale='TAI'):
    """Converts a STARE temporal index value to a STARE timestring

    Parameters
    -------------
    tivs: 1D array-like
        collection of STARE temporal index values
    scale: str
        Temporal scale. Currently only 'TAI'

    Returns
    ---------
    stare_string:
        STARE timestring of the form "%Y-%m-%dT%H:%M:%S.%ms (f_res, b_res) (stare_type)"

    Examples
    ---------
    >>> time_strings = ['2021-08-26T17:03:56.626 (48 48) (1)']
    >>> tiv = pystare.from_stare_timestrings(time_strings, scale='TAI')
    >>> pystare.to_stare_timestring(tiv) == time_strings
    True
    """

    if scale == 'TAI':
        stare_string = pystare.core._to_tai_iso_strings(tivs)
    else:
        raise pystare.exceptions.PyStareError('only TAI is implemented')
    return stare_string


def from_julian_date(jd1, jd2, scale, forward_res=48, reverse_res=48):
    """ Converts two-part Julian Dates (JD) to SIVs.

    [astropy.time](https://docs.astropy.org/en/stable/time/index.html) provides a simple interface to convert between
    common datetime representations (e.g. numpy.datetime64, datetime, iso strings, etc. ) and two-part (JD).
    See in examples below

    from [Julian Day Wikipedia](https://en.wikipedia.org/wiki/Julian_day)
    "the Julian date (JD) of any instant is the Julian day number plus the
    fraction of a day since the preceding noon in Universal Time.
    Julian dates are expressed as a Julian day number with a decimal fraction added.
    For example, the Julian Date for 00:30:00.0 UT January 1, 2013, is 2 456 293.520 833.

    from [pyerfa](https://pyerfa.readthedocs.io/en/latest/api/erfa.d2dtf.html#erfa.d2dtf):
    "d1+d2 is Julian Date, apportioned in any convenient way between
    the two arguments, for example where d1 is the Julian Day Number
    and d2 is the fraction of a day."

    Parameters
    -----------
    jd1: double
        jd1+jd2 is Julian Date apportioned in any convenient
    jd2: double
        jd1+jd2 is Julian Date apportioned in any convenient
    scale: str. Either 'tai' or 'utc
        The time scale (or time standard)
    forward_res: int. Valid range is 0..48
        The forward resolution (c.f :func:`~coarsest_resolution_finer_or_equal_ms()`)
    reverse_res: int. Valid range is 0..48
        The reverse resolution (c.f. :func:`~coarsest_resolution_finer_or_equal_ms()`

    Returns
    --------
    tivs: 1D numpy.array
        STARE temporal index values

    Examples
    ----------
    >>> import astropy
    >>> t = astropy.time.Time('2021-08-26T17:36:46.426092', format='isot')
    >>> t.jd1, t.jd2
    (2459453.0, 0.23387067236111114)

    >>> jd1 = numpy.array([2459453.0])
    >>> jd2 = numpy.array([0.23387067236111114])
    >>> tivs = pystare.from_julian_date(jd1=jd1, jd2=jd2, scale='tai', forward_res=10, reverse_res=10)
    >>> pystare.to_stare_timestring(tivs)
    ['2021-08-26T17:36:46.426 (10 10) (1)']
    >>> tivs = pystare.from_julian_date(jd1=jd1, jd2=jd2, scale='utc', forward_res=10, reverse_res=10)
    >>> pystare.to_stare_timestring(tivs)
    ['2021-08-26T17:37:23.426 (10 10) (1)']
    """

    if isinstance(jd1, float):
        # So we can accept scalars
        jd1 = numpy.array([jd1])
        jd2 = numpy.array([jd2])

    if scale == 'tai':
        tivs = pystare.core._from_JulianTAI(jd1, jd2, forward_res, reverse_res)
    elif scale == 'utc':
        tivs = pystare.core._from_JulianUTC(jd1, jd2, forward_res, reverse_res)
    else:
        pystare.exceptions.PyStareError('scale not implemented')
    return tivs


def to_julian_date(tivs, scale):
    """Converts STARE temporal index values to two-part Julian Dates

    from [Julian Day Wikipedia](https://en.wikipedia.org/wiki/Julian_day)
    "the Julian date (JD) of any instant is the Julian day number plus the
    fraction of a day since the preceding noon in Universal Time.
    Julian dates are expressed as a Julian day number with a decimal fraction added.
    For example, the Julian Date for 00:30:00.0 UT January 1, 2013, is 2 456 293.520 833.

    Parameters
    ----------
    tivs: 1D array-like
        The STARE temporal index values to convert
    scale: str. Either 'tai' or 'utc
        The time scale (or time standard)

    Returns
    --------
    jd1: double
        jd1+jd2 is Julian Date apportioned in any convenient
    jd2: double
        jd1+jd2 is Julian Date apportioned in any convenient

    Examples
    -----------
    >>> tiv = numpy.array([2276038620410065089])
    >>> pystare.to_julian_date(tiv, scale='tai')
    (array([2459215.5]), array([237.71107206]))
    >>> pystare.to_julian_date(tiv, scale='utc')
    (array([2459215.5]), array([237.71064382]))

    >>> import astropy
    >>> timestamps = ['2021-09-26T17:16:46.426092', '2020-09-26T17:16:46.426092']
    >>> t = astropy.time.Time(timestamps, format='isot')
    >>> tivs = pystare.from_julian_date(t.jd1, t.jd2, scale='tai')
    >>> jds = pystare.to_julian_date(tivs, scale='tai')
    >>> t = astropy.time.Time(jds[0], jds[1], format='jd', scale='tai')
    >>> t.isot
    array(['2021-09-26T17:16:46.426', '2020-09-26T17:16:46.426'], dtype='<U23')
    """
    # So we can accept scalars
    if isinstance(tivs, (int, numpy.int64)):
        tivs = numpy.array([tivs])

    if scale == 'tai':
        jd1, jd2 = pystare.core._to_JulianTAI(tivs)
    elif scale == 'utc':
        jd1, jd2 = pystare.core._to_JulianUTC(tivs)
    return jd1, jd2


def adapt_resolutions_shape(tivs, resolutions):
    if isinstance(resolutions, int):
        resolutions = numpy.full(tivs.shape, resolutions)
    elif isinstance(resolutions, list):
        resolutions = numpy.array(resolutions)
    if resolutions.shape != (1,) and resolutions.shape != tivs.shape:
        raise pystare.exceptions.PyStareError('resolution has to have length 1 or same shape as tivs')
    return resolutions


def set_reverse_resolution(tivs, resolutions):
    """Set the reverse resolution of STARE temporal index values

    Parameters
    -----------
    tivs: 1D array-like
        tivs to set the resolution for
    resolutions: 1D array-like
        resolutions to be set. Either single value or same resolution as tivs

    Examples
    ----------
    >>> tivs = numpy.array([2275448179115690537, 2234915782217697833])
    >>> pystare.set_reverse_resolution(tivs, numpy.array([9, 9]))
    array([2275448179115690533, 2234915782217697829])
    >>> pystare.set_reverse_resolution(tivs, [9, 9])
    array([2275448179115690533, 2234915782217697829])
    >>> pystare.set_reverse_resolution(tivs, 9)
    array([2275448179115690533, 2234915782217697829])
    >>> tiv = pystare.set_reverse_resolution(numpy.array([2275448179115690533]), 9)
    >>> pystare.reverse_resolution(tiv)
    array([9])
    """
    resolutions = adapt_resolutions_shape(tivs, resolutions)

    result = numpy.zeros(tivs.shape, dtype=numpy.int64)
    pystare.core._set_reverse_resolution(tivs, resolutions, result)
    return result


def set_forward_resolution(tivs, resolutions):
    """Set the forward resolution of STARE temporal index values

    Parameters
    -----------
    tivs: 1D array-like
        tivs to set the resolution for
    resolutions: 1D array-like
        resolutions to be set. Either single value or same resolution as tivs

    Examples
    ----------
    >>> tivs = numpy.array([2275448179115690537, 2234915782217697833])
    >>> pystare.set_forward_resolution(tivs, numpy.array([9, 9]))
    array([2275448179115690281, 2234915782217697577])
    >>> pystare.set_forward_resolution(tivs, [9, 9])
    array([2275448179115690281, 2234915782217697577])
    >>> pystare.set_forward_resolution(tivs, 9)
    array([2275448179115690281, 2234915782217697577])
    >>> tiv = pystare.set_forward_resolution(numpy.array([2275448179115690533]), 8)
    >>> pystare.forward_resolution(tiv)
    array([8])
    """
    resolutions = adapt_resolutions_shape(tivs, resolutions)

    result = numpy.zeros(tivs.shape, dtype=numpy.int64)
    pystare.core._set_forward_resolution(tivs, resolutions, result)
    return result


def reverse_resolution(indices):
    """ Retrieve the reverse resolution

    Examples
    ----------
    >>> tiv = pystare.set_reverse_resolution(numpy.array([2275448179115690533]), 9)
    >>> pystare.reverse_resolution(tiv)
    array([9])
    """

    result = numpy.zeros(indices.shape, dtype=numpy.int64)
    pystare.core._reverse_resolution(indices, result)
    return result


def forward_resolution(indices):
    """ Retrieve the forward resolution

    Examples
    ----------
    >>> tiv = pystare.set_forward_resolution(numpy.array([2275448179115690533]), 7)
    >>> pystare.forward_resolution(tiv)
    array([7])
    """
    result = numpy.zeros(indices.shape, dtype=numpy.int64)
    pystare.core._forward_resolution(indices, result)
    return result


def coarsen(indices, reverse_increments, forward_increments):
    """TODO: Not tested"""
    result = numpy.zeros(indices.shape, dtype=numpy.int64)
    pystare.core._coarsen(indices, reverse_increments, forward_increments, result)
    return result


def set_temporal_resolutions_from_sorted(sorted_indices, include_bounds=True):
    """
    TODO
    """
    pystare.core._set_temporal_resolutions_from_sorted_inplace(sorted_indices, include_bounds)
    return sorted_indices


def lower_bound_tai(tiv):
    """
    TODO
    """
    tret = tiv.copy()
    pystare.core._scidbLowerBoundTAI(tiv, tret)
    return tret


def upper_bound_tai(tiv):
    """
    TODO
    """
    tret = tiv.copy()
    pystare.core._scidbUpperBoundTAI(tiv, tret)
    return tret


def lower_bound_ms(tiv):
    """
    TODO
    """
    tret = tiv.copy()
    pystare.core._scidbLowerBoundMS(tiv, tret)
    return tret


def upper_bound_ms(tiv):
    """
    TODO
    """
    tret = tiv.copy()
    pystare.core._scidbUpperBoundMS(tiv, tret)
    return tret


def to_temporal_triple_ms(tivs):
    ti_low = pystare.core.scidbLowerBoundMS(tivs)
    ti_hi = pystare.core.scidbUpperBoundMS(tivs)
    return (ti_low, tivs, ti_hi)


def to_temporal_triple_tai(tiv):
    ti_low = lower_bound_tai(tiv)
    ti_hi = upper_bound_tai(tiv)
    return (ti_low, tiv, ti_hi)


def to_temporal_triple_ms(tiv):
    ti_low = lower_bound_ms(tiv)
    ti_hi = upper_bound_ms(tiv)
    return (ti_low, tiv, ti_hi)


def from_temporal_triple(triple, include_bounds=True):
    """Calculate a temporal index value from a low, middle, and high tiv.
    Negative tiv are not used.
    """
    tiv = numpy.zeros([1], dtype=numpy.int64)
    tiv[0] = pystare.core._scidbNewTemporalValue(numpy.array(triple, dtype=numpy.int64), include_bounds)[0]
    return tiv


def temporal_value_intersection_if_overlap(indices1, indices2):
    """Calculate intersection temporal index value element-by-element if they overlap.
    """
    if indices1.shape != indices2.shape:
        raise ValueError("Arrays being compared must have the same shape.")
    cmp = numpy.zeros(indices1.shape, dtype=numpy.int64)
    pystare.core._scidbTemporalValueIntersectionIfOverlap(indices1, indices2, cmp)
    return cmp


def temporal_value_union_if_overlap(indices1, indices2):
    """Calculate union temporal index value element-by-element if they overlap.
    """
    if indices1.shape != indices2.shape:
        raise ValueError("Arrays being compared must have the same shape.")
    cmp = numpy.zeros(indices1.shape, dtype=numpy.int64)
    pystare.core._scidbTemporalValueUnionIfOverlap(indices1, indices2, cmp)
    return cmp


def temporal_overlap_tai(indices1, indices2):
    """Test for overlap, element by element. 0 if no overlap. Uses 'TAI'.
    """
    if indices1.shape != indices2.shape:
        raise ValueError("Arrays being compared must have the same shape.")
    cmp = numpy.zeros(indices1.shape, dtype=numpy.int64)
    pystare.core._scidbOverlapTAI(indices1, indices2, cmp)
    return cmp


def temporal_overlap(indices1, indices2):
    """Test for overlap, element by element. 0 if no overlap. Uses approximate millisecond calculation.
    """
    if indices1.shape != indices2.shape:
        raise ValueError("Arrays being compared must have the same shape.")
    cmp = numpy.zeros(indices1.shape, dtype=numpy.int64)
    pystare.core._scidbOverlap(indices1, indices2, cmp)
    return cmp


def temporal_contains_instant(indices1, indices2):
    """Test if indices1 contain the instants in indices2.
    Compares element by element. Test for overlap, element by element. 0 if no overlap.
    Uses approximate millisecond calculation."""
    if indices1.shape != indices2.shape:
        raise ValueError("Arrays being compared must have the same shape.")
    cmp = numpy.zeros(indices1.shape, dtype=numpy.int64)
    pystare.core._scidbContainsInstant(indices1, indices2, cmp)
    return cmp


