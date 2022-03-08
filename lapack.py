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

# Reference LAPACK implementation

# For clarification about LAPACK/BLAS implementations check:
# https://wiki.debian.org/DebianScience/LinearAlgebraLibraries


def options(opt):
    opt.add_option(
        "--lapack-path", type="string", help="path to LAPACK", dest="lapack_path"
    )
    # C lib LAPACK version
    opt.add_option(
        "--lapack-clib", action="store_true", help="load C lib version LAPACK", dest="lapack_clib"
    )
    # 64-bit indexing
    opt.add_option(
        "--lapack-64", action="store_true", help="enable 64-bit indexing", dest="lapack_64"
    )
    # no search (assuming system blas is present)
    opt.add_option(
        "--lapack-system", action="store_true", default=False, help="using system lapack", dest="lapack_system"
    )


@conf
def check_lapack(ctx):
    # Set the search path
    if ctx.options.lapack_path is None:
        path_check = ["/usr/local", "/usr", "/opt"]
    else:
        path_check = [ctx.options.lapack_path]

    if ctx.options.lapack_system:
        if ctx.options.lapack_64:
            ctx.env.LIB_LAPACK = ["lapack64"]
            if ctx.options.lapack_clib:
                ctx.env.LIB_LAPACK += ["lapacke64"]
        else:
            ctx.env.LIB_LAPACK = ["lapack"]
            if ctx.options.lapack_clib:
                ctx.env.LIB_LAPACK += ["lapacke"]
    else:
        if ctx.options.lapack_64:
            lib_to_check = ["liblapack64"]
            if ctx.options.lapack_clib:
                lib_to_check += ["liblapacke64"]
        else:
            lib_to_check = ["liblapack"]
            if ctx.options.lapack_clib:
                lib_to_check += ["liblapacke"]

        # Check LAPACK libs
        check_lib(ctx, "LAPACK", "", lib_to_check, path_check)

    # Add LAPACK
    if ctx.env.LIB_LAPACK:
        ctx.get_env()["libs"] += ["LAPACK"]


def configure(cfg):
    if not cfg.env.LIB_LAPACK:
        cfg.check_lapack()
