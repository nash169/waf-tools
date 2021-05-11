#! /usr/bin/env python
# encoding: utf-8

from waflib.Configure import conf
from utils import check_include, check_lib


def options(opt):
    opt.add_option(
        "--openmpi-path", type="string", help="path to OpenBLAS", dest="openmpi_path"
    )
    # 64-bit indexing
    opt.add_option(
        "--openmpi-64", action="store_true", help="enable 64-bit indexing", dest="openmpi_64"
    )


@conf
def check_openmpi(ctx):
    # Set the search path
    if ctx.options.openmpi_path is None:
        path_check = ["/usr/local", "/usr", "/opt"]
    else:
        path_check = [ctx.options.openmpi_path]

    # Header check
    check_include(ctx, "OPENMPI", ["openmpi"], ["mpi.h"], path_check)

    # LIB Check
    check_lib(ctx, "OPENMPI", ["openmpi"], ["libmpi"], path_check)


def configure(cfg):
    if not cfg.env.LIB_OPENMPI:
        cfg.check_openmpi()
