#! /usr/bin/env python
# encoding: utf-8

import io

from waflib.Configure import conf
from utils import check_include, check_lib


def options(opt):
    opt.add_option("--corrade-path", type="string",
                   help="path to corrade", dest="corrade_path")
    opt.add_option("--corrade-config", type="string",
                   help="path to corrade", dest="corrade_config")
    opt.add_option("--corrade-component", type="string",
                   help="path to corrade", dest="corrade_component")


@conf
def check_corrade(ctx):
    # Set the search path
    if ctx.options.corrade_path is None:
        path_check = ["/usr/local", "/usr"]
    else:
        path_check = [ctx.options.corrade_path]

    # CORRADE includes
    check_include(ctx, "CORRADE", "", [
                  "Corrade/Corrade.h", "Corrade/configure.h"], path_check)

    # CORRADE configs
    possible_configs = ["GCC47_COMPATIBILITY", "MSVC2015_COMPATIBILITY", "MSVC2017_COMPATIBILITY", "BUILD_DEPRECATED", "BUILD_STATIC", "TARGET_UNIX", "TARGET_APPLE",
                        "TARGET_IOS", "TARGET_IOS_SIMULATOR", "TARGET_WINDOWS", "TARGET_WINDOWS_RT", "TARGET_EMSCRIPTEN", "TARGET_ANDROID", "TESTSUITE_TARGET_XCTEST", "UTILITY_USE_ANSI_COLORS"]
    corrade_config = []

    ctx.start_msg("Getting Corrade configuration")
    config_file = ctx.find_file(
        "Corrade/configure.h", ctx.env.INCLUDES_CORRADE)
    with io.open(config_file, errors="ignore") as f:
        config_content = f.read()
    for config in possible_configs:
        index = config_content.find("#define CORRADE_" + config)
        if index > -1:
            corrade_config.append(config)
    ctx.end_msg(corrade_config)

    # CORRADE components
    if ctx.options.corrade_component is None:
        components = ["Containers", "PluginManager",
                      "TestSuite", "Interconnect", "Utility", "rc"]
    else:
        components = ctx.options.corrade_component

    component_to_check = []
    for component in components:
        if component == "Containers":
            component_to_check = component_to_check + [component, "Utility"]
        elif component == "Interconnect":
            component_to_check = component_to_check + [component, "Utility"]
        elif component == "PluginManager":
            component_to_check = component_to_check + \
                [component, "Containers", "Utility", "rc"]
        elif component == "TestSuite":
            component_to_check = component_to_check + [component, "Utility"]
        elif component == "Utility":
            component_to_check = component_to_check + \
                [component, "Containers", "rc"]
        elif component == "rc":
            component_to_check.append(component)
        else:
            pass
    component_to_check = list(set(component_to_check))

    if "Containers" in component_to_check:
        ctx.env.INCLUDES_CORRADE.append(
            ctx.env.INCLUDES_CORRADE[0] + "/Containers")
        component_to_check.remove("Containers")

    if "rc" in component_to_check:
        bin_check = []
        for path in path_check:
            bin_check.append(path + "/bin")
        ctx.env.EXEC_CORRADE = ctx.env.EXEC_CORRADE + \
            [ctx.find_file("corrade-rc", bin_check)]
        component_to_check.remove("rc")

    for i, component in enumerate(component_to_check):
        component_to_check[i] = 'libCorrade' + component

    check_lib(ctx, "CORRADE", "", component_to_check, path_check)

    if "PluginManager" or "Utility" in component_to_check:
        ctx.env.LIB_CORRADE.append("dl")

    # CORRADE flags
    ctx.env.CXX_FLAGS_CORRADE = ["-Wall", "-Wextra", "-Wold-style-cast", "-Winit-self",
                                 "-Werror=return-type", "-Wmissing-declarations", "-pedantic", "-fvisibility=hidden"]

    if ctx.env.CXX_NAME in ["gcc", "g++"]:
        ctx.env.CXX_FLAGS_CORRADE = ctx.env.CXX_FLAGS_CORRADE + \
            ["-Wzero-as-null-pointer-constant", "-Wdouble-promotion"]
    if ctx.env.CXX_NAME in ["clang", "clang++", "llvm"]:
        ctx.env.CXX_FLAGS_CORRADE = ctx.env.CXX_FLAGS_CORRADE + \
            ["-Wmissing-prototypes", "-Wno-shorten-64-to-32"]

    if ctx.env.LIB_CORRADE:
        if not ctx.get_env()["libs"]:
            ctx.get_env()["libs"] = "CORRADE "
        else:
            ctx.get_env()["libs"] = ctx.get_env()["libs"] + "CORRADE "


def configure(cfg):
    if not cfg.env.LIB_CORRADE:
        cfg.check_corrade()
