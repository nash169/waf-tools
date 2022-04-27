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

import os


def get_directory(ctx, filename, dirs):
    res = ctx.find_file(filename, dirs)
    return res[: -len(filename) - 1]


def check_include(ctx, use_name, folders, include_names, paths, required=[]):
    # Check if lib required
    if use_name in ctx.get_env()["requires"]:
        mandatory = True
    else:
        mandatory = False

    # Set required component if not
    if not required:
        required = include_names

    # Generate include paths
    include_paths = []
    for path in paths:
        if folders:
            for folder in folders:
                include_paths.append(os.path.join(path, folder))
                include_paths.append(os.path.join(path, "include", folder))
                include_paths.append(os.path.join(
                    path, "include/x86_64-linux-gnu", folder))
        include_paths.append(path)
        include_paths.append(os.path.join(path, "include"))
        include_paths.append(os.path.join(path, "include/x86_64-linux-gnu"))

    try:
        for include_name in include_names:
            ctx.start_msg("Checking for '%s' header" % str(include_name))
            try:
                # Add path
                ctx.get_env()["INCLUDES_" + use_name] = ctx.get_env()[
                    "INCLUDES_" + use_name
                ] + [get_directory(ctx, include_name, include_paths)]
                # End header msg (found)
                ctx.end_msg(
                    "'%s' header found in %s"
                    % (include_name, ctx.get_env()["INCLUDES_" + use_name][-1])
                )
            except ctx.errors.ConfigurationError:
                ctx.end_msg("'%s' header not found" % (include_name), "YELLOW")
                if include_name in required:
                    raise ValueError(
                        "%s includes not found - header '%s' required missing"
                        % (use_name, include_name)
                    )
        # Remove duplicates
        ctx.get_env()["INCLUDES_" + use_name] = list(
            set(ctx.get_env()["INCLUDES_" + use_name])
        )
        # Start lib msg
        ctx.start_msg("Checking for %s includes" % str(use_name))
        # End include msg (found)
        ctx.end_msg(
            "%s include found in %s" % (use_name, ctx.get_env()[
                                        "INCLUDES_" + use_name])
        )
    except ValueError as err:
        # Start lib msg
        ctx.start_msg("Checking for %s includes" % str(use_name))
        # End include msg (not found)
        if mandatory:
            ctx.fatal(err)
        ctx.end_msg(err, "YELLOW")


def check_lib(ctx, use_name, folders, lib_names, paths, plugin=False, required=[]):
    # Check if lib required
    if use_name in ctx.get_env()["requires"]:
        mandatory = True
    else:
        mandatory = False

    # Set required component if not
    if not required:
        required = lib_names

    # OSX/Mac uses .dylib and GNU/Linux .so
    suffix = "dylib" if ctx.env["DEST_OS"] == "darwin" else "so"

    # Generate lib paths
    lib_paths = []
    for path in paths:
        if folders:
            for folder in folders:
                lib_paths.append(os.path.join(path, folder))
                lib_paths.append(os.path.join(path, "lib", folder))
                lib_paths.append(os.path.join(path, "lib64", folder))
                lib_paths.append(os.path.join(
                    path, "lib/x86_64-linux-gnu", folder))
                lib_paths.append(os.path.join(path, "lib/intel64", folder))
        lib_paths.append(path)
        lib_paths.append(os.path.join(path, "lib"))
        lib_paths.append(os.path.join(path, "lib64"))
        lib_paths.append(os.path.join(path, "lib/x86_64-linux-gnu"))
        lib_paths.append(os.path.join(path, "lib/intel64"))

    try:
        # Search component/plugin
        for lib_name in lib_names:
            # Start component/plugin msg
            ctx.start_msg(
                "Checking for '%s' component/plugin"
                % str(lib_name[3:] if lib_name[:3] == "lib" else lib_name)
            )
            try:
                try:
                    # Add shared path
                    ctx.get_env()["LIBPATH_" + use_name] = ctx.get_env()[
                        "LIBPATH_" + use_name
                    ] + [get_directory(ctx, lib_name + "." + suffix, lib_paths)]
                    # Add shared lib
                    if not plugin:
                        ctx.get_env()["LIB_" + use_name] = ctx.get_env()[
                            "LIB_" + use_name
                        ] + [lib_name[3:] if lib_name[:3] == "lib" else lib_name]
                    # End shared lib msg (found)
                    ctx.end_msg(
                        "'%s' component/plugin found in %s (shared)"
                        % (
                            lib_name[3:] if lib_name[:3] == "lib" else lib_name,
                            ctx.get_env()["LIBPATH_" + use_name][-1],
                        )
                    )
                except:
                    # Add static path
                    ctx.get_env()["STLIBPATH_" + use_name] = ctx.get_env()[
                        "STLIBPATH_" + use_name
                    ] + [get_directory(ctx, lib_name + ".a", lib_paths)]
                    # Add static lib
                    ctx.get_env()["STLIB_" + use_name] = ctx.get_env()[
                        "STLIB_" + use_name
                    ] + [lib_name[3:] if lib_name[:3] == "lib" else lib_name]
                    # End static lib msg (found)
                    ctx.end_msg(
                        "'%s' component/plugin found in %s (static)"
                        % (
                            lib_name[3:] if lib_name[:3] == "lib" else lib_name,
                            ctx.get_env()["STLIBPATH_" + use_name][-1],
                        )
                    )
            except ctx.errors.ConfigurationError:
                ctx.end_msg(
                    "'%s' component/plugin not found"
                    % (lib_name[3:] if lib_name[:3] == "lib" else lib_name),
                    "YELLOW",
                )
                if lib_name in required:
                    raise ValueError(
                        "%s lib not found - component/plugin '%s' required missing"
                        % (
                            use_name,
                            lib_name[3:] if lib_name[:3] == "lib" else lib_name,
                        )
                    )
        # Remove duplicates
        ctx.get_env()["LIBPATH_" + use_name] = list(
            set(ctx.get_env()["LIBPATH_" + use_name])
        )
        # Start lib msg
        ctx.start_msg("Checking for %s lib" % str(use_name))
        # End lib msg (found)
        ctx.end_msg(
            "%s lib found in %s"
            % (
                use_name,
                ctx.get_env()["LIBPATH_" + use_name]
                + ctx.get_env()["STLIBPATH_" + use_name],
            )
        )
    except ValueError as err:
        # Start lib msg
        ctx.start_msg("Checking for %s lib" % str(use_name))
        # Check if mandatory
        if mandatory:
            ctx.fatal(err)
        # If not don't stop
        ctx.end_msg(err, "YELLOW")


def check_config(ctx, folders, config_name, paths):
    # Generate include paths
    config_paths = []
    for path in paths:
        if folders:
            for folder in folders:
                config_paths.append(os.path.join(path, folder))
                config_paths.append(os.path.join(path, folder, "share/waf"))
        config_paths.append(path)
        config_paths.append(os.path.join(path, "share/waf"))

    # Check for configuration file
    ctx.start_msg("Checking for '%s' configuration file" %
                  str(config_name))
    try:
        # Config path
        config_dir = get_directory(ctx, config_name, config_paths)

        # Store libraries and required flags because they get overwritten
        libs = ctx.get_env()["libs"]
        requires = ctx.get_env()["requires"]
        ctx.env.load(os.path.join(config_dir, config_name))
        ctx.get_env()["libs"] += libs
        ctx.get_env()["requires"] += requires

        # End header msg (found)
        ctx.end_msg("'%s' config found in %s" %
                    (config_name, config_dir))
    except ctx.errors.ConfigurationError:
        ctx.end_msg("'%s' config not found" % (config_name), "YELLOW")
