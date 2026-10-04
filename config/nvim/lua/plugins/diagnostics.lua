return {
	{
		"folke/trouble.nvim",
		cmd = "Trouble",
		opts = {},
		keys = {
			{ "<leader>xx", "<cmd>Trouble diagnostics toggle<CR>", desc = "Workspace diagnostics" },
			{ "<leader>xq", "<cmd>Trouble qflist toggle<CR>", desc = "Quickfix panel" },
		},
	},
}
