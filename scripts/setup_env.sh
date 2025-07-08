#!/bin/bash

# Exit on any error
set -e

echo "Setting up development environment..."

# Install git and other utilities
echo "Installing system packages..."
apt-get update && apt-get install -y rsync wget git zsh tmux htop curl && rm -rf /var/lib/apt/lists/*


# Install oh-my-zsh
echo "Installing oh-my-zsh..."
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended

# Install powerlevel10k theme
echo "Installing powerlevel10k theme..."
git clone --depth=1 https://github.com/romkatv/powerlevel10k.git ${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/themes/powerlevel10k

# Install zsh-autosuggestions
echo "Installing zsh-autosuggestions..."
git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions

# Download zsh-syntax-highlighting
echo "Installing zsh-syntax-highlighting..."
git clone --depth=1 https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting

# Configure zsh plugins
echo "Configuring zsh plugins..."
sed -i 's/plugins=(git)/plugins=(git zsh-autosuggestions zsh-syntax-highlighting)/' ~/.zshrc

# Add zsh-completions to fpath
echo "Adding zsh-completions to fpath..."
echo 'fpath+=${ZSH_CUSTOM:-${ZSH:-~/.oh-my-zsh}/custom}/plugins/zsh-completions/src' >> ~/.zshrc

# Set git configuration
echo "Setting git configuration..."
git config --global user.name "Runyu Lu"
git config --global user.email "runyulu@umich.edu"

# put huggingface token
echo "Putting huggingface token..."
mkdir -p ~/.huggingface
if [ -n "$HUGGINGFACE_TOKEN" ]; then
    echo "$HUGGINGFACE_TOKEN" >> ~/.huggingface/token
    echo "Hugging Face token configured from environment variable"
else
    echo "Warning: HUGGINGFACE_TOKEN environment variable not set"
    echo "Please set it with: export HUGGINGFACE_TOKEN=your_token_here"
fi

apt update && apt install python3-pip
pip install huggingface-hub

echo "Environment setup complete!"
echo "To switch to zsh, run: exec zsh" 

exec zsh
