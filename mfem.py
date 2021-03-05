#! /usr/bin/env python
# encoding: utf-8

from waflib.Configure import conf
from utils import check_include, check_lib

# For clarification about LAPACK/BLAS implementations check:
# https://wiki.debian.org/DebianScience/LinearAlgebraLibraries


def options(opt):
    opt.add_option(
        "--mfem-path", type="string", help="path to libmfem", dest="mfem_path"
    )

    opt.add_option(
        "--mfem-options", type="string", help="options mfem", dest="mfem_options"
    )

    # Load options
    opt.load("openmp arpack", tooldir="waf_tools")


@conf
def check_mfem(ctx):
    # Set the search path
    if ctx.options.mfem_path is None:
        path_check = ["/usr/local", "/usr", "/opt"]
    else:
        path_check = [ctx.options.mfem_path]

    # Components
    options = [
        "openmp",
        "arpack",
    ]

    # Component dependencies
    option_dependencies = {}
    for option in options:
        option_dependencies[option] = []

    option_dependencies["parpack"] = ["arpack"]

    # Components to check
    if ctx.options.mfem_options is None:
        options_to_check = []
    else:
        options_to_check = list(ctx.options.mfem_options.split(","))

    for option in options_to_check:
        if option.upper() not in ctx.get_env()["libs"]:
            # Add option to required libs
            ctx.get_env()["requires"] += [option.upper()]

            # Load option
            ctx.load(option, tooldir="waf_tools")

    # Header check
    check_include(ctx, "MFEM", "", ["mfem.hpp"], path_check)

    # Library Check
    check_lib(ctx, "MFEM", "", ["libmfem"], path_check)

    if ctx.env.LIB_MFEM or ctx.env.STLIB_MFEM:
        ctx.get_env()["libs"] += ["MFEM"]


def configure(cfg):
    if not cfg.env.LIB_MFEM:
        cfg.check_mfem()
