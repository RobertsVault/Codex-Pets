#!/bin/sh
set -eu
base=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
destination="${CODEX_HOME:-$HOME/.codex}/pets"
mkdir -p "$destination"
backup_root="${destination%/*}/pet-backups"
mkdir -p "$backup_root"
for name in mikan doubao; do
    target="$destination/$name"
    staging=$(mktemp -d "$destination/.${name}.install.XXXXXX")
    cp "$base/pets/$name/pet.json" "$base/pets/$name/spritesheet.png" "$staging/"
    backup="$backup_root/$(basename "$staging").backup"
    if [ -e "$target" ]; then mv "$target" "$backup"; fi
    if ! mv "$staging" "$target"; then
        if [ -e "$backup" ]; then mv "$backup" "$target"; fi
        exit 1
    fi
    echo "Installed $name; previous version (if present): $backup"
done
echo 'Refresh the custom pets list in Codex, or restart Codex.'
