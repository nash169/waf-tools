#! /usr/bin/env python
# encoding: utf-8

from waflib.Configure import conf

OPENMP_CODE = """
#include <omp.h>
int main () { return omp_get_num_threads (); }
"""


@conf
def check_openmp(ctx):
    """
    Detects openmp flags and sets the OPENMP ``FCFLAGS``/``LINKFLAGS``
    """
    for x in ("-fopenmp", "-openmp", "-mp", "-xopenmp", "-omp", "-qsmp=omp"):
        try:
            ctx.check(
                msg="Checking for OpenMP flag %s" % x,
                fragment=OPENMP_CODE,
                linkflags=x,
                uselib_store="OPENMP",
            )
            ctx.env["CXXFLAGS"] = ctx.env["CXXFLAGS"] + ctx.env.LINKFLAGS_OPENMP
        except ctx.errors.ConfigurationError:
            pass
        else:
            break
    else:
        ctx.fatal("Could not find OpenMP")


def configure(cfg):
    if not cfg.env.LINKFLAGS_OPENMP:
        cfg.check_openmp()
