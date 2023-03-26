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

from traceback import print_tb
from waflib.Configure import conf


def options(opt):
    opt.add_option(
        "--mpi-path", type="string", help="path to OpenMPI", dest="mpi_path"
    )


@conf
def check_mpi(ctx):
    # Set the search path
    if ctx.options.mpi_path is None:
        path_check = ""
    else:
        path_check = ctx.options.mpi_path

    try:
        # Check for OpenMPI
        ctx.check_cfg(package='MPI', path='mpicc' if ctx.env.CC else 'mpicxx',
                      pkg_config_path=path_check, args='--showme', uselib_store='MPI')
    except:
        # Check for MPICH
        ctx.check_cfg(package='MPI', path='mpicc' if ctx.env.CC else 'mpicxx',
                      pkg_config_path=path_check, args='--compile_info', uselib_store='MPI')

    if ctx.env.HAVE_MPI and "MPI" not in ctx.get_env()["libs"]:
        ctx.get_env()["libs"] += ["MPI"]


def configure(cfg):
    if not cfg.env.LIB_MPI:
        cfg.check_mpi()
