#!/usr/bin/env python
# encoding: utf-8
#
#    This file is part of integrator-lib.
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
        "--zmqstream-path", type="string", help="path to zmq-stream", dest="zmqstream_path",
    )

    # Required package options
    opt.load("eigen zmq", tooldir=osp.join(dir, 'libraries'))


@conf
def check_zmqstream(ctx):
    # Set the search path
    if ctx.options.zmqstream_path is None:
        path_check = ["/usr/local", "/usr"]
    else:
        path_check = [ctx.options.zmqstream_path]

    # integrator-lib includes
    check_include(ctx, "ZMQSTREAM", [""], ["zmq_stream/Publisher.hpp"], path_check)

    # integrator-lib libs
    check_lib(ctx, "ZMQSTREAM", "", ["libZMQStream"], path_check)

    if ctx.env.LIB_ZMQSTREAM or ctx.env.STLIB_ZMQSTREAM:
        # Add dependencies to require libraries
        if "EIGEN" not in ctx.get_env()["libs"]:
            ctx.get_env()["requires"] += ["EIGEN"]
            ctx.load("eigen", tooldir=osp.join(dir, 'libraries'))

        if "ZMQ" not in ctx.get_env()["libs"]:
            ctx.get_env()["requires"] += ["ZMQ"]
            ctx.load("zmq", tooldir=osp.join(dir, 'libraries'))

        # Add library
        ctx.get_env()["libs"] += ["ZMQSTREAM"]


def configure(cfg):
    if not cfg.env.LIB_ZMQSTREAM and not cfg.env.STLIB_ZMQSTREAM:
        cfg.check_zmqstream()
