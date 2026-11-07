# Site web YILGA

Site vitrine de YILGA (services à domicile à Ouagadougou) : accueil, philosophie, guide client, guide
prestataire et téléchargement des APK Android. Pages HTML, CSS et JS écrites à la main, sans
framework, servies par GitHub Pages : https://hamdancoder.github.io/yilga/

Les APK sont publiés dans les *Releases* de ce dépôt ; les liens `releases/latest/download/yilga-client.apk`
et `releases/latest/download/yilga-pro.apk` pointent toujours sur la dernière version.

## Structure

| Chemin | Rôle |
|---|---|
| `index.html` | Accueil : accroche, pourquoi, philosophie, services, comment ça marche, prestataires, téléchargement |
| `guide-client.html`, `guide-prestataire.html` | Les deux guides en six étapes, illustrés par les écrans réels |
| `telecharger.html`, `404.html` | Téléchargement des APK ; page introuvable |
| `assets/site.css`, `assets/site.js` | Styles et script communs (menu mobile, apparition au défilement, parallaxe) |
| `assets/img/captures/` | Captures des apps en WebP, 540 et 1080 px de large |
| `assets/img/og.png` | Image d'aperçu 1200×630 pour WhatsApp et Facebook (source : `outils/og.html`) |
| `outils/` | Vérifications : `verifier.py`, `rendre.sh`, `mesurer.mjs`, `convertir-captures.sh` |
| `docs/` | Conception et plan d'implémentation |
| `_config.yml` | Exclut `docs/`, `outils/`, `publier.sh` et ce README du site publié |

## Contact à renseigner

En tête de `assets/site.js` : `TELEPHONE_YILGA` et `EMAIL_YILGA`. Vides, rien n'est affiché ; renseignés,
ils apparaissent dans le pied de page de toutes les pages.

## Vérifier avant de publier

```bash
python3 outils/verifier.py --reseau        # métadonnées, navigation, liens, images, textes interdits, liens APK
outils/rendre.sh index.html                # rendus 360 / 760 / 1280 px dans outils/rendus/, à regarder
node outils/mesurer.mjs index.html 360 'document.documentElement.scrollWidth'   # 360 attendu
```

Lighthouse (mobile, ≥ 95 attendu partout) :

```bash
python3 -m http.server 8766 --bind 127.0.0.1 &
npx --yes lighthouse http://127.0.0.1:8766/index.html --form-factor=mobile --screenEmulation.mobile \
  --only-categories=performance,accessibility,best-practices,seo --output=json --output-path=outils/rendus/lh-index.json \
  --chrome-flags="--headless=new" --quiet
```

## Publier le site

```bash
git push origin main      # GitHub Pages reconstruit en une à deux minutes
```

## Publier une nouvelle version des APK

```bash
./publier.sh v2026.11.20 chemin/vers/client.apk chemin/vers/pro.apk
```

Puis mettre à jour la taille et la date dans `index.html` et `telecharger.html` (lignes « APK · … Mo · version du … »).

## Reprendre les captures

Émulateur Pixel_8 en mode démo (heure 9:41, batterie pleine, Wi‑Fi) via les drivers `run-yilga-mobile` et
`run-yilga-pro`, captures 1080×2400 dans un dossier, puis :

```bash
outils/convertir-captures.sh /tmp/yilga-shots
```
