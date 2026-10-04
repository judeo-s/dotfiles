return {
	{
		"lewis6991/gitsigns.nvim",
		event = { "BufReadPre", "BufNewFile" },
		opts = {
			on_attach = function(bufnr)
				local gitsigns = require("gitsigns")
				local function map(lhs, rhs, desc)
					vim.keymap.set("n", lhs, rhs, { buffer = bufnr, desc = desc })
				end

				map("<leader>hp", gitsigns.preview_hunk, "Preview Git hunk")
				map("<leader>hs", gitsigns.stage_hunk, "Stage Git hunk")
				map("<leader>hr", gitsigns.reset_hunk, "Reset Git hunk")
				map("<leader>hb", gitsigns.blame_line, "Blame current line")
			end,
		},
	},
}
