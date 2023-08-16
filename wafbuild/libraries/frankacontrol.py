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
    opt.load("libfranka", tooldir=osp.join(dir, 'libraries'))

    # Options
    opt.add_option(
        "--frankacontrol-path", type="string", help="path to franka-control", dest="frankacontrol_path"
    )


@conf
def check_frankacontrol(ctx):
    # Set the search path
    if ctx.options.frankacontrol_path is None:
        path_check = ["/usr/local", "/usr"]
    else:
        path_check = [ctx.options.frankacontrol_path]

    # frankacontrol-lib includes
    check_include(
        ctx, "FRANKACONTROL", [], ["franka_control/Franka.hpp"], path_check
    )

    # frankacontrol-lib libs
    check_lib(ctx, "FRANKACONTROL", "", ["libFrankaControl"], path_check)

    if ctx.env.LIB_FRANKACONTROL or ctx.env.STLIB_FRANKACONTROL:
        # Add dependencies to require libraries
        ctx.get_env()["requires"] += ["LIBFRANKA"]

        # Check for dependencies
        ctx.load("libfranka", tooldir=osp.join(dir, 'libraries'))

        # If not in standard path hard compile dynamic linking (this should probably go directly in utils)
        if ctx.options.frankacontrol_path is not None:
            ctx.env.RPATH_FRANKACONTROL += [ctx.env.LIBPATH_FRANKACONTROL[-1]]

        # Add library
        ctx.get_env()["libs"] += ["FRANKACONTROL"]


def configure(cfg):
    if not cfg.env.LIB_FRANKACONTROL:
        cfg.check_frankacontrol()
