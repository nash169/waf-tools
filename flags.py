#! /usr/bin/env python
# encoding: utf-8

from waflib.Configure import conf


def options(opt):
    opt.add_option(
        "--debug", action="store_true", help="activate debug flags", dest="debug_flags",
    )

    opt.add_option(
        "--release", action="store_true", help="activate release flags", dest="release_flags",
    )

    opt.add_option(
        "--std", type="string", help="C++ Standard", dest="cpp_standard"
    )


@conf
def check_flags(ctx):
    if ctx.options.cpp_standard is not None:
        flags = ["-std=c++"+ctx.options.cpp_standard]
    else:
        # Set C++14 Standard as default
        flags = ["-std=c++17"]

    if ctx.options.release_flags:
        flags += ["-O3",
                  "-xHost" if ctx.env.CXX_NAME in ["icc", "icpc"] else "",
                  "-march=native" if ctx.env.CXX_NAME in [
                      "gcc", "g++", "clang", "clang++"] else "",
                  "-mtune=native" if ctx.env.CXX_NAME in [
                      "icc", "icpc"] else "",
                  "-g",
                  "-faligned-new" if ctx.env.CXX_NAME in [
                      "gcc", "g++", "clang", "clang++"] else "",
                  "-unroll" if ctx.env.CXX_NAME in ["icc", "icpc"] else "",
                  ]
    else:
        flags += ["-Wall", "-w"]

    # Remove empty strings
    flags = [string for string in flags if string != ""]

    # Set compiler flags environment variable
    ctx.env["CXXFLAGS"] += flags


def configure(cfg):
    cfg.check_flags()
