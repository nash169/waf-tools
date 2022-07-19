#!/usr/bin/env python
# encoding: utf-8
#
#    This file is part of waf-tools.
#
#    Copyright (c) 2020, 2021, 2022 Bernardo Fichera <bernardo.fichera@gmail.com>
#
#    Permission is hereby granted, free of charge, to any person obtaining a copy
#    of this software and associated documentation files (the "Software"), to deal
#    in the Software without restriction, including without limitation the rights
#    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#    copies of the Software, and to permit persons to whom the Software is
#    furnished to do so, subject to the following conditions:
#
#    The above copyright notice and this permission notice shall be included in all
#    copies or substantial portions of the Software.
#
#    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#    SOFTWARE.

from waflib.Configure import conf


def options(opt):
    # Load compiler
    opt.load("compiler_cxx")

    opt.add_option(
        "--debug", action="store_true", help="activate debug flags", dest="debug_flags",
    )

    opt.add_option(
        "--std", type="string", help="C++ Standard", dest="cpp_standard"
    )


@conf
def check_flags(ctx):
    # OSX/Mac uses .dylib and GNU/Linux .so
    ctx.env.SUFFIX = "dylib" if ctx.env["DEST_OS"] == "darwin" else "so"

    # Load compiler configuration and generate clangd flags
    ctx.load("compiler_cxx clang_compilation_database")

    if ctx.options.cpp_standard is not None:
        flags = ["-std=c++"+ctx.options.cpp_standard]
    else:
        flags = ["-std=c++17"]

    if ctx.options.debug_flags:
        flags += ["-Wall", "-w"]
        defines = ["DEBUG"]
    else:
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
        defines = ["RELEASE"]

    # Remove empty strings
    flags = [string for string in flags if string != ""]

    # Set compiler flags environment variable
    ctx.env["CXXFLAGS"] += flags
    ctx.env["DEFINES"] += defines


def configure(cfg):
    cfg.check_flags()
