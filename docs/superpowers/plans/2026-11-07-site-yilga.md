# Site web YILGA — plan d'implémentation

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Un site vitrine statique de quatre pages (Accueil, Guide client, Guide prestataire, Télécharger) publié sur `https://hamdancoder.github.io/yilga/`, qui présente YILGA, sa philosophie et deux guides illustrés par les vrais écrans des apps, avec un niveau de finition comparable aux meilleurs sites d'apps grand public.

**Architecture:** Fichiers HTML, CSS et JS écrits à la main, sans framework ni étape de construction, servis par GitHub Pages depuis la racine de la branche `main` du dépôt public `HamdanCoder/yilga` (déjà en ligne avec la page de téléchargement et la release des APK). Un seul `assets/site.css` (jetons, typographie, en-tête, pied, cadres de téléphone, sections) et un seul `assets/site.js` (menu mobile, apparition au défilement). Un dossier `outils/` porte les vérifications automatisées : un contrôleur de pages en Python, un rendu d'écran par Chrome headless, une mesure de débordement par le protocole DevTools, la conversion des captures en WebP.

**Tech Stack:** HTML5, CSS (variables, grid, `prefers-reduced-motion`), JavaScript sans dépendance (IntersectionObserver), Google Fonts Inter, Chrome headless (`/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`), Node 26 (WebSocket natif, pour le protocole DevTools), Python 3 (contrôleur), `cwebp` (installé via Homebrew), `npx lighthouse`, GitHub Pages (Jekyll avec `_config.yml`).

**Spec:** `docs/superpowers/specs/2026-11-07-site-yilga-design.md`

## Global Constraints

- Tout en français, ton sobre ; aucune phrase qui ne corresponde pas à une fonction existante des apps (spec §1 « anti-objectifs », §3).
- Interdits à l'écran : « livraison en 30 minutes », chiffres d'utilisateurs, témoignages, note moyenne, logos partenaires, anglais, « [À compléter] », emoji.
- Couleurs exclusivement : orange `#FF4400`, orange foncé `#E03A00`, orange pâle `#FFEDD5`, encre `#0F172A`, gris `#475569`, gris clair `#94A3B8`, bord `#E2E8F0`, fond `#F8F6F5`, beige studio `#F6EEE6`, blanc. Police : Inter 400 à 800 uniquement.
- Aucune dépendance tierce chargée par les pages autre que Google Fonts ; aucun suivi d'audience ; aucune bannière.
- Liens internes relatifs ; seules l'URL canonique et `og:image` sont absolues, préfixées `https://hamdancoder.github.io/yilga/`.
- Téléphone d'abord : référence 360 px, bascules à 760 px et 1 040 px ; gouttières 20 px ; aucun défilement horizontal à 360 px.
- Typographie : titre d'accueil 56 px ordinateur / 36 px téléphone ; titres de section 36 / 28 ; corps 17 / 16, interligne 1,55 ; largeur de lecture ≤ 62 caractères (`max-width: 62ch`).
- Mouvement : apparition 350 ms une seule fois, survols 150 ms, tout désactivé sous `prefers-reduced-motion: reduce` ; aucune animation en boucle.
- Performance : accueil ≤ 1,5 Mo transférés sur téléphone ; Lighthouse mobile ≥ 95 (performance, accessibilité, bonnes pratiques, SEO) sur les quatre pages.
- Captures : émulateur Pixel 8, 1080×2400, barre d'état en mode démo (heure 9:41, batterie pleine, réseau plein), converties en WebP qualité 85 en 540 px et 1 080 px de large.
- Liens APK : `https://github.com/HamdanCoder/yilga/releases/latest/download/yilga-client.apk` et `…/yilga-pro.apk`.
- Commits : messages en français, suffixe `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>` ; ne jamais pousser `origin main` avant la tâche 7 (la page de téléchargement actuelle est en ligne et doit le rester intacte jusqu'à la publication du site complet).

## Review Focus

1. Un visiteur à 360 px de large ne doit voir aucun défilement horizontal, même sur les pages Guide où les téléphones alternent à gauche et à droite (test : `outils/mesurer.mjs` dans les tâches 1, 3, 4, 5).
2. Sans JavaScript, ou avec `prefers-reduced-motion`, chaque section doit être visible immédiatement : l'état caché de l'apparition n'est appliqué que sous `html.js` (test statique dans `verifier.py`, tâche 1, et rendu avec `--blink-settings=scriptEnabled=false` tâche 3).
3. Un visiteur qui ouvre le menu mobile doit pouvoir le fermer par Échap, par un lien, ou par le bouton, et le défilement de la page doit reprendre (test manuel scripté par DevTools, tâche 1).
4. Les deux liens APK doivent répondre 200 derrière leurs redirections, sur l'Accueil comme sur Télécharger (test réseau dans `verifier.py --reseau`, tâches 3 et 7).
5. Un lien partagé sur WhatsApp doit afficher l'image Open Graph : `og:image` absolue, 1200×630, poids < 300 Ko, présente sur les quatre pages (test dans `verifier.py`, tâche 6).

---

## Structure des fichiers

```
site/
  index.html                 Accueil (tâche 3 ; aujourd'hui la page de téléchargement, remplacée)
  guide-client.html          Guide « Commander avec YILGA » (tâche 4)
  guide-prestataire.html     Guide « Gagner avec Yilga Pro » (tâche 5)
  telecharger.html           Télécharger (tâche 1, reprise de l'index actuel)
  404.html                   Page introuvable (tâche 6)
  _config.yml                Jekyll : exclude docs/, outils/, publier.sh, README.md (tâche 1)
  assets/site.css            Jetons, reset, typographie, en-tête, pied, boutons, cartes, téléphones, sections, reveal (tâche 1, enrichi 3-5)
  assets/site.js             Menu mobile, apparition au défilement, parallaxe accroche (tâche 1, enrichi 3)
  assets/img/logo.png        Copie de logo.png (tâche 1)
  assets/img/favicon.svg, icon-192.png, icon-512.png, apple-touch-icon.png (tâche 6)
  assets/img/og.png          Image Open Graph 1200×630 (tâche 6)
  assets/img/captures/<nom>-540.webp, <nom>-1080.webp (tâche 2)
  outils/verifier.py         Contrôleur des pages (tâche 1, règles ajoutées 2-6)
  outils/rendre.sh           Captures d'écran des pages à 360, 760, 1280 px → outils/rendus/ (tâche 1)
  outils/mesurer.mjs         Mesure par DevTools : débordement horizontal, menu, visibilité (tâche 1)
  outils/convertir-captures.sh  PNG 1080×2400 → WebP 540 et 1080 (tâche 2)
  outils/og.html             Source de l'image Open Graph (tâche 6)
  outils/rendus/             Sorties de rendre.sh, ignorées par git
  publier.sh, README.md      Existants ; README mis à jour tâche 7
```

Contrat partagé entre pages (classes CSS définies tâche 1, utilisées 3-6) :
`html.js` posé par un script inline dans le `<head>` de chaque page ; `.entete` (fixe, `.entete__nav`, `.entete__menu` bouton, `.entete__liens`, lien courant `aria-current="page"`) ; `.pied` ; `.bouton` et `.bouton--secondaire` ; `.conteneur` (max 1 120 px, gouttières 20 px) ; `.section` (espacement 96/64 px) avec `.section__titre` et `.section__surtitre` (orange, 13 px, majuscules espacées) ; `.studio` et `.studio--sombre` ; `.phone` / `.screen` / `.island` / `b.l1 l2 l3 r1` / `.scene` / `.tilt-l` / `.tilt-r` repris de `marketing/source/maquette.css` ; `.reveal` (caché puis `.reveal--vu`).

Contrat des captures (noms de fichiers, tâche 2, consommés 3-5) :
client : `client-code-secret`, `client-telephone`, `client-accueil`, `client-recharge`, `client-ussd`, `client-commande`, `client-menage`, `client-suivi`, `client-recu`, `client-portefeuille` ;
pro : `pro-documents`, `pro-activation`, `pro-accueil`, `pro-demande`, `pro-course`, `pro-portefeuille`, `pro-retrait`, `pro-retrait-agent`, `pro-statistiques`.

---

### Task 1: Outils de vérification et socle commun, prouvés par la page Télécharger

**Files:**
- Create: `outils/verifier.py`, `outils/rendre.sh`, `outils/mesurer.mjs`, `_config.yml`, `.gitignore`, `assets/site.css`, `assets/site.js`, `assets/img/logo.png`, `telecharger.html`
- Modify: `index.html` (inchangé dans le contenu ; seulement si nécessaire pour que `verifier.py` l'ignore : voir étape 3)

**Interfaces:**
- Produces: `python3 outils/verifier.py [--reseau] [--tout]` (`--tout` inclut `index.html` même sans en-tête du site) → code 0 si toutes les pages passent, sinon liste `page: règle: détail` et code 1 ; `outils/rendre.sh <page.html> [largeurs…]` → `outils/rendus/<page>-<largeur>.png` ; `node outils/mesurer.mjs <page.html> <largeur> <expression JS>` → imprime la valeur de l'expression évaluée dans la page rendue à cette largeur (lance Chrome avec `--headless=new --remote-debugging-port=0`, lit l'URL `ws://` sur stderr, utilise `Target.createTarget`, `Target.attachToTarget` (flatten), `Page.navigate`, `Page.loadEventFired`, `Runtime.evaluate` avec `returnByValue`, puis ferme Chrome) ; classes CSS du contrat partagé.

- [ ] **Step 1: Écrire `outils/verifier.py` avec ses règles initiales**

Règles, chacune nommée, appliquées à chaque `*.html` de la racine sauf `index.html` tant qu'il est l'ancienne page (détection : absence de `<nav class="entete__nav"`) et sauf `404.html` pour les règles `nav` et `canonical` :
- `lang` : `<html lang="fr">`.
- `titre` : `<title>` non vide, ≤ 60 caractères.
- `description` : `<meta name="description">` de 50 à 160 caractères.
- `canonical` : `<link rel="canonical" href="https://hamdancoder.github.io/yilga/<page ou vide pour index>">`.
- `og` : `og:title`, `og:description`, `og:image` absolue commençant par `https://hamdancoder.github.io/yilga/assets/img/`, `og:url` = canonical.
- `nav` : un `<nav class="entete__nav">` contenant des liens vers `index.html` (ou `./`), `guide-client.html`, `guide-prestataire.html`, `telecharger.html`, et exactement un `aria-current="page"`.
- `pied` : un `<footer class="pied">`.
- `liens` : chaque `href`/`src` relatif pointe sur un fichier existant (ancre `#…` vérifiée contre les `id` de la page cible).
- `images` : chaque `<img>` a un `alt` ; vide uniquement si `aria-hidden="true"` ou dans `.phone .screen` dont l'alt décrit l'écran (donc : alt non vide pour les captures).
- `interdits` : aucun des textes suivants dans le HTML (insensible à la casse) : `yilga-apk`, `À compléter`, `30 minutes`, `TODO`, `lorem`, `Download`, `http://`.
- `motion` : `assets/site.css` contient `@media (prefers-reduced-motion: reduce)` et la règle cachant `.reveal` est préfixée par `.js ` (règle `.js .reveal{opacity:0`).
- `--reseau` : chaque lien `https://github.com/HamdanCoder/yilga/releases/latest/download/…` répond 200 après redirections (`urllib`, méthode HEAD).

Sortie : une ligne par échec `telecharger.html: canonical: attendu …, trouvé …`, puis `N page(s), M échec(s)` ; code de sortie 1 si M > 0.

- [ ] **Step 2: Lancer le contrôleur sur l'état actuel pour le voir échouer**

Run: `cd ~/IdeaProjects/yilga-v2/site && python3 outils/verifier.py`
Expected: `0 page(s)` (index.html ignoré car ancienne page) puis, après création d'un `telecharger.html` vide de contrat à l'étape 4, échecs `nav`, `canonical`, `og`, `pied`, `motion`. Pour voir le rouge maintenant : `cp index.html telecharger.html && python3 outils/verifier.py` → au moins 5 échecs, code 1.

- [ ] **Step 3: Écrire `outils/rendre.sh` et `outils/mesurer.mjs`, `.gitignore` (`outils/rendus/`), `_config.yml`**

`rendre.sh` : `cd` dans la racine du site, sert la racine avec `python3 -m http.server 8765 --bind 127.0.0.1` en arrière-plan (tué en sortie), puis pour chaque largeur (défaut `360 760 1280`) : Chrome `--headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=2 --window-size=<largeur>,<hauteur calculée par mesurer.mjs : document.documentElement.scrollHeight> --virtual-time-budget=8000 --screenshot=outils/rendus/<page>-<largeur>.png http://127.0.0.1:8765/<page>`. Le serveur HTTP (et non `file://`) est obligatoire : les liens relatifs et Jekyll se comportent comme sur Pages.
`_config.yml` : `exclude: [docs, outils, publier.sh, README.md, .gitignore]`.

- [ ] **Step 4: Écrire `assets/site.css`, `assets/site.js`, copier le logo, écrire `telecharger.html`**

`site.css` : variables du Global Constraints ; reset ; `@import` Inter (`family=Inter:wght@400;500;600;700;800&display=swap`, sous-ensemble latin par défaut) ; échelle typographique ; `.conteneur`, `.section`, `.section__surtitre`, `.section__titre` ; `.entete` fixe 64 px, fond `rgba(248,246,245,.82)` + `backdrop-filter: blur(12px)`, logo 32 px + « YILGA » 800 espacé `.14em`, liens Philosophie (`index.html#philosophie`), Guide (`guide-client.html`), Prestataires (`guide-prestataire.html`), bouton Télécharger (`telecharger.html`) ; sous 760 px les liens passent dans `.entete__liens` plein écran (`position: fixed; inset: 64px 0 0`), ouvert par `.entete__menu` (`aria-expanded`), `body.menu-ouvert{overflow:hidden}` ; `.pied` (marque, « Services à domicile · Ouagadougou », liens des quatre pages, contact rendu seulement si la constante est non vide) ; `.bouton` (orange, texte blanc, 14 px rayon, 150 ms), `.bouton--secondaire` (bord, encre) ; cadres `.phone` repris de `maquette.css` avec `--phone-largeur` (300 px par défaut, 240 px sous 760 px) ; `.studio`, `.studio--sombre` (fond encre, lueurs orange opacité .12) ; `.js .reveal{opacity:0;transform:translateY(16px);transition:opacity .35s,transform .35s}` `.js .reveal--vu{opacity:1;transform:none}` ; `@media (prefers-reduced-motion: reduce){*{transition:none!important;animation:none!important} .js .reveal{opacity:1;transform:none}}` ; `:focus-visible` orange 2 px.
`site.js` : la classe `js` est posée sur `<html>` par un script inline d'une ligne dans le `<head>` de chaque page (`document.documentElement.classList.add('js')`), avant le CSS, pour éviter tout flash ; IntersectionObserver (`threshold: .15`) qui pose `.reveal--vu` et se désabonne ; menu : clic sur `.entete__menu` bascule `aria-expanded` et `body.menu-ouvert`, Échap et clic sur un lien ferment.
`telecharger.html` : contenu de l'`index.html` actuel (deux cartes, quatre étapes, note) sous l'en-tête et au-dessus du pied communs, titre `Télécharger YILGA et Yilga Pro`, description, canonical `https://hamdancoder.github.io/yilga/telecharger.html`, `og:image` provisoire `assets/img/logo.png` (remplacée tâche 6), constantes `TELEPHONE_YILGA = ""` et `EMAIL_YILGA = ""` en tête de `site.js` injectées dans le pied.

- [ ] **Step 5: Vérifier**

Run: `python3 outils/verifier.py && outils/rendre.sh telecharger.html && node outils/mesurer.mjs telecharger.html 360 'document.documentElement.scrollWidth' && node outils/mesurer.mjs telecharger.html 360 'document.querySelector(".entete__menu").click(), document.body.classList.contains("menu-ouvert")'`
Expected: `1 page(s), 0 échec(s)` ; trois PNG dans `outils/rendus/` à ouvrir et regarder (en-tête, cartes, pied lisibles aux trois largeurs) ; `360` ; `true`. Puis `node outils/mesurer.mjs telecharger.html 360 'document.querySelector(".entete__menu").click(); document.dispatchEvent(new KeyboardEvent("keydown",{key:"Escape"})); document.body.classList.contains("menu-ouvert")'` → `false`.

- [ ] **Step 6: Commit**

```bash
git add outils _config.yml .gitignore assets telecharger.html
git commit -m "Socle du site : styles, scripts, outils de vérification, page Télécharger"
```

### Task 2: Captures d'écran manquantes et conversion WebP

**Files:**
- Create: `outils/convertir-captures.sh`, `assets/img/captures/*.webp`
- Modify: `outils/verifier.py` (règle `captures`)

**Interfaces:**
- Consumes: drivers `~/IdeaProjects/yilga-mobile/.claude/skills/run-yilga-mobile/driver.sh` et `~/IdeaProjects/yilga-prestataire/.claude/skills/run-yilga-pro/driver.sh` (`build`, `reload`, `ss <nom>` → `/tmp/yilga-shots/<nom>.png`, `otp`, `tap x y`, `type`), pilotes `client.ts` / `prestataire.ts`, backend local `docker compose up -d` dans `~/IdeaProjects/yilga-v2/backend`, mémoire `emulateur-pieges-adb.md` et `yilga-pro-projet.md` (comptes de test, activation admin).
- Produces: les 19 noms du contrat des captures, en `-540.webp` et `-1080.webp` dans `assets/img/captures/`.

- [ ] **Step 1: Ajouter la règle `captures` à `verifier.py` et la voir échouer**

Règle : pour chaque nom du contrat (liste codée dans le script), `assets/img/captures/<nom>-540.webp` et `<nom>-1080.webp` existent, pèsent < 120 Ko (540) et < 350 Ko (1080). Run: `python3 outils/verifier.py` → Expected: 38 échecs `captures`.

- [ ] **Step 2: Écrire `outils/convertir-captures.sh <dossier source>`**

Pour chaque `<dossier>/<nom>.png` : `cwebp -q 85 -resize 540 0 … -o assets/img/captures/<nom>-540.webp` et `-resize 1080 0` pour la grande. Idempotent.

- [ ] **Step 3: Mettre l'émulateur en mode démo et reprendre toutes les captures**

`adb shell settings put global sysui_demo_allowed 1 ; adb shell am broadcast -a com.android.systemui.demo -e command enter ; … -e command clock -e hhmm 0941 ; … -e command battery -e level 100 -e plugged false ; … -e command network -e mobile show -e level 4 -e datatype lte ; … -e command notifications -e visible false`. Reprendre **toutes** les captures (anciennes et nouvelles) pour une barre d'état uniforme, dans `/tmp/yilga-shots/`, données propres (adresses réelles de Ouagadougou, montants plausibles). Nouvelles : client `client-telephone` (écran du numéro, `auth/phone`), `client-ussd` (`payment/ussd`), `client-menage` (`services/cleaning`) ; Pro `pro-documents` (`verification/documents`), `pro-activation` (`verification/activation`, nécessite un compte fraîchement activé par l'admin : voir mémoire), `pro-retrait` (`portefeuille/retrait`), `pro-retrait-agent` (`portefeuille/retrait-agent`, après une demande de retrait pour afficher le code). Quitter le mode démo : `-e command exit`.

- [ ] **Step 4: Convertir et vérifier**

Run: `outils/convertir-captures.sh /tmp/yilga-shots && python3 outils/verifier.py`
Expected: `1 page(s), 0 échec(s)`. Ouvrir trois WebP au hasard (Read) : barre d'état 9:41, batterie pleine, pas de bandeau de dev Expo.

- [ ] **Step 5: Commit**

```bash
git add outils/convertir-captures.sh outils/verifier.py assets/img/captures
git commit -m "Captures des deux apps en WebP pour le site"
```

### Task 3: Page d'accueil

**Files:**
- Modify: `index.html` (réécrit), `assets/site.css`, `assets/site.js`, `outils/verifier.py`

**Interfaces:**
- Consumes: contrat CSS tâche 1, captures tâche 2.
- Produces: ancres `#philosophie`, `#services`, `#comment`, `#prestataires`, `#telecharger` utilisées par l'en-tête et les guides ; composant `.etape` (numéro, titre, phrase) réutilisé par les pages Guide ; `.carte-telechargement` partagé avec `telecharger.html` (extraire le balisage des deux cartes dans une structure identique sur les deux pages).

- [ ] **Step 1: Ajouter à `verifier.py` les règles `accueil` et les voir échouer**

Règle `accueil` (index.html seulement) : présence des cinq `id` ci-dessus ; `h1` unique ; au moins deux `.phone` dans `.scene` ; dans la section `#services`, chaque « Bientôt » est dans un élément `.bientot` et les cinq libellés Plomberie, Électricité, Coiffure, Chauffeur, Santé y sont, et aucun ailleurs ; les deux liens APK présents ; `img` de l'accroche sans `loading="lazy"`, toutes les autres `img` avec. Règle `poids` : somme des octets des fichiers référencés par index.html (CSS, JS, images `src` et la plus petite source de chaque `srcset`) < 1 500 000. Run: `python3 outils/verifier.py` → Expected: index.html toujours ignoré (ancienne page) ; forcer avec `python3 outils/verifier.py --tout` → échecs `nav`, `accueil`.

- [ ] **Step 2: Écrire `index.html` selon spec §3 et §4.3**

Ordre : en-tête ; accroche `.studio` (`.section__surtitre` « Services à domicile · Ouagadougou », `h1` « Faites livrer. Faites nettoyer. <b>En toute confiance.</b> », sous-titre deux phrases, `.bouton` Télécharger + lien « Voir le guide », `.scene` avec `.phone.tilt-l` `client-accueil` et `.phone.tilt-r` `client-suivi`, `<picture>`/`srcset` 540w 1080w, `sizes`) ; `#pourquoi` trois phrases ; `#philosophie` quatre blocs `.pilier` avec icône trait (jeu de la fiche), titres exacts de la spec §3.2, deux phrases chacun, phrase de clôture ; `#services` deux cartes disponibles + ligne `.bientot` ; `#comment` deux colonnes de trois `.etape` + liens « Voir le guide complet » ; `#prestataires` `.studio--sombre` trois arguments + deux boutons ; `#telecharger` deux `.carte-telechargement` ; pied. Chaque section `.section.reveal`. Titre `YILGA · Livraison et ménage à Ouagadougou`, description ≤ 160, canonical `https://hamdancoder.github.io/yilga/`.
`site.js` : parallaxe des `.scene .phone` sur ordinateur seulement (`matchMedia('(min-width:1040px)')` et non `reduce`), amplitude 24 px sur `scroll`, `requestAnimationFrame`.

- [ ] **Step 3: Vérifier**

Run: `python3 outils/verifier.py --reseau && outils/rendre.sh index.html && for l in 360 760 1280; do node outils/mesurer.mjs index.html $l 'document.documentElement.scrollWidth'; done && node outils/mesurer.mjs index.html 360 'getComputedStyle(document.querySelector(".reveal")).opacity'`
Expected: `0 échec(s)` ; largeurs `360`, `760`, `1280` ; `1` (section du haut révélée). Rendu sans script : Chrome `--blink-settings=scriptEnabled=false --screenshot` sur `http://127.0.0.1:8765/index.html` à 360 px → toutes les sections visibles. Regarder les trois rendus : téléphones de l'accroche nets, aucun texte coupé, piliers deux par ligne à 1 280 px, un par ligne à 360 px.

- [ ] **Step 4: Commit**

```bash
git add index.html assets outils/verifier.py
git commit -m "Page d'accueil : accroche, philosophie, services, parcours, prestataires"
```

### Task 4: Guide client

**Files:**
- Create: `guide-client.html`
- Modify: `assets/site.css` (mise en page `.guide` alternée), `outils/verifier.py` (règle `guide`)

**Interfaces:**
- Consumes: `.etape`, `.phone`, captures client.
- Produces: structure `.guide` (sommaire `nav.guide__sommaire` ancré, `section.guide__etape` avec `.guide__texte` et `.guide__ecran`, alternance par `:nth-child(even)` à partir de 760 px) réutilisée tâche 5.

- [ ] **Step 1: Règle `guide` dans `verifier.py`, en échec**

Pour `guide-*.html` : exactement six `section.guide__etape`, chacune avec un `h2`, un `p` et une `img` dont le `src` est l'une des captures du contrat ; un `nav.guide__sommaire` avec six liens vers les `id` des étapes ; un lien vers l'autre guide ; un lien vers `telecharger.html`. Run: `python3 outils/verifier.py` → page absente, puis après création d'un squelette, échecs `guide`.

- [ ] **Step 2: Écrire `guide-client.html`**

Titre « Commander avec YILGA », introduction une phrase, six étapes de la spec §3.4 avec les captures : 1 `client-telephone`, 2 `client-recharge`, 3 `client-commande`, 4 `client-carte` (course en cours sur la carte), 5 `client-recu`, 6 `client-suivi` (état Terminée, qui porte la carte de notation). Chaque étape : numéro, `h2` ≤ 6 mots, une phrase ≤ 25 mots, mention de l'alternative espèces à l'étape 2 et 3. Bas de page : « Vous êtes livreur ou agent de ménage ? » → `guide-prestataire.html`, bouton Télécharger.

- [ ] **Step 3: Vérifier**

Run: `python3 outils/verifier.py && outils/rendre.sh guide-client.html && node outils/mesurer.mjs guide-client.html 360 'document.documentElement.scrollWidth'`
Expected: `0 échec(s)`, `360` ; rendus : alternance gauche/droite à 1 280 px, empilement à 360 px, sommaire cliquable.

- [ ] **Step 4: Commit**

```bash
git add guide-client.html assets/site.css outils/verifier.py
git commit -m "Guide client : commander avec YILGA en six étapes"
```

### Task 5: Guide prestataire

**Files:**
- Create: `guide-prestataire.html`

**Interfaces:**
- Consumes: `.guide` tâche 4, captures pro.

- [ ] **Step 1: Voir la règle `guide` échouer sur un squelette**

Run: `printf '<!doctype html><html lang="fr"></html>' > guide-prestataire.html && python3 outils/verifier.py` → échecs `guide`, `nav`, `titre`…

- [ ] **Step 2: Écrire `guide-prestataire.html`**

Titre « Gagner avec Yilga Pro », six étapes de la spec §3.4 : 1 `pro-documents`, 2 `pro-activation`, 3 `pro-accueil`, 4 `pro-demande`, 5 `pro-course`, 6 `pro-retrait-agent` (texte : gains, caution, bonus ; code chez un agent ; versement Mobile Money automatique le matin). Lien vers `guide-client.html` (« Vous voulez commander ? ») et bouton Télécharger Yilga Pro.

- [ ] **Step 3: Vérifier**

Run: `python3 outils/verifier.py && outils/rendre.sh guide-prestataire.html && node outils/mesurer.mjs guide-prestataire.html 360 'document.documentElement.scrollWidth'`
Expected: `0 échec(s)`, `360`, rendus regardés.

- [ ] **Step 4: Commit**

```bash
git add guide-prestataire.html
git commit -m "Guide prestataire : gagner avec Yilga Pro en six étapes"
```

### Task 6: Finitions : 404, image Open Graph, favicons, métadonnées

**Files:**
- Create: `404.html`, `outils/og.html`, `assets/img/og.png`, `assets/img/favicon.svg`, `assets/img/icon-192.png`, `assets/img/icon-512.png`, `assets/img/apple-touch-icon.png`
- Modify: les quatre pages (`<head>`), `outils/verifier.py` (règle `finitions`)

- [ ] **Step 1: Règle `finitions` dans `verifier.py`, en échec**

Pour chaque page : `<link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">`, `<link rel="apple-touch-icon" …>`, `<meta name="theme-color" content="#F8F6F5">`, `og:image` = `https://hamdancoder.github.io/yilga/assets/img/og.png`, `og:image:width` 1200, `og:image:height` 630, `twitter:card` `summary_large_image` ; `assets/img/og.png` existe, < 300 Ko, dimensions 1200×630 (lire l'en-tête PNG) ; `404.html` existe avec `.entete` et un lien vers `index.html`. Run → échecs sur les quatre pages.

- [ ] **Step 2: Produire les images et la 404**

`outils/og.html` : 1200×630, `.studio`, logo + « YILGA », accroche de l'accueil, un `.phone.tilt-r` `client-accueil-1080` à droite ; rendu par Chrome `--window-size=1200,630 --force-device-scale-factor=1 --screenshot=assets/img/og.png` via `rendre.sh` (ajouter l'option `--taille 1200x630` si besoin) ; compression `magick assets/img/og.png -strip -colors 255 assets/img/og.png` si > 300 Ko. Favicons : `favicon.svg` = carré orange rayon 22 %, « Y » Inter 800 blanc ; PNG 192/512/180 par `magick -background none favicon.svg -resize …`. `404.html` : en-tête, « Cette page n'existe pas », bouton vers l'accueil, pied.

- [ ] **Step 3: Vérifier**

Run: `python3 outils/verifier.py && outils/rendre.sh 404.html 360`
Expected: `5 page(s), 0 échec(s)` ; rendu 404 regardé.

- [ ] **Step 4: Commit**

```bash
git add 404.html outils/og.html assets/img *.html outils/verifier.py
git commit -m "Finitions : page 404, image Open Graph, favicons, métadonnées"
```

### Task 7: Lighthouse, publication et vérification en ligne

**Files:**
- Modify: `README.md`, `publier.sh` (option `--site` ou simple `git push`), éventuellement `assets/site.css` / pages pour les correctifs Lighthouse

- [ ] **Step 1: Lighthouse sur les quatre pages, en local**

Run: `python3 -m http.server 8765 --bind 127.0.0.1 & for p in index telecharger guide-client guide-prestataire; do npx --yes lighthouse "http://127.0.0.1:8765/$p.html" --preset=perf --form-factor=mobile --screenEmulation.mobile --only-categories=performance,accessibility,best-practices,seo --output=json --output-path=outils/rendus/lh-$p.json --chrome-flags="--headless=new" --quiet; python3 -c "import json;d=json.load(open('outils/rendus/lh-$p.json'))['categories'];print('$p',{k:round(v['score']*100) for k,v in d.items()})"; done; kill %1`
Expected: chaque catégorie ≥ 95 sur chaque page. Sinon, corriger (tailles d'images, `sizes`, contrastes, ordre des titres, `aria-label` du bouton menu, `font-display`) et relancer jusqu'à ≥ 95.

- [ ] **Step 2: README et script**

`README.md` : description du site, structure, « vérifier avant de publier » (`python3 outils/verifier.py --reseau`, `outils/rendre.sh`, Lighthouse), « publier » (`git push origin main`, Pages reconstruit en une à deux minutes), « publier une nouvelle version des APK » (`publier.sh v… client.apk pro.apk` puis mettre à jour taille et date dans `index.html` et `telecharger.html`), où remplir `TELEPHONE_YILGA` et `EMAIL_YILGA`.

- [ ] **Step 3: Publier et vérifier en ligne**

Run: `git push origin main` puis, après deux minutes : `for p in "" telecharger.html guide-client.html guide-prestataire.html; do curl -s -o /dev/null -w "$p %{http_code}\n" "https://hamdancoder.github.io/yilga/$p"; done; curl -s https://hamdancoder.github.io/yilga/docs/superpowers/specs/2026-11-07-site-yilga-design.md -o /dev/null -w "docs %{http_code}\n"; curl -sIL -o /dev/null -w "apk %{http_code}\n" https://github.com/HamdanCoder/yilga/releases/latest/download/yilga-client.apk`
Expected: quatre `200`, `docs 404` (exclu par Jekyll), `apk 200`. Puis rendu de la page en ligne : Chrome `--screenshot` sur `https://hamdancoder.github.io/yilga/` à 360 et 1 280 px, regardé.

- [ ] **Step 4: Commit**

```bash
git add README.md publier.sh
git commit -m "Documentation de vérification et de publication du site"
git push origin main
```
