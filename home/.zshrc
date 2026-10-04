# Use an installed UTF-8 locale so ZLE measures Starship's Unicode correctly.
export LANG=C.UTF-8

# History
HISTFILE=~/.zsh_history
HISTSIZE=10000
SAVEHIST=10000
setopt SHARE_HISTORY HIST_IGNORE_DUPS

# Completion
autoload -Uz compinit && compinit
zstyle ':completion:*' menu select
zstyle ':completion:*' matcher-list 'm:{a-z}={A-Z}'


#PROMPT='%F{blue}%~%f %# '

if command -v eza >/dev/null 2>&1; then
    alias ls='eza --icons=auto --group-directories-first'
else
    alias ls='ls --color=auto'
fi
alias grep='grep --color=auto'
alias v='nvim'

# opencode
export PATH="$HOME/.local/bin:$HOME/.opencode/bin:$PATH"

# Starship
command -v starship >/dev/null 2>&1 && eval "$(starship init zsh)"

# Initialize ZLE plugins after the prompt; syntax highlighting must be last.
[[ -r /usr/share/zsh/plugins/zsh-autosuggestions/zsh-autosuggestions.zsh ]] && source /usr/share/zsh/plugins/zsh-autosuggestions/zsh-autosuggestions.zsh
[[ -r /usr/share/zsh/plugins/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh ]] && source /usr/share/zsh/plugins/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh
