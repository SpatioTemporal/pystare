
# PySTARE Notes

## 2020-04-30 0.3.4 Add spatial_scale_km(resolution) to get estimate of length scale at resolution level.

## 2020-04-30 0.3.3 Fixed np -> numpy error in spatial_resolution...

## 2020-04-10 0.3.1 Fixed srange.contains
We don't have the  numpy.i SWIG mapping for int64_t to Python int working. Using "long long" on C++ and Python int when calling.

## 2020-04-10 0.3.0 Added srange
pystare.srange exposes SpatialRange functionality to Python. Example usage is shown in tests/test_intersections.py in the test_intersect_range_single_res test.

For example,
```
   r0 = pystare.srange()
   r0.add_intervals(hull0)
   r1 = pystare.srange()
   r1.add_intervals(hull1)
   r01 = pystare.srange()
   r01.add_intersect(r0,r1,False)
```
where the above shows how to use sranges to determine the intersection of two sets of intervals (hull0 and hull1) with the result being stored in srange r01.

srange has a SpatialRange object and a number of methods to manage its state.

