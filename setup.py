import argparse
from distutils.errors import CompileError
import os
import sys
from setuptools import setup, Extension, find_packages
from setuptools.command.build_ext import build_ext


# ---------------------------------------------------------------------------------------------------------
# BASE CONFIGURATION
# ---------------------------------------------------------------------------------------------------------

BASE_PACKAGE = "tspgrasp"

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

base_kwargs = dict(
    name = 'tspgrasp',
    package_dir={'': "src"},
    packages = find_packages(where='src'),
    version = '0.1.0',
    license='Apache License 2.0',
    description = 'GRASP for TSP',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author = 'Bruno Scalia C. F. Leite',
    author_email = 'bruscalia12@gmail.com',
    url = 'https://github.com/bruscalia/tsp-grasp',
    download_url = 'https://github.com/bruscalia/tsp-grasp',
    keywords = [
            'Traveling Salesman Problem',
            'TSP',
            'Greedy Randomized Adaptive Search Procedures',
            'Heuristics',
            'Metaheuristics',
            'Meta-heuristics',
            'Greedy Algorithms',
            'Local Search',
            'Variable Neighborhood Search',
            'Simulated Annealing',
        ],
    install_requires=["numpy>=1.19", "Cython"],
    extras_require={
        "dev": ["pytest"],  # for developers
        "plot": ["matplotlib"],  # for optional package features
    }
)

# ---------------------------------------------------------------------------------------------------------
# ARGPARSER
# ---------------------------------------------------------------------------------------------------------

parser = argparse.ArgumentParser()

parser.add_argument('--nopyx', dest='nopyx', action='store_true', help='Whether the pyx files shall be considered at all.')
parser.add_argument('--nocython', dest='nocython', action='store_true', help='Whether pyx files shall be cythonized.')
parser.add_argument('--nolibs', dest='nolibs', action='store_true', help='Whether the libraries should be compiled.')
parser.add_argument('--markcython', dest='markcython', action='store_true', help='Whether to mark the html cython files.')

params, _ = parser.parse_known_args()
sys.argv = [arg for arg in sys.argv if not arg.lstrip("-") in params]

# ---------------------------------------------------------------------------------------------------------
# ADD MARKED HTML FILES FOR CYTHON
# ---------------------------------------------------------------------------------------------------------

if params.markcython:
    import Cython.Compiler.Options
    Cython.Compiler.Options.annotate = True

# ---------------------------------------------------------------------------------------------------------
# CLASS TO BUILD EXTENSIONS
# ---------------------------------------------------------------------------------------------------------

# exception that is thrown when the build fails
class CompilingFailed(Exception):
    pass


# try to compile, if not possible throw exception
def construct_build_ext(build_ext):
    class WrappedBuildExt(build_ext):
        def run(self):
            try:
                build_ext.run(self)
            except BaseException as e:
                raise CompilingFailed(e)

        def build_extension(self, ext):
            try:
                build_ext.build_extension(self, ext)
            except BaseException as e:
                raise CompilingFailed(e)

    return WrappedBuildExt

# ---------------------------------------------------------------------------------------------------------
# HANDLING CYTHON FILES
# ---------------------------------------------------------------------------------------------------------

ROOT = os.path.dirname(os.path.realpath(__file__))
CY_PATH = os.path.join(ROOT, "src", "tspgrasp", "cython")
PYX_FILES = [os.path.join(CY_PATH, f) for f in os.listdir(CY_PATH) if f.endswith(".pyx")]

if params.nopyx:
    ext_modules = []

else:
    try:
        if params.nocython:
            ext_modules = [Extension(f"tspgrasp.{source[:-4]}", [source]) for source in PYX_FILES]
        else:
            try:
                from Cython.Build import cythonize
                ext_modules = cythonize(PYX_FILES)
            except ImportError:
                print('*' * 75)
                print("No Cython package found to convert .pyx files.")
                print("If no compilation occurs, .py files will be used instead, which provide the same results but with worse computational time.")
                print('*' * 75)
                ext_modules = []
    except:
        print('*' * 75)
        print("Problems compiling .pyx files.")
        print("If no compilation occurs, .py files will be used instead, which provide the same results but with worse computational time.")
        print('*' * 75)
        ext_modules = []

if not params.nolibs:

    if len(ext_modules) > 0:
        base_kwargs['ext_modules'] = ext_modules

        try:
            import numpy as np
            base_kwargs['include_dirs'] = [np.get_include()]

        except BaseException:
            raise CompileError(
                "NumPy libraries must be installed for compiled extensions! Speedups are not enabled."
            )

        base_kwargs['cmdclass'] = dict(build_ext=construct_build_ext(build_ext))

    else:
        print('*' * 75)
        print("External cython modules found.")
        print("To verify compilation success run:")
        print("from tspgrasp import cythonized")
        print("This variable will be True to mark compilation success;")
        print("If no compilation occurs, .py files will be used instead, which provide the same results but with worse computational time.")
        print('*' * 75)

# ---------------------------------------------------------------------------------------------------------
# RUN SETUP
# ---------------------------------------------------------------------------------------------------------

compiled_kwargs = base_kwargs.copy()
compiled_kwargs["ext_modules"] = ext_modules

try:
    setup(**compiled_kwargs)
    print('*' * 75)
    print("Installation successful at the first attempt.")
    print("To verify compilation success run:")
    print("from tspgrasp import cythonized")
    print('*' * 75)
except:
    print('*' * 75)
    print("Running setup with cython compilation failed.")
    print("Attempt to a pure Python setup.")
    print("If no compilation occurs, .py files will be used instead, which provide the same results but with worse computational time.")
    print('*' * 75)
    setup(**base_kwargs)
