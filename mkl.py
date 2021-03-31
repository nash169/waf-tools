#! /usr/bin/env python
# encoding: utf-8

from waflib.Configure import conf
from utils import check_include, check_lib


def options(opt):
    # Options
    opt.add_option(
        "--mkl-path", type="string", help="path to Intel Math Kernel Library", dest="mkl_path",
    )
    opt.add_option(
        "--mkl-threading", type="string", help="mkl threading layer", dest="mkl_threading",
    )

    opt.add_option(
        "--mkl-openmp", type="string", help="openmp type", dest="mkl_openmp")

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
    if ctx.options.mkl_threading is None or ctx.options.mkl_threading == "sequential":
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
    elif ctx.options.mkl_threading == "openmp":
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
    elif ctx.options.mkl_threading == "tbb":
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


def configure(cfg):
    if not cfg.env.LIB_MKL:
        cfg.check_mkl()
