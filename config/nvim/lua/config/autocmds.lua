-- Treesitter's legacy Markdown directive is incompatible with Neovim 0.12.
-- Use Neovim's query so fenced code and inline Markdown still get parsed.
if vim.fn.has("nvim-0.12") == 1 then
	local query = vim.fn.readfile(vim.env.VIMRUNTIME .. "/queries/markdown/injections.scm")
	vim.treesitter.query.set("markdown", "injections", table.concat(query, "\n"))
end

-- highlight yanked text for 500ms after yanking
vim.api.nvim_create_autocmd("TextYankPost", {
	callback = function()
		vim.highlight.on_yank({
			higroup = "IncSearch",
			timeout = 500,
		})
	end,
})
