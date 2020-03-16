#! /usr/bin/env python
# encoding: utf-8

import os
import os.path as osp


def get_directory(ctx, filename, dirs):
    res = ctx.find_file(filename, dirs)
    return res[: -len(filename) - 1]


def check_include(ctx, use_name, folder, include_names, paths, required=[]):
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
        if folder:
            include_paths.append(osp.join(path, "include", folder))
        include_paths.append(osp.join(path, "include"))

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
            "%s include found in %s" % (use_name, ctx.get_env()["INCLUDES_" + use_name])
        )
    except ValueError as err:
        # Start lib msg
        ctx.start_msg("Checking for %s includes" % str(use_name))
        # End include msg (not found)
        if mandatory:
            ctx.fatal(err)
        ctx.end_msg(err, "YELLOW")


def check_lib(ctx, use_name, folder, lib_names, paths, required=[]):
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
        if folder:
            lib_paths.append(osp.join(path, "lib", folder))
            lib_paths.append(osp.join(path, "lib/x86_64-linux-gnu", folder))
            lib_paths.append(osp.join(path, "lib/intel64", folder))
        lib_paths.append(osp.join(path, "lib"))
        lib_paths.append(osp.join(path, "lib/x86_64-linux-gnu"))
        lib_paths.append(osp.join(path, "lib/intel64"))

    try:
        # Search component/plugin
        for lib_name in lib_names:
            # Start component/plugin msg
            ctx.start_msg(
                "Checking for '%s' component/plugin"
                % str(lib_name[3:] if lib_name[:3] == "lib" else lib_name)
            )
            try:
                # Add path
                ctx.get_env()["LIBPATH_" + use_name] = ctx.get_env()[
                    "LIBPATH_" + use_name
                ] + [get_directory(ctx, lib_name + "." + suffix, lib_paths)]
                # Add lib
                ctx.get_env()["LIB_" + use_name] = ctx.get_env()["LIB_" + use_name] + [
                    lib_name[3:] if lib_name[:3] == "lib" else lib_name
                ]
                # End lib msg (found)
                ctx.end_msg(
                    "'%s' component/plugin found in %s"
                    % (
                        lib_name[3:] if lib_name[:3] == "lib" else lib_name,
                        ctx.get_env()["LIBPATH_" + use_name][-1],
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
            "%s lib found in %s" % (use_name, ctx.get_env()["LIBPATH_" + use_name])
        )
    except ValueError as err:
        # Start lib msg
        ctx.start_msg("Checking for %s lib" % str(use_name))
        # Check if mandatory
        if mandatory:
            ctx.fatal(err)
        # If not don't stop
        ctx.end_msg(err, "YELLOW")


def check_config(ctx, use_name, folder, config_names, paths, required=[]):
    pass