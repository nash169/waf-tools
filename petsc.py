#! /usr/bin/env python
# encoding: utf-8

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
