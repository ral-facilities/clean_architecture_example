#!/bin/bash
set -euo pipefail

# Verify the user is inside a Git repository.
if ! REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null)"; then
    echo "Error: you have to be inside a Git repository to run pre-commit." >&2
    exit 1
fi

DEV_SETUP_DIR="${REPO_ROOT}/.dev-setup"
PRE_COMMIT_HOOK="${DEV_SETUP_DIR}/pre-commit.hook"
PRE_COMMIT_WRAPPER="${DEV_SETUP_DIR}/pre-commit"

# Ensure scripts are executable.
chmod +x "${PRE_COMMIT_HOOK}" "${PRE_COMMIT_WRAPPER}"

# Install Git hook.
if cp "${PRE_COMMIT_HOOK}" "${REPO_ROOT}/.git/hooks/pre-commit"; then
    echo "Pre-commit hook installed successfully."
    echo
    echo "NOTE: If you don't want pre-commit to run automatically on every commit, run:"
    echo "  rm -f ${REPO_ROOT}/.git/hooks/pre-commit"
    echo
else
    echo "Failed to install pre-commit hook." >&2
fi

# Install wrapper.
if cp "${PRE_COMMIT_WRAPPER}" /usr/local/bin/pre-commit; then
    echo "Pre-commit wrapper script installed to /usr/local/bin/pre-commit."
else
    echo "Failed to install pre-commit wrapper script." >&2
fi

# Verify and install Docker if necessary.

# Packages to check.
docker_packages=(
    docker-ce
    docker-ce-cli
    containerd.io
    docker-compose-plugin
)

# Check if all packages are installed.
missing=()
for pkg in "${docker_packages[@]}"; do
    if ! rpm -q "$pkg" &>/dev/null; then
        missing+=("$pkg")
    fi
done

# If any are missing, install everything.
if [ "${#missing[@]}" -gt 0 ]; then
    echo "Some Docker packages are missing: ${missing[*]}"

    # Check for Podman, which conflicts with Docker.
    if dnf list installed podman podman-docker runc &>/dev/null; then
        echo "ERROR: Podman or other conflicting packages are installed."
        echo "Please remove them manually before installing Docker:"
        echo "  dnf remove -y podman podman-docker runc"
        exit 1
    fi

    echo "Installing Docker packages..."
    dnf install -y dnf-plugins-core
    dnf config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
    dnf install -y "${docker_packages[@]}"
else
    echo "Docker is already installed, skipping installation."
fi

# Check if the Docker service is running.
if ! systemctl is-active --quiet docker; then
    echo "Starting and enabling docker.service..."
    systemctl enable --now docker
else
    echo "Docker service is already running."
fi

echo
echo "Pre-commit installation and Docker setup complete."
