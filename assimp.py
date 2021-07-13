#! /usr/bin/env python
# encoding: utf-8

from waflib.Configure import conf
from utils import check_include, check_lib


def options(opt):
    # Select installation path
    opt.add_option(
        "--assimp-path", type="string", help="path to assimp", dest="assimp_path"
    )


@conf
def check_assimp(ctx):
    # Set the search path
    if ctx.options.assimp_path is None:
        path_check = ["/usr/local", "/usr", "/opt"]
    else:
        path_check = [ctx.options.assimp_path]

    # ASSIMP includes
    check_include(ctx, "ASSIMP", [""], ["assimp/BaseImporter.h"], path_check)

    # ASSIMP lib
    check_lib(ctx, "ASSIMP", [""], ["libassimp"], path_check)

    # If ASSIMP headers found
    if ctx.env.INCLUDES_ASSIMP:
        # Add ASSIMP label to the list of libraries
        ctx.get_env()["libs"] += ["ASSIMP"]


def configure(cfg):
    if not cfg.env.INCLUDES_ASSIMP:
        cfg.check_assimp()
