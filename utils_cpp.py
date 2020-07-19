#! /usr/bin/env python
# encoding: utf-8

from waflib.Configure import conf
from utils import check_include, check_lib


def options(opt):
    # Required package options
    opt.load("eigen corrade", tooldir="waf_tools")

    # Options
    opt.add_option(
        "--utilscpp-path",
        type="string",
        help="path to utilscpp-lib",
        dest="utilscpp_path",
    )


@conf
def check_utilscpp(ctx):
    # Set the search path
    if ctx.options.utilscpp_path is None:
        path_check = ["/usr/local", "/usr"]
    else:
        path_check = [ctx.options.utilscpp_path]

    # utilscpp-lib includes
    check_include(ctx, "UTILSCPP", ["utils_cpp"], ["UtilsCpp.hpp"], path_check)

    # utilscpp-lib libs
    check_lib(ctx, "UTILSCPP", "", ["libUtilsCpp"], path_check)

    if ctx.env.LIB_UTILSCPP or ctx.env.STLIB_UTILSCPP:
        # Add dependencies to require libraries
        ctx.get_env()["requires"] = ctx.get_env()["requires"] + ["EIGEN", "CORRADE"]

        # Check for dependencies
        ctx.load("eigen corrade", tooldir="waf_tools")

        # Add library
        ctx.get_env()["libs"] = ctx.get_env()["libs"] + ["UTILSCPP"]


def configure(cfg):
    if not cfg.env.LIB_UTILSCPP and not cfg.env.STLIB_UTILSCPP:
        cfg.check_utilscpp()