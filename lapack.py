#! /usr/bin/env python
# encoding: utf-8

from waflib.Configure import conf
from utils import check_lib

# For clarification about LAPACK/BLAS implementations check:
# https://wiki.debian.org/DebianScience/LinearAlgebraLibraries


def options(opt):
    opt.add_option(
        "--lapack-path", type="string", help="path to LAPACK", dest="lapack_path"
    )
    # C lib LAPACK version
    opt.add_option(
        "--lapack-clib", action="store_true", help="load C lib version LAPACK", dest="lapack_clib"
    )
    # 64-bit indexing
    opt.add_option(
        "--lapack-64", action="store_true", help="enable 64-bit indexing", dest="lapack_64"
    )


@conf
def check_lapack(ctx):
    # Set the search path
    if ctx.options.lapack_path is None:
        path_check = ["/usr/local", "/usr", "/opt"]
    else:
        path_check = [ctx.options.lapack_path]

    if ctx.options.lapack_64:
        lib_to_check = ["liblapack64"]
        if ctx.options.lapack_clib:
            lib_to_check += ["liblapacke64"]
    else:
        lib_to_check = ["liblapack"]
        if ctx.options.lapack_clib:
            lib_to_check += ["liblapacke"]

    # Check LAPACK libs
    check_lib(ctx, "LAPACK", "", lib_to_check, path_check)

    # Add LAPACK
    if ctx.env.LIB_LAPACK:
        ctx.get_env()["libs"] += ["LAPACK"]


def configure(cfg):
    if not cfg.env.LIB_LAPACK:
        cfg.check_lapack()
