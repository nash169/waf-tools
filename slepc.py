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
    if ctx.options.slepc_path is not None:
        os.environ['PKG_CONFIG_PATH'] = os.path.join(
            ctx.options.slepc_path, "lib/pkgconfig")
        if ctx.options.petsc_path is not None:
            os.environ['PKG_CONFIG_PATH'] += ":" + \
                os.path.join(ctx.options.petsc_path, "lib/pkgconfig")

    ctx.check_cfg(package='SLEPc', args=[
                  '--cflags', '--libs'], uselib_store='SLEPC')

    # Remove automatic PETSc detection
    ctx.env.LIB_SLEPC = ctx.env.LIB_SLEPC[:-1]
    ctx.env.LIBPATH_SLEPC = ctx.env.LIBPATH_SLEPC[:-1]
    ctx.env.INCLUDES_SLEPC = ctx.env.INCLUDES_SLEPC[:-2]

    if ctx.env.HAVE_SLEPC and "SLEPC" not in ctx.get_env()["libs"]:
        # Check for PETSc
        if "PETSC" not in ctx.get_env()["libs"]:
            ctx.load("petsc", tooldir="waf_tools")

        ctx.get_env()["libs"] += ["SLEPC"]


def configure(cfg):
    if not cfg.env.LIB_SLEPC:
        cfg.check_slepc()
