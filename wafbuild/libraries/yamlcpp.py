#!/usr/bin/env python
# encoding: utf-8
#
#    This file is part of utils-lib.
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
    # Options
    opt.add_option(
        "--yamlcpp-path", type="string", help="path to yamlcpp-lib", dest="yamlcpp_path",
    )


@conf
def check_yamlcpp(ctx):
    # Set the search path
    if ctx.options.yamlcpp_path is None:
        path_check = ["/usr/local", "/usr"]
    else:
        path_check = [ctx.options.yamlcpp_path]

    # yamlcpp-lib includes
    check_include(ctx, "YAMLCPP", [""], ["yaml-cpp/yaml.h"], path_check)

    # yamlcpp-lib libs
    check_lib(ctx, "YAMLCPP", "", ["libyaml-cpp"], path_check)

    if ctx.env.LIB_YAMLCPP or ctx.env.STLIB_YAMLCPP:
        # Add library
        ctx.get_env()["libs"] += ["YAMLCPP"]


def configure(cfg):
    if not cfg.env.LIB_YAMLCPP and not cfg.env.STLIB_YAMLCPP:
        cfg.check_yamlcpp()
