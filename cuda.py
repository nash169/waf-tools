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
        "--cuda-path", type="string", help="path to cuda", dest="cuda_path"
    )

    opt.add_option("--cuda-components", type="string",
                   help="CUDA components", dest="cuda_components")


@conf
def check_cuda(ctx):
    # Set the search path
    if ctx.options.cuda_path is None:
        path_check = ["/usr/local", "/usr", "/opt"]
    else:
        path_check = [ctx.options.cuda_path]

    # find headers
    check_include(ctx, "CUDA", ["cuda/include"], ["cuda.h"], path_check)

    # available libraries
    libs = ['libnvptxcompiler_static', 'libmetis_static', 'libOpenCL', 'libaccinj64', 'libcudart', 'libcusparse_static', 'libnppicc', 'libnppc', 'libnvrtc-builtins',
            'libcufft_static_nocallback', 'libnppig_static', 'libcupti', 'libnppitc', 'libnppicc_static', 'libnppist_static', 'libnvperf_host', 'libcurand_static',
            'libnppitc_static', 'libcufftw_static', 'libcublas_static', 'libcublasLt', 'libnvjpeg', 'libnppidei', 'libnvrtc', 'libcurand', 'libnppig', 'libnppial',
            'libnppidei_static', 'libcusolver', 'libnpps', 'libnpps_static', 'libcusolver_static', 'libnvblas', 'libcufft', 'libnppif', 'libcusparse',
            'libnvperf_target', 'liblapack_static', 'libcufftw', 'libnvjpeg_static', 'libnppisu_static', 'libnvidia-ml', 'libcupti_static', 'libnvperf_host_static',
            'libcufft_static', 'libcublasLt_static', 'libcudadevrt', 'libnppc_static', 'libpcsamplingutil', 'libcuinj64', 'libcublas', 'libculibos', 'libnppisu',
            'libnppist', 'libnppim', 'libnppim_static', 'libcuda', 'libnppial_static', 'libnvToolsExt', 'libcusolverMg', 'libnppif_static', 'libcudart_static',
            "libcudnn"]  # libcudnn technically not part of CUDA

    # select libraries to check
    if ctx.options.cuda_components is None:
        # Defaults libraries (used by libtorch)
        lib_check = [
            "libcuda,libnvrtc,libnvToolsExt,libcudart,libcufft,libcurand,libcublas,libcudnn"]
    else:
        lib_check = []
        for lib in list(ctx.options.cuda_components.split(",")):
            if lib in libs:
                lib_check += [lib]
            else:
                ctx.msg(lib + " not found", "YELLOW")

    # find libraries
    check_lib(ctx, "CUDA", ["cuda/lib64",
                            "cuda/lib64/stubs"], lib_check, path_check)

    if ctx.env.LIB_CUDA:
        # add library to the used ones
        ctx.get_env()["libs"] += ["CUDA"]
        # add pthread manually (fix this)
        ctx.env.LIB_CUDA += ["pthread"]


def configure(cfg):
    if not cfg.env.LIB_CUDA:
        cfg.check_cuda()
