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

from waflib.Configure import conf
from wafbuild.utils import check_include, check_lib


def options(opt):
    # Options
    opt.add_option("--superlu-path", type="string",
                   help="path to superlu", dest="superlu_path")

    # Distributed SUPERLU
    opt.add_option(
        "--superlu-dist", action="store_true", help="distributed version SUPERLU", dest="superlu_dist"
    )


@conf
def check_superlu(ctx):
    # Set the search path
    if ctx.options.superlu_path is None:
        path_check = ["/usr/local", "/usr"]
    else:
        path_check = [ctx.options.superlu_path]

    if ctx.options.superlu_dist:
        # SUPERLU includes
        check_include(ctx, "SUPERLU", ["superlu-dist"],
                      ["superlu_defs.h"], path_check)
        # SUPERLU libs
        check_lib(ctx, "SUPERLU", [""], ["libsuperlu_dist"], path_check)
    else:
        # SUPERLU includes
        check_include(ctx, "SUPERLU", ["superlu"], [
                      "supermatrix.h"], path_check)
        # SUPERLU libs
        check_lib(ctx, "SUPERLU", [""], ["libsuperlu"], path_check)

    if ctx.env.LIB_SUPERLU:
        ctx.get_env()["libs"] = ctx.get_env()["libs"] + ["SUPERLU"]


def configure(cfg):
    if not cfg.env.LIB_SUPERLU:
        cfg.check_superlu()
