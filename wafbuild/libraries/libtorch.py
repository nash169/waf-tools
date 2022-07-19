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
from wafbuild.utils import check_include, check_lib, dir
import os
import os.path as osp


def options(opt):
    opt.add_option(
        "--libtorch-path", type="string", help="path to libtorch", dest="libtorch_path"
    )

    opt.add_option(
        "--libtorch-cuda", action="store_true", help="activate CUDA support", dest="libtorch_cuda"
    )

    opt.add_option(
        "--libtorch-c11", action="store", help="support to C++11 interface", dest="libtorch_c11", default='True'
    )

    opt.add_option(
        "--libtorch-components", type="string", help="manually select libraries", dest="libtorch_components"
    )

    # Load options
    opt.load("cuda", tooldir=osp.join(dir, 'compilers'))


@conf
def check_libtorch(ctx):
    # Set the search path
    if ctx.options.libtorch_path is None:
        path_check = ["/usr/local", "/usr", "/opt"]
    else:
        path_check = [ctx.options.libtorch_path]

    # Libtorch includes
    check_include(ctx, "LIBTORCH", ["include/torch/csrc/api/include"], ["torch/script.h",
                                                                        "torch/torch.h"], path_check)

    # Define os-based components
    if ctx.env["DEST_OS"] == "darwin":
        libs = ['libnnpack', 'libonnx_proto', 'libtorch_python', 'libqnnpack', 'libbackend_with_compiler', 'libtorch', 'libfbjni', 'libbreakpad', 'libcpuinfo',
                'libXNNPACK', 'libbenchmark', 'libdnnl', 'libtorch_global_deps', 'libiomp5', 'libfmt', 'libpthreadpool', 'libprotobuf', 'libprotoc', 'libprotobuf-lite',
                'libcaffe2_protos', 'libtorch_cpu', 'libonnx', 'libtensorpipe', 'libgtest_main', 'libjitbackend_test', 'libc10', 'libtorchbind_test', 'libgtest',
                'libbenchmark_main', 'libshm', 'libfoxi_loader', 'libfbgemm', 'libgmock', 'libtensorpipe_uv', 'libkineto', 'libclog', 'libcpuinfo_internals',
                'libbreakpad_common', 'libpytorch_jni', 'libgloo', 'libpytorch_qnnpack', 'libnnpack_reference_layers', 'libasmjit', 'libgmock_main']
    else:
        libs = ['libpthreadpool', 'libbenchmark_main', 'libbackend_with_compiler', 'libkineto', 'libtorch_cuda_cu', 'libtorchbind_test', 'libtorch', 'libfmt', 'libprotoc',
                'libtorch_cuda', 'libcaffe2_nvrtc', 'libgloo_cuda', 'libgtest_main', 'libasmjit', 'libnnpack', 'libnnapi_backend', 'libcaffe2_protos', 'libclog',
                'libnnpack_reference_layers', 'libonnx', 'libcpuinfo', 'libfbgemm', 'libprotobuf', 'libprotobuf-lite', 'libtorch_cpu', 'libshm', 'libjitbackend_test',
                'libXNNPACK', 'libc10_cuda', 'libgtest', 'libbenchmark', 'libpytorch_qnnpack', 'libgmock', 'libgmock_main', 'libdnnl', 'libbreakpad', 'libqnnpack',
                'libgloo', 'libtensorpipe', 'libc10d_cuda_test', 'libc10', 'libtensorpipe_uv', 'libonnx_proto', 'libtorch_python', 'libfoxi_loader', 'libtorch_cuda_cpp',
                'libcpuinfo_internals', 'libbreakpad_common', 'libtensorpipe_cuda', 'libtorch_global_deps']

    # Select components
    if ctx.options.libtorch_components is None:
        # Defaults libraries (used by libtorch)
        lib_check = ["libtorch",  "libtorch_cpu", "libc10"]  # libkineto
    else:
        lib_check = []
        for lib in list(ctx.options.libtorch_components.split(",")):
            if lib in libs:
                lib_check += [lib]
            else:
                ctx.msg(lib + " not found", "YELLOW")

    # Add cuda if requested
    if ctx.options.libtorch_cuda and ctx.env["DEST_OS"] != "darwin":
        ctx.get_env()["requires"] += ["CUDA"]
        # Load CUDA necessary components
        ctx.options.cuda_components = (
            "libcuda,libnvrtc,libnvToolsExt,libcudart,libcufft,libcurand,libcublas,libcudnn"
        )
        ctx.load("cuda", tooldir=osp.join(dir, 'compilers'))
        # Add CUDA related components
        lib_check += ["libtorch_cuda", "libtorch_cuda_cpp",
                      "libc10_cuda", "libtorch_cuda_cu"]
        # Add flags to force linking against CUDA
        ctx.env.LINKFLAGS_LIBTORCH += ["-Wl,--no-as-needed"]

    # LIB Check
    check_lib(ctx, "LIBTORCH", "", lib_check, path_check)

    # Libtorch defines
    ctx.env.DEFINES_LIBTORCH += ["USE_DISTRIBUTED", "USE_C10D_NCCL",
                                 "USE_C10D_GLOO", "USE_RPC", "USE_TENSORPIPE"]

    # CXX flags
    ctx.env.CXXFLAGS_LIBTORCH += [
        "-D_GLIBCXX_USE_CXX11_ABI=1" if ctx.options.libtorch_c11.lower() in ['true', 't', '1', 'y', 'yes'] else "-D_GLIBCXX_USE_CXX11_ABI=0"]

    # LD flags
    ctx.env.LDFLAGS_LIBTORCH += [
        "-D_GLIBCXX_USE_CXX11_ABI=1" if ctx.options.libtorch_c11.lower() in ['true', 't', '1', 'y', 'yes'] else "-D_GLIBCXX_USE_CXX11_ABI=0"]

    # If not in standard path hard compile dynamic linking
    if ctx.options.libtorch_path is not None:
        ctx.env.RPATH_LIBTORCH += [ctx.env.LIBPATH_LIBTORCH[-1]]

    if ctx.env.LIB_LIBTORCH:
        ctx.get_env()["libs"] += ["LIBTORCH"]


def configure(cfg):
    if not cfg.env.LIB_LIBTORCH:
        cfg.check_libtorch()
