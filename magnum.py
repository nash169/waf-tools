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

import re

from waflib.Configure import conf
from utils import check_include, check_lib


def options(opt):
    # Required package options
    opt.load("corrade eigen opengl egl sdl2", tooldir="waf_tools")

    # Add options
    opt.add_option(
        "--magnum-path", type="string", help="path to Magnum", dest="magnum_path"
    )
    opt.add_option(
        "--magnum-components",
        type="string",
        help="Magnum components",
        dest="magnum_components",
    )
    opt.add_option(
        "--magnum-plugins", type="string", help="Magnum plugins", dest="magnum_plugins"
    )
    opt.add_option(
        "--magnum-integrations",
        type="string",
        help="Magnum integrations",
        dest="magnum_integrations",
    )


@conf
def check_magnum(ctx):
    # Set the search path
    if ctx.options.magnum_path is None:
        path_check = ["/usr/local", "/usr"]
    else:
        path_check = [ctx.options.magnum_path]

    # Magnum binaries
    binaries = [
        "distancefieldconverter",
        "fontconverter",
        "imageconverter",
        "info",
        "al-info",
    ]

    # Magnum configurations
    configs = [
        "BUILD_DEPRECATED",
        "BUILD_STATIC",
        "BUILD_MULTITHREADED",
        "TARGET_GL",
        "TARGET_GLES",
        "TARGET_GLES2",
        "TARGET_GLES3",
        "TARGET_DESKTOP_GLES",
        "TARGET_WEBGL",
        "TARGET_HEADLESS",
    ]

    # Magnum components
    components = [
        "Audio",
        "DebugTools",
        "EglContext",
        "GL",
        "GlfwApplication",
        "GlxApplication",
        "GlxContext",
        "MeshTools",
        "OpenDdl",
        "OpenGLTester",
        "Primitives",
        "SceneGraph",
        "Sdl2Application",
        "Shaders",
        "Text",
        "TextureTools",
        "Trade",
        "Vk",
        "WindowlessEglApplication",
        "WindowlessGlxApplication",
        "XEglApplication",
    ]

    # Component dependencies
    component_dependencies = {}
    for component in components:
        component_dependencies[component] = []

    component_dependencies["Shapes"] = ["SceneGraph"]
    component_dependencies["Text"] = ["TextureTools"]
    component_dependencies["DebugTools"] = [
        "MeshTools",
        "Primitives",
        "SceneGraph",
        "Shaders",
    ]
    component_dependencies["Primitives"] = ["Trade"]
    component_dependencies["MagnumFont"] = [
        "TgaImporter", "Text", "TextureTools"]
    component_dependencies["MagnumFontConverter"] = [
        "TgaImageConverter",
        "Text",
        "TextureTools",
    ]
    component_dependencies["ObjImporter"] = ["MeshTools"]
    component_dependencies["WavAudioImporter"] = ["Audio"]

    # Magnum Plugins
    plugins_audioimporters = [
        "AnyAudioImporter",
        "DrFlacAudioImporter",
        "DrMp3AudioImporter",
        "DrWavAudioImporter",
        "StbVorbisAudioImporter",
        "WavAudioImporter",
    ]

    plugins_fonts = ["FreeTypeFont", "HarfBuzzFont",
                     "MagnumFont", "StbTrueTypeFont"]

    plugins_imageconverters = [
        "AnyImageConverter",
        "JpegImageConverter",
        "MiniExrImageConverter",
        "PngImageConverter",
        "StbImageConverter",
        "TgaImageConverter",
    ]

    plugins_importers = [
        "AnyImageImporter",
        "AnySceneImporter",
        "AssimpImporter",
        "DdsImporter",
        "DevIlImageImporter",
        "JpegImporter",
        "ObjImporter",
        "OpenGexImporter",
        "PngImporter",
        "PrimitiveImporter",
        "StanfordImporter",
        "StbImageImporter",
        "TgaImporter",
        "TinyGltfImporter",
    ]

    plugins = (
        plugins_audioimporters
        + plugins_fonts
        + plugins_imageconverters
        + plugins_importers
    )

    # Plugin dependencies
    plugin_dependencies = {}
    for plugin in plugins:
        plugin_dependencies[plugin] = []

    plugin_dependencies["AssimpImporter"] = ["AnyImageImporter"]
    plugin_dependencies["OpenGexImporter"] = ["AnyImageImporter"]
    plugin_dependencies["HarfBuzzFont"] = ["FreeTypeFont"]

    # Plugin components dependencies
    plugin_components_dependencies = {}
    for plugin in plugins:
        if re.match(re.compile(".+AudioImporter$"), plugin):
            plugin_components_dependencies[plugin] = ["Audio"]
        elif re.match(re.compile(".+(Font|FontConverter)$"), plugin):
            plugin_components_dependencies[plugin] = ["Text"]
        else:
            plugin_components_dependencies[plugin] = []

    # Magnum integration
    integrations = ["Bullet", "Dart", "Eigen"]

    # Integration dependencies
    integration_dependencies = {}
    for integration in integrations:
        integration_dependencies[integration] = []

    # Integration components dependencies
    integration_components_dependencies = {}
    for integration in integrations:
        integration_components_dependencies[integration] = []

    integration_components_dependencies["Bullet"] = ["SceneGraph", "Shaders"]
    integration_components_dependencies["Dart"] = [
        "SceneGraph",
        "Primitives",
        "MeshTools",
    ]

    # Components to check
    if ctx.options.magnum_components is None:
        components_to_check = []
    else:
        components_to_check = list(ctx.options.magnum_components.split(","))
        print(components_to_check)

    # Add component dependencies
    for component in components_to_check:
        components_to_check = components_to_check + \
            component_dependencies[component]

    # Plugins to check
    if ctx.options.magnum_plugins is None:
        plugins_to_check = []
    else:
        plugins_to_check = list(ctx.options.magnum_plugins.split(","))

    # Add plugin/component dependencies
    for plugin in plugins_to_check:
        plugins_to_check = plugins_to_check + plugin_dependencies[plugin]
        components_to_check = (
            components_to_check + plugin_components_dependencies[plugin]
        )

    # Integrations to check
    if ctx.options.magnum_integrations is None:
        integrations_to_check = []
    else:
        integrations_to_check = list(
            ctx.options.magnum_integrations.split(","))

    # Add integration/component dependencies
    for integration in integrations_to_check:
        integrations_to_check = (
            integrations_to_check + integration_dependencies[integration]
        )
        components_to_check = (
            components_to_check +
            integration_components_dependencies[integration]
        )

    # Clean & add prefix
    components_to_check = list(set(components_to_check))
    plugins_to_check = list(set(plugins_to_check))

    integrations_to_check = list(set(integrations_to_check))
    if "Eigen" in integrations_to_check:
        integrations_to_check.remove("Eigen")
        with_eigen = True
    else:
        with_eigen = False

    for i, component in enumerate(components_to_check):
        components_to_check[i] = "libMagnum" + component

    for i, integration in enumerate(integrations_to_check):
        integrations_to_check[i] = "libMagnum" + integration + "Integration"

    # Check includes
    include_folders = ["Magnum"]
    includes_to_check = ["Magnum.h"]
    for plugin in plugins_to_check:
        includes_to_check = includes_to_check + [plugin + ".h"]
        include_folders = include_folders + ["MagnumPlugins/" + plugin]

    check_include(ctx, "MAGNUM", include_folders,
                  includes_to_check, path_check)

    # Check libraries
    lib_to_check = ["libMagnum"] + components_to_check + integrations_to_check
    lib_folders = [
        "magnum/audioimporters",
        "magnum/fonts",
        "magnum/imageconverters",
        "magnum/importers",
    ]
    check_lib(ctx, "MAGNUM", lib_folders, lib_to_check, path_check)
    check_lib(ctx, "MAGNUM", lib_folders, plugins_to_check, path_check, True)

    if ctx.env.LIB_MAGNUM:
        # Check dependencies
        ctx.get_env()["requires"] = ctx.get_env()["requires"] + ["CORRADE"]
        ctx.load("corrade", tooldir="waf_tools")

        if "libMagnumGL" in components_to_check:
            ctx.get_env()["requires"] = ctx.get_env()["requires"] + ["OPENGL"]
            ctx.load("opengl", tooldir="waf_tools")

        if "libMagnumSdl2Application" in components_to_check:
            ctx.get_env()["requires"] = ctx.get_env()["requires"] + ["SDL2"]
            ctx.load("sdl2", tooldir="waf_tools")

        if with_eigen:
            ctx.get_env()["requires"] = ctx.get_env()["requires"] + ["EIGEN"]
            ctx.load("eigen", tooldir="waf_tools")

        # Add library
        ctx.get_env()["libs"] = ctx.get_env()["libs"] + ["MAGNUM"]


def configure(cfg):
    if not cfg.env.LIB_MAGNUM:
        cfg.check_magnum()


# [
#     "Shapes",
#     "GlutApplication",
#     "WindowlessCglApplication",
#     "WindowlessIosApplication",
#     "WindowlessWglApplication",
#     "WindowlessWindowsEglApplication",
#     "CglContext",
#     "WglContext",
#     "MagnumFontConverter"
# ]
