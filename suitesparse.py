#! /usr/bin/env python
# encoding: utf-8

from waflib.Configure import conf
from utils import check_include, check_lib


def options(opt):
    # Options
    opt.add_option("--suitesparse-path", type="string",
                   help="path to suitesparse", dest="suitesparse_path")


@conf
def check_suitesparse(ctx):
    # Set the search path
    if ctx.options.suitesparse_path is None:
        path_check = ["/usr/local", "/usr"]
    else:
        path_check = [ctx.options.suitesparse_path]

    # SUITESPARSE includes
    check_include(ctx, "SUITESPARSE", ["suitesparse"], ["SuiteSparseQR.hpp"], path_check)

    # SUITESPARSE libs
    check_lib(ctx, "SUITESPARSE", [""], ["libklu", "libbtf", "libumfpack", "libcholmod", "libcolamd", "libamd", "libcamd", "libccolamd", "libsuitesparseconfig"], path_check)

    if ctx.env.LIB_SUITESPARSE:
        ctx.get_env()["libs"] = ctx.get_env()["libs"] + ["SUITESPARSE"]


def configure(cfg):
    if not cfg.env.LIB_SUITESPARSE:
        cfg.check_suitesparse()
