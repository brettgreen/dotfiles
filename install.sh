#!/bin/bash
# Bootstrap script for setting up a new machine

set -e

echo "Installing Homebrew packages..."
brew install stow
brew install zellij
brew install --cask ghostty
brew install --cask font-jetbrains-mono

echo "Linking dotfiles with stow..."
cd "$(dirname "$0")"
stow -v zsh ghostty zellij git

echo "Done! Open Ghostty to get started."
