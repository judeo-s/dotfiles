-- Preserve the desktop shortcut combinations while using Caelestia.
-- Window appearance remains controlled by the main Hyprland configuration.
hl.env("TERMINAL", "foot")

hl.on("hyprland.start", function()
    hl.exec_cmd('command -v caelestia >/dev/null 2>&1 && sh "$HOME/.config/caelestia/start.sh"')
    hl.exec_cmd("command -v cliphist >/dev/null 2>&1 && wl-paste --type text --watch cliphist store")
    hl.exec_cmd("command -v cliphist >/dev/null 2>&1 && wl-paste --type image --watch cliphist store")
end)

hl.bind("SUPER + SPACE", hl.dsp.exec_cmd("caelestia shell drawers toggle launcher"))
hl.bind("SUPER + A", hl.dsp.exec_cmd("caelestia shell drawers toggle dashboard"))
hl.bind("SUPER + SHIFT + V", hl.dsp.exec_cmd("caelestia clipboard"))
-- Nexus contains the wallpaper picker and shell settings.
hl.bind("SUPER + W", hl.dsp.exec_cmd("caelestia shell nexus open"))
hl.bind("SUPER + comma", hl.dsp.exec_cmd("caelestia shell nexus open"))
hl.bind("ALT + SHIFT + W", hl.dsp.exec_cmd("caelestia shell nexus open"))
hl.bind("ALT + SHIFT + comma", hl.dsp.exec_cmd("caelestia shell nexus open"))
hl.bind("SUPER + ESCAPE", hl.dsp.exec_cmd("caelestia shell drawers toggle session"))
hl.bind("SUPER + L", hl.dsp.global("caelestia:lock"))
-- Caelestia has no equivalent of Noctalia's carousel; retain window cycling.
hl.bind("ALT + TAB", hl.dsp.window.cycle_next())
hl.bind("SUPER + S", hl.dsp.exec_cmd("hyprshot -m region --clipboard"))

hl.bind("XF86AudioRaiseVolume",
    hl.dsp.exec_cmd("wpctl set-volume -l 1 @DEFAULT_AUDIO_SINK@ 5%+"),
    { locked = true, repeating = true })
hl.bind("XF86AudioLowerVolume",
    hl.dsp.exec_cmd("wpctl set-volume @DEFAULT_AUDIO_SINK@ 5%-"),
    { locked = true, repeating = true })
hl.bind("XF86AudioMute",
    hl.dsp.exec_cmd("wpctl set-mute @DEFAULT_AUDIO_SINK@ toggle"),
    { locked = true })
hl.bind("XF86AudioMicMute",
    hl.dsp.exec_cmd("wpctl set-mute @DEFAULT_AUDIO_SOURCE@ toggle"),
    { locked = true })
hl.bind("XF86MonBrightnessUp",
    hl.dsp.exec_cmd("brightnessctl -e4 -n2 set 5%+"),
    { locked = true, repeating = true })
hl.bind("XF86MonBrightnessDown",
    hl.dsp.exec_cmd("brightnessctl -e4 -n2 set 5%-"),
    { locked = true, repeating = true })
