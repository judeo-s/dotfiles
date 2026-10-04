#!/bin/sh
# The installer writes this machine-local file; it is not shared across hosts.
settings="${XDG_CONFIG_HOME:-$HOME/.config}/caelestia/machine.env"
if [ -r "$settings" ]; then
    . "$settings"
fi
export QT_QPA_PLATFORM=wayland
if [ "${CAELESTIA_VIRGL_WORKAROUND:-0}" = 1 ]; then
    # Tested on the Apple M4 / VirGL VM: Qt otherwise gets GL 2.1 and panel
    # background shaders fail. Do not enable by default on physical hardware.
    export QSG_RHI_BACKEND=opengl
    export MESA_GL_VERSION_OVERRIDE=3.3
    export MESA_GLSL_VERSION_OVERRIDE=330
fi
exec caelestia shell -d "$@"
