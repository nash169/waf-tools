#! /usr/bin/env python
# encoding: utf-8

from waflib.Configure import conf
from utils import check_include, check_lib


def options(opt):
    # Options
    opt.add_option("--superlu-path", type="string",
                   help="path to superlu", dest="superlu_path")

    # Distributed SUPERLU
    opt.add_option(
        "--superlu-dist", action="store_true", help="distributed version SUPERLU", dest="superlu_dist"
    )


@conf
def check_superlu(ctx):
    # Set the search path
    if ctx.options.superlu_path is None:
        path_check = ["/usr/local", "/usr"]
    else:
        path_check = [ctx.options.superlu_path]

    if ctx.options.superlu_dist:
        # SUPERLU includes
        check_include(ctx, "SUPERLU", ["superlu-dist"],
                      ["superlu_defs.h"], path_check)
        # SUPERLU libs
        check_lib(ctx, "SUPERLU", [""], ["libsuperlu_dist"], path_check)
    else:
        # SUPERLU includes
        check_include(ctx, "SUPERLU", ["superlu"], [
                      "supermatrix.h"], path_check)
        # SUPERLU libs
        check_lib(ctx, "SUPERLU", [""], ["libsuperlu"], path_check)

    if ctx.env.LIB_SUPERLU:
        ctx.get_env()["libs"] = ctx.get_env()["libs"] + ["SUPERLU"]


def configure(cfg):
    if not cfg.env.LIB_SUPERLU:
        cfg.check_superlu()
