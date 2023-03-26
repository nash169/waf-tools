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
        "--utilslib-path", type="string", help="path to utilslib-lib", dest="utilslib_path",
    )

    # Required package options
    opt.load("eigen corrade", tooldir=osp.join(dir, 'libraries'))


@conf
def check_utilslib(ctx):
    # Set the search path
    if ctx.options.utilslib_path is None:
        path_check = ["/usr/local", "/usr"]
    else:
        path_check = [ctx.options.utilslib_path]

    # utilslib-lib includes
    check_include(ctx, "UTILSLIB", [""], [
                  "utils_lib/FileManager.hpp"], path_check)

    # utilslib-lib libs
    check_lib(ctx, "UTILSLIB", "", ["libUtils"], path_check)

    if ctx.env.LIB_UTILSLIB or ctx.env.STLIB_UTILSLIB:
        # Add dependencies to require libraries
        if "EIGEN" not in ctx.get_env()["libs"]:
            ctx.get_env()["requires"] += ["EIGEN"]
            ctx.load("eigen", tooldir="waf_tools")

        if "CORRADE" not in ctx.get_env()["libs"]:
            ctx.get_env()["requires"] += ["CORRADE"]
            ctx.load("corrade", tooldir="waf_tools")

        # Add library
        ctx.get_env()["libs"] += ["UTILSLIB"]


def configure(cfg):
    if not cfg.env.LIB_UTILSLIB and not cfg.env.STLIB_UTILSLIB:
        cfg.check_utilslib()
