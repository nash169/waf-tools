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

# For clarification about ARPACK/BLAS implementations check:
# https://wiki.debian.org/DebianScience/LinearAlgebraLibraries


def options(opt):
    opt.add_option(
        "--arpack-path", type="string", help="path to ARPACK", dest="arpack_path"
    )
    # Parallel ARPACK
    opt.add_option(
        "--arpack-parallel", action="store_true", help="parallel version ARPACK", dest="arpack_parallel"
    )


@conf
def check_arpack(ctx):
    # Set the search path
    if ctx.options.arpack_path is None:
        path_check = ["/usr/local", "/usr", "/opt"]
    else:
        path_check = [ctx.options.arpack_path]

    lib_to_check = ["libarpack"]
    if ctx.options.arpack_parallel:
        lib_to_check += ["libparpack"]

    # Check ARPACK libs
    check_lib(ctx, "ARPACK", "", lib_to_check, path_check)

    # Add ARPACK
    if ctx.env.LIB_ARPACK:
        ctx.get_env()["libs"] += ["ARPACK"]


def configure(cfg):
    if not cfg.env.LIB_ARPACK:
        cfg.check_arpack()
