#! /usr/bin/env python
# encoding: utf-8

from waflib.Configure import conf
from utils import check_include, check_lib


def options(opt):
    # Options
    opt.add_option("--x11-path", type="string",
                   help="path to x11", dest="x11_path")


@conf
def check_x11(ctx):
    # Set the search path
    if ctx.options.x11_path is None:
        path_check = ["/usr/local", "/usr"]
    else:
        path_check = [ctx.options.x11_path]

    # X11 includes
    check_include(ctx, "X11", ["X11"], ["Xlib.h"], path_check)

    # X11 libs
    check_lib(ctx, "X11", "", ["libX11"], path_check)

    if ctx.env.LIB_X11:
        ctx.get_env()["libs"] = ctx.get_env()["libs"] + ["X11"]


def configure(cfg):
    if not cfg.env.LIB_X11:
        cfg.check_x11()
