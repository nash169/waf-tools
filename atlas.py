#! /usr/bin/env python
# encoding: utf-8

from waflib.Configure import conf
from utils import check_include, check_lib

# ATLAS implementation of BLAS provides optimized subset of LAPACK

# For clarification about LAPACK/BLAS implementations check:
# https://wiki.debian.org/DebianScience/LinearAlgebraLibraries


def options(opt):
    opt.add_option(
        "--atlas-path", type="string", help="path to ATLAS", dest="atlas_path"
    )

    # Not active yet
    opt.add_option(
        "--atlas-blas", action="store_true", help="Activates only BLAS subset", dest="atlas_blas"
    )

    # Not active yet
    opt.add_option(
        "--atlas-lapack", action="store_true", help="Activates only LAPACK subset", dest="atlas_blas"
    )

    # Not active yet
    opt.add_option(
        "--atlas-cblas", action="store_true", help="Activates only C BLAS subset", dest="atlas_blas"
    )

    # Not active yet
    opt.add_option(
        "--atlas-f77blas", action="store_true", help="Activates only fortran BLAS subset", dest="atlas_blas"
    )


@conf
def check_atlas(ctx):
    # Set the search path
    if ctx.options.atlas_path is None:
        path_check = ["/usr/local", "/usr", "/opt"]
    else:
        path_check = [ctx.options.atlas_path]

    # HEADER Check
    check_include(ctx, "ATLAS", ["atlas"], [
                  "atlas_buildinfo.h", "clapack.h"], path_check)

    # LIB Check
    check_lib(ctx, "ATLAS", "", ["libatlas"], path_check)

    if ctx.env.LIB_ATLAS:
        ctx.get_env()["libs"] += ["ATLAS"]

        # Remove LAPACK if present (ATLAS has its own implementation)
        # This should take place just when the complete atlas implementation is requested
        if "LAPACK" in ctx.get_env()["libs"]:
            ctx.get_env()["libs"].remove("LAPACK")
            ctx.get_env()["requires"].remove("LAPACK")


def configure(cfg):
    if not cfg.env.LIB_ATLAS:
        cfg.check_atlas()
