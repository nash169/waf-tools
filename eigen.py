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
from utils import check_include


def options(opt):
    # Select installation path
    opt.add_option(
        "--eigen-path", type="string", help="path to eigen", dest="eigen_path"
    )
    # Activate OPENMP
    opt.add_option(
        "--eigen-openmp", action="store_true", help="enable OpenMP", dest="eigen_openmp",
    )
    # Activate LAPACK
    opt.add_option(
        "--eigen-lapack", action="store_true", help="enable LAPACK", dest="eigen_lapack"
    )
    # Activate (Open)BLAS
    opt.add_option(
        "--eigen-blas", type="string", help="enable BLAS", dest="eigen_blas"
    )
    # Activate MKL
    opt.add_option(
        "--eigen-mkl", action="store_true", help="enable MKL", dest="eigen_mkl"
    )

    # Load options
    opt.load("lapack blas openblas atlas mkl", tooldir="waf_tools")


@conf
def check_eigen(ctx):
    # Set the search path
    if ctx.options.eigen_path is None:
        path_check = ["/usr/local", "/usr", "/opt"]
    else:
        path_check = [ctx.options.eigen_path]

    # EIGEN includes
    check_include(ctx, "EIGEN", ["eigen3"], ["Eigen/Core"], path_check)

    # If EIGEN headers found
    if ctx.env.INCLUDES_EIGEN:
        # Add EIGEN label to the list of libraries
        ctx.get_env()["libs"] += ["EIGEN"]

    # Load OPENMP tool
    if ctx.options.eigen_openmp:
        ctx.load("openmp", tooldir="waf_tools")

    # Load LAPACK C interface and add compiler DEFINES
    if ctx.options.eigen_lapack and "EIGEN_USE_LAPACKE" not in ctx.env.DEFINES_EIGEN:
        if "LAPACK" not in ctx.get_env()["libs"] and ctx.options.lapack_clib is None:
            # Add LAPACK to required libs
            ctx.get_env()["requires"] += ["LAPACK"]

            # Request C lib LAPACK version
            ctx.options.lapack_clib = True

            # Load LAPACK
            ctx.load("lapack", tooldir="waf_tools")

        # Add EIGEN flags for LAPACK
        ctx.env.DEFINES_EIGEN += ["EIGEN_USE_LAPACKE"]

    # Load (Open)BLAS and add compiler DEFINES
    if ctx.options.eigen_blas is not None and "EIGEN_USE_BLAS" not in ctx.env.DEFINES_EIGEN:
        if ctx.options.eigen_blas == "openblas" and "OPENBLAS" not in ctx.get_env()["libs"]:
            # Add OpenBLAS to required libs and find it
            ctx.get_env()["requires"] += ["OPENBLAS"]
            ctx.load("openblas", tooldir="waf_tools")
        elif ctx.options.eigen_blas == "atlas" and "ATLAS" not in ctx.get_env()["libs"]:
            # Add OpenBLAS to required libs and find it
            ctx.get_env()["requires"] += ["ATLAS"]
            ctx.load("atlas", tooldir="waf_tools")
        elif ctx.options.eigen_blas == "blas" and "BLAS" not in ctx.get_env()["libs"]:
            # Add BLAS to required libs and find it
            ctx.get_env()["requires"] += ["BLAS"]
            ctx.load("blas", tooldir="waf_tools")

        # Add EIGEN flags for OpenBLAS
        ctx.env.DEFINES_EIGEN += ["EIGEN_USE_BLAS"]

    # Load MKL tool and add compiler DEFINES
    if ctx.options.eigen_mkl and "EIGEN_USE_MKL_VML" not in ctx.env.DEFINES_EIGEN:
        if "MKL" not in ctx.get_env()["libs"]:
            # Add MKL to required libs and find it
            ctx.get_env()["requires"] += ["MKL"]
            ctx.load("mkl", tooldir="waf_tools")

        # Add EIGEN flags for MKL
        ctx.env.DEFINES_EIGEN += ["EIGEN_USE_MKL_VML", "MKL_DIRECT_CALL"]


def configure(cfg):
    if not cfg.env.INCLUDES_EIGEN:
        cfg.check_eigen()
