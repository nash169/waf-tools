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

    # MKL libs
    if ctx.options.mkl_threading is None or ctx.options.mkl_threading == "sequential":
        if ctx.env.CXXNAME in ["icc", "icpc"]:
            check_lib(ctx, "MKL", "", ["libpthread",
                                       "libm", "libdl"], path_check)
            ctx.env.CXXFLAGS_MKL = ["-mkl=sequential"]
        else:
            check_lib(
                ctx,
                "MKL",
                "",
                [
                    "libmkl_intel_ilp64",
                    "libmkl_sequential",
                    "libmkl_core",
                    "libpthread",
                    "libm",
                    "libdl",
                ],
                path_check,
            )
            ctx.env.CXXFLAGS_MKL = ["-m64"]
            ctx.env.LINKFLAGS_MKL = ["-Wl,--no-as-needed"]
    elif ctx.options.mkl_threading == "openmp":
        if ctx.env.CXXNAME in ["icc", "icpc"]:
            check_lib(
                ctx, "MKL", "", ["libiomp5", "libpthread",
                                 "libm", "libdl"], path_check
            )
            ctx.env.CXXFLAGS_MKL = ["-mkl=parallel"]
        else:
            lib_openmp = "iomp5" if ctx.options.mkl_openmp == "intel" else "gomp"

            check_lib(
                ctx,
                "MKL",
                "",
                [
                    "libmkl_intel_ilp64",
                    "libmkl_gnu_thread"
                    if lib_openmp == "gomp"
                    else "libmkl_intel_thread",
                    "libmkl_core",
                    "lib" + lib_openmp,
                    "libpthread",
                    "libm",
                    "libdl",
                ],
                path_check,
            )
            ctx.env.CXXFLAGS_MKL = ["-m64"]
            ctx.env.LINKFLAGS_MKL = ["-Wl,--no-as-needed"]
    elif ctx.options.mkl_threading == "tbb":
        if "TBB" not in ctx.get_env()["libs"]:
            ctx.get_env()["requires"] += ["TBB"]
            ctx.load("tbb", tooldir="waf_tools")

        if ctx.env.CXXNAME in ["icc", "icpc"]:
            check_lib(ctx, "MKL", "", ["libpthread",
                                       "libm", "libdl"], path_check)
            ctx.env.CXXFLAGS_MKL = ["-mkl=parallel"]
        else:
            check_lib(
                ctx,
                "MKL",
                "",
                ["libmkl_intel_ilp64", "libmkl_tbb_thread", "libmkl_core"],
                path_check,
            )
            ctx.env.CXXFLAGS_MKL = ["-m64"]

            if ctx.env["DEST_OS"] != "darwin":
                ctx.env.LINKFLAGS_MKL = ["-Wl,--no-as-needed"]

        ctx.env.LIB_MKL = ["stdc++"] + ctx.env.LIB_MKL

    # Add MKL
    if ctx.env.LIB_MKL:
        # MKL defines
        ctx.env.DEFINES_MKL = ["MKL_ILP64"]  # Eigen suggests "MKL_LP64"
        # Add to used libraries
        ctx.get_env()["libs"] += ["MKL"]


def configure(cfg):
    if not cfg.env.LIB_MKL:
        cfg.check_mkl()
