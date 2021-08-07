#! /usr/bin/env python
# encoding: utf-8

from waflib.Configure import conf
from utils import check_include, check_lib


def options(opt):
    # Options
    opt.add_option("--hypre-path", type="string",
                   help="path to hypre", dest="hypre_path")


@conf
def check_hypre(ctx):
    # Set the search path
    if ctx.options.hypre_path is None:
        path_check = ["/usr/local", "/usr"]
    else:
        path_check = [ctx.options.hypre_path]

    # HYPRE includes
    check_include(ctx, "HYPRE", ["hypre"], ["HYPRE.h"], path_check)

    # HYPRE libs
    check_lib(ctx, "HYPRE", "", ["libHYPRE", "libHYPRE_core"], path_check)

    if ctx.env.LIB_HYPRE or ctx.env.STLIB_HYPRE:
        ctx.get_env()["libs"] += ["HYPRE"]


def configure(cfg):
    if not cfg.env.LIB_HYPRE:
        cfg.check_hypre()
