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
from wafbuild.utils import check_include, check_lib


def options(opt):
    # Add options
    opt.add_option("--ogre-path", type="string",
                   help="path to Ogre", dest="ogre_path")
    opt.add_option(
        "--ogre-components",
        type="string",
        help="Ogre components",
        dest="ogre_components",
    )
    opt.add_option(
        "--ogre-plugins", type="string", help="Ogre plugins", dest="ogre_plugins"
    )


@conf
def check_ogre(ctx):
    # Set the search path
    if ctx.options.ogre_path is None:
        path_check = ["/usr/local", "/usr"]
    else:
        path_check = [ctx.options.ogre_path]

    # Ogre components
    components = [
        "Bites",
        "HLMS",
        "MeshLodGenerator",
        "Overlay",
        "Paging",
        "Property",
        "RTShaderSystem",
        "Terrain",
        "Volume",
    ]

    if ctx.options.ogre_components is None:
        components = ["Bites", "Overlay", "RTShaderSystem", "MeshLodGenerator"]
    else:
        components = list(ctx.options.ogre_components.split(","))

    for i, component in enumerate(components):
        components[i] = "libOgre" + component

    # Ogre plugins
    plugins = [
        "Plugin_BSPSceneManager",
        "Plugin_CgProgramManager",
        "Plugin_OctreeSceneManager",
        "Plugin_PCZSceneManager",
        "Plugin_ParticleFX",
        "RenderSystem_GL",
        "RenderSystem_GLES2",
        "RenderSystem_GL3Plus",
        "RenderSystem_Direct3D9",
        "RenderSystem_Direct3D11",
        "Codec_STBI",
        "Codec_FreeImage",
        "Codec_EXR",
    ]

    if ctx.options.ogre_plugins is None:
        plugins = []
    else:
        plugins = list(ctx.options.ogre_plugins.split(","))

    # OGRE includes
    check_include(ctx, "OGRE", ["OGRE"], ["Ogre.h"], path_check)

    # OGRE libs
    lib_to_check = ["libOgreMain"] + components
    check_lib(ctx, "OGRE", ["OGRE"], lib_to_check, path_check)
    check_lib(ctx, "OGRE", ["OGRE"], plugins, path_check, True)

    if ctx.env.LIB_OGRE:
        for component in components:
            ctx.env.INCLUDES_OGRE.append(
                ctx.env.INCLUDES_OGRE[0] + "/" + component)

        ctx.get_env()["libs"] = ctx.get_env()["libs"] + ["OGRE"]


def configure(cfg):
    if not cfg.env.LIB_OGRE:
        cfg.check_ogre()
