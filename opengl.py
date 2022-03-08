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
    # Options
    opt.add_option(
        "--opengl-path", type="string", help="path to opengl", dest="opengl_path"
    )


@conf
def check_opengl(ctx):
    # Set the search path
    if ctx.options.opengl_path is None:
        path_check = ["/usr/local", "/usr"]
    else:
        path_check = [ctx.options.opengl_path]

    if ctx.env["DEST_OS"] == "darwin":
        # OpenGL frameworks
        ctx.get_env()["FRAMEWORK_OPENGL"] = ["Foundation", "OpenGL"]
    else:
        # OpenGL includes
        check_include(ctx, "OPENGL", ["GL"], ["gl.h"], path_check)

        # OpenGL libs
        check_lib(ctx, "OPENGL", "", ["libGL"], path_check)

    if ctx.env.LIB_OPENGL or ctx.env.FRAMEWORK_OPENGL:
        ctx.get_env()["libs"] = ctx.get_env()["libs"] + ["OPENGL"]


def configure(cfg):
    if not cfg.env.LIB_OPENGL:
        cfg.check_opengl()
