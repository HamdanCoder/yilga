#!/usr/bin/env bash
# Publie la page de téléchargement et les APK sur GitHub (dépôt public HamdanCoder/yilga-apk).
#   publier.sh                      # première publication : crée le dépôt, la release, la page
#   publier.sh v2026.11.20 client.apk pro.apk   # nouvelle version : ajoute une release
set -euo pipefail
DEPOT=HamdanCoder/yilga-apk
ICI="$(cd "$(dirname "$0")" && pwd)"
APK="$ICI/../apk"
TAG="${1:-v2026.10.22}"
CLIENT="${2:-$APK/yilga-client-2026-10-22.apk}"
PRO="${3:-$APK/yilga-pro-2026-10-22.apk}"

TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
cp "$CLIENT" "$TMP/yilga-client.apk"; cp "$PRO" "$TMP/yilga-pro.apk"

if ! gh repo view "$DEPOT" >/dev/null 2>&1; then
  echo "→ création du dépôt public $DEPOT"
  (cd "$ICI" && gh repo create "$DEPOT" --public --source . --push \
      --description "Téléchargement des applications Android YILGA et Yilga Pro (APK)")
  echo "→ activation de GitHub Pages (branche main, racine)"
  gh api -X POST "repos/$DEPOT/pages" -f build_type=legacy -f 'source[branch]=main' -f 'source[path]=/' >/dev/null
else
  (cd "$ICI" && git push -q origin main)
fi

echo "→ release $TAG"
gh release create "$TAG" "$TMP/yilga-client.apk" "$TMP/yilga-pro.apk" --repo "$DEPOT" \
  --title "Version du ${TAG#v}" --notes "APK Android signés avec la clé de développement, backend https://api-v2.yilga.ci-hamdan.cloud."

echo "→ vérification des liens"
for n in yilga-client yilga-pro; do
  printf '%s : ' "$n"; curl -sIL -o /dev/null -w '%{http_code} %{size_download}o\n' \
    "https://github.com/$DEPOT/releases/latest/download/$n.apk"
done
echo
echo "Page    : https://hamdancoder.github.io/yilga-apk/   (en ligne 1 à 2 minutes après la première publication)"
echo "YILGA   : https://github.com/$DEPOT/releases/latest/download/yilga-client.apk"
echo "Yilga Pro : https://github.com/$DEPOT/releases/latest/download/yilga-pro.apk"
