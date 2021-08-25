import datetime
import numpy
import pystare
import re


def from_utc(datetime, forward_resolution, reverse_resolution):
    return pystare.core._from_utc(datetime, forward_resolution, reverse_resolution)


def to_utc_approximate(indices):
    return pystare.core._to_utc_approximate(indices)


def from_utc_variable(datetime, forward_resolution, reverse_resolution):
    return pystare.core._from_utc_variable(datetime, forward_resolution, reverse_resolution)


def current_datetime():
    """
    Get a tiv from datetime.now().
    To convert back use numpy.array(pystare.to_utc_approximate(i),dtype='datetime64[ms]'"
    """
    # bad: hard-coded resolution 48
    now = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")[0:-3]
    now = numpy.array([now], dtype=numpy.datetime64)
    now = now.astype(numpy.int64)
    return pystare.from_utc(now, 48, 48)


def coarsest_resolution_finer_or_equal_ms(ms):
    resolutions = numpy.zeros(ms.shape, dtype=numpy.int64)
    pystare.core._coarsest_resolution_finer_or_equal_milliseconds(ms, resolutions)
    return resolutions


def cmp_temporal(indices1, indices2):
    out_length = len(indices1) * len(indices2)
    cmp = numpy.zeros([out_length], dtype=numpy.int64)
    pystare.core._cmp_temporal(indices1, indices2, cmp)
    return cmp


def from_tai_iso_strings(tai_strings_in):
    tai_strings = numpy.copy(tai_strings_in)
    out_length = len(tai_strings)
    tivs = numpy.zeros([out_length], dtype=numpy.int64)
    p = re.compile('^([0-9]{4})-([0-2][0-9])-([0-3][0-9])T([0-2][0-9]):([0-5][0-9]):([0-5][0-9])(.([0-9]+))?(\s\(([0-9]+)\s([0-9]+)\)\s\(([0-9])\))?$')
    for k in range(out_length):
        s = p.match(tai_strings[k])
        if s is not None:
            if s.groups()[7] is None:
                tai_strings[k] = tai_strings[k] + '.000 (48 48) (1)'
            elif s.groups()[8] is None:
                tai_strings[k] = tai_strings[k] + ' (48 48) (1)'
        else:
            raise ValueError('from_tai_iso_strings: unknown input "' + tai_strings[k] + '"')
    pystare.core._from_tai_iso_strings(list(tai_strings), tivs)
    return tivs


def to_tai_iso_strings(tivs):
    tai_strings = pystare.core._to_tai_iso_strings(tivs)
    return tai_strings


def to_temporal_triple_ms(tivs):
    ti_low = pystare.core.scidbLowerBoundMS(tivs)
    ti_hi = pystare.core.scidbUpperBoundMS(tivs)
    return (ti_low, tivs, ti_hi)


def lower_bound_tai(tiv):
    tret = tiv.copy()
    pystare.core._scidbLowerBoundTAI(tiv, tret)
    return tret


def upper_bound_tai(tiv):
    tret = tiv.copy()
    pystare.core._scidbUpperBoundTAI(tiv, tret)
    return tret


def lower_bound_ms(tiv):
    tret = tiv.copy()
    pystare.core._scidbLowerBoundMS(tiv, tret)
    return tret


def upper_bound_ms(tiv):
    tret = tiv.copy()
    pystare.core._scidbUpperBoundMS(tiv, tret)
    return tret


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


def to_julian_tai(indices):
    d1 = numpy.zeros(indices.shape, dtype=numpy.double)
    d2 = numpy.zeros(indices.shape, dtype=numpy.double)
    pystare.core._to_JulianTAI(indices, d1, d2)
    return d1, d2


def from_julian_tai(d1, d2):
    indices = numpy.zeros(d1.shape, dtype=numpy.int64)
    pystare.core._from_JulianTAI(d1, d2, indices)
    return indices


def to_julian_utc(indices):
    d1 = numpy.zeros(indices.shape, dtype=numpy.double)
    d2 = numpy.zeros(indices.shape, dtype=numpy.double)
    pystare.core._to_JulianUTC(indices, d1, d2)
    return d1, d2


def from_julian_utc(d1, d2):
    indices = numpy.zeros(d1.shape, dtype=numpy.int64)
    pystare.core._from_JulianUTC(d1, d2, indices)
    return indices


def set_reverse_resolution(indices, resolutions):
    result = numpy.zeros(indices.shape, dtype=numpy.int64)
    pystare.core._set_reverse_resolution(indices, resolutions, result)
    return result


def set_forward_resolution(indices, resolutions):
    result = numpy.zeros(indices.shape, dtype=numpy.int64)
    pystare.core._set_forward_resolution(indices, resolutions, result)
    return result


def reverse_resolution(indices):
    result = numpy.zeros(indices.shape, dtype=numpy.int64)
    pystare.core._reverse_resolution(indices, result)
    return result


def forward_resolution(indices):
    result = numpy.zeros(indices.shape, dtype=numpy.int64)
    pystare.core._forward_resolution(indices, result)
    return result


def coarsen(indices, reverse_increments, forward_increments):
    """TODO: Not tested"""
    result = numpy.zeros(indices.shape, dtype=numpy.int64)
    pystare.core._coarsen(indices, reverse_increments, forward_increments, result)
    return result


def set_temporal_resolutions_from_sorted(sorted_indices, include_bounds=True):
    pystare.core._set_temporal_resolutions_from_sorted_inplace(sorted_indices, include_bounds)
    return sorted_indices

