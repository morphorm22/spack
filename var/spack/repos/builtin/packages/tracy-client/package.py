# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class TracyClient(CMakePackage):
    """A real time, nanosecond resolution, remote telemetry, hybrid frame and sampling
    profiler for games and other applications. Client library."""

    homepage = "https://github.com/wolfpld/tracy"
    url = "https://github.com/wolfpld/tracy/archive/v0.0.0.tar.gz"
    maintainers = ["msimberg"]

    version("master", git="https://github.com/wolfpld/tracy.git", branch="master")
    version(
        "0.8.1",
        sha256="004992012b2dc879a9f6d143cbf94d7ea30e88135db3ef08951605d214892891",
    )

    variant(
        "shared",
        default=True,
        description="Build the client library as a shared library",
    )

    variants = {
        "enable": (True, "Enable profiling"),
        "on_demand": (False, "On-demand profiling"),
        "callstack": (False, "Enfore callstack collection for tracy regions"),
        "no_callstack": (False, "Disable all callstack related functionality"),
        "no_callstack_inlines": (False, "Disables the inline functions in callstacks"),
        "only_localhost": (False, "Only listen on the localhost interface"),
        "no_broadcast": (
            False,
            "Disable client discovery by broadcast to local network",
        ),
        "only_ipv4": (
            False,
            "Tracy will only accept connections on IPv4 addresses (disable IPv6)",
        ),
        "no_code_transfer": (False, "Disable collection of source code"),
        "no_context_switch": (False, "Disable capture of context switches"),
        "no_exit": (
            False,
            "Client executable does not exit until all profile data is sent to server",
        ),
        "no_sampling": (False, "Disable call stack sampling"),
        "no_verify": (False, "Disable zone validation for C API"),
        "no_vsync_capture": (False, "Disable capture of hardware Vsync events"),
        "no_frame_image": (False, "Disable the frame image support and its thread"),
        "no_system_tracing": (False, "Disable systrace sampling"),
        "delayed_init": (
            False,
            "Enable delayed initialization of the library (init on first call)",
        ),
        "manual_lifetime": (
            False,
            "Enable the manual lifetime management of the profile",
        ),
        "fibers": (False, "Enable fibers support"),
        "no_crash_handler": (False, "Disable crash handling"),
        "timer_fallback": (False, "Use lower resolution timers"),
    }

    for k, v in variants.items():
        variant(k, default=v[0], description=v[1])

    def cmake_args(self):
        args = [
            self.define_from_variant("TRACY_%s" + k.upper(), v[0])
            for k, v in variants.items()
        ]
        args.append(self.define_from_variant("BUILD_SHARED_LIBS", "shared"))
        return args
