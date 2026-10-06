#!/usr/bin/env sh
# Генерація + експорт + перевірки всіх схем (або переданих): ./make.sh [назва ...] [--publish]
set -e
cd "$(dirname "$0")"
python3 -m generator "$@"
