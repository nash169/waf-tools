#!/usr/bin/env python
# encoding: utf-8
#
#    This file is part of utils-lib.
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

import os.path as osp
from waflib.Configure import conf
from wafbuild.utils import check_include, check_lib, dir


def options(opt):
    # Options
    opt.add_option(
        "--optimizationlib-path", type="string", help="path to optimizationlib-lib", dest="optimizationlib_path",
    )

    # Required package options
    opt.load("eigen nlopt ipopt qpoases", tooldir=osp.join(dir, 'libraries'))


@conf
def check_optimizationlib(ctx):
    # Set the search path
    if ctx.options.optimizationlib_path is None:
        path_check = ["/usr/local", "/usr"]
    else:
        path_check = [ctx.options.optimizationlib_path]

    # optimization-lib includes
    check_include(ctx, "OPTIMIZATIONLIB", [""], [
                  "optimization_lib/AbstractOptimizer.hpp"], path_check)

    # optimization-lib libs
    check_lib(ctx, "OPTIMIZATIONLIB", "", ["libOptimization"], path_check)

    if ctx.env.LIB_OPTIMIZATIONLIB or ctx.env.STLIB_OPTIMIZATIONLIB:
        # Add dependencies to require libraries
        if "EIGEN" not in ctx.get_env()["libs"]:
            ctx.env.REQUIRED += ["EIGEN"]
            ctx.load("eigen", tooldir=osp.join(dir, 'libraries'))

        if "NLOPT" not in ctx.get_env()["libs"]:
            ctx.load("nlopt", tooldir=osp.join(dir, 'libraries'))

        if "IPOPT" not in ctx.get_env()["libs"]:
            ctx.load("ipopt", tooldir=osp.join(dir, 'libraries'))

        if "QPOASES" not in ctx.get_env()["libs"]:
            ctx.load("qpoases", tooldir=osp.join(dir, 'libraries'))

        # Add library
        ctx.get_env()["libs"] += ["OPTIMIZATIONLIB"]


def configure(cfg):
    if not cfg.env.LIB_OPTIMIZATIONLIB and not cfg.env.STLIB_OPTIMIZATIONLIB:
        cfg.check_optimizationlib()
