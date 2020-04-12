#! /usr/bin/env python
# encoding: utf-8

from waflib.Configure import conf
from utils import check_include, check_lib


def options(opt):
    # Required package options
    opt.load("eigen corrade", tooldir="waf_tools")

    # Options
    opt.add_option(
        "--integrator-path",
        type="string",
        help="path to integrator-lib",
        dest="integrator_path",
    )


@conf
def check_integrator(ctx):
    # Set the search path
    if ctx.options.integrator_path is None:
        path_check = ["/usr/local", "/usr"]
    else:
        path_check = [ctx.options.integrator_path]

    # integrator-lib includes
    check_include(
        ctx, "INTEGRATOR", ["integrator_lib"], ["AbstractIntegrator.hpp"], path_check
    )

    # integrator-lib libs
    check_lib(ctx, "INTEGRATOR", "", ["libIntegrator"], path_check)

    if ctx.env.LIB_INTEGRATOR:
        # Add dependencies to require libraries
        ctx.get_env()["requires"] = ctx.get_env()["requires"] + ["EIGEN", "CORRADE"]

        # Check for dependencies
        ctx.load("eigen corrade", tooldir="waf_tools")

        # Add library
        ctx.get_env()["libs"] = ctx.get_env()["libs"] + ["INTEGRATOR"]


def configure(cfg):
    if not cfg.env.LIB_INTEGRATOR:
        cfg.check_integrator()