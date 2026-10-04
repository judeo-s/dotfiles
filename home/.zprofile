# Start Hyprland through UWSM when this login session is eligible.
if command -v uwsm >/dev/null 2>&1 && uwsm check may-start; then
	exec uwsm start hyprland.desktop
fi
