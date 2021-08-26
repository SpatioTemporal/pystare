
%module core

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
  // printf("freearg char**\n");
  free((char *) $1);
}

%typemap(out) char** {
    // printf("c**-000\n");
  int len;
  int i;
  len = 0;
  while ($1[len]) len++;
    // printf("c**-100 len = %d\n",len);
  $result = PyList_New(len);
    // printf("c**-200\n");
  for (i = 0; i < len; i++) {
    // printf("out %d -> %s\n",i,$1[i]);
    PyList_SetItem($result, i, PyString_FromString($1[i]));
    // printf("c**-399\n");
  }
    // printf("c**-999\n");
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
    (int64_t* indices, int len),
    (int64_t* reverse_increment, int lenr),
    (int64_t* forward_increment, int lenf)
}

%apply (int64_t * INPLACE_ARRAY1, int DIM1) {
    (int64_t* intersection, int leni),    
    (int64_t* range_indices, int len_ri),
    (int64_t* result_size, int len_rs),
    (int64_t* out_array, int out_length),
    (int64_t* cmp, int len12),
    (int64_t* forward_resolution, int lenf),
    (int64_t* reverse_resolution, int lenr),
    (int64_t* indices_inplace, int len)
}

%apply (double * INPLACE_ARRAY1, int DIM1) {
  (double* triangle_info_lats, int dmy1),
  (double* triangle_info_lons, int dmy2),
  (double* d1, int nd1),
  (double* d2, int nd2)
}

# %apply (int64_t * ARGOUT_ARRAY1, int DIM1 ) {
# 	(int64_t* out_array, int out_length)
#   (int64_t* range_indices, int len_ri)
# }

%apply (double* in_array, int length, int64_t* out_array) {
  (double* lon, int len_lon, int64_t* indices),
  (double* milliseconds, int len, int64_t* out_array)
}

%apply (int64_t* in_array, int length, int* out_array) {
  (int64_t* indices, int len,  int* levels), 
  (int64_t* indices2, int len2,  int* intersects)
}

%apply (int64_t* in_array, int length, int64_t* out_array) {
  (int64_t* datetime, int len,  int64_t* indices_out),
  (int64_t* indices, int len,  int64_t* datetime_out),
  (int64_t* indices, int len,  int64_t* new_indices)
}

%apply (int64_t* in_array, int length, double* out_array) {
    (int64_t* indices, int len,  double* areas),
    (int64_t* resolutions, int len, double* millisecond)
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

%pythoncode %{%}
   
%include "PySTARE.h"
