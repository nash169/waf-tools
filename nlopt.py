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
from utils import check_include, check_lib


def options(opt):
    opt.add_option(
        "--nlopt-path", type="string", help="path to NLOPT", dest="nlopt_path"
    )


@conf
def check_nlopt(ctx):
    # Set the search path
    if ctx.options.nlopt_path is None:
        path_check = ["/usr/local", "/usr", "/opt"]
    else:
        path_check = [ctx.options.nlopt_path]

    # Header check
    check_include(ctx, "NLOPT", "", ["nlopt.hpp"], path_check)

    # Library Check
    check_lib(ctx, "NLOPT", "", ["libnlopt"], path_check)
    # check_lib(ctx, "NLOPT", "", ["libnlopt_cxx"], path_check)

    if ctx.env.LIB_NLOPT:
        ctx.get_env()["libs"] += ["NLOPT"]


def configure(cfg):
    if not cfg.env.LIB_NLOPT:
        cfg.check_nlopt()
