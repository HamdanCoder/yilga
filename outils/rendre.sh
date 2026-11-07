#!/bin/zsh
# Rendu d'une page du site à plusieurs largeurs, par émulation d'écran (DevTools).
#   outils/rendre.sh <page.html> [largeur…]      (défaut : 360 760 1280)
# Sorties : outils/rendus/<page>-<largeur>.png (échelle 2, page entière).
set -e
cd "$(dirname "$0")/.."
page=$1; shift; largeurs=("$@"); (( $#largeurs == 0 )) && largeurs=(360 760 1280); nom=${page:r}
for l in $largeurs; do
  node outils/mesurer.mjs "$page" "$l" 'document.documentElement.scrollWidth' --png "outils/rendus/$nom-$l.png" >/dev/null
done
