#! /usr/bin/env python
# encoding: utf-8

from waflib.Configure import conf
from utils import check_lib


def options(opt):
    opt.add_option(
        "--blas-path", type="string", help="path to BLAS", dest="blas_path"
    )
    # 64-bit indexing
    opt.add_option(
        "--blas-64", action="store_true", help="enable 64-bit indexing", dest="blas_64"
    )


@conf
def check_blas(ctx):
    # Set the search path
    if ctx.options.blas_path is None:
        path_check = ["/usr/local", "/usr", "/opt"]
    else:
        path_check = [ctx.options.blas_path]

    # LIB Check
    if ctx.options.blas_64:
        check_lib(ctx, "BLAS", "", ["libblas64"], path_check)
    else:
        check_lib(ctx, "BLAS", "", ["libblas"], path_check)

    if ctx.env.LIB_BLAS:
        ctx.get_env()["libs"] = ctx.get_env()["libs"] + ["BLAS"]


def configure(cfg):
    if not cfg.env.LIB_BLAS:
        cfg.check_blas()
