#!/usr/bin/env bash
set -o errexit

# Use existing Rust if present; otherwise install into $HOME (writable)
if command -v cargo >/dev/null 2>&1; then
  echo "Rust already available: $(cargo --version)"
else
  echo "Installing Rust toolchain to \$HOME..."
  export RUSTUP_HOME="$HOME/.rustup"
  export CARGO_HOME="$HOME/.cargo"
  export RUSTUP_INIT_SKIP_PATH_CHECK=yes
  curl https://sh.rustup.rs -sSf | sh -s -- -y --no-modify-path
fi

# Ensure cargo is on PATH for this shell
if [ -f "$HOME/.cargo/env" ]; then
  # shellcheck disable=SC1090
  source "$HOME/.cargo/env"
fi

# Python deps
pip install --upgrade pip
pip install -r requirements.txt
