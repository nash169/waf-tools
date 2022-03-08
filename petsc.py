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

# Tips for configuring PETSc
# ./configure --with-cc=mpicc --with-cxx=mpicxx --with-fc=mpif90 \
#             --with-debugging=0 \
#             COPTFLAGS='-O3 -march=native -mtune=native' CXXOPTFLAGS='-O3 -march=native -mtune=native' FOPTFLAGS='-O3 -march=native -mtune=native' \
#             --with-openmp \
#             --with-scalar-type=complex \
#             --with-PACKAGENAME-dir=PATH

# To control the number of OpenMP threads each MPI process utilizes you can set the environmental variable OMP_NUM_THREADS n
# or the PETSc command line option -omp_num_threads n.

import os
from waflib.Configure import conf


def options(opt):
    opt.add_option(
        "--petsc-path", type="string", help="path to OpenBLAS", dest="petsc_path"
    )

    # Load options
    opt.load("mpi", tooldir="waf_tools")


@conf
def check_petsc(ctx):
    # Set the search path
    if ctx.options.petsc_path is None:
        path_check = ""
    else:
        path_check = os.path.join(ctx.options.petsc_path, "lib/pkgconfig")

    ctx.check_cfg(package='PETSc', pkg_config_path=path_check,
                  args=['--cflags', '--libs'], uselib_store='PETSC')

    compiler = ctx.check_cfg(package='PETSc', pkg_config_path=path_check,
                             args=['--variable=ccompiler'], uselib_store='PETSC')

    if ctx.env.HAVE_PETSC and "PETSC" not in ctx.get_env()["libs"]:
        # Add MPI if PETSc has been compiled with it
        if compiler == "mpicc":
            ctx.load("mpi", tooldir="waf_tools")

        ctx.get_env()["libs"] += ["PETSC"]


def configure(cfg):
    if not cfg.env.LIB_PETSC:
        cfg.check_petsc()
