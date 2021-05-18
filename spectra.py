#! /usr/bin/env python
# encoding: utf-8

from waflib.Configure import conf
from utils import check_include


def options(opt):
    # Select installation path
    opt.add_option(
        "--spectra-path", type="string", help="path to spectra", dest="spectra_path"
    )

    # Load options
    opt.load("eigen", tooldir="waf_tools")


@conf
def check_spectra(ctx):
    # Set the search path
    if ctx.options.spectra_path is None:
        path_check = ["/usr/local", "/usr", "/opt"]
    else:
        path_check = [ctx.options.spectra_path]

    # SPECTRA includes
    check_include(ctx, "SPECTRA", ["Spectra"], [
                  "SymEigsSolver.h"], path_check)

    # If SPECTRA headers found
    if ctx.env.INCLUDES_SPECTRA:
        if "EIGEN" not in ctx.get_env()["libs"]:
            ctx.load("eigen", tooldir="waf_tools")

        # Add SPECTRA label to the list of libraries
        ctx.get_env()["libs"] += ["SPECTRA"]


def configure(cfg):
    if not cfg.env.INCLUDES_SPECTRA:
        cfg.check_spectra()
