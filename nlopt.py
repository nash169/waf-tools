#! /usr/bin/env python
# encoding: utf-8

from waflib.Configure import conf
from utils import check_include, check_lib


def options(opt):
    opt.add_option(
        "--nlopt-path", type="string", help="path to NLOPT", dest="nlopt_path"
    )


@conf
def check_nlopt(ctx):
    # Set the search path
    if ctx.options.nlopt_path is None:
        path_check = ["/usr/local", "/usr", "/opt"]
    else:
        path_check = [ctx.options.nlopt_path]

    # Header check
    check_include(ctx, "NLOPT", "", ["nlopt.hpp"], path_check)

    # Library Check
    check_lib(ctx, "NLOPT", "", ["libnlopt"], path_check)
    # check_lib(ctx, "NLOPT", "", ["libnlopt_cxx"], path_check)

    if ctx.env.LIB_NLOPT:
        ctx.get_env()["libs"] += ["NLOPT"]


def configure(cfg):
    if not cfg.env.LIB_NLOPT:
        cfg.check_nlopt()
