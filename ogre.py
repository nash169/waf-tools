#! /usr/bin/env python
# encoding: utf-8

from waflib.Configure import conf
from utils import check_include, check_lib


def options(opt):
    # Add options
    opt.add_option("--ogre-path", type="string", help="path to Ogre", dest="ogre_path")
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
            ctx.env.INCLUDES_OGRE.append(ctx.env.INCLUDES_OGRE[0] + "/" + component)

        ctx.get_env()["libs"] = ctx.get_env()["libs"] + ["OGRE"]


def configure(cfg):
    if not cfg.env.LIB_OGRE:
        cfg.check_ogre()
