#! /usr/bin/env python
# encoding: utf-8

from waflib.Configure import conf
from utils import check_include, check_lib


def options(opt):
    # Options
    opt.add_option("--pinocchio-path", type="string",
                   help="path to pinocchio", dest="pinocchio_path")


@conf
def check_pinocchio(ctx):
    # Set the search path
    if ctx.options.pinocchio_path is None:
        path_check = ["/usr/local", "/usr"]
    else:
        path_check = [ctx.options.pinocchio_path]

    # PINOCCHIO includes
    check_include(ctx, "PINOCCHIO", [""], ["pinocchio/config.hpp"], path_check)

    # PINOCCHIO libs
    check_lib(ctx, "PINOCCHIO", "", ["libpinocchio"], path_check)

    if ctx.env.LIB_PINOCCHIO:
        ctx.get_env()["libs"] = ctx.get_env()["libs"] + ["PINOCCHIO"]


def configure(cfg):
    if not cfg.env.LIB_PINOCCHIO:
        cfg.check_pinocchio()
