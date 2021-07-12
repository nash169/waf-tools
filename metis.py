#! /usr/bin/env python
# encoding: utf-8

from waflib.Configure import conf
from utils import check_include, check_lib


def options(opt):
    # Options
    opt.add_option("--metis-path", type="string",
                   help="path to metis", dest="metis_path")

    opt.add_option("--metis-parallel", action="store_true", help="parallel version of METIS", dest="metis_parallel")


@conf
def check_metis(ctx):
    # Set the search path
    if ctx.options.metis_path is None:
        path_check = ["/usr/local", "/usr"]
    else:
        path_check = [ctx.options.metis_path]

    # METIS includes
    check_include(ctx, "METIS", "", ["metis.h"], path_check)

    # METIS libs
    check_lib(ctx, "METIS", "", ["libmetis"], path_check)

    if ctx.options.metis_parallel:
        check_include(ctx, "METIS", "", ["parmetis.h"], path_check)

        check_lib(ctx, "METIS", "", ["libparmetis"], path_check)

    if ctx.env.LIB_METIS or ctx.env.STLIB_METIS:
        ctx.get_env()["libs"] += ["METIS"]


def configure(cfg):
    if not cfg.env.LIB_METIS:
        cfg.check_metis()
