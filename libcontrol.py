#! /usr/bin/env python
# encoding: utf-8

from waflib.Configure import conf
from utils import check_include, check_lib


def options(opt):
    # Required package options
    opt.load("eigen", tooldir="waf_tools")
    opt.load("corrade", tooldir="waf_tools")

    # Options
    opt.add_option(
        "--libcontrol-path",
        type="string",
        help="path to libcontrol",
        dest="libcontrol_path",
    )


@conf
def check_libcontrol(ctx):
    # Set the search path
    if ctx.options.libcontrol_path is None:
        path_check = ["/usr/local", "/usr"]
    else:
        path_check = [ctx.options.libcontrol_path]

    # LIBCONTROL includes
    check_include(ctx, "LIBCONTROL", "", ["libcontrol/ControlState.hpp"], path_check)

    # LIBCONTROL libs
    check_lib(ctx, "LIBCONTROL", "", ["libControl"], path_check)

    if ctx.env.LIB_LIBCONTROL:
        ctx.get_env()["requires"] = ctx.get_env()["requires"] + ["EIGEN", "CORRADE"]
        ctx.load("eigen", tooldir="waf_tools")
        ctx.load("corrade", tooldir="waf_tools")

        ctx.get_env()["libs"] = ctx.get_env()["libs"] + ["LIBCONTROL"]


def configure(cfg):
    if not cfg.env.LIB_LIBCONTROL:
        cfg.check_libcontrol()
