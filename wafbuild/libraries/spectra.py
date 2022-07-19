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
from wafbuild.utils import check_include, dir


def options(opt):
    # Select installation path
    opt.add_option(
        "--spectra-path", type="string", help="path to spectra", dest="spectra_path"
    )

    # Load options
    opt.load("eigen", tooldir=osp.join(dir, 'compilers'))


@conf
def check_spectra(ctx):
    # Set the search path
    if ctx.options.spectra_path is None:
        path_check = ["/usr/local", "/usr", "/opt"]
    else:
        path_check = [ctx.options.spectra_path]

    # SPECTRA includes
    check_include(ctx, "SPECTRA", ["Spectra"], [
                  "SymEigsSolver.h"], path_check)

    # If SPECTRA headers found
    if ctx.env.INCLUDES_SPECTRA:
        if "EIGEN" not in ctx.get_env()["libs"]:
            ctx.load("eigen", tooldir=osp.join(dir, 'compilers'))

        # Add SPECTRA label to the list of libraries
        ctx.get_env()["libs"] += ["SPECTRA"]


def configure(cfg):
    if not cfg.env.INCLUDES_SPECTRA:
        cfg.check_spectra()
