#! /usr/bin/env python
# encoding: utf-8

from waflib.Configure import conf
from utils import check_include, check_lib


def options(opt):
    opt.add_option(
        "--ipopt-path", type="string", help="path to IPOPT", dest="ipopt_path"
    )


@conf
def check_ipopt(ctx):
    # Set the search path
    if ctx.options.ipopt_path is None:
        path_check = ["/usr/local", "/usr", "/opt"]
    else:
        path_check = [ctx.options.ipopt_path]

    # Header check
    check_include(ctx, "IPOPT", ["coin-or", "coin"], ["IpNLP.hpp"], path_check)

    # Library Check
    check_lib(ctx, "IPOPT", "", ["libipopt"], path_check)

    if ctx.env.LIB_IPOPT:
        ctx.get_env()["libs"] += ["IPOPT"]


def configure(cfg):
    if not cfg.env.LIB_IPOPT:
        cfg.check_ipopt()
