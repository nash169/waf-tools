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
