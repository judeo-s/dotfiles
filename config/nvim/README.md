# Neovim config

> [!WARNING]
> Supports Neovim 0.11 + only

> [!SUMMARY]
> Trying to keep it as simple as possible:

---

# Lsp

- lspconfig with neovim 0.11+ `vim.lsp.config/enable` features
- found in `lua/plugins/lsp.lua`
- add lsp to where you see things like these and add yours
  ```lua
  vim.lsp.config('server-name',
    {
      capabilities = globalcapabilites
      -- other bad configs
    }
  )
  vim.lsp.enable('server-name')
  ```
- or do `:Mason`

- Diagnostics , important, there are 2 functions (this is also found in `lsp.lua`)

  ```lua
      -- this will make diagnostics show constantly
      function enable_diagnostics_default()

      -- this will make diagnostics on Keybinding
      function enable_toggle_diagnostics(keybinding)

      -- default
      enable_diagnostics_default()
  ```

---

# Cmp & snip

- i dunno, nvim.mini handles it

---

# others

- found in `lua/plugins/others.lua`

  | plugin            | function                   |
  | ----------------- | -------------------------- |
  | neotree           | minimal file tree          |
  | harpoon           | minimal file buffer editor |
  | presence          | discord flex               |
  | whichkey          | helps find keybindings     |
  | nvim window       | easy window move           |
  | vimtex            | latex                      |
  | lualine           | the bar at the bottom      |
  | markview          | render md                  |
  | indent blank line | the color indent           |
  | typr              | mavis becon                |

---

# install Dependencies

- only for Archlinux
  `chmod +x ./install.sh`

---

# Git, diagnostics, and search

Workflow additions inspired by [coffebar's Neovim config](https://github.com/coffebar/dotfiles/tree/main/.config/nvim).
`<leader>` is Space. New plugins are installed automatically by Lazy on startup.

| Mapping | Action |
| --- | --- |
| `<leader>hp` | Preview Git hunk |
| `<leader>hs` | Stage Git hunk |
| `<leader>hr` | Reset Git hunk (discard its changes) |
| `<leader>hb` | Blame current line |
| `<leader>xx` | Toggle workspace diagnostics in Trouble |
| `<leader>xq` | Toggle quickfix panel in Trouble |
| `<leader>sg` | Telescope grep with ripgrep arguments |
| `<leader>sr` | Open Spectre search/replace |

Git mappings are buffer-local and become available when Gitsigns attaches to a file.
Configuration lives in `lua/plugins/git.lua`, `diagnostics.lua`, and `search.lua`.

Search uses the current working directory. In the argument-enabled picker, enter
`"search term" -g '*.lua'` to restrict results to Lua files. Spectre uses `rg` for
searching and `sed` for replacement; both must be on PATH. In Spectre, enter the
search/replacement text, review matches, then use `<leader>R` to replace all results
or `?` to view its mappings.

Neo-tree (`\`) now has Files/Buffers/Git source tabs, switched with `<` and `>`.
In its Files view, `Y` copies the selected item's absolute path to the unnamed and
system clipboard registers; `<C-f>` searches the selected directory (or the parent
directory of a selected file). These options are in `lua/plugins/others.lua`.

## Markdown rendering

Markview automatically renders Markdown in Normal mode and while entering `:`
commands. Insert and Visual modes show raw Markdown. Press `<leader>md` (Space,
then `m`, then `d`) to toggle rendering manually.

The `markdown` and `markdown_inline` Treesitter parsers are installed through the
parser list in `lua/plugins/others.lua`. On Neovim 0.12, `lua/config/autocmds.lua`
uses Neovim's bundled Markdown injection query for compatible inline and fenced
code parsing.
