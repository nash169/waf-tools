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

OPENMP_CODE = """
#include <omp.h>
int main() { return omp_get_num_threads(); }
"""


@conf
def check_openmp(ctx):
    """
    Detects openmp flags and sets the OPENMP ``FCFLAGS``/``LINKFLAGS``
    """
    for x in ("-fopenmp", "-openmp", "-mp", "-xopenmp", "-omp", "-qsmp=omp", "-lomp"):
        try:
            ctx.check(
                msg="Checking for OpenMP flag %s" % x,
                fragment=OPENMP_CODE,
                cxxflags=["-Xpreprocessor", "-fopenmp"] if x == "-lomp" else x,
                linkflags=x,
                use="omp",
                uselib_store="OPENMP",
            )
        except ctx.errors.ConfigurationError:
            pass
        else:
            break
    else:
        ctx.fatal("Could not find OpenMP")

    if ctx.env.LINKFLAGS_OPENMP:
        ctx.get_env()["libs"] = ctx.get_env()["libs"] + ["OPENMP"]


def configure(cfg):
    if not cfg.env.LINKFLAGS_OPENMP:
        cfg.check_openmp()
