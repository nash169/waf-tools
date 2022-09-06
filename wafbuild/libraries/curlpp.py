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
        "--curlpp-path", type="string", help="path to curlpp", dest="curlpp_path"
    )


@conf
def check_curlpp(ctx):
    # Set the search path
    if ctx.options.curlpp_path is None:
        path_check = ["/usr/local", "/usr", "/opt"]
    else:
        path_check = [ctx.options.curlpp_path]

    # CURL and CURLPP includes
    check_include(ctx, "CURLPP", [""], [
                  "curl/curl.h", "curlpp/cURLpp.hpp"], path_check)

    # CURL and CURLPP lib
    check_lib(ctx, "CURLPP", [""], ["libcurl", "libcurlpp"], path_check)

    # If CURLPP headers found
    if ctx.env.INCLUDES_CURLPP:
        # Add CURLPP label to the list of libraries
        ctx.get_env()["libs"] += ["CURLPP"]


def configure(cfg):
    if not cfg.env.INCLUDES_CURLPP:
        cfg.check_curlpp()
