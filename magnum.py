#! /usr/bin/env python
# encoding: utf-8

import re

from waflib.Configure import conf
from utils import check_include, check_lib


def options(opt):
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

    # Magnum components
    components = [
        "Audio",
        "DebugTools",
        "MeshTools",
        "Primitives",
        "SceneGraph",
        "Shaders",
        "Shapes",
        "Text",
        "TextureTools",
        "Trade",
        "GlfwApplication",
        "GlutApplication",
        "GlxApplication",
        "Sdl2Application",
        "XEglApplication",
        "WindowlessCglApplication",
        "WindowlessEglApplication",
        "WindowlessGlxApplication",
        "WindowlessIosApplication",
        "WindowlessWglApplication",
        "WindowlessWindowsEglApplication",
        "CglContext",
        "EglContext",
        "GlxContext",
        "WglContext",
        "OpenGLTester",
        "MagnumFont",
        "MagnumFontConverter",
        "ObjImporter",
        "TgaImageConverter",
        "TgaImporter",
        "WavAudioImporter",
        "distancefieldconverter",
        "fontconverter",
        "imageconverter",
        "info",
        "al-info",
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
    component_dependencies["MagnumFont"] = ["TgaImporter", "Text", "TextureTools"]
    component_dependencies["MagnumFontConverter"] = [
        "TgaImageConverter",
        "Text",
        "TextureTools",
    ]
    component_dependencies["ObjImporter"] = ["MeshTools"]
    component_dependencies["WavAudioImporter"] = ["Audio"]

    # Magnum Plugins
    plugins = [
        "AnyAudioImporter",
        "AnyImageConverter",
        "AnyImageImporter",
        "AnySceneImporter",
        "AssimpImporter",
        "DdsImporter",
        "DevIlImageImporter",
        "DrFlacAudioImporter",
        "DrWavAudioImporter",
        "FreeTypeFont",
        "HarfBuzzFont",
        "JpegImporter",
        "MiniExrImageConverter",
        "OpenGexImporter",
        "PngImageConverter",
        "PngImporter",
        "StanfordImporter",
        "StbImageConverter",
        "StbImageImporter",
        "StbTrueTypeFont",
        "StbVorbisAudioImporter",
    ]

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
        components_to_check = [
            "Sdl2Application",
            "Shaders",
            "Primitives",
            "MeshTools",
            "SceneGraph",
            "Trade",
        ]
    else:
        components_to_check = ctx.options.magnum_components

    # Add component dependencies
    for component in components_to_check:
        components_to_check = components_to_check + component_dependencies[component]

    # Plugins to check
    if ctx.options.magnum_plugins is None:
        plugins_to_check = ["AnySceneImporter", "AssimpImporter"]
    else:
        plugins_to_check = ctx.options.magnum_plugins

    # Add plugin/component dependencies
    for plugin in plugins_to_check:
        plugins_to_check = plugins_to_check + plugin_dependencies[plugin]
        components_to_check = (
            components_to_check + plugin_components_dependencies[plugin]
        )

    # Integrations to check
    if ctx.options.magnum_plugins is None:
        integrations_to_check = ["Bullet", "Dart"]
    else:
        integrations_to_check = ctx.options.magnum_integrations

    # Add integration/component dependencies
    for integration in integrations_to_check:
        integrations_to_check = (
            integrations_to_check + integration_dependencies[integration]
        )
        components_to_check = (
            components_to_check + integration_components_dependencies[integration]
        )

    # Clean & add prefix
    components_to_check = list(set(components_to_check))
    plugins_to_check = list(set(plugins_to_check))
    integrations_to_check = list(set(integrations_to_check))

    for i, component in enumerate(components_to_check):
        components_to_check[i] = "libMagnum" + component

    for i, integration in enumerate(integrations_to_check):
        integrations_to_check[i] = "libMagnum" + integration + "Integration"

    # Check includes
    check_include(ctx, "MAGNUM", ["Magnum"], ["Magnum.h"], path_check)

    # Check libraries
    lib_to_check = (
        ["libMagnum"] + components_to_check + plugins_to_check + integrations_to_check
    )
    folders_to_check = [
        "magnum/audioimporters",
        "magnum/fonts",
        "magnum/imageconverters",
        "magnum/importers",
    ]
    check_lib(ctx, "MAGNUM", folders_to_check, lib_to_check, path_check)

    if ctx.env.LIB_MAGNUM:
        for component in components:
            ctx.env.INCLUDES_MAGNUM.append(ctx.env.INCLUDES_MAGNUM[0] + "/" + component)

        ctx.get_env()["libs"] = ctx.get_env()["libs"] + ["MAGNUM"]


def configure(cfg):
    if not cfg.env.LIB_MAGNUM:
        cfg.check_magnum()
