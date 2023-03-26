#!/usr/bin/env python
# encoding: utf-8
#
#    This file is part of waf-tools.
#
#    Copyright (c) 2020, 2021, 2022 Bernardo Fichera <bernardo.fichera@gmail.com>
#
#    Permission is hereby granted, free of charge, to any person obtaining a copy
#    of this software and associated documentation files (the "Software"), to deal
#    in the Software without restriction, including without limitation the rights
#    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#    copies of the Software, and to permit persons to whom the Software is
#    furnished to do so, subject to the following conditions:
#
#    The above copyright notice and this permission notice shall be included in all
#    copies or substantial portions of the Software.
#
#    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#    SOFTWARE.

# Tips for configuring SLEPc
# ./configure --with-debugging=0
#             --with-scalar-type=complex/real
#             --with-PACKAGENAME-dir=PATH

import os
import os.path as osp
from waflib.Configure import conf
from wafbuild.utils import dir


def options(opt):
    opt.add_option(
        "--slepc-path", type="string", help="path to OpenBLAS", dest="slepc_path"
    )

    opt.load("petsc", tooldir=osp.join(dir, 'libraries'))


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
    ctx.env.INCLUDES_SLEPC = ctx.env.INCLUDES_SLEPC[:-1]

    if ctx.env.HAVE_SLEPC and "SLEPC" not in ctx.get_env()["libs"]:
        # Check for PETSc
        if "PETSC" not in ctx.get_env()["libs"]:
            ctx.load("petsc", tooldir=osp.join(dir, 'libraries'))

        ctx.get_env()["libs"] += ["SLEPC"]


def configure(cfg):
    if not cfg.env.LIB_SLEPC:
        cfg.check_slepc()
