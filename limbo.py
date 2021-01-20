#! /usr/bin/env python
# encoding: utf-8

from waflib.Configure import conf
from utils import check_include, check_lib


def options(opt):
    # Required package options
    opt.load("eigen corrade", tooldir="waf_tools")

    # Options
    opt.add_option(
        "--limbo-path", type="string", help="path to limbo-lib", dest="limbo_path",
    )

    opt.add_option(
        "--limbo-nlopt", action="store_true", help="NLOPT Optimization support for Limbo", dest="limbo_nlopt"
    )

    opt.add_option(
        "--limbo-cmaes", action="store_true", help="CMAES Optimization support for Limbo", dest="limbo_cmaes"
    )

    # Load options
    opt.load("eigen nlopt libcmaes", tooldir="waf_tools")


@conf
def check_limbo(ctx):
    # Set the search path
    if ctx.options.limbo_path is None:
        path_check = ["/usr/local", "/usr"]
    else:
        path_check = [ctx.options.limbo_path]

    # limbo-lib includes (since limbo is not installed we look into dir src for the headers)
    check_include(ctx, "LIMBO", ["src"], ["limbo/limbo.hpp"], path_check)

    # limbo-lib libs (since limbo is not installed we look into dir build for the compiled library)
    check_lib(ctx, "LIMBO", ["build/src"], ["liblimbo"], path_check)

    if ctx.env.LIB_LIMBO or ctx.env.STLIB_LIMBO:
        # Add dependencies
        if "EIGEN" not in ctx.get_env()["requires"]:
            ctx.get_env()["requires"] += ["EIGEN"]

        if "EIGEN" not in ctx.get_env()["libs"]:
            ctx.load("eigen", tooldir="waf_tools")

        if ctx.options.limbo_nlopt:
            if "NLOPT" not in ctx.get_env()["requires"]:
                ctx.get_env()["requires"] += ["NLOPT"]

            if "NLOPT" not in ctx.get_env()["libs"]:
                ctx.load("nlopt", tooldir="waf_tools")

        if ctx.options.limbo_cmaes:
            if "LIBCMAES" not in ctx.get_env()["requires"]:
                ctx.get_env()["requires"] += ["LIBCMAES"]

            if "LIBCMAES" not in ctx.get_env()["libs"]:
                ctx.load("libcmaes", tooldir="waf_tools")

        # Add library
        ctx.get_env()["libs"] += ["LIMBO"]


def configure(cfg):
    if not cfg.env.LIB_LIMBO and not cfg.env.STLIB_LIMBO:
        cfg.check_limbo()
