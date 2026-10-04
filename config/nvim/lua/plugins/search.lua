return {
	{
		"nvim-telescope/telescope-live-grep-args.nvim",
		dependencies = { "nvim-telescope/telescope.nvim" },
		keys = {
			{
				"<leader>sg",
				function()
					require("telescope").extensions.live_grep_args.live_grep_args()
				end,
				desc = "Grep with arguments",
			},
		},
		config = function()
			require("telescope").load_extension("live_grep_args")
		end,
	},
	{
		"nvim-pack/nvim-spectre",
		dependencies = { "nvim-lua/plenary.nvim" },
		cmd = "Spectre",
		opts = {},
		keys = {
			{
				"<leader>sr",
				function()
					require("spectre").open()
				end,
				desc = "Project search and replace",
			},
		},
	},
}
