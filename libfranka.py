#! /usr/bin/env python
# encoding: utf-8

from waflib.Configure import conf
from utils import check_include, check_lib


def options(opt):
    # Required package options
    opt.load("eigen", tooldir="waf_tools")

    # Options
    opt.add_option(
        "--libfranka-path", type="string", help="path to libfranka-lib", dest="libfranka_path"
    )


@conf
def check_libfranka(ctx):
    # Set the search path
    if ctx.options.libfranka_path is None:
        path_check = ["/usr/local", "/usr"]
    else:
        path_check = [ctx.options.libfranka_path]

    # libfranka-lib includes
    check_include(
        ctx, "LIBFRANKA", ["franka"], ["vacuum_gripper_state.h"], path_check
    )

    # libfranka-lib libs
    check_lib(ctx, "LIBFRANKA", "", ["libfranka"], path_check)

    if ctx.env.LIB_LIBFRANKA:
        # Add dependencies to require libraries
        ctx.get_env()["requires"] = ctx.get_env()["requires"] + ["EIGEN"]

        # Check for dependencies
        ctx.load("eigen", tooldir="waf_tools")

        # Add library
        ctx.get_env()["libs"] = ctx.get_env()["libs"] + ["LIBFRANKA"]


def configure(cfg):
    if not cfg.env.LIB_LIBFRANKA:
        cfg.check_libfranka()
