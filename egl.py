#! /usr/bin/env python
# encoding: utf-8

from waflib.Configure import conf
from utils import check_include, check_lib


def options(opt):
    # Options
    opt.add_option("--egl-path", type="string", help="path to egl", dest="egl_path")


@conf
def check_egl(ctx):
    # Set the search path
    if ctx.options.egl_path is None:
        path_check = ["/usr/local", "/usr"]
    else:
        path_check = [ctx.options.egl_path]

    # EGL includes
    check_include(ctx, "EGL", ["EGL"], ["egl.h"], path_check)

    # EGL libs
    check_lib(ctx, "EGL", "", ["libEGL"], path_check)

    if ctx.env.LIB_EGL:
        ctx.get_env()["libs"] = ctx.get_env()["libs"] + ["EGL"]


def configure(cfg):
    if not cfg.env.LIB_EGL:
        cfg.check_egl()
