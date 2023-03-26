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

# For clarification about LAPACK/BLAS implementations check:
# https://wiki.debian.org/DebianScience/LinearAlgebraLibraries


def options(opt):
    opt.add_option(
        "--openblas-path", type="string", help="path to OpenBLAS", dest="openblas_path"
    )

    # 64-bit indexing
    opt.add_option(
        "--openblas-64", action="store_true", help="enable 64-bit indexing", dest="openblas_64"
    )

    # blas
    opt.add_option(
        "--openblas-blas", action="store", help="enable openblas blas", dest="openblas_noblas", default=True
    )

    # lapack
    opt.add_option(
        "--openblas-lapack", action="store", help="enable openblas lapack", dest="openblas_lapack", default=False
    )

    # C lapack
    opt.add_option(
        "--openblas-lapacke", action="store", help="enable openblas C lapack", dest="openblas_lapacke", default=False
    )


@conf
def check_openblas(ctx):
    # Set the search path
    if ctx.options.openblas_path is None:
        path_check = ["/usr/local", "/usr", "/opt"]
    else:
        path_check = [ctx.options.openblas_path]

    # BLAS
    lib_check = []
    if ctx.options.openblas_blas:
        lib_check += ["libopenblas64" if ctx.options.openblas_64 else "libopenblas"]
    # LAPACK
    if ctx.options.openblas_lapack:
        lib_check += ["liblapack64" if ctx.options.openblas_64 else "liblapack"]
    # C LAPACK
    if ctx.options.openblas_lapacke:
        lib_check += ["liblapacke64" if ctx.options.openblas_64 else "liblapacke"]

    check_lib(ctx, "OPENBLAS", "", lib_check, path_check)

    if ctx.env.LIB_OPENBLAS:
        ctx.get_env()["libs"] += ["OPENBLAS"]

        if ctx.options.openblas_blas and "BLAS" in ctx.get_env()["libs"]:
            ctx.get_env()["libs"].remove("BLAS")

        # Remove system LAPACK if use the OpenBLAS LAPACK
        if ctx.options.openblas_lapack and "LAPACK" in ctx.get_env()["libs"]:
            ctx.get_env()["libs"].remove("LAPACK")


def configure(cfg):
    if not cfg.env.LIB_OPENBLAS:
        cfg.check_openblas()
