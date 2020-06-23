#! /usr/bin/env python
# encoding: utf-8

from waflib.Configure import conf
from utils import check_include, check_lib


def options(opt):
    # Required package options
    opt.load("eigen corrade", tooldir="waf_tools")

    # Options
    opt.add_option(
        "--control-path", type="string", help="path to control-lib", dest="control_path"
    )


@conf
def check_control(ctx):
    # Set the search path
    if ctx.options.control_path is None:
        path_check = ["/usr/local", "/usr"]
    else:
        path_check = [ctx.options.control_path]

    # control-lib includes
    check_include(
        ctx, "CONTROL", ["control_lib"], ["AbstractController.hpp"], path_check
    )

    # control-lib libs
    check_lib(ctx, "CONTROL", "", ["libControl"], path_check)

    if ctx.env.LIB_CONTROL or ctx.env.STLIB_CONTROL:
        # Add dependencies to require libraries
        ctx.get_env()["requires"] = ctx.get_env()["requires"] + ["EIGEN", "CORRADE"]

        # Check for dependencies
        ctx.load("eigen corrade", tooldir="waf_tools")

        # Add library
        ctx.get_env()["libs"] = ctx.get_env()["libs"] + ["CONTROL"]


def configure(cfg):
    if not cfg.env.LIB_CONTROL and not cfg.env.STLIB_CONTROL:
        cfg.check_control()
