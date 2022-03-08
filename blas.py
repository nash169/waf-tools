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
from utils import check_lib

# Reference BLAS implementation

# For clarification about LAPACK/BLAS implementations check:
# https://wiki.debian.org/DebianScience/LinearAlgebraLibraries


def options(opt):
    opt.add_option(
        "--blas-path", type="string", help="path to BLAS", dest="blas_path"
    )
    # 64-bit indexing
    opt.add_option(
        "--blas-64", action="store_true", help="enable 64-bit indexing", dest="blas_64"
    )
    # no search (assuming system blas is present)
    opt.add_option(
        "--blas-system", action="store_true", default=False, help="using system blas", dest="blas_system"
    )


@conf
def check_blas(ctx):
    # Set the search path
    if ctx.options.blas_path is None:
        path_check = ["/usr/local", "/usr", "/opt"]
    else:
        path_check = [ctx.options.blas_path]

    if ctx.options.blas_system:
        if ctx.options.blas_64:
            ctx.env.LIB_BLAS = ["blas64"]
        else:
            ctx.env.LIB_BLAS = ["blas"]

        # Accelerate framework for macOS
        if ctx.env["DEST_OS"] == "darwin":
            ctx.get_env()["FRAMEWORK_BLAS"] = ["Accelerate"]
    else:
        # LIB Check
        if ctx.options.blas_64:
            check_lib(ctx, "BLAS", "", ["libblas64"], path_check)
        else:
            check_lib(ctx, "BLAS", "", ["libblas"], path_check)

    if ctx.env.LIB_BLAS:
        ctx.get_env()["libs"] = ctx.get_env()["libs"] + ["BLAS"]


def configure(cfg):
    if not cfg.env.LIB_BLAS:
        cfg.check_blas()
