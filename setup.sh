#!/usr/bin/env sh
set -eu

DISCORD_URL="https://github.com/Rapptz/discord.py.git"
DISCORD_BRANCH="v1.x"
DISCORD_DIR="discord.py"
FLUXER_URL="https://github.com/Fluxer-py/fluxer.py.git"
FLUXER_COMMIT="300d48e45deb88cbc1130b8749a5ad31cbc45d8b"
FLUXER_DIR="fluxer.py-old"
CHECK_ONLY=0

usage() {
    echo "Usage: ./setup.sh [--check]"
}

if [ "${1:-}" = "--check" ]; then
    CHECK_ONLY=1
elif [ "${1:-}" != "" ]; then
    usage
    exit 2
fi

if [ "${2:-}" != "" ]; then
    usage
    exit 2
fi

if ! command -v git >/dev/null 2>&1; then
    echo "[setup] git is required but was not found on PATH."
    exit 1
fi

if [ "$CHECK_ONLY" = "1" ]; then
    echo "[setup] setup.sh syntax check OK."
    exit 0
fi

ensure_git_repo() {
    target=$1
    if [ -e "$target" ] && [ ! -d "$target/.git" ]; then
        echo "[setup] Blocked: $target exists but is not an independent git checkout."
        exit 1
    fi
}

ensure_clean() {
    target=$1
    if [ -n "$(git -C "$target" status --porcelain)" ]; then
        echo "[setup] Blocked: $target has uncommitted changes."
        exit 1
    fi
}

sync_discord() {
    ensure_git_repo "$DISCORD_DIR"
    if [ ! -e "$DISCORD_DIR" ]; then
        echo "[setup] Cloning $DISCORD_DIR branch $DISCORD_BRANCH..."
        git clone --branch "$DISCORD_BRANCH" --single-branch "$DISCORD_URL" "$DISCORD_DIR"
        echo "[setup] $DISCORD_DIR cloned."
        return
    fi

    ensure_clean "$DISCORD_DIR"
    echo "[setup] Updating $DISCORD_DIR to origin/$DISCORD_BRANCH..."
    git -C "$DISCORD_DIR" fetch origin "$DISCORD_BRANCH"
    git -C "$DISCORD_DIR" checkout "$DISCORD_BRANCH"
    git -C "$DISCORD_DIR" pull --ff-only origin "$DISCORD_BRANCH"
    echo "[setup] $DISCORD_DIR is on $DISCORD_BRANCH."
}

sync_fluxer() {
    ensure_git_repo "$FLUXER_DIR"
    if [ ! -e "$FLUXER_DIR" ]; then
        echo "[setup] Cloning $FLUXER_DIR..."
        git clone "$FLUXER_URL" "$FLUXER_DIR"
        echo "[setup] $FLUXER_DIR cloned."
    fi

    ensure_clean "$FLUXER_DIR"
    echo "[setup] Fetching $FLUXER_DIR and checking out $FLUXER_COMMIT..."
    git -C "$FLUXER_DIR" fetch origin
    git -C "$FLUXER_DIR" checkout --detach "$FLUXER_COMMIT"
    echo "[setup] $FLUXER_DIR pinned to $FLUXER_COMMIT."
}

sync_discord
sync_fluxer

echo "[setup] Done."

