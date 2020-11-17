#! /usr/bin/env python
# encoding: utf-8

from waflib.Configure import conf
from utils import check_lib


def options(opt):
    opt.add_option(
        "--atlas-path", type="string", help="path to ATLAS", dest="atlas_path"
    )


@conf
def check_atlas(ctx):
    # Set the search path
    if ctx.options.atlas_path is None:
        path_check = ["/usr/local", "/usr", "/opt"]
    else:
        path_check = [ctx.options.atlas_path]

    # LIB Check
    check_lib(ctx, "ATLAS", "", ["libatlas", "liblapack_atlas"], path_check)

    if ctx.env.LIB_ATLAS:
        ctx.get_env()["libs"] = ctx.get_env()["libs"] + ["ATLAS"]


def configure(cfg):
    if not cfg.env.LIB_ATLAS:
        cfg.check_atlas()
