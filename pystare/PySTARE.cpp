/*
 * PySTARE.cpp
 *
 *  Created on: Jun 13, 2019
 *      Author: mrilee
 *
 *  Copyright (C) 2019 Rilee Systems Technologies LLC
 */


#include "PySTARE.h"

#include <algorithm>

// Info
const char* stare_version() { return STARE_version(); }

// Spatial
void _from_latlon(double* lat, int len_lat, double * lon, int len_lon, int64_t* indices, int level) {
    for (int i=0; i<len_lat; i++) {        
        indices[i] = stare.ValueFromLatLonDegrees(lat[i], lon[i], level);
    }
}

void _from_latlon2D(double* lat, int lalen1, int lalen2, 
                 double* lon, int lolen1, int lolen2, 
                 int64_t* indices, int len1, int len2, int level, bool adapt_resolution) {
    int n;   
    static EmbeddedLevelNameEncoding lj;       // Use this to get the mask
    int lvl;
    
    for (int i=0; i<lalen1; i++) {        
        for (int j=0; j<lalen2; j++) {   
            n = i * lalen2 + j;
            indices[n] = stare.ValueFromLatLonDegrees(lat[n], lon[n], level);   
            if (adapt_resolution) {
                if (j==0) {        
                    indices[n+1] = stare.ValueFromLatLonDegrees(lat[n+1], lon[n+1], level);            
                    lvl = stare.cmpSpatialResolutionEstimateI(indices[n], indices[n+1]);
                    indices[n] = (indices[n]& ~lj.levelMaskSciDB) | lvl;
                } else {                    
                    lvl = stare.cmpSpatialResolutionEstimateI(indices[n-1], indices[n]);
                    indices[n] = (indices[n]& ~lj.levelMaskSciDB) | lvl;
                }
            }
        }
    }
}



void _to_latlon(int64_t* indices, int len, double* lat, double* lon) {
    for (int i=0; i< len; i++) { 
        LatLonDegrees64 latlon = stare.LatLonDegreesFromValue(indices[i]);
		lat[i] = latlon.lat; 
        lon[i] = latlon.lon;
    }    
}

void _to_latlonlevel(int64_t* indices, int len, double* lat, double* lon, int* levels) {
    for (int i=0; i<len; i++) {                
        LatLonDegrees64 latlon = stare.LatLonDegreesFromValue(indices[i]);
        lat[i] = latlon.lat; 
        lon[i] = latlon.lon;
        levels[i] = stare.ResolutionLevelFromValue(indices[i]);
    }
}

void _to_level(int64_t* indices, int len, int* levels) {
    for (int i=0; i<len; i++) {                
        levels[i] = stare.ResolutionLevelFromValue(indices[i]);
    }
}

/*
 * Broken or dangerous
 *
void to_vertices(int64_t* indices, int len, int64_t* vertices0, int64_t* vertices1, int64_t* vertices2, int64_t* centroid) {
    for (int i=0; i<len; i++) {
        Triangle tr = stare.TriangleFromValue(indices[i]);
#if DIAG
        cout << "tr: " << setw(16) << hex << indices[i] << dec << " ";
        for(int j=0; j<3; ++j) { cout << setw(16) << tr.vertices[j] << "; "; }
#endif
        vertices0[i] = stare.ValueFromSpatialVector(tr.vertices[0]);
        vertices1[i] = stare.ValueFromSpatialVector(tr.vertices[1]);
        vertices2[i] = stare.ValueFromSpatialVector(tr.vertices[2]);
        centroid[i]  = stare.ValueFromSpatialVector(tr.centroid);
#if DIAG
        cout << setw(16) << hex
        		<< vertices0[i] << " "
				<< vertices1[i] << " "
				<< vertices2[i] << dec;
        cout << endl << flush;
#endif
    }
}
*/

/*
 * len of the output arrays is 4 times the input array lenght (len).
 */
void _to_vertices_latlon(int64_t* indices, int len, double* triangle_info_lats, int dmy1, double* triangle_info_lons, int dmy2 ) {
	double lat = 0, lon = 0;
	int k=0;
    for (int i=0; i<len; i++) {
        Triangle tr = stare.TriangleFromValue(indices[i]);
#if DIAG
        cout << "tr: " << setw(16) << hex << indices[i] << dec << " ";
        for(int j=0; j<3; ++j) { cout << setw(16) << tr.vertices[j] << "; "; }
#endif
        for(int j=0; j<3; ++j) {
        	tr.vertices[j].getLatLonDegrees(lat,lon);
        	triangle_info_lats[k] = lat; triangle_info_lons[k] = lon;
        	++k;
        }
    	tr.centroid.getLatLonDegrees(lat, lon);
    	triangle_info_lats[k] = lat; triangle_info_lons[k] = lon;
    	++k;
#if DIAG
        cout << setw(16) << hex
        		<< vertices0[i] << " "
				<< vertices1[i] << " "
				<< vertices2[i] << dec;
        cout << endl << flush;
#endif
    }
}

void _to_area(int64_t* indices, int len, double* areas) {
    for (int i=0; i<len; i++) {
        areas[i] = stare.AreaFromValue(indices[i]);        
    }
}

/**
 * Go from an array of [id|id..term] to a pair of arrays [id][term] to aid tests for inclusion.
 */


void _from_intervals(int64_t* intervals, int len, int64_t* indices_starts, int64_t* indices_terminators ) {
	// cout << "len: " << len << endl << flush;
	// if(false) {
	EmbeddedLevelNameEncoding leftJustified;
	int i=0, iDest=0;
	do {
		indices_starts[iDest] = intervals[i];
		if(i+1 < len) {
			if( (intervals[i+1] & leftJustified.levelMaskSciDB) == leftJustified.levelMaskSciDB ) {
				indices_terminators[iDest++] = intervals[++i]; // If the next one is a terminator, use it.
			} else {
				leftJustified.setIdFromSciDBLeftJustifiedFormat(intervals[i]);
				indices_terminators[iDest++] = leftJustified.getSciDBTerminatorLeftJustifiedFormat(); // If next is not, make one.
			}
		} else {
			leftJustified.setIdFromSciDBLeftJustifiedFormat(intervals[i]);
			indices_terminators[iDest++] = leftJustified.getSciDBTerminatorLeftJustifiedFormat(); // No more left, make on.
		}
		++i; // Next
	} while(i<len);
	if(iDest<len) {
		indices_starts[iDest]=-998;
		indices_terminators[iDest]=-999;
	}
//	}
//	for(int i=0; i< len; ++i) {
//		indices_starts[i]=i*10;
//		indices_terminators[i]=i*100;
//	}
}

StareResult _expand_intervals(int64_t* indices, int len, int resolution, bool multi_resolution) {
  STARE_SpatialIntervals si(indices,indices+len);
  StareResult result;
  result.add_indexValues(expandIntervalsMultiRes(si,resolution, multi_resolution));
  return result;
}

StareResult _to_neighbors(int64_t* indices, int len) { 
  STARE_ArrayIndexSpatialValues sivs(indices, indices+len);
  StareResult result;
  STARE_ArrayIndexSpatialValues neighbors;
  for(int i = 0; i < len; ++i )  {
    STARE_ArrayIndexSpatialValues n = stare.NeighborsOfValue(indices[i]);
    neighbors.insert( neighbors.end(), n.begin(), n.end() );
  }
  result.add_indexValues(neighbors);
  return result;
}

void _adapt_resolution_to_proximity(int64_t* indices, int len, int64_t* range_indices, int len_ri) {
  // if len != len_ri, throw something...
  STARE_ArrayIndexSpatialValues sivs(indices, indices+len);
  STARE_ArrayIndexSpatialValues result = stare.adaptSpatialResolutionEstimates(sivs);
  for(int i = 0; i < len; ++i) {
    range_indices[i] = result[i];
  }
  // Consider stare.adaptSpatialResolutionEstimatesInPlace(range_indices); or even indices...
}
StareResult _to_circular_cover(double lat, double lon, double radius, int resolution) {
  StareResult result; 
  result.add_intervals(stare.CoverCircleFromLatLonRadiusDegrees(lat,lon,radius,resolution));
  return result;
}
StareResult _to_box_cover_from_latlon(double* lat, int len_lat, double* lon, int len_lon, int resolution) {
  StareResult result;
  LatLonDegrees64ValueVector points;
  for(int i=0; i<len_lat; ++i) {
    points.push_back(LatLonDegrees64(lat[i], lon[i]));
  }
  result.add_intervals(stare.CoverBoundingBoxFromLatLonDegrees(points, resolution));
  return result;
}

void _to_compressed_range(int64_t* indices, int len, int64_t* range_indices, int len_ri) {
	STARE_SpatialIntervals si(indices, indices+len);
	SpatialRange r(si);
	r.compress();
	STARE_SpatialIntervals result = r.toSpatialIntervals(); 
	for(int i=0; i<result.size(); ++i) {
		range_indices[i] = result[i];
	}
}

StareResult _to_hull_range(int64_t* indices, int len, int resolution) {
  StareResult result;
  STARE_ArrayIndexSpatialValues sivs(indices, indices+len);
  result.add_intervals( stare.ConvexHull(sivs, resolution));
  return result;
}

StareResult _to_hull_range_from_latlon(double* lat, int len_lat, double* lon, int len_lon, int resolution) { 
  StareResult result;
  LatLonDegrees64ValueVector points;
  for(int i=0; i<len_lat; ++i) {
    points.push_back(LatLonDegrees64(lat[i], lon[i]));
  }
  result.add_intervals(stare.ConvexHull(points, resolution));
  return result;
}

StareResult _to_nonconvex_hull_range_from_latlon(double* lat, int len_lat, double* lon, int len_lon, int resolution) {
  StareResult result;
  LatLonDegrees64ValueVector points;
  for(int i=0; i<len_lat; ++i) {
    points.push_back(LatLonDegrees64(lat[i], lon[i]));
  }
  result.add_intervals(stare.NonConvexHull(points, resolution));
  return result;
}

void _intersect(int64_t* indices1, int len1, int64_t* indices2, int len2, int64_t* intersection, int leni) {
  STARE_SpatialIntervals si1(indices1, indices1+len1);
  STARE_SpatialIntervals si2(indices2, indices2+len2);
  SpatialRange r1(si1);   
  SpatialRange r2(si2);
  SpatialRange *ri = sr_intersect(r1, r2, false);
  STARE_SpatialIntervals result_intervals = ri->toSpatialIntervals();
  delete ri;
#if 0
  cout << "_intersect:result_intervals" << endl << flush;
  for(int i=0; i < result_intervals.size(); ++i) {
    if ( i < 10 ) {
      cout << "_intersect:result_intervals: " << setw(4) << dec << i << " " << setw(16) << hex << result_intervals[i] << endl << flush;
    }
  }
#endif
  //  cout << "_intersect:expandIntervals" << endl << flush;
  STARE_ArrayIndexSpatialValues result = expandIntervals(result_intervals);
  // cout << "_intersect:size" << endl << flush;
  int leni_ = result.size();
#if 0
  cout << "_intersect:leni_" << " " << leni << endl << flush;
  cout << "_intersect:result" << endl << flush;
#endif
  for(int i=0; i<leni_; ++i) {
#if 0
    if( i < 10 ) {
      cout << "_intersect:result: " << setw(4) << dec << i << " " << setw(16) << hex << result[i] << endl << flush;
    }
#endif
    intersection[i] = result[i];
  }
}

void _intersects(int64_t* indices1, int len1, int64_t* indices2, int len2, int* intersects, int method) {
  if( method == 0 ) {
    STARE_SpatialIntervals si1(indices1, indices1+len1);
    SpatialRange r1(si1); // Possibly avoid copy above with new constructor?
    for(int i=0; i<len2; ++i) {
      intersects[i] = 0;
      int istat = r1.intersects(indices2[i]);
      if( istat != 0 ) {
	intersects[i] = 1;
      }
    }
  } else if( method == 1 ) {
    // Binary sort and search
    sort(indices1,indices1+len1);
    for(int i=0; i<len2; ++i) {
      STARE_ArrayIndexSpatialValue test_siv = indices2[i];
      intersects[i] = 0;
      int start=0;
      int end=len1-1;
      int m = (start+end)/2;
      bool done = false;
      while( !done ) {
	m = (start+end)/2;
	if(indices1[m] < test_siv) {
	  start = m+1;
	  done = start > end;
	} else if(indices1[m] > test_siv) {
	  end = m-1;
	  done = start > end;
	} else {
	  intersects[i] = 1; done = true;
	}
      }
      if( intersects[i] == 0 ) {
	if( (end >= 0) || (start < len1) ) {
	  if( 0 <= m-1 ) {
	    if( cmpSpatial(indices1[m-1],test_siv) != 0 ) {
	      intersects[i] = 1;
	    }
	  }
	  if( (0 <= m) && (m < len1) ) {
	    if( cmpSpatial(indices1[m],test_siv) != 0 ) {
	      intersects[i] = 1;
	    }
	  }
	  if( m+1 < len1 ) {
	    if( cmpSpatial(indices1[m+1],test_siv) != 0 ) {
	      intersects[i] = 1;
	    }
	  }
	}
      }
    }    
  } else {
    // Fall-through

    for(int i=0; i<len2; ++i) {        
      intersects[i] = 0;
      for(int j=0; j<len1; ++j) {
	if (cmpSpatial(indices2[i], indices1[j]) != 0) {
	  intersects[i] = 1;
	  break;
	}            
      }
    }
  } 
}

void _intersect_multiresolution(int64_t* indices1, int len1, int64_t* indices2, int len2, int64_t* intersection, int leni) {
  // cout << "lens: " << len1 << " " << len2 << " " << leni << endl << flush;
	STARE_SpatialIntervals si1(indices1, indices1+len1), si2(indices2, indices2+len2);
	// cout << 100 << endl << flush;

    // intersection[0] = 69;
	SpatialRange r1(si1), r2(si2);
	// cout << 200 << endl << flush;
	// SpatialRange *ri = r1 & r2;
	// SpatialRange ri = sr_intersect(r1,r2,true);
	SpatialRange *ri = sr_intersect(r1,r2,true); // Should be true here, was false.
	// cout << 300 << endl << flush;
	STARE_SpatialIntervals result_intervals = ri->toSpatialIntervals();
	delete ri;
	// STARE_ArrayIndexSpatialValues result = expandIntervals(result_intervals);
	STARE_ArrayIndexSpatialValues result = expandIntervalsMultiRes(result_intervals,-1,true);
	// cout << 400 << endl << flush;
	leni = result.size();
	// cout << 500 << " result size " << result.size() << endl << flush;
	for(int i=0; i<leni; ++i) {
		intersection[i] = result[i];
	}
	// cout << 600 << endl << flush;
}

void _cmp_spatial(int64_t* indices1, int len1, int64_t* indices2, int len2, int64_t* cmp, int len12) {
	STARE_ArrayIndexSpatialValues sivs1(indices1, indices1+len1), sivs2(indices2, indices2+len2);
	int k=0;
	for(int i=0; i<len1; ++i) {
		for(int j=0; j<len2; ++j) {
			cmp[k] = cmpSpatial(indices1[i], indices2[j]); // i.e. [i*len2+j]
			++k;
		}
	}
}

// Temporal

void _coarsest_resolution_finer_or_equal_milliseconds(double*  milliseconds, int len, int64_t* out_array) {
  TemporalIndex tIndex;
  for(int i=0; i<len; ++i) {
    out_array[i] = tIndex.coarsestResolutionFinerOrEqualMilliseconds(milliseconds[i]);
  }
}

void _milliseconds_at_resolution(int64_t* resolutions, int len, double* millisecond) {
  TemporalIndex tIndex;
  for(int i=0; i<len; ++i) {
    millisecond[i] = tIndex.millisecondsAtResolution(resolutions[i]);
  }
}

void _from_utc(int64_t *datetime, int len, int64_t *indices_out
	      , int forward_resolution
	      , int reverse_resolution
	      ) {
	// datetime is in ms (numpy default).
	// double jd19700101_erfa = 2440587.5;

//    cout << "from_utc resolution: " << resolution << endl << flush;
	// cout << "from_utc" << endl << flush;
    int type = 1;
    for (int i=0; i<len; i++) {
    	int64_t idt = datetime[i]/1000;
        indices_out[i] = stare.ValueFromUTC((time_t&)idt
					    , forward_resolution
					    , reverse_resolution
					    , type);
        idt = datetime[i]%1000;
        stare.tIndex.set_millisecond(idt);
        indices_out[i] = stare.getArrayIndexTemporalValue();
        /*
        double jd = stare.toJulianDayUTC();
        double delta = jd - 2440587.5;
        double iDelta = delta*86400.0;
        cout
		<< setprecision(16)
		<< dec << i << " dt,jd,delta,iDelta "
		<< datetime[i] << " "
		<< setw(16) << setfill('0')	<< hex
		<< indices_out[i] << " "
		 << dec
		 << setw(20) << setfill(' ') << scientific
		 << jd << " "
		 << setw(20) << setfill(' ') << scientific
	     << delta << " "
		 << setw(20) << setfill(' ') << scientific
		 << iDelta << " "
		 << stare.tIndex.toStringJulianTAI()
		 << endl << flush;
		 */
    }
//    cout << endl << flush;
}

void _from_utc_variable(int64_t *datetime, int len, int64_t *indices_out, int64_t* forward_resolution, int lenf, int64_t* reverse_resolution, int lenr) {
	// datetime is in ms (numpy default).
	// double jd19700101_erfa = 2440587.5;

//    cout << "from_utc resolution: " << resolution << endl << flush;
	// cout << "from_utc" << endl << flush;
    int type = 1;
    for (int i=0; i<len; i++) {
    	int64_t idt = datetime[i]/1000;
        indices_out[i] = stare.ValueFromUTC((time_t&)idt
					    , forward_resolution[i]
					    , reverse_resolution[i]
					    , type);
        idt = datetime[i]%1000;
        stare.tIndex.set_millisecond(idt);
        indices_out[i] = stare.getArrayIndexTemporalValue();
        /*
        double jd = stare.toJulianDayUTC();
        double delta = jd - 2440587.5;
        double iDelta = delta*86400.0;
        cout
		<< setprecision(16)
		<< dec << i << " dt,jd,delta,iDelta "
		<< datetime[i] << " "
		<< setw(16) << setfill('0')	<< hex
		<< indices_out[i] << " "
		 << dec
		 << setw(20) << setfill(' ') << scientific
		 << jd << " "
		 << setw(20) << setfill(' ') << scientific
	     << delta << " "
		 << setw(20) << setfill(' ') << scientific
		 << iDelta << " "
		 << stare.tIndex.toStringJulianTAI()
		 << endl << flush;
		 */
    }
//    cout << endl << flush;
}

void _to_utc_approximate(int64_t *indices, int len, int64_t *datetime_out) {
	double jd19700101_erfa = 2440587.5;
//	cout << "to_utc_approximate" << endl << flush;
  for (int i=0; i<len; i++) {
    stare.setArrayIndexTemporalValue(indices[i]);
    double jd = stare.toJulianDayUTC();
    // double jdt = stare.toJulianDayTAI();
    double delta = jd-jd19700101_erfa;
    int64_t iDelta = int64_t(delta*86400000.0+0.5); // m-sec now. since that's what numpy defaults to it seems
    /*
	   cout << setprecision(16)
		 << " jd,jdt,delta,iDelta "
		 << hex << setw(16) << setfill('0')
		 << indices[i] << " "
		 << dec
		 << setw(20) << setfill(' ') << scientific
		 << jd << " "
		 << setw(20) << setfill(' ') << scientific
		 << jdt << " "
		 << setw(20) << setfill(' ') << scientific
	     << delta << " "
		 << setw(20) << setfill(' ') << scientific
		 << iDelta << " "
		 << stare.tIndex.toStringJulianTAI()
		 << endl << flush;
     */
    datetime_out[i] = iDelta;
  }
//  cout << endl << flush;
}

void _cmp_temporal(int64_t* indices1, int len1, int64_t* indices2, int len2, int64_t* cmp, int len12) {
  // STARE_ArrayIndexTemporalValues tivs1(indices1,indices1+len1), tivs2(indices2,indices2+len2);
	int k=0;
	for(int i=0; i<len1; ++i) {
		for(int j=0; j<len2; ++j) {
			cmp[k] = cmpTemporalAtResolution2(indices1[i],indices2[j]); // i.e. [i*len2+j]
			++k;
		}
	}
}

void _from_tai_iso_strings(char ** taiStrings, int64_t* out_array, int out_length) {
    int i = 0;
    while (taiStrings[i]) {
      out_array[i] = fromStringJulianTAI_ISO(taiStrings[i]);
	 free(taiStrings[i]); // Good bye, memory leak!
         i++;
    }
    // i is the length
    return;
}

char **  _to_tai_iso_strings(int64_t* indices, int len ) {
  // printf("to_ti: len: %d\n",len);
  char ** taiStrings = (char **) malloc((len+1) * sizeof(char*));
  for( int i = 0; i < len+1; ++ i ) {
    taiStrings[i] = (char *) NULL;
  }
  // printf("to_ti:100\n");
    int i = 0;
    while (i < len) {
      // printf("to_ti: i: %d\n",i);
      // printf("to_ti: x%016x",indices[i]);
      string s = toStringJulianTAI_ISO(indices[i]);
      taiStrings[i] = (char*)malloc((s.size()+1)*sizeof(char));
      // printf(" s.size: %d ",s.size());
      s.copy(taiStrings[i],s.size());
      taiStrings[i][s.size()] = '\0';
      // printf("%s\n",taiStrings[i]);
      i++;
    }
    // printf("to_ti:999\n");
    // i is the length
    return taiStrings;
}

void _scidbUpperBoundTAI(int64_t* indices, int len, int64_t* out_array, int out_length) {
  for( int i=0; i < len; ++i ) {
    out_array[i] = scidbUpperBoundTAI(indices[i]);
  }
}
void _scidbLowerBoundTAI(int64_t* indices, int len, int64_t* out_array, int out_length) {
  for( int i=0; i < len; ++i ) {
    out_array[i] = scidbLowerBoundTAI(indices[i]);
  }
}
void _scidbUpperBoundMS(int64_t* indices, int len, int64_t* out_array, int out_length) {
  for( int i=0; i < len; ++i ) {
    out_array[i] = scidbUpperBoundMS(indices[i]);
  }
}
void _scidbLowerBoundMS(int64_t* indices, int len, int64_t* out_array, int out_length) {
  for( int i=0; i < len; ++i ) {
    out_array[i] = scidbLowerBoundMS(indices[i]);
  }
}
void _scidbNewTemporalValue(int64_t* indices, int len, int64_t* new_indices, bool include_bounds) {
  new_indices[0] = scidbNewTemporalValue(indices[0],indices[1],indices[2],include_bounds);
}

void _scidbTemporalValueIntersectionIfOverlap (int64_t* indices1, int len1, int64_t* indices2, int len2, int64_t* cmp, int len12){
  for( int i = 0; i < len1; ++i ) {
    cmp[i] = scidbTemporalValueIntersectionIfOverlap(indices1[i],indices2[i]);
  }
}
void _scidbTemporalValueUnionIfOverlap        (int64_t* indices1, int len1, int64_t* indices2, int len2, int64_t* cmp, int len12){
  for( int i = 0; i < len1; ++i ) {
    cmp[i] = scidbTemporalValueUnionIfOverlap(indices1[i],indices2[i]);
  }
}
void _scidbOverlapTAI                         (int64_t* indices1, int len1, int64_t* indices2, int len2, int64_t* cmp, int len12){
  for( int i = 0; i < len1; ++i ) {
    cmp[i] = scidbOverlapTAI(indices1[i],indices2[i]) ? 1 : 0;
  }
}
void _scidbOverlap                            (int64_t* indices1, int len1, int64_t* indices2, int len2, int64_t* cmp, int len12){
  for( int i = 0; i < len1; ++i ) {
    cmp[i] = scidbOverlap(indices1[i],indices2[i]) ? 1 : 0;
  }
}
void _scidbContainsInstant                    (int64_t* indices1, int len1, int64_t* indices2, int len2, int64_t* cmp, int len12){
  for( int i = 0; i < len1; ++i ) {
    cmp[i] = scidbContainsInstant(indices1[i],indices2[i]) ? 1 : 0;
  }
}
void _to_JulianTAI   (int64_t* indices, int len, double* d1, int nd1, double* d2, int nd2) {
  for( int j=0; j < len; ++j ) {
    TemporalIndex tIndex(indices[j]);
    tIndex.toJulianTAI(d1[j],d2[j]);
  }
}

void _from_JulianTAI (double* d1, int nd1, double* d2, int nd2, int64_t* out_array, int out_length, int f_res, int r_res) {
  TemporalIndex tIndex;
  for( int j=0; j < nd1; ++j ) {
    // cout << "tIndex " << j << " . " << flush;
    TemporalIndex tIndexResult = tIndex.fromJulianTAI( d1[j], d2[j], f_res, r_res);
    // cout << " result " << flush;
    out_array[j] = tIndexResult.scidbTemporalIndex();
    // cout << out_array[j] << flush << endl;
    // cout << endl << flush;
  }
}

void _from_JulianUTC  (double* d1, int nd1, double* d2, int nd2, int64_t* out_array, int out_length, int f_res, int r_res) {
  for( int j=0; j < nd1; ++j ) {
    TemporalIndex tIndex;
    TemporalIndex tIndexResult = tIndex.fromJulianUTC( d1[j], d2[j], f_res, r_res );
    out_array[j] = tIndexResult.scidbTemporalIndex();
  }
}
void _to_JulianUTC   (int64_t* indices, int len, double* d1, int nd1, double* d2, int nd2) {
  for( int j=0; j < len; ++j ) {
    TemporalIndex tIndex(indices[j]);
    tIndex.toJulianUTC(d1[j],d2[j]);
  }
}


////////////////////////////////////////////////////////////////////////////////
//

void _set_temporal_resolutions_from_sorted_inplace (int64_t* indices_inplace, int len, bool include_bounds) {
  set_temporal_resolutions_from_sorted_inplace(indices_inplace,len,include_bounds);
}

void _set_reverse_resolution(int64_t* indices, int len,
                             int64_t* reverse_resolution, int lenr,
                             int64_t* out_array, int out_length
                             ) {
  for( int i = 0; i < len; ++i ) {
    out_array[i] = set_reverse_resolution(indices[i], reverse_resolution[i]);
  }
}
void _set_forward_resolution(int64_t* indices, int len,
                             int64_t* forward_resolution, int lenf,
                             int64_t* out_array, int out_length
                             ) {
  for( int i = 0; i < len; ++i ) {
    out_array[i] = set_forward_resolution(indices[i], forward_resolution[i]);
  }
}

void _forward_resolution(int64_t* indices, int len,
                         int64_t* out_array, int out_length
                         ) {
  for( int i = 0; i < len; ++i ) {
    out_array[i] = forward_resolution(indices[i]);
  }
}

void _reverse_resolution(int64_t* indices, int len,
                         int64_t* out_array, int out_length
                         ) {
  for( int i = 0; i < len; ++i ) {
    out_array[i] = reverse_resolution(indices[i]);
  }
}

void _coarsen(int64_t* indices, int len,
                 int64_t* reverse_increment, int lenr,
                 int64_t* forward_increment, int lenf,
                 int64_t* out_array, int out_length
                 ) {
  for( int i = 0; i < len; ++i ) {
    out_array[i] = coarsen(indices[i],reverse_increment[i],forward_increment[i]);
  }
}
  


////////////////////////////////////////////////////////////////////////////////
//
StareResult::~StareResult() {}
int  StareResult::get_size() {
  switch( sCase ) {
  case ArrayIndexSpatialValues : return get_size_as_values();
  case SpatialIntervals        : return get_size_as_intervals();
  }
  return -1; // Maybe throw something instead.
}
void StareResult::set_values_multi_resolution(bool multi_resolution) {
  values_multi_resolution = multi_resolution;  
}
int  StareResult::get_size_as_values() {
  if( sCase == SpatialIntervals ) {
    convert();
  }
  return sisvs.size();
}
int  StareResult::get_size_as_intervals() {
  if( sCase == ArrayIndexSpatialValues ) {
    convert();
  }
  return sis.size();
}
void StareResult::copy             (int64_t* indices, int len) {
  switch( sCase ) {
  case ArrayIndexSpatialValues :
    copy_as_values(indices,len);
    ; break;
  case SpatialIntervals :
    copy_as_intervals(indices,len);
    ; break;
  }
}
void StareResult::copy_as_values   (int64_t* indices, int len) {
  switch( sCase ) {
  case SpatialIntervals :
    convert();
    ; break;
  }
  for(int i = 0; i < min(len,(int)sisvs.size()); ++i) {
    indices[i] = sisvs[i];
  }
}
void StareResult::copy_as_intervals(int64_t* indices, int len) {
  switch( sCase ) {
  case ArrayIndexSpatialValues :
    convert();
    ; break;
  }
  for(int i = 0; i < min(len,(int)sis.size()); ++i) {
    indices[i] = sis[i];
  }
}
void StareResult::convert() {
  if( converted ) {
    return;
  }
  switch( sCase ) {
  case ArrayIndexSpatialValues :
    {
      SpatialRange r(sisvs);
      sis = r.toSpatialIntervals();
    }
    break;
  case SpatialIntervals :
    sisvs = expandIntervalsMultiRes(sis,-1,values_multi_resolution);
    break;
  }
  converted = true;
}
////////////////////////////////////////////////////////////////////////////////



////////////////////////////////////////////////////////////////////////////////
//

srange::srange() {}

srange::srange(int64_t* indices, int len) {
  STARE_ArrayIndexSpatialValues sis(indices, indices+len);
  range.addSpatialIntervals(sis);
}

srange::~srange() {}

void srange::add_intervals(int64_t* indices, int len) {
  STARE_SpatialIntervals sis(indices, indices+len);
  range.addSpatialIntervals(sis);
}

// bool srange::contains(int64_t siv) {
bool srange::contains(long long siv) {
  return range.contains(siv);
}

void srange::acontains(int64_t* indices1, int len1, int64_t* range_indices, int len_ri, int fill_value ) {
  for( int i=0; i<min(len1,len_ri); ++i ) {
    if( range.contains(indices1[i]) ) {
      range_indices[i] = indices1[i];
    } else {
      range_indices[i] = fill_value;
    }
  }
}
void srange::extract_intervals() {
  sis = range.toSpatialIntervals();
  intervals_extracted = true;
}
void srange::set_values_multi_resolution(bool multi_resolution) {
  values_multi_resolution = multi_resolution;
}
void srange::extract_values() {
  if( !intervals_extracted ) {
    extract_intervals();
  }
  sivs = expandIntervalsMultiRes(sis,-1,values_multi_resolution);
  values_extracted = true;
}

int srange::get_size_as_intervals() {
  if( !intervals_extracted ) {
    extract_intervals();
  }
  return sis.size();
}
void srange::copy_intervals(int64_t* indices, int len) {
  int n_sis = get_size_as_intervals();
  for( int i=0; i<min(len,(int)n_sis); ++i ) {
    indices[i] = sis[i];
  }
}
int srange::get_size_as_values() {
  if( !values_extracted ) {
    extract_values();
  }
  return sivs.size();
}
void srange::copy_values(int64_t* indices, int len) {
  int n_sivs = get_size_as_values();
  for(  int i=0; i < min(len,n_sivs); ++i ) {
    indices[i] = sivs[i];
  }
}
void srange::reset_extraction() {
  intervals_extracted = false;
  values_extracted = false;
  sis.clear();
  sivs.clear();
}
void srange::reset() {
  reset_extraction();
  range.reset();
}
void srange::purge() {
  reset_extraction();
  range.purge();
}

