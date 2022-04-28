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

from email.policy import default
from waflib.Configure import conf
from utils import check_lib

# Reference LAPACK implementation

# For clarification about LAPACK/BLAS implementations check:
# https://wiki.debian.org/DebianScience/LinearAlgebraLibraries


def options(opt):
    opt.add_option(
        "--lapack-path", type="string", help="path to LAPACK", dest="lapack_path"
    )

    # 64-bit indexing
    opt.add_option(
        "--lapack-64", action="store_true", help="enable 64-bit indexing", dest="lapack_64"
    )

    # C++ LAPACK
    opt.add_option(
        "--lapack-fortran", action="store", help="load C lib version LAPACK", dest="lapack_fortran", default=True
    )

    # C LAPACK
    opt.add_option(
        "--lapack-c", action="store", help="load C lib version LAPACK", dest="lapack_c", default=False
    )


@conf
def check_lapack(ctx):
    # Set the search path
    if ctx.options.lapack_path is None:
        path_check = ["/usr/local", "/usr", "/opt"]
    else:
        path_check = [ctx.options.lapack_path]

    if ctx.env["DEST_OS"] == "darwin" and ctx.options.lapack_path is None:
        if ctx.options.lapack_fortran:
            ctx.env.LIB_LAPACK = [
                "lapack64" if ctx.options.lapack_64 else "lapack"]
        if ctx.options.lapack_c:
            ctx.env.LIB_LAPACK += ["lapacke64" if ctx.options.lapack_64 else "lapacke"]
    else:
        lib_check = []
        if ctx.options.lapack_fortran:
            lib_check += [
                "liblapack64" if ctx.options.lapack_64 else "liblapack"]
        if ctx.options.lapack_c:
            lib_check += ["liblapacke64" if ctx.options.lapack_64 else "liblapacke"]
        # Check LAPACK libs
        check_lib(ctx, "LAPACK", "", lib_check, path_check)

    # Add LAPACK
    if ctx.env.LIB_LAPACK:
        ctx.get_env()["libs"] += ["LAPACK"]


def configure(cfg):
    if not cfg.env.LIB_LAPACK:
        cfg.check_lapack()
