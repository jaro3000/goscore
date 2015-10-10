import numpy

from distutils.core import setup, Extension
from Cython.Build import cythonize

extension=[
    Extension(
        "*",
        ['goscore/*.pyx'],
        language="c++",
        include_dirs = [numpy.get_include()],
        libraries = [],
        library_dirs = ["/usr/local/lib"]
    )
]


setup(
    name = "Goscore server",
    ext_modules = cythonize(extension),  # accepts a glob pattern
)
