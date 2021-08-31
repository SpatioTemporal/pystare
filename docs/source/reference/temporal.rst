pystare.temporal
====================================
.. currentmodule:: pystare.temporal


Conversions
--------------
.. autosummary::
    :toctree: api/

    from_ms_since_epoch_utc
    to_ms_since_epoch_utc

++++++++
Strings
++++++++
.. autosummary::
    :toctree: api/

    from_iso_strings
    from_stare_timestrings
    to_stare_timestring

++++++++
Julian
++++++++
.. autosummary::
    :toctree: api/

    from_julian_date
    to_julian_date

+++++++++
Triples
+++++++++
.. autosummary::
    :toctree: api/

    to_temporal_triple_ms
    from_temporal_triple

Timestring manipulations
-------------------------
.. autosummary::
    :toctree: api/

    analyze_iso8601_string
    validate_iso8601_string
    validate_iso8601_strings
    validate_stare_timestring
    validate_stare_timestrings
    force_3ms
    iso_to_stare_timestrings

Resolution functions
---------------------
.. autosummary::
    :toctree: api/

    coarsest_resolution_finer_or_equal_ms
    milliseconds_at_resolution
    set_reverse_resolution
    set_forward_resolution
    reverse_resolution
    forward_resolution
    coarsen



Overlay functions
--------------------
.. autosummary::
    :toctree: api/

    cmp_temporal
    temporal_value_intersection_if_overlap
    temporal_value_union_if_overlap
    temporal_contains_instant

N/A
-----------
.. autosummary::
    :toctree: api/

    from_utc_variable
    now

