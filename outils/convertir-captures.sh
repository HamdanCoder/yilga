#!/bin/zsh
# Convertit les captures PNG (1080×2400) en WebP qualité 85, en 540 et 1080 px de large.
#   outils/convertir-captures.sh <dossier des PNG>
set -e
cd "$(dirname "$0")/.."
src=$1; [[ -d "$src" ]] || { echo "dossier introuvable : $src" >&2; exit 1 }
mkdir -p assets/img/captures
for f in "$src"/*.png; do
  nom=${${f:t}:r}
  cwebp -quiet -q 85 -resize 540 0 "$f" -o "assets/img/captures/$nom-540.webp"
  cwebp -quiet -q 85 -resize 1080 0 "$f" -o "assets/img/captures/$nom-1080.webp"
  printf '%s : %s Ko / %s Ko\n' "$nom" $(( $(stat -f %z "assets/img/captures/$nom-540.webp") / 1000 )) $(( $(stat -f %z "assets/img/captures/$nom-1080.webp") / 1000 ))
done
