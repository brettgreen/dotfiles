#!/bin/bash
# Bootstrap script for setting up a new machine

set -e

DOTFILES="$(cd "$(dirname "$0")" && pwd)"

echo "Installing Homebrew packages..."
brew install stow
brew install zellij
brew install --cask ghostty
brew install --cask font-jetbrains-mono
brew install --cask cursor

echo "Linking dotfiles with stow..."
cd "$DOTFILES"
stow -v zsh ghostty zellij git claude

# Cursor / VS Code settings (can't use stow — path has spaces)
echo "Linking Cursor settings..."
CURSOR_DIR="$HOME/Library/Application Support/Cursor/User"
mkdir -p "$CURSOR_DIR"
ln -sf "$DOTFILES/cursor/settings.json" "$CURSOR_DIR/settings.json"
ln -sf "$DOTFILES/cursor/keybindings.json" "$CURSOR_DIR/keybindings.json"

# VS Code gets the same settings as Cursor
echo "Linking VS Code settings..."
VSCODE_DIR="$HOME/Library/Application Support/Code/User"
mkdir -p "$VSCODE_DIR"
ln -sf "$DOTFILES/cursor/settings.json" "$VSCODE_DIR/settings.json"
ln -sf "$DOTFILES/cursor/keybindings.json" "$VSCODE_DIR/keybindings.json"

echo "Done! Open Ghostty to get started."
