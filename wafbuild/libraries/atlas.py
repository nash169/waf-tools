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

# ATLAS implementation of BLAS provides optimized subset of LAPACK

# For clarification about LAPACK/BLAS implementations check:
# https://wiki.debian.org/DebianScience/LinearAlgebraLibraries


def options(opt):
    opt.add_option(
        "--atlas-path", type="string", help="path to ATLAS", dest="atlas_path"
    )

    # Activate BLAS
    opt.add_option(
        "--atlas-blas", action="store", help="Activates only BLAS subset", dest="atlas_blas", default=True
    )

    # Activate LAPACK
    opt.add_option(
        "--atlas-lapack", action="store", help="Activates only LAPACK subset", dest="atlas_lapack", default=False
    )

    # Activate C LAPACK
    opt.add_option(
        "--atlas-lapacke", action="store", help="Activates only C LAPACK subset", dest="atlas_lapacke", default=False
    )


@conf
def check_atlas(ctx):
    # Set the search path
    if ctx.options.atlas_path is None:
        path_check = ["/usr/local", "/usr", "/opt"]
    else:
        path_check = [ctx.options.atlas_path]

    # # HEADER Check
    # check_include(ctx, "ATLAS", ["atlas"], [
    #               "atlas_buildinfo.h", "clapack.h"], path_check)

    # LIB Check
    lib_check = []
    if ctx.options.atlas_blas:
        lib_check += ["libblas"]  # libatlas

    if ctx.options.atlas_lapack:
        lib_check += ["liblapack"]

    if ctx.options.atlas_lapacke:
        lib_check += ["liblapacke"]

    check_lib(ctx, "ATLAS", "", lib_check, path_check)

    if ctx.env.LIB_ATLAS:
        ctx.get_env()["libs"] += ["ATLAS"]

        if ctx.options.atlas_blas and "BLAS" in ctx.get_env()["libs"]:
            ctx.get_env()["libs"].remove("BLAS")
            ctx.get_env()["requires"].remove("BLAS")

        if ctx.options.atlas_lapack and "LAPACK" in ctx.get_env()["libs"]:
            ctx.get_env()["libs"].remove("LAPACK")
            ctx.get_env()["requires"].remove("LAPACK")


def configure(cfg):
    if not cfg.env.LIB_ATLAS:
        cfg.check_atlas()
