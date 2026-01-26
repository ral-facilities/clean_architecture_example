#!/usr/bin/env bash
set -euo pipefail

DOCKERFILE_PATH="$1"
# Remove DOCKERFILE_PATH from arguments.
shift

cd /app

# Detect if this is a Node-based repo by Dockerfile path.
if [[ "${DOCKERFILE_PATH}" == *"Dockerfile.node"* ]]; then

    # Determine package manager.
    if [[ -f yarn.lock ]]; then
        pkg_manager="yarn"
    elif [[ -f package-lock.json ]]; then
        pkg_manager="npm-ci"
    elif [[ -f package.json ]]; then
        pkg_manager="npm"
    else
        echo "[entrypoint] Node repository detected, but no package manager found."
        exit 1
    fi

    # Shallow check for dependencies.
    if ! npm ls --depth=0 >/dev/null 2>&1; then
        echo "[entrypoint] Installing/updating dependencies..."

        rm -rf node_modules/*

        # Install dependencies.
        case "$pkg_manager" in
            yarn)
                corepack enable
                yarn install --frozen-lockfile || yarn install
                ;;
            npm-ci)
                npm ci || npm install
                ;;
            npm)
                npm install
                ;;
        esac
    fi

fi

# Run pre-commit using script so it thinks it's in a TTY. Otherwise, it doesn't show colours.
cmd=$(printf '%q ' pre-commit "$@")
exec script -qfec "$cmd" /dev/null
