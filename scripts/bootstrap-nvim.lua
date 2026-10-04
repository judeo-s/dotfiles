-- Run inside headless Neovim so plugin/task failures propagate to install.sh.
local ok, err = xpcall(function()
	local lazy = require("lazy")
	local config = require("lazy.core.config")
	local plugin_state = require("lazy.core.plugin")
	local function check_tasks()
		local failures = {}
		for name, plugin in pairs(config.plugins) do
			if plugin.url and (not plugin._.installed or plugin_state.has_errors(plugin)) then
				failures[#failures + 1] = name
			end
		end
		if #failures > 0 then
			table.sort(failures)
			error("Plugin installation failed: " .. table.concat(failures, ", "))
		end
	end
	-- Explicitly retry missing plugins, then restore existing ones to the lockfile.
	lazy.install({ wait = true, lockfile = true, show = false })
	check_tasks()
	lazy.restore({ wait = true, show = false })
	check_tasks()
end, debug.traceback)

if not ok then
	vim.api.nvim_err_writeln(err)
	vim.cmd("cquit 1")
else
	vim.cmd("qa!")
end
