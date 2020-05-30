
# PySTARE Notes

## 2020-05-28 0.5.0

Added auto-sizing of results to many returns. Changed default in
from_polygon to nonconvex=True. Fixed subtle case where trixel was
dropped because its center, vertices, and mid-edge points were all
outside the polygon. Added a calculation that checks for intersecting
edges between the test trixel edges and the polygon edges.

CW polygons now yield the complement of the nonconvex hull. CCW
returns the interior and boundary.

## 2020-05-22 0.4.1 Tweaked a test case.

## 2020-05-22 0.4.0 Add non convex hull routine.

## 2020-05-01 0.3.6 Add spatial_ helper routines.

## 2020-04-30 0.3.5 Add spatial_scale_km(resolution) to get estimate of length scale at resolution level.

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

