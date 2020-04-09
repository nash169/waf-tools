#! /usr/bin/env python
# encoding: utf-8

from waflib.Configure import conf
from utils import check_include, check_lib


def options(opt):
    # Options
    opt.add_option(
        "--opengl-path", type="string", help="path to opengl", dest="opengl_path"
    )


@conf
def check_opengl(ctx):
    # Set the search path
    if ctx.options.opengl_path is None:
        path_check = ["/usr/local", "/usr"]
    else:
        path_check = [ctx.options.opengl_path]

    # OpenGL includes
    check_include(ctx, "OPENGL", ["GL"], ["gl.h"], path_check)

    # OpenGL libs
    check_lib(ctx, "OPENGL", "", ["libGL"], path_check)

    if ctx.env.LIB_OPENGL:
        ctx.get_env()["libs"] = ctx.get_env()["libs"] + ["OPENGL"]


def configure(cfg):
    if not cfg.env.LIB_OPENGL:
        cfg.check_opengl()
