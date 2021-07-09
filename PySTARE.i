
%module pystare

%{
  #define SWIG_FILE_WITH_INIT  /* To import_array() below */
  #include "PySTARE.h"
  #include <vector>
  #include <string>
%}

%include "numpy.i"

%include "std_vector.i"
%include "std_string.i"

namespace std {
%template(VectorString) vector< string >;    
};

/*
%template(StringVector) std::vector< std::string >;
*/

/* %include "stl.i" */

/*
%template(StringVector) vector< string >;
%template(StringVector) std::vector< std::string >;
namespace std {
%template(StringVector) std::vector<std::string>;
%template(ConstCharVector) std::vector<const char*>;
}
*/

%init %{
    import_array();
%}

/* maps ONE double input vector to ONE int64_t output vector of the same length */
/* We use this to create a STARE array of the same size as a longitude array. 
/* The latitude array is passed separately. We have to do it separately since we can only map ONE input at a time */
/* Consequently, we are not verifying that lat and lon are the same length within the typemap */
%typemap(in, numinputs=1)
  (double* in_array, int length, int64_t* out_array)
   (PyObject* out=NULL)
{
  int is_new_object=0;
  npy_intp size[1] = { -1};
  PyArrayObject* array = obj_to_array_contiguous_allow_conversion($input, NPY_DOUBLE, &is_new_object);
  if (!array || !require_dimensions(array, 1)) SWIG_fail;
  size[0] = PyArray_DIM(array, 0);    
  out = PyArray_SimpleNew(1, size, NPY_INT64);
  if (!out) SWIG_fail;  
  $1 = (double*) array_data(array);
  $2 = (int) array_size(array,0);    
  $3 = (int64_t*) array_data((PyArrayObject*)out);
}

%typemap(in, numinputs=1)
  (double* in_array, int length, int64_t* out_array)
   (PyObject* out=NULL)
{
  int is_new_object=0;
  npy_intp size[1] = { -1};
  PyArrayObject* array = obj_to_array_contiguous_allow_conversion($input, NPY_DOUBLE, &is_new_object);
  if (!array || !require_dimensions(array, 1)) SWIG_fail;
  size[0] = PyArray_DIM(array, 0);    
  out = PyArray_SimpleNew(1, size, NPY_INT64);
  if (!out) SWIG_fail;  
  $1 = (double*) array_data(array);
  $2 = (int) array_size(array,0);    
  $3 = (int64_t*) array_data((PyArrayObject*)out);
}

/* maps ONE int64_t input vector to ONE int output vector of the same length */
/* We use this to create a level/resolution array of the same size as a STARE array. */
%typemap(in, numinputs=1)
  (int64_t* in_array, int length, int* out_array)
   (PyObject* out=NULL)
{
  int is_new_object=0;
  npy_intp size[1] = { -1};
  PyArrayObject* array = obj_to_array_contiguous_allow_conversion($input, NPY_INT64, &is_new_object);
  if (!array || !require_dimensions(array, 1)) SWIG_fail;
  size[0] = PyArray_DIM(array, 0);    
  out = PyArray_SimpleNew(1, size, NPY_INT);
  if (!out) SWIG_fail;  
  $1 = (int64_t*) array_data(array);
  $2 = (int) array_size(array,0);    
  $3 = (int*) array_data((PyArrayObject*)out);
}

/* maps ONE int64_t input vector to ONE int64_t output vector of the same length */
/* We use this to create a STARE array ... to_compressed_range */
%typemap(in, numinputs=1)
  (int64_t* in_array, int length, int64_t* out_array)
   (PyObject* out=NULL)
{
  int is_new_object=0;
  npy_intp size[1] = { -1};
  PyArrayObject* array = obj_to_array_contiguous_allow_conversion($input, NPY_INT64, &is_new_object);
  if (!array || !require_dimensions(array, 1)) SWIG_fail;
  size[0] = PyArray_DIM(array, 0);    
  out = PyArray_SimpleNew(1, size, NPY_INT64);
  if (!out) SWIG_fail;  
  $1 = (int64_t*) array_data(array);
  $2 = (int) array_size(array,0);    
  $3 = (int64_t*) array_data((PyArrayObject*)out);
}

/* maps ONE int64_t input vector to ONE int64_t output vector */
/* We use this to create a STARE array ... to_hull_range */
%typemap(in, numinputs=1)
  (int64_t* in_array, int length, int resolution, int64_t* out_array, int len_out, int* result_size)
   (PyObject* out=NULL)
{
  int is_new_object=0;
  npy_intp size[1] = { -1};
  
  PyArrayObject* array = obj_to_array_contiguous_allow_conversion($input, NPY_INT64, &is_new_object);
  if (!array || !require_dimensions(array, 1)) SWIG_fail;
  size[0] = PyArray_DIM(array, 0);
  
  out = PyArray_SimpleNew(1, size, NPY_INT64);
  if (!out) SWIG_fail;  
  $1 = (int64_t*) array_data(array);
  $2 = (int) array_size(array,0);    
  $3 = (int) array_size(array,0);    
  $4 = (int64_t*) array_data((PyArrayObject*)out);
  $5 = (int*) array_data((PyArrayObject*)(PyArray_SimpleNew(1,1,NPY_INT)));
}

/* maps ONE int64_t input vector to ONE double output vector of the same length */
/* We use this to create an area array of the same size as a STARE array. */
%typemap(in, numinputs=1)
  (int64_t* in_array, int length, double* out_array)
   (PyObject* out=NULL)
{
  int is_new_object=0;
  npy_intp size[1] = { -1};
  PyArrayObject* array = obj_to_array_contiguous_allow_conversion($input, NPY_INT64, &is_new_object);
  if (!array || !require_dimensions(array, 1)) SWIG_fail;
  size[0] = PyArray_DIM(array, 0);    
  out = PyArray_SimpleNew(1, size, NPY_DOUBLE);
  if (!out) SWIG_fail;  
  $1 = (int64_t*) array_data(array);
  $2 = (int) array_size(array,0);    
  $3 = (double*) array_data((PyArrayObject*)out);
}

/* maps ONE int64_t input vector to TWO double output vectors of the same length */
/* We use this to convert STARE index to lat+lon */
%typemap(in, numinputs=1)
  (int64_t* in_array, int length, double* out_array1, double* out_array2)
  (PyObject* out1=NULL, PyObject* out2=NULL)
{
  int is_new_object=0;
  npy_intp size[1] = { -1};
  PyArrayObject* array = obj_to_array_contiguous_allow_conversion($input, NPY_INT64, &is_new_object);
  if (!array || !require_dimensions(array, 1)) SWIG_fail;
 
  size[0] = PyArray_DIM(array, 0);  
   
  out1 = PyArray_SimpleNew(1, size, NPY_DOUBLE);
  if (!out1) SWIG_fail;
  out2 = PyArray_SimpleNew(1, size, NPY_DOUBLE);
  if (!out2) SWIG_fail;
   
  $1 = (int64_t*) array_data(array);
  $2 = (int) array_size(array,0);  
  $3 = (double*) array_data((PyArrayObject*)out1);
  $4 = (double*) array_data((PyArrayObject*)out2);
}

/* maps ONE int64_t input vector to TWO double output vectors of 4 times the length */
/* We use this to convert STARE index to lat+lon */
%typemap(in, numinputs=1)
  (int64_t* in_array, int length, double* out_array1, int dmy1, double* out_array2, int dmy2)
  (PyObject* out1=NULL, PyObject* out2=NULL)
{
  int is_new_object=0;
  npy_intp size[1] = { -1};
  PyArrayObject* array = obj_to_array_contiguous_allow_conversion($input, NPY_INT64, &is_new_object);
  if (!array || !require_dimensions(array, 1)) SWIG_fail;
 
  size[0] = 4*PyArray_DIM(array, 0);  
   
  out1 = PyArray_SimpleNew(1, size, NPY_DOUBLE);
  if (!out1) SWIG_fail;
  out2 = PyArray_SimpleNew(1, size, NPY_DOUBLE);
  if (!out2) SWIG_fail;
   
  $1 = (int64_t*) array_data(array);
  $2 = (int) array_size(array,0);  
  $3 = (double*) array_data((PyArrayObject*)out1);
  $4 = (int) array_size(array,0);
  $5 = (double*) array_data((PyArrayObject*)out2);
  $6 = (int) array_size(array,0);
}

/* maps ONE int64_t input vector to TWO int64_t output vectors of the same length */
/* We use this to convert STARE intervals to start/terminator arrays to aid comparison */
%typemap(in, numinputs=1)
  (int64_t* in_array, int length, int64_t* out_array1, int64_t* out_array2)
  (PyObject* out1=NULL, PyObject* out2=NULL)
{
  int is_new_object=0;
  npy_intp size[1] = { -1};
  PyArrayObject* array = obj_to_array_contiguous_allow_conversion($input, NPY_INT64, &is_new_object);
  if (!array || !require_dimensions(array, 1)) SWIG_fail;
 
  size[0] = PyArray_DIM(array, 0);  
   
  out1 = PyArray_SimpleNew(1, size, NPY_INT64);
  if (!out1) SWIG_fail;
  out2 = PyArray_SimpleNew(1, size, NPY_INT64);
  if (!out2) SWIG_fail;
   
  $1 = (int64_t*) array_data(array);
  $2 = (int) array_size(array,0);  
  $3 = (int64_t*) array_data((PyArrayObject*)out1);
  $4 = (int64_t*) array_data((PyArrayObject*)out2);
}


/* maps ONE int64_t input array to TWO double and ONE 1D int output array with the same length */
/* We use this to convert STARE index to lat+lon+level */
%typemap(in, numinputs=1)
  (int64_t* in_array, int length, double* out_array1, double* out_array2, int* out_array3)
  (PyObject* out1=NULL, PyObject* out2=NULL, PyObject* out3=NULL)
{
  int is_new_object=0;
  npy_intp size[1] = { -1};
  PyArrayObject* array = obj_to_array_contiguous_allow_conversion($input, NPY_INT64, &is_new_object);
  if (!array || !require_dimensions(array, 1)) SWIG_fail;
 
  size[0] = PyArray_DIM(array, 0);  
   
  out1 = PyArray_SimpleNew(1, size, NPY_DOUBLE);
  if (!out1) SWIG_fail;
  out2 = PyArray_SimpleNew(1, size, NPY_DOUBLE);
  if (!out2) SWIG_fail;
  out3 = PyArray_SimpleNew(1, size, NPY_INT);
  if (!out3) SWIG_fail;
   
  $1 = (int64_t*) array_data(array);
  $2 = (int) array_size(array,0);  
  $3 = (double*) array_data((PyArrayObject*)out1);
  $4 = (double*) array_data((PyArrayObject*)out2);
  $5 = (int*) array_data((PyArrayObject*)out3);
}

/*
 * maps ONE int64_t input array to THREE 1D int output array with the same length 
 * We use this to convert STARE index to triangle vertices & centroid
 */
%typemap(in, numinputs=1)
  (int64_t* in_array, int length, int64_t* out_array1, int64_t* out_array2, int64_t* out_array3, int64_t* out_array4)
  (PyObject* out1=NULL, PyObject* out2=NULL, PyObject* out3=NULL, PyObject* out4=NULL)
{
  int is_new_object=0;
  npy_intp size[1] = { -1};
  PyArrayObject* array = obj_to_array_contiguous_allow_conversion($input, NPY_INT64, &is_new_object);
  if (!array || !require_dimensions(array, 1)) SWIG_fail;
 
  size[0] = PyArray_DIM(array, 0); 
   
  out1 = PyArray_SimpleNew(1, size, NPY_INT64);
  if (!out1) SWIG_fail;
  out2 = PyArray_SimpleNew(1, size, NPY_INT64);
  if (!out2) SWIG_fail;
  out3 = PyArray_SimpleNew(1, size, NPY_INT64);
  if (!out3) SWIG_fail;
  out4 = PyArray_SimpleNew(1, size, NPY_INT64);
  if (!out4) SWIG_fail;
   
  $1 = (int64_t*) array_data(array);
  $2 = (int) array_size(array,0);  
  $3 = (int64_t*) array_data((PyArrayObject*)out1);
  $4 = (int64_t*) array_data((PyArrayObject*)out2);
  $5 = (int64_t*) array_data((PyArrayObject*)out3);
  $6 = (int64_t*) array_data((PyArrayObject*)out4);
}

/*
 * char** 
 * From http://www.swig.org/Doc1.3/Python.html#Python_nn59
 */
/* %module argv */

// This tells SWIG to treat char ** as a special case

%typemap(in) char ** {
  /* Check if is a list  */
  if (PyList_Check($input)) {
    int size = PyList_Size($input);
    int i = 0;
    $1 = (char **) malloc((size+1) * sizeof(char*));
    for (i = 0; i < size; i++) {
      PyObject *o = PyList_GetItem($input,i);
      if (PyUnicode_Check(o)) {
	// printf("100\n");
	Py_ssize_t size_ = 0;
	// printf("110\n");
	const char *pc = PyUnicode_AsUTF8AndSize(o,&size_);
	// $1[i] = PyUnicode_AsUTF8AndSize(o,&size_);
	// printf("120\n");
	string s(pc,size_);
	// printf("130\n");
	// It would be great to be able to just pass in the const char*.
	$1[i] = (char*) malloc((size_+1) * sizeof(char)); // Hello memory leak...
	// printf("135\n");
	size_t len = s.copy($1[i],size_);
	// printf("140\n");
      } else {
        PyErr_SetString(PyExc_TypeError,"list must contain strings");
        free($1);
        return NULL;
      }
    }
    $1[i] = 0;
  } else if ($input == Py_None) {
    $1 =  NULL;
  } else {
    PyErr_SetString(PyExc_TypeError,"not a list");
    return NULL;
  }
}

%typemap(freearg) char** {
    printf("freearg char**\n");
  free((char *) $1);
}

%typemap(out) char** {
    printf("c**-000\n");
  int len;
  int i;
  len = 0;
  while ($1[len]) len++;
    printf("c**-100 len = %d\n",len);
  $result = PyList_New(len);
    printf("c**-200\n");
  for (i = 0; i < len; i++) {
    printf("out %d -> %s\n",i,$1[i]);
    PyList_SetItem($result, i, PyString_FromString($1[i]));
    printf("c**-399\n");
  }
    printf("c**-999\n");
}


// Now a test function
%inline %{
  int print_args(char **argv) {
    int i = 0;
    while (argv[i]) {
         printf("argv[%d] = %s\n", i,argv[i]);
	 free(argv[i]); // Good bye, memory leak!
         i++;
    }
    return i;
}
%}



/****************/
/* OUT typemaps */
/****************/

%typemap(argout)
  (double* in_array, int length, int64_t* out_array)
{
  $result = (PyObject*)out$argnum;
}


%typemap(argout)
  (int64_t* in_array, int length, int* out_array)  
{
  $result = (PyObject*)out$argnum;
}

%typemap(argout)
  (int64_t* in_array, int length, int64_t* out_array)
{
  $result = (PyObject*)out$argnum;
}

%typemap(argout)
  (int64_t* in_array, int length, int64_t* out_array)
{
  $result = (PyObject*)out$argnum;
}

%typemap(argout)
  (int64_t* in_array, int length, double* out_array)
{
  $result = (PyObject*)out$argnum;
}

%typemap(argout)
    (int64_t* in_array, int length, double* out_array1, double* out_array2)
{
  $result = PyTuple_New(2);
  PyTuple_SetItem($result, 0, (PyObject*)out1$argnum);
  PyTuple_SetItem($result, 1, (PyObject*)out2$argnum);
}
%typemap(argout)
    (int64_t* in_array, int length, double* out_array1, int dmy1, double* out_array2, int dmy2)
{
  $result = PyTuple_New(2);
  PyTuple_SetItem($result, 0, (PyObject*)out1$argnum);
  PyTuple_SetItem($result, 1, (PyObject*)out2$argnum);
}
%typemap(argout)
    (int64_t* in_array, int length, int64_t* out_array1, int64_t* out_array2)
{
  $result = PyTuple_New(2);
  PyTuple_SetItem($result, 0, (PyObject*)out1$argnum);
  PyTuple_SetItem($result, 1, (PyObject*)out2$argnum);
}

%typemap(argout)
    (int64_t* in_array, int length, double* out_array1, double* out_array2, int* out_array3)
{
  $result = PyTuple_New(3);
  PyTuple_SetItem($result, 0, (PyObject*)out1$argnum);
  PyTuple_SetItem($result, 1, (PyObject*)out2$argnum);
  PyTuple_SetItem($result, 2, (PyObject*)out3$argnum);
}

%typemap(argout)
    (int64_t* in_array, int length, int64_t* out_array1, int64_t* out_array2, int64_t* out_array3, int64_t* out_array4)
{
  $result = PyTuple_New(4);
  PyTuple_SetItem($result, 0, (PyObject*)out1$argnum);
  PyTuple_SetItem($result, 1, (PyObject*)out2$argnum);
  PyTuple_SetItem($result, 2, (PyObject*)out3$argnum);
  PyTuple_SetItem($result, 3, (PyObject*)out4$argnum);
}

/* expand_intervals
%typemap(argout)
    (int64_t* in_array, int length, int resolution, int64_t* out_array1, int dmy1, int64_t* out_array2, int dmy2)
{
  $result = PyTuple_New(2);
  PyTuple_SetItem($result, 0, (PyObject*)out1$argnum);
  PyTuple_SetItem($result, 1, (PyObject*)out2$argnum);
}
 */

%typemap(argout) 
(int64_t* in_array1, int length1, int64_t* in_array2, int length2, int64_t* out_array, int out_length)
{
  $result = (PyObject*)out$argnum;
}
  
/*
 %typemap(argout) 
 (double* in_array1, int length1, double* in_array2, int length2, int resolution, int64_t* out_array1, int out_length1, int64_t* out_array2, int out_length2)
 {
   $result = (PyObject*)out$argnum;
 }
*/

/* Applying the typemaps */



%apply (double * INPLACE_ARRAY2, int DIM1, int DIM2) {
    (double* lat, int lalen1, int lalen2),
    (double* lon, int lolen1, int lolen2)
}

%apply (int64_t * INPLACE_ARRAY2, int DIM1, int DIM2) {
    (int64_t* indices, int len1, int len2)
}

%apply (double * IN_ARRAY1, int DIM1) {
    (double* lat, int len_lat),
    (double* lon, int len_lon)
}

%apply (int64_t * IN_ARRAY1, int DIM1) {
    (int64_t* datetime, int len),
    (int64_t* indices1, int len1),
    (int64_t* indices2, int len2),
    (int64_t* indices, int len)
}

%apply (int64_t * INPLACE_ARRAY1, int DIM1) {
    (int64_t* intersection, int leni),    
    (int64_t* range_indices, int len_ri),
    (int64_t* result_size, int len_rs),
    (int64_t* out_array, int out_length),
    (int64_t* cmp, int len12)
}


%apply (double * INPLACE_ARRAY1, int DIM1) {
	(double* triangle_info_lats, int dmy1),
	(double* triangle_info_lons, int dmy2)
}

# %apply (int64_t * ARGOUT_ARRAY1, int DIM1 ) {
# 	(int64_t* out_array, int out_length)
#   (int64_t* range_indices, int len_ri)
# }

%apply (double* in_array, int length, int64_t* out_array) {
    (double* lon, int len_lon, int64_t* indices)
}

%apply (int64_t* in_array, int length, int* out_array) {
  (int64_t* indices, int len,  int* levels), 
  (int64_t* indices2, int len2,  int* intersects)
}

%apply (int64_t* in_array, int length, int64_t* out_array) {
  (int64_t* datetime, int len,  int64_t* indices_out),
  (int64_t* indices, int len,  int64_t* datetime_out)
}

%apply (int64_t* in_array, int length, double* out_array) {
    (int64_t* indices, int len,  double* areas)
}

%apply (int64_t* in_array, int length, double* out_array1, double* out_array2) {
    (int64_t* indices, int len, double* lat, double* lon)
}

%apply (int64_t* in_array, int length, double* out_array1, double* out_array2, int* out_array3) {
    (int64_t* indices, int len, double* lat, double* lon, int* levels)
}

%apply (int64_t* in_array, int length, int64_t* out_array1, int64_t* out_array2, int64_t* out_array3, int64_t* out_array4) {
    (int64_t* indices, int len, int64_t* vertices0, int64_t* vertices1, int64_t* vertices2, int64_t* centroid)
}

%apply (int64_t* in_array, int length, int64_t* out_array1, int64_t* out_array2) {
	(int64_t* intervals, int len, int64_t* indices_starts, int64_t* indices_terminators )
}

%apply (int64_t* in_array, int length, double* out_array1, int dmy1, double* out_array2, int dmy2) {
   (int64_t* indices, int len, double* triangle_info_lats, int dmy1, double* triangle_info_lons, int dmy2)
}

/*
%pythonprepend from_utc(int64_t*, int, int64_t*, int) %{
    import numpy
    datetime = datetime.astype(numpy.int64)
%}
*/

%pythoncode %{
import numpy
from pkg_resources import get_distribution
import re
  
__version__ = get_distribution('pystare').version

class PyStareError(Exception):
    pass

class PyStareArrayBoundsExceeded(Exception):
    pass

def to_neighbors(indices):
    result = _to_neighbors(indices)
    range_indices = numpy.full([result.get_size_as_values()],-1,dtype=numpy.int64)
    result.copy_as_values(range_indices)
    return range_indices

def to_compressed_range(indices):
    out_length = len(indices)
    range_indices = numpy.full([out_length],-1,dtype=numpy.int64)
    len_ri = 0
    _to_compressed_range(indices,range_indices)
    endarg = 0
    while (endarg < out_length) and (range_indices[endarg] > 0):
      endarg = endarg + 1
    # endarg = numpy.argmax(range_indices < 0)
    range_indices = range_indices[:endarg]
    return range_indices
    
def expand_intervals(intervals, resolution, multi_resolution=False):
    result = _expand_intervals(intervals,resolution,multi_resolution)
    expanded_intervals = numpy.zeros([result.get_size_as_intervals()],dtype=numpy.int64)
    result.copy_as_values(expanded_intervals)
    return expanded_intervals

#    result      = numpy.full([result_size_limit],-1,dtype=numpy.int64)
#    result_size = numpy.full([1],-1,dtype=numpy.int64)
#    _expand_intervals(intervals,resolution,result,result_size)
#    result = result[:result_size[0]]
#    return result

def adapt_resolution_to_proximity(indices):
    result = numpy.copy(indices)
    _adapt_resolution_to_proximity(indices,result)
    return result
    
def to_hull_range(indices, resolution):
    result = _to_hull_range(indices, resolution)
    range_indices = numpy.full([result.get_size_as_intervals()], -1, dtype=numpy.int64)
    result.copy_as_intervals(range_indices)
    return range_indices
    
def from_latlon2D(lat, lon, resolution=27, adapt_resolution=False):
    if adapt_resolution:
        resolution = 27
    indices = numpy.full(lon.shape, -1, dtype=numpy.int64)
    _from_latlon2D(lat, lon, indices, 27, adapt_resolution)
    return indices    

def to_hull_range_from_latlon(lat, lon, resolution):
    result = _to_hull_range_from_latlon(lat, lon, resolution)
    range_indices = numpy.full([result.get_size_as_intervals()], -1, dtype=numpy.int64)
    result.copy_as_intervals(range_indices)
    return range_indices

def to_nonconvex_hull_range_from_latlon(lat, lon, resolution):
    result        = _to_nonconvex_hull_range_from_latlon(lat,lon,resolution);
    out_length    = result.get_size_as_intervals()
    range_indices = numpy.zeros([out_length],dtype=numpy.int64)
    result.copy_as_intervals(range_indices)
    return range_indices

def to_circular_cover(lat, lon, radius, resolution):
    result = _to_circular_cover(lat, lon, radius, resolution)
    out_length = result.get_size_as_intervals()
    range_indices = numpy.zeros([out_length],dtype=numpy.int64)
    result.copy_as_intervals(range_indices);
    return range_indices

def circular_cover_from(index,radius,resolution):
    latsv,lonsv,lat_center,lon_center = to_vertices_latlon([index])
    return to_circular_cover(lat_center[0],lon_center[0],radius,resolution)

def to_box_cover_from_latlon(lat, lon, resolution):
    "Construct numpy array of intervals covering a 4-corner box specified using lat and lon."
    result = _to_box_cover_from_latlon(lat, lon, resolution)
    range_indices = numpy.zeros([result.get_size_as_intervals()],dtype=numpy.int64)
    result.copy_as_intervals(range_indices)
    return range_indices
      
def to_vertices_latlon(indices):
	out_length = len(indices)
	lats = numpy.zeros([4*out_length],dtype=numpy.double)
	lons = numpy.zeros([4*out_length],dtype=numpy.double)
	# _to_vertices_latlon(indices,lats,lons,0)
	lats, lons = _to_vertices_latlon(indices)
	latsv = numpy.zeros([3*out_length],dtype=numpy.double)
	lonsv = numpy.zeros([3*out_length],dtype=numpy.double)
	lat_center = numpy.zeros([out_length],dtype=numpy.double)
	lon_center = numpy.zeros([out_length],dtype=numpy.double)
	
	k=0
	l=0
	for i in range(out_length):
		latsv[l]   = lats[ k   ]
		lonsv[l]   = lons[ k   ]
		
		latsv[l+1] = lats[ k+1 ]
		lonsv[l+1] = lons[ k+1 ]
				
		latsv[l+2] = lats[ k+2 ]
		lonsv[l+2] = lons[ k+2 ]
				
		lat_center [i]   = lats[ k+3 ]
		lon_center [i]   = lons[ k+3 ]
		k = k + 4
		l = l + 3
	return latsv,lonsv,lat_center,lon_center
    
def cmp_spatial(indices1, indices2):
    """
        calls cmp_spatial returning an element of {-1,0,1} depending on which, if either, element contains the other. Returns an array of x in {-1,0,1}, but cmp_spatial calculates all pairs (like an exterior product).
    """
    out_length = len(indices1)*len(indices2)
    cmp = numpy.zeros([out_length],dtype=numpy.int64)
    _cmp_spatial(indices1,indices2,cmp)
    return cmp
	    
def cmp_temporal(indices1, indices2):
	out_length = len(indices1)*len(indices2)
	cmp = numpy.zeros([out_length],dtype=numpy.int64)
	_cmp_temporal(indices1,indices2,cmp)
	return cmp


def from_tai_iso_strings(taiStrings):
    out_length = len(taiStrings)
    tIndices   = numpy.zeros([out_length],dtype=numpy.int64)
    p = re.compile('^([0-9]{4})-([0-2][0-9])-([0-3][0-9])T([0-2][0-9]):([0-5][0-9]):([0-5][0-9])(.([0-9]{3}))?(\s\(([0-9]+)\s([0-9]+)\)\s\(([0-9])\))?$')
    for k in range(out_length):
        s = p.match(taiStrings[k])
        if s is not None:
           if s.groups()[7] is None:
              taiStrings[k] = taiStrings[k] + '.000 (48 48) (1)'
           elif s.groups()[8] is None:
              taiStrings[k] = taiStrings[k] + ' (48 48) (1)'
        else:
           raise ValueError('from_tai_iso_strings: unknown input "'+taiStrings[k]+'"')
    _from_tai_iso_strings(taiStrings,tIndices)
    return tIndices

def to_tai_iso_strings(tIndices):
    taiStrings = _to_tai_iso_strings(tIndices)
    return taiStrings

def to_temporal_triple_ms(tIndexValue):
    ti_low = scidbLowerBoundMS(tIndexValue)
    ti_hi  = scidbUpperBoundMS(tIndexValue)
    return (ti_low,tIndexValue,ti_hi)

def lowerBoundTAI(tIndexValue):
    tret = tIndexValue.copy()
    _scidbLowerBoundTAI(tIndexValue,tret)
    return tret
    
def upperBoundTAI(tIndexValue):
    tret = tIndexValue.copy()
    _scidbUpperBoundTAI(tIndexValue,tret)
    return tret

def to_temporal_triple_tai(tIndexValue):
    print('type ti: ',type(tIndexValue),tIndexValue)
    ti_low = lowerBoundTAI(tIndexValue)
    ti_hi  = upperBoundTAI(tIndexValue)
    return (ti_low,tIndexValue,ti_hi)
    
def intersects(indices1, indices2, method=0):
    # method = {'skiplist': 0, 'binsearch': 1, 'nn': 2}[method]
    return _intersects(indices1, indices2, method).astype(numpy.bool)
	
def intersect(indices1, indices2, multiresolution=True):
    """
     constructs SpatialRange objects from its arguments and then returns the intersection of those. Returns an array of spatial index values.
    """
    out_length = 2*max(len(indices1), len(indices2))
    intersected = numpy.full([out_length], -1, dtype=numpy.int64)
    leni = 0
    if(multiresolution):
      _intersect_multiresolution(indices1, indices2, intersected)
    else:
      _intersect(indices1, indices2, intersected)
      print('isect:  ',intersected[0:20])

    # Argmax returns 0 if intersected is non-negative, and not len(intersected)+1
    # It's supposed to be the first index of the max val, but if all false...
    endarg = numpy.argmax(intersected < 0)
    if endarg == 0:
      if intersected[0] >= 0:
         endarg = len(intersected)
    print('endarg: ',endarg)
    intersected = intersected[:endarg]
    print('isect- ',intersected)
    return intersected

def shiftarg_lon(lon):
    "If lon is outside +/-180, then correct back."
    if(lon>180):
        return ((lon + 180.0) % 360.0)-180.0
    else:
        return lon

def shiftarg_lat(lat):
    "If lat is outside +/-90, then correct back."
    if(lat>90):
        return ((lat + 90.0) % 180.0)-90.0
    else:
        return lat
        
def spatial_resolution_from_km(km,return_int=True):
    if return_int:
        return 10-numpy.log2(km/10)
    else:
        return int(10-numpy.log2(km/10))

def spatial_scale_km(resolution):
    "A rough estimate for the length scale at level."
    return 10*(2.0**(10-resolution))
	  
def triangulate(lats,lons):
    "Help prepare data for matplotlib.tri.Triangulate."
    intmat=[]
    npts=int(len(lats)/3)
    k=0
    for i in range(npts):
        intmat.append([k,k+1,k+2])
        k=k+3
    for i in range(len(lons)):
        lons[i] = shiftarg_lon(lons[i])
    # print('triangulating1 done.')      
    return lons,lats,intmat 

def triangulate_indices(indices):
    """
    Prepare data for matplotlib.tri.Triangulate.
    
    Usage: 
     lons,lats,intmat = triangulate_indices(indices)
     triang = tri.Triangulation(lons,lats,intmat)
     plt.triplot(triang,'r-',transform=transform,lw=1,markersize=3)    
    """
    latv,lonv,lat_center,lon_center = to_vertices_latlon(indices)
    lons,lats,intmat = triangulate(latv,lonv)
    return lons,lats,intmat


spatial_resolution_mask =  31
spatial_location_mask   = ~31

# TODO Replace hardcoded below with the variables above.
	  
def spatial_increment_from_level(level):
    if level < 0 or level > 27:
        raise PyStareError()
    return 1 << (59-2*level)

def spatial_resolution(sid):
    return sid & 31 # levelMaskSciDB

def spatial_terminator_mask(level):
    return ((1 << (1+ 58-2*level))-1)

def spatial_terminator(sid):
    return sid | ((1 << (1+ 58-2*(sid & 31)))-1)

def spatial_coerce_resolution(sid,resolution):
    return (sid & ~31) | resolution

def spatial_clear_to_resolution(sid):
    resolution = sid & 31
    mask =  spatial_terminator_mask(spatial_resolution(sid))
    return (sid & ~mask) + resolution
	 
%}   
   
%include "PySTARE.h"
