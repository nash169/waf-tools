#! /usr/bin/env python
# encoding: utf-8

from waflib.Configure import conf


def options(opt):
    opt.add_option(
        "--mpi-path", type="string", help="path to OpenMPI", dest="mpi_path"
    )


@conf
def check_mpi(ctx):
    # Set the search path
    if ctx.options.petsc_path is None:
        path_check = ""
    else:
        path_check = ctx.options.petsc_path

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
