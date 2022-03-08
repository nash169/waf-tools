#!/usr/bin/env python
# encoding: utf-8
#
#    This file is part of waf-tools.
#
#    Copyright (c) 2020, 2021, 2022 Bernardo Fichera <bernardo.fichera@gmail.com>
#
#    Permission is hereby granted, free of charge, to any person obtaining a copy
#    of this software and associated documentation files (the "Software"), to deal
#    in the Software without restriction, including without limitation the rights
#    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#    copies of the Software, and to permit persons to whom the Software is
#    furnished to do so, subject to the following conditions:
#
#    The above copyright notice and this permission notice shall be included in all
#    copies or substantial portions of the Software.
#
#    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#    SOFTWARE.

from waflib.Configure import conf
from utils import check_include, check_lib

# For clarification about LAPACK/BLAS implementations check:
# https://wiki.debian.org/DebianScience/LinearAlgebraLibraries


def options(opt):
    opt.add_option(
        "--mfem-path", type="string", help="path to libmfem", dest="mfem_path"
    )

    opt.add_option(
        "--mfem-options", type="string", help="options mfem", dest="mfem_options"
    )

    # Load options
    opt.load("mpi hypre metis openmp arpack petsc slepc eigen spectra lapack blas suitesparse superlu",
             tooldir="waf_tools")


@conf
def check_mfem(ctx):
    # Set the search path
    if ctx.options.mfem_path is None:
        path_check = ["/usr/local", "/usr", "/opt"]
    else:
        path_check = [ctx.options.mfem_path]

    # Components
    options = [
        "mpi",
        "hypre",
        "metis",
        "openmp",
        "arpack",
        "petsc",
        "slepc",
        "eigen",
        "spectra",
        "lapack",
        "suitesparse",
        "superlu"
    ]

    # Options dependencies
    option_dependencies = {}
    for option in options:
        option_dependencies[option] = []

    option_dependencies["mpi"] = ["hypre", "metis"]
    option_dependencies["petsc"] = ["mpi"]
    option_dependencies["slepc"] = ["petsc"]
    option_dependencies["spectra"] = ["eigen"]
    # add options to choose blas version
    option_dependencies["lapack"] = ["blas"]

    # Options to check
    if ctx.options.mfem_options is None:
        options_to_check = []
    else:
        options_to_check = list(ctx.options.mfem_options.split(","))

    if "superlu" in options_to_check:
        ctx.options.superlu_dist = True

    # Add dependencies options to check
    dependencies_to_check = []
    for option in options_to_check:
        if option_dependencies[option] is not None and option_dependencies[option] not in dependencies_to_check and option_dependencies[option] not in options_to_check:
            dependencies_to_check += option_dependencies[option]
    options_to_check += dependencies_to_check

    # Check option required
    for option in options_to_check:
        if option.upper() not in ctx.get_env()["libs"]:
            # Add option to required libs
            ctx.get_env()["requires"] += [option.upper()]

            # Load option
            ctx.load(option, tooldir="waf_tools")

    # Header check
    check_include(ctx, "MFEM", "", ["mfem.hpp"], path_check)

    # Library Check
    check_lib(ctx, "MFEM", "", ["libmfem"], path_check)

    if ctx.env.LIB_MFEM or ctx.env.STLIB_MFEM:
        ctx.get_env()["libs"] += ["MFEM"]


def configure(cfg):
    if not cfg.env.LIB_MFEM:
        cfg.check_mfem()
