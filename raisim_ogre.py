#! /usr/bin/env python
# encoding: utf-8

from waflib.Configure import conf
from utils import check_include, check_lib, get_directory


def options(opt):
    # Required package options
    opt.load("raisim", tooldir="waf_tools")
    opt.load("ogre", tooldir="waf_tools")

    opt.add_option(
        "--raisimogre-path",
        type="string",
        help="path to raisimOgre",
        dest="raisimogre_path",
    )


@conf
def check_raisim_ogre(ctx):
    # Set the search path
    if ctx.options.raisimogre_path is None:
        path_check = ["/usr/local", "/usr"]
    else:
        path_check = [ctx.options.raisimogre_path]

    # RaiSim Ogre includes
    check_include(ctx, "RAISIMOGRE", "", ["raisim/OgreVis.hpp"], path_check)

    # RaiSim Ogre libs
    check_lib(ctx, "RAISIMOGRE", "", ["libraisimOgre"], path_check)

    if ctx.env.LIB_RAISIMOGRE:
        ctx.get_env()["requires"] = ctx.get_env()["requires"] + ["RAISIM", "OGRE"]

        if ctx.options.raisimogre_path:
            ctx.options.ogre_path = ctx.options.raisimogre_path
            ctx.options.raisim_path = ctx.options.raisimogre_path

        ctx.load("eigen", tooldir="waf_tools")
        ctx.load("eigen", tooldir="waf_tools")

        ctx.env.LIB_RAISIMOGRE.append("assimp")
        config_check = []
        for path in path_check:
            config_check.append(path + "/share")

        try:
            ctx.start_msg("Checking for RaisimOgre config files")

            config_path = get_directory(ctx, "raisimOgre/ogre/ogre.cfg", config_check)

            ctx.end_msg("RaisimOgre configs found in %s" % str(config_path))

            ctx.env.DEFINES_RAISIMOGRE = [
                "OGRE_CONFIG_DIR=" + config_path + "/raisimOgre/ogre/",
                "RAISIM_OGRE_RESOURCE_DIR=" + config_path + "/raisimOgre/rsc/",
            ]
        except:
            ctx.end_msg(
                "RaisimOgre configs not found in %s" % str(config_check), "YELLOW"
            )

        ctx.get_env()["libs"] = ctx.get_env()["libs"] + ["RAISIMOGRE"]


def configure(cfg):
    if not cfg.env.LIB_RAISIMOGRE:
        cfg.check_raisim_ogre()
