#! /usr/bin/env python
# encoding: utf-8

from waflib.Configure import conf
from utils import check_lib

# For clarification about ARPACK/BLAS implementations check:
# https://wiki.debian.org/DebianScience/LinearAlgebraLibraries


def options(opt):
    opt.add_option(
        "--arpack-path", type="string", help="path to ARPACK", dest="arpack_path"
    )
    # Parallel ARPACK
    opt.add_option(
        "--arpack-parallel", action="store_true", help="parallel version ARPACK", dest="arpack_parallel"
    )


@conf
def check_arpack(ctx):
    # Set the search path
    if ctx.options.arpack_path is None:
        path_check = ["/usr/local", "/usr", "/opt"]
    else:
        path_check = [ctx.options.arpack_path]

    lib_to_check = ["libarpack"]
    if ctx.options.arpack_parallel:
        lib_to_check += ["libparpack"]

    # Check ARPACK libs
    check_lib(ctx, "ARPACK", "", lib_to_check, path_check)

    # Add ARPACK
    if ctx.env.LIB_ARPACK:
        ctx.get_env()["libs"] += ["ARPACK"]


def configure(cfg):
    if not cfg.env.LIB_ARPACK:
        cfg.check_arpack()
