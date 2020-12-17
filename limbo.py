#! /usr/bin/env python
# encoding: utf-8

from waflib.Configure import conf
from utils import check_include, check_lib


def options(opt):
    # Required package options
    opt.load("eigen corrade", tooldir="waf_tools")

    # Options
    opt.add_option(
        "--limbo-path",
        type="string",
        help="path to limbo-lib",
        dest="limbo_path",
    )


@conf
def check_limbo(ctx):
    # Set the search path
    if ctx.options.limbo_path is None:
        path_check = ["/usr/local", "/usr"]
    else:
        path_check = [ctx.options.limbo_path]

    # limbo-lib includes
    check_include(ctx, "LIMBO", "", ["limbo/limbo.hpp"], path_check)

    # limbo-lib libs
    check_lib(ctx, "LIMBO", ["limbo"], ["liblimbo"], path_check)

    if ctx.env.LIB_LIMBO or ctx.env.STLIB_LIMBO:
        # Add dependencies to require libraries
        ctx.get_env()["requires"] = ctx.get_env()[
            "requires"] + ["EIGEN", "CORRADE"]

        # Check for dependencies
        ctx.load("eigen corrade", tooldir="waf_tools")

        # Add library
        ctx.get_env()["libs"] = ctx.get_env()["libs"] + ["LIMBO"]


def configure(cfg):
    if not cfg.env.LIB_LIMBO and not cfg.env.STLIB_LIMBO:
        cfg.check_limbo()
