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
        "--bullet-path", type="string", help="path to bullet", dest="bullet_path"
    )

    opt.add_option(
        "--bullet-components",
        type="string",
        help="Bullet components",
        dest="bullet_components",
    )


@conf
def check_bullet(ctx):
    # Set the search path
    if ctx.options.bullet_path is None:
        path_check = ["/usr/local", "/usr"]
    else:
        path_check = [ctx.options.bullet_path]

    # bullet-lib includes
    check_include(ctx, "BULLET", ["bullet"], [
                  "btBulletDynamicsCommon.h"], path_check)

    # bullet-lib libs
    components = ["LinearMath", "Bullet3Common", "BulletInverseDynamics",
                  "BulletCollision", "BulletDynamics", "BulletSoftBody",
                  "OpenGLWindow", "BulletXmlWorldImporter", "BulletWorldImporter",
                  "BulletRobotics", "BulletFileLoader", "BulletExampleBrowserLib"]

    # Components to check
    if ctx.options.bullet_components is None:
        components_to_check = []
    else:
        components_to_check = list(ctx.options.bullet_components.split(","))

    for i, component in enumerate(components_to_check):
        components_to_check[i] = "lib" + component

    check_lib(ctx, "BULLET", "", components_to_check, path_check)

    if ctx.env.LIB_BULLET or ctx.env.STLIB_BULLET:
        # Add library
        ctx.get_env()["libs"] += ["BULLET"]


def configure(cfg):
    if not cfg.env.LIB_BULLET and not cfg.env.STLIB_BULLET:
        cfg.check_bullet()
