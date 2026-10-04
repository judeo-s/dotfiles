#
# ~/.bashrc
#

# If not running interactively, don't do anything
[[ $- != *i* ]] && return

if command -v eza >/dev/null 2>&1; then
    alias ls='eza --icons=auto --group-directories-first'
else
    alias ls='ls --color=auto'
fi
alias grep='grep --color=auto'
alias v='nvim'
PS1='[\u@\h \W]\$ '

# opencode
export PATH="$HOME/.local/bin:$HOME/.opencode/bin:$PATH"
