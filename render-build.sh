#!/usr/bin/env bash
set -o errexit

# Install Rust (needed for pydantic-core/orjson on Py 3.13)
curl https://sh.rustup.rs -sSf | sh -s -- -y
source "$HOME/.cargo/env"

# Install Python deps
pip install --upgrade pip
pip install -r requirements.txt
