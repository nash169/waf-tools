#! /usr/bin/env python
# encoding: utf-8

# Tips for configuring SLEPc
# ./configure --with-debugging=0
#             --with-scalar-type=complex/real
#             --with-PACKAGENAME-dir=PATH

import os
from waflib.Configure import conf


def options(opt):
    opt.add_option(
        "--slepc-path", type="string", help="path to OpenBLAS", dest="slepc_path"
    )

    opt.load("petsc", tooldir="waf_tools")


@conf
def check_slepc(ctx):
    # Set the search path
    if ctx.options.slepc_path is None:
        path_check = ""
    else:
        path_check = os.path.join(ctx.options.slepc_path, "lib/pkgconfig")

    ctx.check_cfg(package='SLEPc', pkg_config_path=path_check,
                  args='--cflags --libs', uselib_store='SLEPC')

    if ctx.env.HAVE_SLEPC and "SLEPC" not in ctx.get_env()["libs"]:
        # Check for PETSc
        if "PETSC" not in ctx.get_env()["libs"]:
            ctx.load("petsc", tooldir="waf_tools")
            
        ctx.get_env()["libs"] += ["SLEPC"]


def configure(cfg):
    if not cfg.env.LIB_SLEPC:
        cfg.check_slepc()
