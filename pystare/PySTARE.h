/**
 * PySTARE.h
 *
 *  Created on: Jun 13, 2019
 *      Author: mrilee
 *
 *  Copyright (C) 2019 Rilee Systems Technologies LLC
 *
 *
 *  EXAMPLE
 *
 *  p = newSTARE(); d=np.array([1,2,3],dtype=np.double); i=np.zeros(3,dtype=np.int64); ValueFromJDTAINP(p,i,d,100);
 *
 *  lat=np.array([-45],dtype=np.double); lon=np.array([135],dtype=np.double); i=np.zeros(1,dtype=np.int64);  ValueFromLatLonDegreesLevelNP( p, i, lat, lon, 20 ); print(lat,lon,i)
 *
 *  [-45.] [135.] [720575940379279476]
 *
 *  deleteSTARE(p);
 */

#ifndef INCLUDE_PYSTARE_H_
#define INCLUDE_PYSTARE_H_

#include <stdio.h>
#include "STARE.h"
#include "SpatialRange.h"
#include "TemporalIndex.h"

static STARE stare;

// Info & Utility
const char* stare_version();

// Spatial
void _from_latlon(double* lat, int len_lat,
                  double * lon, int len_lon,
                  int64_t* indices, int level);

void _from_latlon2D(double* lat, int lalen1, int lalen2, 
                    double* lon, int lolen1, int lolen2, 
                    int64_t* indices, int len1, int len2, 
                    int level, bool adapt_resolution,
		    bool fill_value_enabled,
		    double fill_value_in,
		    int fill_value_out // Careful with the cast
		    );

void _to_latlon(int64_t* indices, int len, double* lat, double* lon);
void _to_latlonlevel(int64_t* indices, int len, double* lat, double* lon, int* levels);
void _to_level(int64_t* indices, int len,  int* levels);
void _to_area(int64_t* indices, int len, double* areas);
void _from_intervals(int64_t* intervals, int len, int64_t* indices_starts, int64_t* indices_terminators );

// Broken or dangerous. void to_vertices(int64_t* indices, int len, int64_t* vertices0, int64_t* vertices1, int64_t* vertices2, int64_t* centroid);
void _to_vertices_latlon(int64_t* indices, int len, double* triangle_info_lats, int dmy1, double* triangle_info_lons, int dmy2 );

void _to_compressed_range(int64_t* indices, int len, int64_t* range_indices, int len_ri);
void _intersect(int64_t* indices1, int len1, int64_t* indices2, int len2, int64_t* intersection, int leni);
void _intersect_multiresolution(int64_t* indices1, int len1, int64_t* indices2, int len2, int64_t* intersection, int leni);
void _cmp_spatial(int64_t* indices1, int len1, int64_t* indices2, int len2, int64_t* cmp, int len12);
void _intersects(int64_t* indices1, int len1, int64_t* indices2, int len2, int* intersects, int method=0);

// Temporal
void _from_utc(int64_t *datetime, int len, int64_t *indices_out, int forward_resolution, int reverse_resolution);
void _from_utc_variable(int64_t *datetime, int len, int64_t *indices_out, int64_t* forward_resolution, int lenf, int64_t* reverse_resolution, int lenr);
void _to_utc_approximate(int64_t* indices, int len, int64_t* datetime_out);
void _cmp_temporal(int64_t* indices1, int len1, int64_t* indices2, int len2, int64_t* cmp, int len12);
void _coarsest_resolution_finer_or_equal_milliseconds(double*  milliseconds, int len, int64_t* out_array);
void _milliseconds_at_resolution(int64_t* resolutions, int len, double* millisecond);
void _from_tai_iso_strings(char **taiStrings, int64_t* out_array, int out_length);
char** _to_tai_iso_strings(int64_t* indices, int len);

void _scidbTemporalValueIntersectionIfOverlap (int64_t* indices1, int len1, int64_t* indices2, int len2, int64_t* cmp, int len12);
void _scidbTemporalValueUnionIfOverlap        (int64_t* indices1, int len1, int64_t* indices2, int len2, int64_t* cmp, int len12);
void _scidbOverlapTAI                         (int64_t* indices1, int len1, int64_t* indices2, int len2, int64_t* cmp, int len12);
void _scidbOverlap                            (int64_t* indices1, int len1, int64_t* indices2, int len2, int64_t* cmp, int len12);
void _scidbContainsInstant                    (int64_t* indices1, int len1, int64_t* indices2, int len2, int64_t* cmp, int len12);

void _set_reverse_resolution(int64_t* indices, int len,
                             int64_t* reverse_resolution, int lenr,
                             int64_t* out_array, int out_length
                             );

void _set_forward_resolution(int64_t* indices, int len,
                             int64_t* forward_resolution, int lenf,
                             int64_t* out_array, int out_length
                             );

void _forward_resolution(int64_t* indices, int len,
                         int64_t* out_array, int out_length
                         );

void _reverse_resolution(int64_t* indices, int len,
                         int64_t* out_array, int out_length
                         );
                         
void _coarsen(int64_t* indices, int len,
                 int64_t* reverse_increment, int lenr,
                 int64_t* forward_increment, int lenf,
                 int64_t* out_array, int out_length
                 );

//void to_utc(int64_t* indices, int len, double* julian_day);
//void from_tai(double* julian_day, int len, int64_t indices);
//void to_tai(int64_t* indices, int len, double* julian_day);

/*
  From TemporalIndex.h
 */
void _scidbUpperBoundTAI(int64_t* indices, int len, int64_t* out_array, int out_length);
void _scidbLowerBoundTAI(int64_t* indices, int len, int64_t* out_array, int out_length);
void _scidbUpperBoundMS(int64_t* indices, int len, int64_t* out_array, int out_length);
void _scidbLowerBoundMS(int64_t* indices, int len, int64_t* out_array, int out_length);
void _scidbNewTemporalValue(int64_t* indices, int len, int64_t* new_indices, bool include_bounds);

void _from_JulianTAI (double* d1, int nd1, double* d2, int nd2, int64_t* indices, int f_res, int r_res);
void _to_JulianTAI   (int64_t* indices, int len, double* d1, double* d2);

void _from_JulianUTC (double* d1, int nd1, double* d2, int nd2, int64_t* indices, int f_res, int r_res);
void _to_JulianUTC   (int64_t* indices, int len, double* d1, double* d2);

void _set_temporal_resolutions_from_sorted_inplace (int64_t* indices_inplace, int len, bool include_bounds);

/****/

enum StareResultCase { SpatialIntervals, ArrayIndexSpatialValues };

class StareResult {
 public:
  StareResult() {};
  void add_intervals(STARE_SpatialIntervals sis) { this->sis = sis; this->sCase = SpatialIntervals; }
  void add_indexValues(STARE_ArrayIndexSpatialValues sisvs) { this->sisvs = sisvs; this->sCase = ArrayIndexSpatialValues; }
  virtual ~StareResult();
  int                           get_size();
  bool                          values_multi_resolution = true;
  void                          set_values_multi_resolution(bool multi_resolution);
  int                           get_size_as_values();
  int                           get_size_as_intervals();
  void                          copy             (int64_t* indices, int len);
  void                          copy_as_values   (int64_t* indices, int len);
  void                          copy_as_intervals(int64_t* indices, int len);
  void                          convert();
  bool                          converted = false;
  STARE_SpatialIntervals        sis;
  STARE_ArrayIndexSpatialValues sisvs;
  StareResultCase               sCase;
};

// void _to_neighbors(int64_t* indices, int len, int64_t* range_indices, int len_ri);
StareResult _to_neighbors(int64_t* indices, int len);

StareResult _to_circular_cover(double lat, double lon, double radius, int resolution);
StareResult _to_nonconvex_hull_range_from_latlon(double* lat, int len_lat, double* lon, int len_lon, int resolution);

// void _expand_intervals(int64_t* indices, int len, int resolution, int64_t* range_indices, int len_ri, int64_t* result_size, int len_rs);
StareResult _expand_intervals(int64_t* indices, int len, int resolution, bool multi_resolution);

// void _to_box_cover_from_latlon(double* lat, int len_lat, double* lon, int len_lon, int resolution, int64_t* range_indices, int len_ri, int64_t* result_size, int len_rs);
StareResult _to_box_cover_from_latlon(double* lat, int len_lat, double* lon, int len_lon, int resolution);

// void _to_hull_range   (int64_t* indices, int len, int resolution, int64_t* range_indices, int len_ri, int64_t* result_size, int len_rs);
StareResult _to_hull_range   (int64_t* indices, int len, int resolution);

// void _to_hull_range_from_latlon(double* lat, int len_lat, double* lon, int len_lon, int resolution, int64_t* range_indices, int len_ri, int64_t* result_size, int len_rs);
StareResult _to_hull_range_from_latlon(double* lat, int len_lat, double* lon, int len_lon, int resolution); // , int64_t* range_indices, int len_ri, int64_t* result_size, int len_rs);

void _adapt_resolution_to_proximity(int64_t* indices, int len, int64_t* range_indices, int len_ri);

/**
 * A wrapper for SpatialRange.
 */
class srange {
public:
  srange();
  srange(int64_t* indices, int len);
  virtual ~srange();

  void add_intervals(int64_t* indices, int len);
  void add_range(const SpatialRange& r) { range.addSpatialRange(r); }
  
  // bool contains(int64_t siv);
  bool contains(long long siv);
  void acontains(int64_t* indices1, int len1, int64_t* indices2, int len2, int fill_value = -1 );

  bool intervals_extracted = false;
  void extract_intervals();
  int get_size_as_intervals();
  void copy_intervals(int64_t* indices, int len);

  bool values_extracted = false;
  bool values_multi_resolution = true;
  void set_values_multi_resolution(bool multi_resolution);
  void extract_values(); // defaults to !multi_res
  int get_size_as_values(); // defaults to !multi_res
  void copy_values(int64_t* indices, int len);

  void reset_extraction();
  void reset();
  void purge();
  void compress() { range.compress(); }

  SpatialRange range;
  STARE_SpatialIntervals sis;
  STARE_ArrayIndexSpatialValues sivs;

  void add_intersect(const srange& one, const srange& other,bool compress) {
    // cout << " compress " << compress << endl << flush;
    
//   HstmRange *range1 = new HstmRange(range.range->range->RangeFromIntersection(other.range.range->range,compress)); // NOTE mlr Probably about the safest way to inst. SpatialRange.
// // #define DIAG
// #ifdef DIAG
// 	KeyPair kp; 
//     range1->reset(); 
//     range1->getNext(kp);
// 	cout << "sr_i range1,r->r,nr " << range1 << " " << range1->range << " " << range1->range->nranges() << " : "
// 			<< setw(16) << setfill('0') << hex << kp.lo << " "
// 			<< setw(16) << setfill('0') << hex << kp.hi << " "
// 			<< dec
// 			<< endl << flush;
// 	EmbeddedLevelNameEncoding leftJustified;
// 	leftJustified.setId(kp.lo); 
//     cout << "kp.lo lj " << setw(16) << setfill('0') << hex << leftJustified.getSciDBLeftJustifiedFormat() << endl << flush;
// 	leftJustified.setId(kp.hi); cout << "kp.hi lj " << setw(16) << setfill('0') << hex << leftJustified.getSciDBLeftJustifiedFormat() << endl << flush;
// 	cout << " r-r-my_los " << hex << range1->range->my_los << endl << flush;
// 	cout << dec;
// #endif
//    cout << 1000 << endl << flush;
    // SpatialRange *res = new SpatialRange(range1);
    // Yay! Works: SpatialRange *res = (one.range & other.range);
    SpatialRange *res = sr_intersect(one.range,other.range,compress);
    //    cout << 1100 << " 11 nr = " << res->range->range->nranges() << endl << flush;
    // srange result; result.set_tag(999);
    range.addSpatialRange(*res);
    // STARE_SpatialIntervals sis_res = res->toSpatialIntervals();
    //    cout << 1150 << endl << flush;
    // range.addSpatialIntervals(sis_res);
    // cout << 1200 << " 12 nr = " << range.range->range->nranges() << endl << flush;
    // res->purge();
    // delete res;
    //    cout << 1300 << endl << flush;
  }
};

#endif

