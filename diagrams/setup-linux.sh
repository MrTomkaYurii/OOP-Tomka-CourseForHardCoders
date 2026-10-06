#!/usr/bin/env bash
# Оточення для пайплайну схем на Linux (хмарна сесія Claude Code, CI, Docker).
# Ставить: draw.io desktop + xvfb, шрифт JetBrains Mono, Python (Pillow, PyYAML), .NET 10 SDK.
# Ідемпотентний: повторний запуск пропускає вже встановлене.
#
#   bash diagrams/setup-linux.sh
set -euo pipefail

DRAWIO_VERSION="${DRAWIO_VERSION:-31.7.0}"
SUDO=""
if [ "$(id -u)" -ne 0 ]; then SUDO="sudo"; fi
export DEBIAN_FRONTEND=noninteractive

say() { printf '\n── %s\n' "$*"; }

say "apt: xvfb, шрифти, Python"
$SUDO apt-get update -qq
$SUDO apt-get install -y -qq --no-install-recommends \
    ca-certificates curl unzip xvfb xauth fontconfig \
    python3 python3-pil python3-yaml >/dev/null

say "JetBrains Mono"
if fc-list | grep -qi "JetBrains Mono"; then
    echo "вже є"
elif $SUDO apt-get install -y -qq --no-install-recommends fonts-jetbrains-mono >/dev/null 2>&1; then
    echo "з apt"
else
    tmp=$(mktemp -d)
    curl -fsSL -o "$tmp/jbm.zip" https://github.com/JetBrains/JetBrainsMono/releases/download/v2.304/JetBrainsMono-2.304.zip
    unzip -q "$tmp/jbm.zip" -d "$tmp"
    $SUDO mkdir -p /usr/local/share/fonts/jetbrains-mono
    $SUDO cp "$tmp"/fonts/ttf/*.ttf /usr/local/share/fonts/jetbrains-mono/
    rm -rf "$tmp"
    echo "з GitHub"
fi
$SUDO fc-cache -f >/dev/null

say "draw.io ${DRAWIO_VERSION}"
if command -v drawio >/dev/null 2>&1; then
    echo "вже є: $(command -v drawio)"
else
    tmp=$(mktemp -d)
    curl -fsSL -o "$tmp/drawio.deb" \
        "https://github.com/jgraph/drawio-desktop/releases/download/v${DRAWIO_VERSION}/drawio-amd64-${DRAWIO_VERSION}.deb"
    $SUDO apt-get install -y -qq "$tmp/drawio.deb" >/dev/null
    rm -rf "$tmp"
fi
# Electron потребує бібліотек, яких .deb draw.io не оголошує залежностями.
# libasound2 в Ubuntu 24.04 перейменовано на libasound2t64.
$SUDO apt-get install -y -qq --no-install-recommends libasound2t64 >/dev/null 2>&1 \
    || $SUDO apt-get install -y -qq --no-install-recommends libasound2 >/dev/null
$SUDO apt-get install -y -qq --no-install-recommends \
    libgbm1 libnss3 libgtk-3-0 libxss1 libxtst6 libdrm2 libsecret-1-0 >/dev/null 2>&1 || true

say ".NET 10 SDK"
if command -v dotnet >/dev/null 2>&1 && dotnet --list-sdks | grep -q '^10\.'; then
    echo "вже є: $(dotnet --version)"
elif $SUDO apt-get install -y -qq dotnet-sdk-10.0 >/dev/null 2>&1; then
    # пакет Ubuntu: працює й тоді, коли мережева політика блокує хости Microsoft
    echo "з apt: $(dotnet --version)"
else
    curl -fsSL https://dot.net/v1/dotnet-install.sh -o /tmp/dotnet-install.sh
    bash /tmp/dotnet-install.sh --channel 10.0 --install-dir "$HOME/.dotnet" >/dev/null
    $SUDO ln -sf "$HOME/.dotnet/dotnet" /usr/local/bin/dotnet
    echo "встановлено: $(dotnet --version)"
fi
export DOTNET_CLI_TELEMETRY_OPTOUT=1 DOTNET_NOLOGO=1

say "Перевірка: рендер однієї схеми"
cd "$(dirname "$0")"
python3 -m generator reflection-type --themes dark
echo
echo "Готово. Повний прогін: ./make.sh   |   публікація: ./make.sh <id> --publish"
