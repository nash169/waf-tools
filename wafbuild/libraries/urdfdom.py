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


def options(opt):
    # Select installation path
    opt.add_option(
        "--urdfdom-path", type="string", help="path to urdfdom", dest="urdfdom_path"
    )

    # Headers
    opt.add_option(
        "--urdfdom-headers", action="store_true", help="search for urdfdom headers", dest="urdfdom_headers"
    )


@conf
def check_urdfdom(ctx):
    # Set the search path
    if ctx.options.urdfdom_path is None:
        path_check = ["/usr/local", "/usr", "/opt"]
    else:
        path_check = [ctx.options.urdfdom_path]

    # URDFDOM includes
    check_include(ctx, "URDFDOM", [""], [
                  "urdf_parser/urdf_parser.h"], path_check)

    # URDFDOM additional headers
    if ctx.options.urdfdom_headers:
        check_include(ctx, "URDFDOM", [""],
                      [
            "urdf_exception/exception.h",
            "urdf_model/model.h",
            "urdf_model_state/model_state.h",
            "urdf_sensor/sensor.h",
            "urdf_world/world.h",
        ],
            path_check)

    # URDFDOM lib
    check_lib(ctx, "URDFDOM", [""],
              [
        "liburdfdom_model",
        "liburdfdom_model_state",
        "liburdfdom_sensor",
        "liburdfdom_world",
    ],
        path_check)

    # If URDFDOM headers found
    if ctx.env.INCLUDES_URDFDOM:
        # Add URDFDOM label to the list of libraries
        ctx.get_env()["libs"] += ["URDFDOM"]


def configure(cfg):
    if not cfg.env.INCLUDES_URDFDOM:
        cfg.check_urdfdom()
