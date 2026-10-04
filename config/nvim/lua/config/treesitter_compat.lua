local M = {}

function M.setup()
	if vim.fn.has("nvim-0.12") ~= 1 then
		return
	end

	-- Neovim 0.12 removed the all=false query-handler compatibility option.
	-- The legacy Tree-sitter branch still uses it for single-node callbacks.
	local query = vim.treesitter.query
	local original_predicate = query.add_predicate
	local original_directive = query.add_directive
	local function adapt(register)
		return function(name, handler, opts)
			if type(opts) == "table" and opts.all == false then
				local legacy_handler = handler
				handler = function(match, ...)
					local nodes = {}
					for id, captured in pairs(match) do
						nodes[id] = type(captured) == "table" and captured[1] or captured
					end
					return legacy_handler(nodes, ...)
				end
				opts = { force = opts.force }
			end
			return register(name, handler, opts)
		end
	end

	query.add_predicate = adapt(original_predicate)
	query.add_directive = adapt(original_directive)
	-- Its plugin startup file may already have registered the old handlers.
	-- Re-register them through the adapter (the plugin uses force=true).
	package.loaded["nvim-treesitter.query_predicates"] = nil
	local ok, err = pcall(require, "nvim-treesitter.query_predicates")
	query.add_predicate = original_predicate
	query.add_directive = original_directive
	if not ok then
		error(err)
	end
end

return M
