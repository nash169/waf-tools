#! /usr/bin/env python
# encoding: utf-8

from waflib.Configure import conf
from utils import check_include, check_lib


def options(opt):
    # Select installation path
    opt.add_option(
        "--urdfdom-path", type="string", help="path to urdfdom", dest="urdfdom_path"
    )


@conf
def check_urdfdom(ctx):
    # Set the search path
    if ctx.options.urdfdom_path is None:
        path_check = ["/usr/local", "/usr", "/opt"]
    else:
        path_check = [ctx.options.urdfdom_path]

    # URDFDOM includes
    check_include(ctx, "URDFDOM", [""],
                  [
                  "urdf_model/model.h",
                  "urdf_sensor/sensor.h",
                  "urdf_model_state/model_state.h",
                  "urdf_world/world.h",
                  "urdf_exception/exception.h",
                  "urdf_parser/urdf_parser.h"
                  ],
                  path_check)

    # URDFDOM lib
    check_lib(ctx, "URDFDOM", [""],
              [
        "liburdfdom_model",
        "liburdfdom_world",
        "liburdfdom_sensor",
        "liburdfdom_model_state"
    ],
        path_check)

    # If URDFDOM headers found
    if ctx.env.INCLUDES_URDFDOM:
        # Add URDFDOM label to the list of libraries
        ctx.get_env()["libs"] += ["URDFDOM"]


def configure(cfg):
    if not cfg.env.INCLUDES_URDFDOM:
        cfg.check_urdfdom()
