cimport cython
cimport numpy as cnp
import numpy as np
from libcpp.vector cimport vector

@cython.overflowcheck(False)
@cython.boundscheck(False)
def transform(cnp.ndarray inp, cnp.ndarray out):
    assert(inp.dtype == np.float64)
    assert(out.dtype == np.float64)
    cdef int n = inp.shape[0]
    cdef int m = inp.shape[1]
    cdef int angle
    cdef vector[double] sin_a
    sin_a.resize(out.shape[0])
    cdef vector[double] cos_a
    cos_a.resize(out.shape[0])
    cdef int x
    cdef int output_r
    cdef int y
    cdef double radius
    cdef int on = out.shape[0]
    cdef int om = out.shape[1]

    cdef double[:] cinp = inp.reshape(n*m)
    cdef double[:] cout = out.reshape(on*om)

    cdef double max_radius = np.sqrt(n*n + m*m)

    for angle in range(out.shape[0]):
        sin_a[angle] = np.sin(2.*np.pi*(<double>angle/on))
        cos_a[angle] = np.cos(2.*np.pi*(<double>angle/on))


    for x in range(n):
        for y in range(m):
            if cinp[x* m + y] < 15:
                continue
            for angle in range(on):
                radius = sin_a[angle]*x + cos_a[angle]*y
                radius = (radius/(2. * max_radius)) + 0.5
                output_r = <int>(om*radius)
                if 0 <= output_r <= om - 1:
                    cout[angle*om + output_r] += cinp[x*m + y]
    return out
