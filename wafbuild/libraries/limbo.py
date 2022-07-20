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

import os.path as osp
from waflib.Configure import conf
from wafbuild.utils import check_include, check_lib, dir


def options(opt):
    # Required package options
    opt.load("eigen corrade nlopt libcmaes",
             tooldir=osp.join(dir, 'libraries'))

    # Options
    opt.add_option(
        "--limbo-path", type="string", help="path to limbo-lib", dest="limbo_path",
    )

    opt.add_option(
        "--limbo-nlopt", action="store_true", help="NLOPT Optimization support for Limbo", dest="limbo_nlopt"
    )

    opt.add_option(
        "--limbo-cmaes", action="store_true", help="CMAES Optimization support for Limbo", dest="limbo_cmaes"
    )


@conf
def check_limbo(ctx):
    # Set the search path
    if ctx.options.limbo_path is None:
        path_check = ["/usr/local", "/usr"]
    else:
        path_check = [ctx.options.limbo_path]

    # limbo-lib includes (since limbo is not installed we look into dir src for the headers)
    check_include(ctx, "LIMBO", ["src"], ["limbo/limbo.hpp"], path_check)

    # limbo-lib libs (since limbo is not installed we look into dir build for the compiled library)
    check_lib(ctx, "LIMBO", ["build/src"], ["liblimbo"], path_check)

    if ctx.env.LIB_LIMBO or ctx.env.STLIB_LIMBO:
        # Add dependencies
        if "EIGEN" not in ctx.get_env()["requires"]:
            ctx.get_env()["requires"] += ["EIGEN"]

        if "EIGEN" not in ctx.get_env()["libs"]:
            ctx.load("eigen", tooldir=osp.join(dir, 'compilers'))

        if ctx.options.limbo_nlopt:
            if "NLOPT" not in ctx.get_env()["requires"]:
                ctx.get_env()["requires"] += ["NLOPT"]

            if "NLOPT" not in ctx.get_env()["libs"]:
                ctx.load("nlopt", tooldir=osp.join(dir, 'compilers'))

        if ctx.options.limbo_cmaes:
            if "LIBCMAES" not in ctx.get_env()["requires"]:
                ctx.get_env()["requires"] += ["LIBCMAES"]

            if "LIBCMAES" not in ctx.get_env()["libs"]:
                ctx.load("libcmaes", tooldir=osp.join(dir, 'compilers'))

        # Add library
        ctx.get_env()["libs"] += ["LIMBO"]


def configure(cfg):
    if not cfg.env.LIB_LIMBO and not cfg.env.STLIB_LIMBO:
        cfg.check_limbo()
