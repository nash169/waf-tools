#! /usr/bin/env python
# encoding: utf-8

from email.policy import default
from waflib.Configure import conf
from utils import check_include, check_lib


def options(opt):
    opt.add_option(
        "--python-path", type="string", help="path to PYTHON", dest="python_path"
    )
    opt.add_option(
        "--python-version", type="string", default="3.8", help="version of PYTHON", dest="python_version"
    )


@conf
def check_python(ctx):
    # Set the search path
    if ctx.options.python_path is None:
        path_check = ["/usr/local", "/usr", "/opt"]
    else:
        path_check = [ctx.options.python_path]

    # Header check
    check_include(ctx, "PYTHON", [
                  "python" + ctx.options.python_version], ["Python.h"], path_check)

    # Library Check
    check_lib(ctx, "PYTHON", "", ["libpython" +
                                  ctx.options.python_version], path_check)

    if ctx.env.LIB_PYTHON:
        ctx.get_env()["libs"] += ["PYTHON"]


def configure(cfg):
    if not cfg.env.LIB_PYTHON:
        cfg.check_python()
