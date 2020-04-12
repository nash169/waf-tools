#! /usr/bin/env python
# encoding: utf-8

from waflib.Configure import conf
from utils import check_include, check_lib


def options(opt):
    # Required package options
    opt.load("eigen magnum", tooldir="waf_tools")

    # Options
    opt.add_option(
        "--magnum-dynamics-path",
        type="string",
        help="path to magnum-dynamics",
        dest="magnum-dynamics_path",
    )


@conf
def check_magnum_dynamics(ctx):
    # Set the search path
    if ctx.options.dynamics_path is None:
        path_check = ["/usr/local", "/usr"]
    else:
        path_check = [ctx.options.dynamics_path]

    # magnum-dynamics includes
    check_include(
        ctx, "MAGNUMDYNAMICS", ["magnum_dynamics"], ["MagnumApp.hpp"], path_check
    )

    # magnum-dynamics libs
    check_lib(ctx, "MAGNUMDYNAMICS", "", ["libMagnumDynamics"], path_check)

    if ctx.env.LIB_MAGNUMDYNAMICS:
        # Add dependencies to require libraries
        ctx.get_env()["requires"] = ctx.get_env()["requires"] + ["EIGEN", "MAGNUM"]

        # Check for dependencies
        ctx.load("eigen magnum", tooldir="waf_tools")

        # Add library
        ctx.get_env()["libs"] = ctx.get_env()["libs"] + ["MAGNUMDYNAMICS"]


def configure(cfg):
    if not cfg.env.LIB_MAGNUMDYNAMICS:
        cfg.check_magnum_dynamics()
