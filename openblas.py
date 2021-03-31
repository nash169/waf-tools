#! /usr/bin/env python
# encoding: utf-8

from waflib.Configure import conf
from utils import check_lib

# For clarification about LAPACK/BLAS implementations check:
# https://wiki.debian.org/DebianScience/LinearAlgebraLibraries


def options(opt):
    opt.add_option(
        "--openblas-path", type="string", help="path to OpenBLAS", dest="openblas_path"
    )
    # 64-bit indexing
    opt.add_option(
        "--openblas-64", action="store_true", help="enable 64-bit indexing", dest="openblas_64"
    )


@conf
def check_openblas(ctx):
    # Set the search path
    if ctx.options.openblas_path is None:
        path_check = ["/usr/local", "/usr", "/opt"]
    else:
        path_check = [ctx.options.openblas_path]

    # LIB Check
    if ctx.options.openblas_64:
        check_lib(ctx, "OPENBLAS", "", ["libopenblas64"], path_check)
    else:
        check_lib(ctx, "OPENBLAS", "", ["libopenblas"], path_check)

    if ctx.env.LIB_OPENBLAS:
        ctx.get_env()["libs"] += ["OPENBLAS"]


def configure(cfg):
    if not cfg.env.LIB_OPENBLAS:
        cfg.check_openblas()
