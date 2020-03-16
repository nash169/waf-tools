#! /usr/bin/env python
# encoding: utf-8

from waflib.Configure import conf
from utils import check_include, check_lib


def options(opt):
    # Required package options
    opt.load("eigen", tooldir="waf_tools")

    # Options
    opt.add_option(
        "--raisim-path", type="string", help="path to raisim", dest="raisim_path"
    )


@conf
def check_raisim(ctx):
    # Set the search path
    if ctx.options.raisim_path is None:
        path_check = ["/usr/local", "/usr"]
    else:
        path_check = [ctx.options.raisim_path]

    # RaiSim includes
    check_include(ctx, "RAISIM", "", ["raisim/World.hpp"], path_check)

    # RaiSim libs
    check_lib(ctx, "RAISIM", "", ["libraisim"], path_check)

    if ctx.env.LIB_RAISIM:
        ctx.get_env()["requires"] = ctx.get_env()["requires"] + ["EIGEN"]
        ctx.load("eigen", tooldir="waf_tools")

        ctx.env.STLIB_RAISIM = ["IrrXML"]
        ctx.env.LIB_RAISIM = ctx.env.LIB_RAISIM + ["png", "raisimODE"]

        ctx.get_env()["libs"] = ctx.get_env()["libs"] + ["RAISIM"]


def configure(cfg):
    if not cfg.env.LIB_RAISIM:
        cfg.check_raisim()
