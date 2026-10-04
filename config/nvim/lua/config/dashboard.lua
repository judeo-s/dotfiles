-- Adapted from R7rainz/neovim-conf's Alpha dashboard.
local M = {}

function M.setup()
	local alpha = require("alpha")
	local dashboard = require("alpha.themes.dashboard")
	local quotes = {
		"What we assembled with trembling hands, rose to question its maker.",
		"The interface is quiet. The ideas are not.",
		"Precision over noise. Focus over frenzy.",
		"Write less. Mean more.",
		"Tools fade. Craft remains.",
		"A sharp editor reveals dull thinking.",
		"Small feedback loops build large systems.",
		"Clean edges, ruthless intent.",
		"Every keystroke is a design decision.",
		"Speed is earned by clarity.",
	}
	local quote = quotes[math.random(#quotes)]

	local function text(value)
		return { type = "text", val = value, opts = { position = "center", hl = "Comment" } }
	end

	local function grid_line(left, right)
		local function pad(value)
			return value .. string.rep(" ", math.max(0, 22 - vim.fn.strdisplaywidth(value)))
		end
		return text(" " .. pad(left) .. " | " .. pad(right))
	end

	local grid = {
		type = "group",
		val = {
			text(" ┌────────────────────────┬────────────────────────┐"),
			grid_line("[f] Find Files", "[r] Recent Files"),
			grid_line("[g] Find Text", "[d] Restore Directory"),
			grid_line("[c] Config", "[n] New File"),
			grid_line("[s] Restore Session", "[l] Lazy"),
			grid_line("[q] Quit", ""),
			text(" └────────────────────────┴────────────────────────┘"),
		},
		opts = { spacing = 0 },
	}

	local function footer()
		local stats = require("lazy").stats()
		local version = vim.version()
		return string.format(
			"%s  •  %d plugins  •  %.2fms  •  v%d.%d.%d",
			os.date("%d-%m-%Y  %H:%M"),
			stats.count,
			stats.startuptime or 0,
			version.major,
			version.minor,
			version.patch
		)
	end

	dashboard.section.header.opts.hl = "Comment"
	dashboard.section.footer.opts.hl = "Comment"
	dashboard.section.footer.val = footer()
	dashboard.config.layout = {
		{ type = "padding", val = 0 },
		dashboard.section.header,
		{ type = "padding", val = 2 },
		text(quote),
		{ type = "padding", val = 0 },
		grid,
		dashboard.section.footer,
	}
	alpha.setup(dashboard.opts)
	require("alpha_ascii").setup({ header = "random" })

	-- Keep the same artwork library while fitting smaller terminal windows.
	local original_header = vim.deepcopy(dashboard.section.header.val)
	local function fit_header()
		local max_width = math.max(1, math.floor(vim.o.columns * 0.68))
		local max_lines = math.max(1, vim.o.lines - 15)
		local first = math.max(1, math.floor((#original_header - max_lines) / 2) + 1)
		local lines = {}
		for i = first, math.min(#original_header, first + max_lines - 1) do
			lines[#lines + 1] = vim.fn.strcharpart(original_header[i], 0, max_width)
		end
		dashboard.section.header.val = lines
	end
	fit_header()

	local function picker(name, opts)
		vim.schedule(function()
			local options = require("telescope.themes").get_dropdown(vim.tbl_extend("force", {
				previewer = false,
				layout_strategy = "center",
				layout_config = { width = 0.82, height = 0.58 },
			}, opts or {}))
			require("telescope.builtin")[name](options)
		end)
	end

	local group = vim.api.nvim_create_augroup("RainzDashboard", { clear = true })
	vim.api.nvim_create_autocmd("FileType", {
		group = group,
		pattern = "alpha",
		callback = function(event)
			vim.opt_local.number = false
			vim.opt_local.relativenumber = false
			vim.opt_local.foldenable = false
			vim.opt_local.fillchars = { eob = " " }
			local actions = {
				f = function() picker("find_files") end,
				r = function() picker("oldfiles", { prompt_title = "Recent Files" }) end,
				g = function() picker("live_grep") end,
				d = "<cmd>AutoSession search<CR>",
				c = function() picker("find_files", { cwd = vim.fn.stdpath("config") }) end,
				n = "<cmd>enew<CR><cmd>startinsert<CR>",
				s = "<cmd>AutoSession restore<CR>",
				l = "<cmd>Lazy<CR>",
				q = "<cmd>quit<CR>",
			}
			for key, action in pairs(actions) do
				vim.keymap.set("n", key, action, { buffer = event.buf, silent = true, nowait = true })
			end
		end,
	})

	vim.api.nvim_create_autocmd("User", {
		group = group,
		pattern = { "AlphaReady", "LazyDone", "VeryLazy" },
		callback = function()
			dashboard.section.footer.val = footer()
			if vim.bo.filetype == "alpha" then
				vim.schedule(function() pcall(vim.cmd.AlphaRedraw) end)
			end
		end,
	})
	vim.api.nvim_create_autocmd("VimResized", {
		group = group,
		callback = function()
			fit_header()
			if vim.bo.filetype == "alpha" then
				pcall(vim.cmd.AlphaRedraw)
			end
		end,
	})
end

return M
