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
from wafbuild.utils import check_lib

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


@conf
def check_blas(ctx):
    # Set the search path
    if ctx.options.blas_path is None:
        path_check = ["/usr/local", "/usr", "/opt"]
    else:
        path_check = [ctx.options.blas_path]

    # Accelerate framework for macOS
    if ctx.env["DEST_OS"] == "darwin":
        ctx.env.LIB_BLAS = ["blas64" if ctx.options.blas_64 else "blas"]
        ctx.get_env()["FRAMEWORK_BLAS"] = ["Accelerate"]
    else:
        check_lib(ctx, "BLAS", "", [
                  "libblas64" if ctx.options.blas_64 else "libblas"], path_check)

    if ctx.env.LIB_BLAS:
        ctx.get_env()["libs"] += ["BLAS"]


def configure(cfg):
    if not cfg.env.LIB_BLAS:
        cfg.check_blas()
