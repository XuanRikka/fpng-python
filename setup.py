from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
import platform
import numpy


class BuildExt(build_ext):
    def build_extensions(self):
        compiler_type = self.compiler.compiler_type

        if compiler_type == 'msvc':
            extra_args = []
            if platform.machine() in {"AMD64", "x86_64"}:
                extra_args += ["/arch:AVX", "/arch:AVX2"]
        else:
            extra_args = ['-fno-strict-aliasing']
            if platform.machine() in {"AMD64", "x86_64"}:
                extra_args += ["-msse4.1", "-mpclmul"]

        for ext in self.extensions:
            ext.extra_compile_args = extra_args

        super().build_extensions()


ext_modules = [
    Extension(
        "pyfpng",
        sources=["src/fpng-python.cpp", "fpng/src/fpng.cpp"],
        include_dirs=["fpng/src/", numpy.get_include()],
    )
]

setup(
    name="pyfpng",
    version="0.1.0",
    ext_modules=ext_modules,
    cmdclass={'build_ext': BuildExt},
)