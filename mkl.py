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


def options(opt):
    # Options
    opt.add_option(
        "--mkl-path", type="string", help="path to Intel Math Kernel Library", dest="mkl_path",
    )
    opt.add_option(
        # sequential - openmp - tbb
        "--mkl-parallel", type="string", help="mkl threading layer", dest="mkl_parallel", default="sequential"
    )
    opt.add_option(
        # intel - std
        "--mkl-openmp", type="string", help="openmp type", dest="mkl_openmp", default="intel"
    )

    opt.add_option(
        "--mkl-64", action="store_true", help="API with 64 bit integer", dest="mkl_64"
    )

    # Required package options
    opt.load("tbb", tooldir="waf_tools")


@conf
def check_mkl(ctx):
    # Set the search path
    if ctx.options.mkl_path is None:
        path_check = ["/opt/intel", "/opt/intel/mkl", "/usr/local", "/usr"]
    else:
        path_check = [ctx.options.mkl_path]

    # MKL includes
    check_include(ctx, "MKL", ["mkl"], ["mkl.h"], path_check)

    # Sequential
    if ctx.options.mkl_parallel == "sequential":
        if ctx.env.CXXNAME in ["icc", "icpc"]:
            # Check lib
            check_lib(ctx, "MKL", "",
                      [
                          "libpthread",
                          "libm",
                          "libdl"
                      ],
                      path_check)
            # Add compiler options
            ctx.env.CXXFLAGS_MKL = ["-mkl=sequential"]
        else:
            check_lib(ctx, "MKL", "",
                      [
                          "libmkl_intel_ilp64" if ctx.options.mkl_64 else "libmkl_intel_lp64",
                          "libmkl_sequential",
                          "libmkl_core",
                          "libpthread",
                          "libm",
                          "libdl",
                      ],
                      path_check)
            # Add compiler options
            ctx.env.CXXFLAGS_MKL = ["-m64"]
            # Add link flags
            if ctx.env["DEST_OS"] != "darwin":
                ctx.env.LINKFLAGS_MKL = ["-Wl,--no-as-needed"]
    # OpenMP
    elif ctx.options.mkl_parallel == "openmp":
        if ctx.env.CXXNAME in ["icc", "icpc"]:
            check_lib(ctx, "MKL", "",
                      [
                          "libiomp5",
                          "libpthread",
                          "libm",
                          "libdl"
                      ],
                      path_check)
            # Add compiler options
            ctx.env.CXXFLAGS_MKL = ["-mkl=parallel"]
        else:
            lib_openmp = "iomp5" if ctx.options.mkl_openmp == "intel" else "gomp"

            check_lib(ctx, "MKL", "",
                      [
                          "libmkl_intel_ilp64" if ctx.options.mkl_64 else "libmkl_intel_lp64",
                          "libmkl_gnu_thread" if lib_openmp == "gomp" else "libmkl_intel_thread",
                          "libmkl_core",
                          "lib" + lib_openmp,
                          "libpthread",
                          "libm",
                          "libdl",
                      ],
                      path_check)
            # Add compiler options
            ctx.env.CXXFLAGS_MKL = ["-m64"]
            # Add link flags
            if ctx.env["DEST_OS"] != "darwin":
                ctx.env.LINKFLAGS_MKL = ["-Wl,--no-as-needed"]
    elif ctx.options.mkl_parallel == "tbb":
        # Load TBB
        if "TBB" not in ctx.get_env()["libs"]:
            ctx.get_env()["requires"] += ["TBB"]
            ctx.load("tbb", tooldir="waf_tools")

        if ctx.env.CXXNAME in ["icc", "icpc"]:
            check_lib(ctx, "MKL", "",
                      [
                          "libpthread",
                          "libm",
                          "libdl"
                      ],
                      path_check)
            # Add compiler options
            ctx.env.CXXFLAGS_MKL = ["-mkl=parallel"]
        else:
            check_lib(ctx, "MKL", "",
                      [
                          "libmkl_intel_ilp64" if ctx.options.mkl_64 else "libmkl_intel_lp64",
                          "libmkl_tbb_thread",
                          "libmkl_core",
                          # "libtbb" found via tool
                          "libpthread",
                          "libm",
                          "libdl",
                      ],
                      path_check)
            # Add standard library manually
            ctx.env.LIB_MKL += ["stdc++"]
            # Add compiler options
            ctx.env.CXXFLAGS_MKL = ["-m64"]
            # Add link flags
            if ctx.env["DEST_OS"] != "darwin":
                ctx.env.LINKFLAGS_MKL = ["-Wl,--no-as-needed"]
    # Add MKL
    if ctx.env.LIB_MKL:
        # MKL defines
        if ctx.options.mkl_64:
            ctx.env.DEFINES_MKL = ["MKL_ILP64"]  # Eigen suggests "MKL_LP64"

        # Add to used libraries
        ctx.get_env()["libs"] += ["MKL"]

        # Remove LAPACK if present (MKL has its own implementation)
        if "LAPACK" in ctx.get_env()["libs"]:
            ctx.get_env()["libs"].remove("LAPACK")
            ctx.get_env()["requires"].remove("LAPACK")

        # Remove BLAS and others if present (MKL has its own implementation)
        if "BLAS" in ctx.get_env()["libs"]:
            ctx.get_env()["libs"].remove("BLAS")
            ctx.get_env()["requires"].remove("BLAS")
        if "OPENBLAS" in ctx.get_env()["libs"]:
            ctx.get_env()["libs"].remove("OPENBLAS")
            ctx.get_env()["requires"].remove("OPENBLAS")
        if "ATLAS" in ctx.get_env()["libs"]:
            ctx.get_env()["libs"].remove("ATLAS")
            ctx.get_env()["requires"].remove("ATLAS")


def configure(cfg):
    if not cfg.env.LIB_MKL:
        cfg.check_mkl()
