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
from utils import check_include, check_lib
import os
import os.path as osp


def options(opt):
    opt.add_option(
        "--libtorch-path", type="string", help="path to libtorch", dest="libtorch_path"
    )


@conf
def check_libtorch(ctx):
    # Set the search path
    if ctx.options.libtorch_path is None:
        path_check = ["/usr/local", "/usr", "/opt"]
    else:
        path_check = [ctx.options.libtorch_path]

    # kernel-lib includes
    check_include(ctx, "LIBTORCH", ["include/torch/csrc/api/include"], ["torch/script.h",
                                                                        "torch/torch.h"], path_check)

    # LIB Check
    if ctx.env["DEST_OS"] == "darwin":
        libraries = ['libnnpack', 'libonnx_proto', 'libtorch_python', 'libqnnpack', 'libbackend_with_compiler', 'libtorch', 'libfbjni', 'libbreakpad', 'libcpuinfo', 'libXNNPACK', 'libbenchmark', 'libdnnl', 'libtorch_global_deps', 'libiomp5', 'libfmt', 'libpthreadpool', 'libprotobuf', 'libprotoc', 'libprotobuf-lite', 'libcaffe2_protos', 'libtorch_cpu', 'libonnx', 'libtensorpipe',
                     'libgtest_main', 'libjitbackend_test', 'libc10', 'libtorchbind_test', 'libgtest', 'libbenchmark_main', 'libshm', 'libfoxi_loader', 'libfbgemm', 'libgmock', 'libtensorpipe_uv', 'libkineto', 'libclog', 'libcpuinfo_internals', 'libbreakpad_common', 'libpytorch_jni', 'libgloo', 'libpytorch_qnnpack', 'libnnpack_reference_layers', 'libasmjit', 'libgmock_main']
    else:
        libraries = ['libtorch_cpu', 'libnnapi_backend', 'libnnpack', 'libgloo', 'libcaffe2_nvrtc', 'libpthreadpool', 'libc10_cuda', 'libqnnpack', 'libtensorpipe', 'libprotoc', 'libfmt', 'libtorch_cuda', 'libnnpack_reference_layers', 'libgmock', 'libgtest_main', 'libXNNPACK', 'libbreakpad', 'libonnx_proto', 'libtorch_python', 'libfoxi_loader', 'libtorch', 'libtorchbind_test', 'libbenchmark_main', 'libshm', 'libjitbackend_test',
                     'libc10d_cuda_test', 'libclog', 'libtensorpipe_cuda', 'libgmock_main', 'libasmjit', 'libgtest', 'libnvrtc-builtins', 'libdnnl', 'libcaffe2_protos', 'libprotobuf', 'libprotobuf-lite', 'libgloo_cuda', 'libonnx', 'libc10', 'libtensorpipe_uv', 'libpytorch_qnnpack', 'libcpuinfo', 'libfbgemm', 'libtorch_global_deps', 'libbenchmark', 'libcpuinfo_internals', 'libbackend_with_compiler', 'libkineto', 'libbreakpad_common']

    check_lib(ctx, "LIBTORCH", "", libraries, path_check)

    if ctx.env.LIB_LIBTORCH:
        ctx.get_env()["libs"] += ["LIBTORCH"]


def configure(cfg):
    if not cfg.env.LIB_LIBTORCH:
        cfg.check_libtorch()
