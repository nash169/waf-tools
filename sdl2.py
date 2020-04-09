#! /usr/bin/env python
# encoding: utf-8

from waflib.Configure import conf
from utils import check_include, check_lib


def options(opt):
    # Options
    opt.add_option("--sdl2-path", type="string", help="path to sdl2", dest="sdl2_path")


@conf
def check_sdl2(ctx):
    # Set the search path
    if ctx.options.sdl2_path is None:
        path_check = ["/usr/local", "/usr"]
    else:
        path_check = [ctx.options.sdl2_path]

    # SDL2 includes
    check_include(ctx, "SDL2", ["SDL2"], ["SDL.h"], path_check)

    # SDL2 libs
    check_lib(ctx, "SDL2", "", ["libSDL2"], path_check)

    if ctx.env.LIB_SDL2:
        ctx.get_env()["libs"] = ctx.get_env()["libs"] + ["SDL2"]


def configure(cfg):
    if not cfg.env.LIB_SDL2:
        cfg.check_sdl2()
