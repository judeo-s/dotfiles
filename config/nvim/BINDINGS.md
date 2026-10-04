# Neovim key bindings

Reference for this configuration: all explicitly configured key bindings, plus
the enabled editing defaults and contextual plugin mappings described below.
Plugin defaults were checked against the locally installed versions. Standard
Vim editing commands are documented in `:help index`; this is a configuration
reference rather than a replacement for that manual.

## Notation and modes

- **Leader** is **Space**: `<leader>ff` means Space, then `f`, then `f`.
- **Local leader** is **`,`** after startup. `lua/config/lazy.lua` initially sets
  it to `\`, but the VimTeX configuration changes it to `,`.
- Keys are case-sensitive: `Mm` means Shift+m, then lowercase m; it is not Alt+m.
- `<C-x>` = Ctrl+x; `<A-x>` / `<M-x>` = Alt+x; `<S-Tab>` = Shift+Tab.
- `<CR>` = Enter; `<BS>` = Backspace; `<Esc>` = Escape.
- `N` = Normal; `I` = Insert; `V` = Visual; `S` = Select;
  `O` = Operator-pending; `C` = Command-line; `T` = Terminal-input mode.
- Sequences such as `sv`, `gc`, and `<C-w><Left>` are pressed in order.
- Buffer-local mappings take precedence over global mappings. For example,
  Tab cycles Harpoon entries while editing, but selects items inside Neo-tree.

## Contents

- [General editing](#general-editing)
- [Windows and tabs](#windows-and-tabs)
- [Files, search, and pickers](#files-search-and-pickers)
- [Harpoon](#harpoon)
- [Git](#git)
- [Diagnostics and LSP](#diagnostics-and-lsp)
- [Completion, snippets, and pairs](#completion-snippets-and-pairs)
- [Comments and surrounding text](#comments-and-surrounding-text)
- [Neo-tree](#neo-tree)
- [Telescope and clipboard history](#telescope-and-clipboard-history)
- [Spectre search and replace](#spectre-search-and-replace)
- [Trouble](#trouble)
- [Diffview](#diffview)
- [LaTeX and VimTeX](#latex-and-vimtex)
- [Lspsaga windows](#lspsaga-windows)
- [Command-line completion](#command-line-completion)
- [Lazy and Mason](#lazy-and-mason)
- [Other Neovim defaults](#other-neovim-defaults)
- [Disabled bindings and precedence](#disabled-bindings-and-precedence)
- [Inspecting bindings](#inspecting-bindings)

## General editing

Source: `lua/config/keymaps.lua`, `lua/plugins/formatter.lua`, and
`lua/plugins/others.lua`.

| Keys | Mode | Action |
| --- | --- | --- |
| `<leader>n` | N | Toggle both absolute and relative line numbers |
| `H` | N | Move to first nonblank character (`^`) |
| `L` | N | Move to end of line (`$`) |
| `x` | N | Delete a character into the black-hole register, preserving clipboard/register contents |
| `p` | V, S | Replace selection without yanking the removed text (`"_dP`) |
| `jk` | I | Leave insert mode |
| `<A-j>` | N | Move current line down and reindent |
| `<A-k>` | N | Move current line up and reindent |
| `<A-j>` | V, S | Move selected lines down, reselect, and reindent |
| `<A-k>` | V, S | Move selected lines up, reselect, and reindent |
| `<leader>mp` | N, V, S | Format file or selected range using Conform, with LSP fallback |
| `<leader>r` | V, S | Open the refactoring selection menu |
| `<leader>md` | N | Toggle Markview Markdown rendering |
| `Q` | N | Execute current line through `zsh` and replace it with command output; requires `zsh` |
| `<Left>`, `<Right>`, `<Up>`, `<Down>` | N | Print a reminder to use `h`, `l`, `k`, `j`; do not move |
| `<Esc>` | T | Leave terminal-input mode and return to Normal mode |
| `<leader>L` | N | Open Lazy plugin manager |
| `<leader>M` | N | Open Mason tool/server manager |
| `<leader>?` | N | Show buffer-local bindings with Which-key |

Formatting also runs automatically on save. Ordinary yank/paste operations use
the system clipboard because `clipboard=unnamedplus` is enabled.

Markdown rendering is enabled automatically in Normal, Operator-pending, and
Command-line (`:`) modes. Insert and Visual modes show raw Markdown for editing.
`<leader>md` toggles rendering manually. The `markdown` and `markdown_inline`
Treesitter parsers are included in the configured parser list.

## Windows and tabs

Source: `lua/config/keymaps.lua`, `lua/plugins/others.lua`.

| Keys | Mode | Action |
| --- | --- | --- |
| `sv` | N | Create a vertical split and move to the next window |
| `ss` | N | Create a horizontal split |
| `se` | N | Equalize split sizes |
| `sh` / `sj` / `sk` / `sl` | N | Focus left / down / up / right window |
| `<C-w><Left>` / `<C-w><Right>` | N | Decrease / increase window width |
| `<C-w><Up>` / `<C-w><Down>` | N | Increase / decrease window height |
| `<leader>w` | N | Show window picker; press the displayed label (`1`–`8`) |
| `<leader>tn` | N | Open a new Neovim tab page |
| `<leader>tc` | N | Close current Neovim tab page |

Neovim tab pages are different from Neo-tree's Files/Buffers/Git source tabs.

## Files, search, and pickers

All entries below are **Normal mode** mappings.
Sources: `lua/plugins/others.lua`, `lua/plugins/search.lua`.

| Keys | Action |
| --- | --- |
| `\` | Open/reveal the current file in Neo-tree |
| `<leader>ff` | Telescope: find files |
| `<leader><leader>` | Telescope: recently opened files |
| `<leader>lg` | Telescope: live text search |
| `<leader>sg` | Telescope: live grep with ripgrep arguments |
| `<leader>sr` | Open Spectre project search/replace |
| `<leader>bu` | Telescope: open buffers, most recently used first |
| `<leader>fh` | Telescope: help tags |
| `<leader>man` | Telescope: man pages |
| `<leader>com` | Telescope: available commands |
| `<leader>gf` | Telescope: Git files |
| `<leader>gs` | Telescope: Git status |
| `<leader>cs` | Telescope: colorschemes |
| `<leader>cc` | Telescope: clipboard history (Neoclip) |

Search defaults to the current working directory. In `<leader>sg`, try
`"search term" -g '*.lua'` to search only Lua files. No automatic quote-prompt
shortcut is configured; `<C-k>` still moves up in this picker.

## Harpoon

Source: `lua/plugins/others.lua`; quick-menu defaults from Harpoon.

| Keys | Context | Action |
| --- | --- | --- |
| `Mm` | N, editing | Add current file to Harpoon and show a notification |
| `M1`, `M2`, `M3`, `M4`, `M5` | N, editing | Open Harpoon entry 1–5 |
| `<leader>mm` | N | Toggle Harpoon quick menu |
| `<Tab>` | N, editing | Next Harpoon entry, wrapping; `:bnext` if list is empty |
| `<S-Tab>` | N, editing | Previous Harpoon entry, wrapping; `:bprevious` if list is empty |
| `<CR>` | N, quick menu | Open selected entry |
| `q`, `<Esc>` | N, quick menu | Close menu |

The quick menu is editable: normal buffer edits such as `dd` remove entries;
reorder lines to reorder the list.

## Git

Sources: `lua/plugins/git.lua`, `lua/plugins/others.lua`.

| Keys | Mode/context | Action |
| --- | --- | --- |
| `<leader>hp` | N, Gitsigns-attached file | Preview hunk |
| `<leader>hs` | N, Gitsigns-attached file | Stage hunk |
| `<leader>hr` | N, Gitsigns-attached file | Reset hunk (discard its changes) |
| `<leader>hb` | N, Gitsigns-attached file | Show blame for current line |
| `<leader>gd` | N | Open Diffview |
| `<leader>gx` | N | Close Diffview |

Gitsigns mappings are buffer-local. Additional Git actions are available in
Neo-tree's Git source, Telescope's Git pickers, and Diffview below.

## Diagnostics and LSP

The first two bindings are configured in `lua/plugins/diagnostics.lua`.
The remaining bindings are provided by the installed Neovim 0.12 runtime;
LSP actions require an attached server supporting the operation.

| Keys | Mode | Action |
| --- | --- | --- |
| `<leader>xx` | N | Toggle workspace diagnostics in Trouble |
| `<leader>xq` | N | Toggle quickfix list in Trouble |
| `grn` | N | Rename symbol |
| `gra` | N, V | Code actions |
| `grr` | N | References |
| `gri` | N | Implementations |
| `grt` | N | Type definition |
| `grx` | N | Run code lens |
| `gO` | N | Document symbols |
| `K` | N, supported LSP buffer | Hover documentation (may be overridden by filetype plugins) |
| `<C-s>` | I, S | Signature help |
| `[d` / `]d` | N | Previous / next diagnostic |
| `[D` / `]D` | N | First / last diagnostic in current buffer |
| `<C-w>d`, `<C-w><C-d>` | N | Show diagnostics under cursor |

Your config also opens diagnostic floats automatically on cursor hold. The
optional `E` diagnostics-toggle mapping is **not enabled**. There are no custom
`gd`, `gD`, or `<leader>rn` LSP mappings in this configuration.

## Completion, snippets, and pairs

Source: `lua/plugins/cmp.lua`; Mini and autopairs defaults.

| Keys | Mode/context | Action |
| --- | --- | --- |
| `<Tab>` | I | Next completion item if popup is visible; otherwise insert Tab |
| `<S-Tab>` | I | Previous completion item if popup is visible; otherwise normal Shift+Tab |
| `<C-Space>` | I | Trigger Mini two-stage completion |
| `<A-Space>` | I | Trigger fallback completion |
| `<C-f>` / `<C-b>` | I | Scroll Mini info/signature window down / up |
| `<C-j>` | I | Expand snippet |
| `<C-l>` | I, active snippet | Jump to next snippet tabstop |
| `<C-h>` | I, active snippet | Jump to previous snippet tabstop |
| `<C-c>` | I, active snippet | Stop snippet session |
| `<CR>` | I | Autopairs completion confirmation / pair-aware newline (see note) |
| `<BS>` | I, autopairs buffer | Pair-aware deletion |

The snippet jump/stop mappings exist only during an active MiniSnippets session.
Typing opening brackets or quotes also invokes autopairs rules automatically.

**Enter precedence:** `cmp.lua` initially maps Enter to confirm a selected
completion, or confirm and insert a newline when none is selected. Autopairs
loads on `InsertEnter` and replaces that mapping with its own handler. The
effective binding after entering Insert mode is autopairs' `completion_confirm`.

## Comments and surrounding text

These are enabled plugin defaults from Comment.nvim and nvim-surround.

### Comment.nvim

| Keys | Mode | Action |
| --- | --- | --- |
| `gcc` | N | Toggle current line comment; accepts a count |
| `gc{motion}` | N | Toggle line comments over a motion |
| `gc` | V | Toggle line comments on selection |
| `gbc` | N | Toggle block comment on current line |
| `gb{motion}` | N | Toggle block comment over a motion |
| `gb` | V | Toggle block comment on selection |
| `gco` | N | Insert commented line below and enter Insert mode |
| `gcO` | N | Insert commented line above and enter Insert mode |
| `gcA` | N | Append comment at end of line and enter Insert mode |

Neovim also supplies the `gc` comment text object in Operator-pending mode.

### nvim-surround

| Keys | Mode | Action |
| --- | --- | --- |
| `ys{motion}{surround}` | N | Add surrounding pair to motion |
| `yss{surround}` | N | Surround current line |
| `yS{motion}{surround}` | N | Surround motion with delimiters on separate lines |
| `ySS{surround}` | N | Surround current line with delimiters on separate lines |
| `ds{surround}` | N | Delete surrounding pair |
| `cs{old}{new}` | N | Change surrounding pair |
| `cS{old}{new}` | N | Change pair, placing replacements on separate lines |
| `S{surround}` | V | Surround selection |
| `gS{surround}` | V | Surround selection with delimiters on separate lines |
| `<C-g>s` | I | Add surrounding pair around cursor |
| `<C-g>S` | I | Add surrounding pair on separate lines |

Examples: `ysiw"` surrounds a word with quotes, `ds"` removes surrounding quotes,
and `cs"'` changes double quotes to single quotes.

## Neo-tree

Open with `\`. These bindings apply with focus **inside Neo-tree** in Normal
mode. Source tabs are **Files → Buffers → Git**. Customizations live in
`lua/plugins/others.lua`; other entries below come from installed defaults.

### Common tree controls

| Keys | Action |
| --- | --- |
| `<` / `>` | Previous / next source tab (usually Shift+, / Shift+.) |
| `<CR>`, double left-click | Open item / expand directory |
| `<Space>` | Toggle node expansion |
| `<C-s>` | Quick-jump using displayed labels, then open/toggle target |
| `<Tab>` | Select item |
| `<C-S-i>` | Invert selection |
| `<C-;>` | Clear selection |
| `S` / `s` | Open in horizontal / vertical split |
| `t` | Open in new tab page |
| `w` | Open using window picker |
| `P` | Toggle floating preview |
| `l` | Focus preview |
| `<C-b>` | Scroll preview (configured direction `10`) |
| `<C-f>` | Scroll preview (direction `-10`), except Files uses directory grep |
| `<Esc>` | Cancel preview / floating tree |
| `C` | Close node |
| `z` | Close all nodes |
| `R` | Refresh |
| `a` | Add file or directory by name |
| `A` | Add directory; Git source overrides this to stage all |
| `d` | Delete item; Buffers source overrides this to delete buffer |
| `T` | Move item to trash (requires a supported trash utility) |
| `u` / `U` | Undo trash operation / restore from trash |
| `r` | Rename |
| `y` / `x` / `p` | Copy / cut / paste using Neo-tree's file clipboard |
| `<C-r>` | Clear Neo-tree clipboard |
| `c` / `m` | Copy / move to entered destination |
| `e` | Toggle automatic width expansion |
| `q` | Close tree window |
| `?` | Show local mapping help |

### Files source

| Keys | Action |
| --- | --- |
| `\` | Close tree window (custom) |
| `Y` | Copy absolute path to unnamed and system clipboard registers (custom) |
| `<C-f>` | Close tree and Telescope-grep selected directory, or selected file's parent (custom) |
| `H` | Toggle hidden files |
| `/` | Fuzzy-find files |
| `D` | Fuzzy-find directories |
| `#` | Fuzzy-sort |
| `f` | Filter on submit |
| `<C-x>` | Clear filter |
| `<BS>` | Navigate up one directory |
| `.` | Set selected directory as root |
| `[g` / `]g` | Previous / next Git-modified file |
| `i` | Show file details |
| `b` | Rename basename |
| `o` | Show ordering menu |
| `oc` / `od` / `og` | Order by creation time / diagnostics / Git status |
| `om` / `on` / `os` / `ot` | Order by modification time / name / size / type |

Fuzzy-finder popup: `<Down>` / `<C-n>` and `<Up>` / `<C-p>` move the cursor;
`j` / `k` do so in Normal mode. `<Esc>` closes, `<S-CR>` closes keeping the
filter, `<C-CR>` closes clearing the filter, and `<C-w>` deletes a word.

### Buffers and Git sources

Both provide `i`, `b`, `o`, `oc`, `od`, `om`, `on`, `os`, and `ot` as above.
Buffers also provides `<BS>` and `.` as above.

| Keys | Source | Action |
| --- | --- | --- |
| `d`, `bd` | Buffers | Delete selected buffer |
| `A` | Git | Stage all files |
| `ga` | Git | Stage selected file |
| `gu` | Git | Unstage selected file |
| `gt` | Git | Toggle selected file's staged state |
| `gr` | Git | Revert selected file |
| `gc` | Git | Commit |
| `gp` | Git | Push |
| `gl` | Git | Pull |
| `gg` | Git | Commit and push |
| `gU` | Git | Undo last commit |

Use `q` to close any source. The custom `\` close binding is Files-only.

## Telescope and clipboard history

### Common picker controls

These are local to Telescope prompts. Pickers normally start in Insert mode;
Escape enters Normal mode, and another Escape closes.

| Keys | Mode | Action |
| --- | --- | --- |
| `<C-j>` / `<C-k>` | I | Next / previous item (custom) |
| `<C-n>` / `<C-p>` | I | Next / previous item |
| `<Down>` / `<Up>` | I, N | Next / previous item |
| `j` / `k` | N | Next / previous item |
| `H`, `gg` / `M` / `L`, `G` | N | First / middle / last item |
| `<CR>` | I, N | Open/accept selection |
| `<C-x>` / `<C-v>` / `<C-t>` | I, N | Open in horizontal split / vertical split / tab |
| `<C-c>` | I | Close picker |
| `<Esc>` | N | Close picker |
| `<Tab>` / `<S-Tab>` | I, N | Toggle selection and move to worse / better match |
| `<C-u>` / `<C-d>` | I, N | Scroll preview up / down |
| `<PageUp>` / `<PageDown>` | I, N | Scroll results up / down |
| `<C-q>` | I, N | Send results to quickfix and open it |
| `<A-q>` | I, N | Send selected results to quickfix and open it |
| `<C-l>` | I | Complete tag |
| `<C-w>` | I | Delete previous word |
| `<C-/>`, `<C-_>` | I | Show picker bindings |
| `?` | N | Show picker bindings |
| `<C-d>` | I, buffers picker | Delete selected buffer (overrides preview scrolling) |

Some specialized pickers add actions; use the picker help keys for that view.

### Neoclip (`<leader>cc`)

Neoclip overrides several common Telescope mappings:

| Insert-mode keys | Normal-mode keys | Action |
| --- | --- | --- |
| `<CR>` | `<CR>` | Put selected entry into default register |
| `<C-p>` | `p` | Paste after cursor |
| `<C-k>` | `P` | Paste before cursor |
| `<C-q>` | `q` | Replay selected macro entry |
| `<C-d>` | `d` | Delete history entry |
| `<C-e>` | `e` | Edit history entry |

## Spectre search and replace

Open with `<leader>sr`. These are Normal-mode mappings in the Spectre panel.

| Keys | Action |
| --- | --- |
| `<Tab>` / `<S-Tab>` | Next / previous query field |
| `dd` | Include/exclude result item |
| `<CR>` | Open selected file/result |
| `<leader>q` | Send results to quickfix |
| `<leader>c` | Input replacement command |
| `<leader>o` | Show options |
| `<leader>rc` | Replace current item |
| `<leader>R` | Replace all enabled results |
| `<leader>v` | Change result view mode |
| `trs` / `tro` | Select sed / oxi replacement engine (engine must be installed) |
| `tu` | Toggle update-on-write |
| `ti` | Toggle case-insensitive search |
| `th` | Toggle hidden-file search |
| `<leader>l` | Resume last search |
| `<leader>rp` | Pick replacement template |
| `<leader>rd` | Delete matching line |

## Trouble

Open using `<leader>xx` or `<leader>xq`, then focus its window with your split
navigation or `<leader>w`. Trouble defaults to opening without stealing focus.
All following mappings are Normal mode except the explicitly marked Visual one.

| Keys | Action |
| --- | --- |
| `?` | Help |
| `r` / `R` | Refresh / toggle automatic refresh |
| `q` / `<Esc>` | Close / cancel |
| `<CR>`, double left-click | Jump to item |
| `o` | Jump and close |
| `<C-s>` / `<C-v>` | Jump in horizontal / vertical split |
| `}`, `]]` / `{`, `[[` | Next / previous item |
| `dd` | Delete item where source supports it |
| `d` (V) | Delete selected items where supported |
| `i` | Inspect item |
| `p` / `P` | Preview / toggle automatic preview |
| `gb` | Toggle current-buffer filter |
| `s` | Cycle severity filter |
| `zo` / `zO` | Open fold / open recursively |
| `zc` / `zC` | Close fold / close recursively |
| `za` / `zA` | Toggle fold / toggle recursively |
| `zm` / `zM` | Fold more / close all folds |
| `zr` / `zR` | Fold less / open all folds |
| `zx` / `zX` | Update folds / update all folds |
| `zn` / `zN` / `zi` | Disable / enable / toggle folding |

## Diffview

Open with `<leader>gd`, close with `<leader>gx`. Mappings below are installed
Diffview defaults and are local to its tab/windows.

### Diff buffers and panels

| Keys | Mode | Action |
| --- | --- | --- |
| `<Tab>` / `<S-Tab>` | N | Open next / previous file diff |
| `[F` / `]F` | N | Open first / last file diff |
| `gf` | N | Open file in previous tab page |
| `<C-w><C-f>` | N | Open file in a split |
| `<C-w>gf` | N | Open file in a new tab page |
| `<leader>e` | N | Focus file panel |
| `<leader>b` | N | Toggle file panel |
| `g<C-x>` | N | Cycle layouts |
| `g?` | N | Contextual help |
| `[x` / `]x` | N, diff/file panel | Previous / next merge conflict |

### File panel

| Keys | Action (N) |
| --- | --- |
| `j`, `<Down>` / `k`, `<Up>` | Next / previous entry |
| `<CR>`, `o`, `l`, double left-click | Open selected diff |
| `-`, `s` | Toggle stage/unstage for entry |
| `S` / `U` | Stage / unstage all entries |
| `X` | Restore entry to left-side state |
| `L` | Open commit log |
| `zo` / `h`, `zc` / `za` | Open / close / toggle fold |
| `zR` / `zM` | Open / close all folds |
| `<C-b>` / `<C-f>` | Scroll diff view up / down |
| `i` | Toggle list/tree layout |
| `f` | Toggle flattened empty directories |
| `R` | Refresh file list |

### Merge conflict resolution

| Keys | Context | Action |
| --- | --- | --- |
| `<leader>co` / `<leader>ct` / `<leader>cb` / `<leader>ca` | N, diff buffer | Choose ours / theirs / base / all for current conflict |
| `dx` | N, diff buffer | Choose none: delete current conflict region |
| `<leader>cO` / `<leader>cT` / `<leader>cB` / `<leader>cA` | N, diff buffer or file panel | Choose ours / theirs / base / all for entire file |
| `dX` | N, diff buffer or file panel | Delete all conflict regions in file |
| `2do` / `3do` | N, V, 3-way or 4-way diff | Obtain hunk from ours / theirs |
| `1do` | N, V, 4-way diff | Obtain hunk from base |

### File history and auxiliary panels

Open history with `:DiffviewFileHistory` (no custom global key).
The history panel shares entry navigation/opening, fold controls, scrolling,
`L`, `X`, and the common diff/panel controls above. It additionally binds:

| Keys | Context | Action |
| --- | --- | --- |
| `g!` | History | Open options |
| `<C-A-d>` | History | Open selected history entry in a Diffview |
| `y` | History | Copy commit hash |
| `<Tab>` | Options | Change selected option |
| `q` | Options/help | Close panel |
| `g?` | Options | Show help |
| `<Esc>` | Help | Close help |

## LaTeX and VimTeX

VimTeX defaults are buffer-local to TeX files. The actual local leader is `,`.
Build/view operations use `latexmk` and Zathura as configured in
`lua/plugins/others.lua`; those programs must be installed.

### Project commands

| Keys | Mode | Action |
| --- | --- | --- |
| `,li` / `,lI` | N | Show project info / full info |
| `,lx` / `,lX` | N | Reload VimTeX / reload project state |
| `,ls` | N | Toggle main file |
| `,lq` | N | Show log |
| `,la` | N | Context menu |
| `,ll` | N | Start/toggle continuous compilation |
| `,lS` | N | Single-shot compilation |
| `,lo` | N | Show compiler output |
| `,lL` | N, V | Compile selected portion |
| `,lk` / `,lK` | N | Stop current / all compilers |
| `,le` | N | Show compilation errors |
| `,lc` / `,lC` | N | Clean auxiliary files / full clean |
| `,lg` / `,lG` | N | Current / all compiler status |
| `,lt` / `,lT` | N | Open / toggle table of contents |
| `,lv` | N | Open PDF viewer / forward search |
| `,lm` | N | Show insert-mode mapping list |
| `K` | N | Documentation for package under cursor |

### Structural editing

| Keys | Mode | Action |
| --- | --- | --- |
| `csc` / `dsc` | N | Change / delete surrounding command |
| `cse` / `dse` | N | Change / delete surrounding environment |
| `cs$` / `ds$` | N | Change / delete surrounding math environment |
| `csd` / `dsd` | N | Change math delimiters / delete delimiters |
| `tsc` | N | Toggle command star |
| `tss` | N | Toggle environment star |
| `tse` | N | Toggle environment |
| `ts$` | N | Toggle math environment |
| `tsb` | N | Toggle command line break |
| `tsf` | N, V | Toggle fraction form |
| `tsd` / `tsD` | N, V | Cycle delimiter modifiers forward / backward |
| `<F6>` | N, V | Surround line / selection with an environment |
| `<F7>` | N, V, I | Create LaTeX command |
| `<F8>` | N | Add modifiers to surrounding math delimiters |
| `]]` | I | Close current environment or delimiter |

### Motions and text objects

Motions apply in **N, V, O**. The bracket indicates direction: `[` previous,
`]` next. For paired lowercase/uppercase letters, lowercase targets the start
and uppercase targets the end.

| Keys | Target |
| --- | --- |
| `%` | Matching delimiter/environment |
| `[[` / `]]` | Previous / next section start |
| `[]` / `][` | Previous / next section end |
| `[m`, `]m` / `[M`, `]M` | Environment start / end |
| `[n`, `]n` / `[N`, `]N` | Math-zone start / end |
| `[r`, `]r` / `[R`, `]R` | Frame start / end |
| `[/`, `]/` / `[*`, `]*` | Comment start / end |

Text objects apply in **V, O**: `i` selects inside, `a` selects around.

| Inside / around | Object |
| --- | --- |
| `ic` / `ac` | Command |
| `id` / `ad` | Delimiters |
| `ie` / `ae` | Environment |
| `i$` / `a$` | Math environment |
| `iP` / `aP` | Section |
| `im` / `am` | Item |

### Math insert shortcuts

These **Insert-mode** shortcuts are math-context mappings. Prefix the suffix in
the tables with a **backtick**. For example, backtick then `a` inserts `\alpha`.
`,lm` displays the installed list in Neovim.

| Suffix | Expansion | Suffix | Expansion |
| --- | --- | --- | --- |
| `a` | `\alpha` | `b` | `\beta` |
| `c` | `\chi` | `d` | `\delta` |
| `e` | `\epsilon` | `f` | `\phi` |
| `g` | `\gamma` | `h` | `\eta` |
| `i` | `\iota` | `k` | `\kappa` |
| `l` | `\lambda` | `m` | `\mu` |
| `n` | `\nu` | `p` | `\pi` |
| `q` | `\theta` | `r` | `\rho` |
| `s` | `\sigma` | `t` | `\tau` |
| `u` | `\upsilon` | `w` | `\omega` |
| `x` | `\xi` | `y` | `\psi` |
| `z` | `\zeta` | `D` | `\Delta` |
| `F` | `\Phi` | `G` | `\Gamma` |
| `L` | `\Lambda` | `P` | `\Pi` |
| `Q` | `\Theta` | `S` | `\Sigma` |
| `U` | `\Upsilon` | `W` | `\Omega` |
| `X` | `\Xi` | `Y` | `\Psi` |
| `ve` | `\varepsilon` | `vf` | `\varphi` |
| `vk` | `\varkappa` | `vp` | `\varpi` |
| `vq` | `\vartheta` | `vr` | `\varrho` |
| `0` | `\emptyset` | `2` | `\sqrt` |
| `6` | `\partial` | `8` | `\infty` |
| `=` | `\equiv` | `\` | `\setminus` |
| `.` | `\cdot` | `*` | `\times` |
| `<` | `\langle` | `>` | `\rangle` |
| `H` | `\hbar` | `+` | `\dagger` |
| `[` | `\subseteq` | `]` | `\supseteq` |
| `(` | `\subset` | `)` | `\supset` |
| `A` | `\forall` | `B` | `\boldsymbol` |
| `E` | `\exists` | `N` | `\nabla` |
| `jj` | `\downarrow` | `jJ` | `\Downarrow` |
| `jk` | `\uparrow` | `jK` | `\Uparrow` |
| `jh` | `\leftarrow` | `jH` | `\Leftarrow` |
| `jl` | `\rightarrow` | `jL` | `\Rightarrow` |

Two backticks insert two literal backticks. Math-style shortcuts use a different
prefix: `#b` → `mathbf`, `#B` → `mathbb`, `#c` → `mathcal`, `#f` → `mathfrak`,
`#/` → `slashed`, and `#-` → `overline` through VimTeX's math-style handler.

## Lspsaga windows

Your config enables Lspsaga, but gives it **no global launch mappings**. Run
commands such as `:Lspsaga finder`, `:Lspsaga outline`, `:Lspsaga code_action`,
or `:Lspsaga peek_definition`. The following are its default contextual keys.

| Window | Keys and actions |
| --- | --- |
| Preview scrolling | `<C-f>` down; `<C-b>` up |
| Hover | `gx` opens link using the configured default browser command |
| Diagnostics | `o` execute action; `<CR>` toggle/jump; `q` quit; `q` or `<Esc>` close diagnostic display; displayed numbers select shortcuts |
| Code actions | `<CR>` execute; `q` quit; displayed numbers select actions |
| Finder | `[w` shuttle focus; `o` toggle/open; `s` vertical split; `i` horizontal split; `t` tab edit; `r` new tab; `q` quit; `<C-c>k` close |
| Peek definition | `<C-o>` edit; `<C-v>` vertical split; `<C-x>` horizontal split; `<C-t>` tab edit; `<C-c>n` new tab; `q` quit; `<Esc>` close |
| Rename | `<CR>` execute; `<C-k>` quit; `x` select in project rename view |
| Outline | `o` toggle/jump; `e` jump; `q` quit |
| Call/type hierarchy | `e` edit; `s` vertical split; `i` horizontal split; `t` tab edit; `[w` shuttle focus; `u` toggle/request; `q` quit; `<C-c>k` close |

## Command-line completion

Wilder is enabled for `:`, `/`, and `?` prompts.

| Keys | Mode | Action |
| --- | --- | --- |
| `<Tab>` | C | Next Wilder completion when active; otherwise normal Tab |
| `<S-Tab>` | C | Previous Wilder completion when active; otherwise normal Shift+Tab |
| `<Down>` | C | Accept completion when possible; otherwise normal Down |
| `<Up>` | C | Reject completion when possible; otherwise normal Up |

## Lazy and Mason

These keys are local to each manager's Normal-mode UI.

### Lazy (`<leader>L`)

| Keys | Action |
| --- | --- |
| `H` | Plugin list/home |
| `I` / `i` | Install missing plugins / selected plugin |
| `U` / `u` | Update all / selected plugin |
| `S` | Sync: install, clean, and update |
| `X` / `x` | Clean unused plugins / delete selected plugin |
| `C` / `c` | Check updates for all / selected plugin |
| `L` / `gl` | Recent update log for all / selected plugin |
| `R` / `r` | Restore lockfile versions / selected plugin or commit |
| `gb` | Build selected plugin |
| `P` / `D` | Profiling / debug view |
| `?` | Help |
| `<CR>` | Toggle plugin details |
| `K` | Hover information |
| `d` | Diff |
| `]]` / `[[` | Next / previous plugin |
| `<C-s>` / `<C-f>` | Profile sort / filter |
| `<C-c>` | Abort running tasks |
| `q` | Close |

### Mason (`<leader>M`)

| Keys | Action |
| --- | --- |
| `<CR>` | Expand package / toggle installation log |
| `i` | Install selected package |
| `u` / `U` | Update selected / all installed packages |
| `c` / `C` | Check selected package version / all outdated packages |
| `X` | Uninstall selected package |
| `<C-c>` | Cancel installation |
| `<C-f>` | Apply language filter |
| `g?` | Toggle help |

## Other Neovim defaults

These useful runtime mappings were observed in the installed Neovim 0.12.
They supplement the LSP defaults already listed. Filetype/plugin mappings can
override them, especially in TeX and tree/picker windows.

| Keys | Mode | Action |
| --- | --- | --- |
| `[b` / `]b`, `[B` / `]B` | N | Previous / next buffer; first / last buffer |
| `[q` / `]q`, `[Q` / `]Q` | N | Previous / next quickfix entry; first / last entry |
| `[<C-q>` / `]<C-q>` | N | Previous / next file in quickfix |
| `[l` / `]l`, `[L` / `]L` | N | Previous / next location-list entry; first / last entry |
| `[<C-l>` / `]<C-l>` | N | Previous / next file in location list |
| `[a` / `]a`, `[A` / `]A` | N | Previous / next argument-list file; first / last file |
| `[t` / `]t`, `[T` / `]T` | N | Previous / next tag; first / last tag |
| `[<C-t>` / `]<C-t>` | N | Previous / next preview tag |
| `[<Space>` / `]<Space>` | N | Add empty line above / below |
| `Y` | N | Yank from cursor to end of line |
| `<C-l>` | N | Clear search highlighting and redraw |
| `gx` | N, V | Open path/URI with system handler |
| `%` / `g%` | N, V, O | Matchit forward / backward matching item |
| `[%` / `]%` | N, V, O | Matchit previous / next outer matching group |
| `a%` | V | Select matching group with Matchit |
| `in` / `an` | V, O | Treesitter inner child / outer parent node |
| `[n` / `]n` | V | Previous / next Treesitter node |
| `[N` / `]N` | V | Previous / next Treesitter sibling node |
| `*` / `#` | V | Search forward / backward for selection |
| `@` / `Q` | V | Execute macro / last macro over selected lines |
| `<Tab>` / `<S-Tab>` | S | Built-in snippet forward/backward jump if active; separate from MiniSnippets |

## Disabled bindings and precedence

- `<leader>rw` belongs to **inc-rename**, which has `enabled = false`; it is not
  an active shortcut. Use Neovim's `grn` with an LSP server instead.
- `E` appears as the default argument of an unused diagnostics-toggle function
  in `lsp.lua`. The config calls `enable_diagnostics_default()` instead.
- `<CR>` in Insert mode is replaced by autopairs after its lazy load, as noted
  above. The reference documents both the configured intent and effective map.
- `H`, `L`, `x`, `Q`, and the Normal-mode arrow keys override standard Vim
  behavior globally. Plugin buffer-local maps can override them again.
- `cs` is a surround operator in Normal mode, `<leader>cs` opens colorschemes,
  and TeX-specific `csc`/`cse` operate on LaTeX commands/environments.
- Inside Neoclip, `<C-k>` pastes before the cursor instead of moving up.
- VimTeX's local leader is `,`; the global Neo-tree shortcut remains `\`.
- Dashboard shortcuts may be generated from recent files/projects. Follow the
  labels displayed on that dashboard rather than treating them as fixed keys.
- Typr, Rustaceanvim, crates.nvim, Treesitter, and the visual/status plugins have
  no additional explicit global shortcuts in your config. Command entry points
  include `:Typr`, `:TyprStats`, `:RustLsp`, and `:TSUpdate`.

## Inspecting bindings

| Command/key | Purpose |
| --- | --- |
| `<leader>?` | Show buffer-local mappings via Which-key |
| `:map` | List Normal/Visual/Select/Operator-pending mappings |
| `:imap` / `:cmap` / `:tmap` | List Insert / Command-line / Terminal mappings |
| `:verbose nmap <Space>ff` | Find where a Normal-mode binding was last defined |
| `:verbose imap <CR>` | Inspect effective Insert-mode Enter binding |
| `:map <buffer>` | Inspect mappings local to current buffer |
| `:Telescope keymaps` | Search mappings interactively |
| Neo-tree `?`, Telescope `?` or `<C-/>`, Trouble `?`, Diffview `g?` | Contextual plugin help |
| `:help vimtex-default-mappings`, `,lm` in TeX | VimTeX mappings and insert shortcuts |
| `:help index` | Full standard Vim/Neovim key reference |

Mappings created by lazy-loaded plugins appear after loading the plugin;
buffer-local and snippet-session mappings appear only in their own contexts.
