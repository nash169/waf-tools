#! /usr/bin/env python
# encoding: utf-8

from waflib.Configure import conf
from utils import check_include, check_lib

# For clarification about LAPACK/BLAS implementations check:
# https://wiki.debian.org/DebianScience/LinearAlgebraLibraries


def options(opt):
    opt.add_option(
        "--libcmaes-path", type="string", help="path to libCMAES", dest="libcmaes_path"
    )


@conf
def check_libcmaes(ctx):
    # Set the search path
    if ctx.options.libcmaes_path is None:
        path_check = ["/usr/local", "/usr", "/opt"]
    else:
        path_check = [ctx.options.libcmaes_path]

    # kernel-lib includes
    check_include(ctx, "LIBCMAES", ["libcmaes"], ["cmaes.h"], path_check)

    # LIB Check
    check_lib(ctx, "LIBCMAES", "", ["libcmaes"], path_check)

    if ctx.env.LIB_LIBCMAES:
        ctx.get_env()["libs"] = ctx.get_env()["libs"] + ["LIBCMAES"]


def configure(cfg):
    if not cfg.env.LIB_LIBCMAES:
        cfg.check_libcmaes()
