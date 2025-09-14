from setuptools import setup, Extension
import pybind11

ext_modules = [
    Extension(
        "power_cpp",
        ["power.cpp"],
        include_dirs=[pybind11.get_include()],
        language="c++"
    )
]

setup(
    name="power_cpp",
    ext_modules=ext_modules,
)
