# Site web YILGA — conception

Date : 2026-11-07.
Dépôt : `~/IdeaProjects/yilga-v2/site` (dépôt git local, ex-`telechargement`, à publier en dépôt public
`HamdanCoder/yilga` servi par GitHub Pages sur `https://hamdancoder.github.io/yilga/`).
Statut : à valider avant plan d'implémentation.

## 1. Intention

Le site est **l'image marketing de YILGA**. Un visiteur y arrive depuis un lien WhatsApp, une affiche
(QR code) ou une recherche, pour trois raisons, dans cet ordre : découvrir ce qu'est YILGA, comprendre
sa philosophie (pourquoi on peut lui faire confiance), et apprendre à s'en servir pas à pas. Au bout du
chemin, il télécharge l'app, ou il envoie le lien à quelqu'un.

Deux publics, à Ouagadougou :
- **le client** : un habitant équipé d'un Android et d'un compte Orange Money ou Moov Money, sans carte
  bancaire, qui veut faire livrer un colis dans l'heure ou faire faire un ménage à prix connu ;
- **le prestataire** : un livreur à moto ou une personne faisant des ménages, à son compte, qui veut
  des courses près de lui et ses gains vite, sans frais surprise.

Réussite : un visiteur comprend en trente secondes ce que fait YILGA et pourquoi c'est plus sûr que le
gré à gré ; un prestataire comprend comment il sera payé ; le site tient la comparaison visuelle avec
les sites des meilleures apps de services (netteté, rythme, finitions), et le fondateur n'a pas honte
de l'envoyer à un partenaire.

### Hors périmètre et anti-objectifs

- Pas de volet investisseurs : ni rail de paiement, ni SMS-Gateway, ni chiffres de marché, ni projections.
  Le site parle au grand public et aux prestataires.
- Pas de contenu qui promet ce que les apps ne font pas : pas de « livraison en 30 minutes », pas de
  plomberie ou de coiffure présentées comme disponibles, pas de témoignages inventés, pas de chiffres
  d'utilisateurs, pas de note moyenne, pas de logos de partenaires.
- Pas d'anglais, pas de blog, pas de formulaire de contact ni d'inscription web (tout se passe dans les apps),
  pas de cookies ni de bannière, pas de suivi d'audience.
- Pas de framework ni d'étape de construction : des fichiers HTML, CSS et JS écrits à la main.
- Pas de gabarit générique « landing page » : le site doit ressembler à YILGA, pas à un modèle acheté.

## 2. Décisions prises avec le fondateur

| Sujet | Décision | Origine |
|---|---|---|
| Raison d'être | Découvrir YILGA, sa philosophie, le guide d'utilisation | Fondateur |
| Guide | Deux parcours illustrés par les vraies captures : « Commander avec YILGA » (client) et « Gagner avec Yilga Pro » (prestataire), le second servant au recrutement | Fondateur a laissé le choix, « la meilleure option marketing » |
| Structure | Quatre pages : Accueil, Guide client, Guide prestataire, Télécharger | Validée par le fondateur |
| Adresse | Gratuite pour le moment, comme la page de téléchargement : GitHub Pages | Fondateur |
| Niveau d'exigence | « Très haute qualité, c'est l'image marketing de notre solution » | Fondateur |
| Langue et ton | Français, sobre, comme les apps et les affiches | Règle du projet |

## 3. Ce que le site dit (contenu)

Toute phrase du site doit correspondre à une fonction qui existe dans les apps (sources : `docs/PRD.md` du
back-end, specs des deux apps, écrans réels). Le rédacteur n'invente rien ; s'il hésite, il retire.

### 3.1 Le problème (section « Pourquoi YILGA »)

À Ouagadougou, livraison et ménage se font de gré à gré. Le client craint la surfacturation et le
travail non fait ; le prestataire craint le déplacement gratuit et le non-paiement ; personne n'a de
recours ni d'historique. Trois phrases, pas plus, à la deuxième personne quand c'est possible.

### 3.2 La philosophie (section « Notre philosophie »)

Fil conducteur : **la confiance est une fonctionnalité**. Quatre mécanismes, un bloc chacun, titre court
et deux phrases :

1. **Le prix avant la commande.** Le ménage est au tarif fixé par YILGA, la livraison à un prix affiché
   avant de confirmer. Rien ne change entre la commande et la fin.
2. **Payé seulement quand c'est fait.** Avec le portefeuille, l'argent est réservé à l'acceptation et
   débité après la prestation, une fois passé le délai pour contester. En cas de désaccord, un humain
   de YILGA tranche.
3. **Des prestataires vérifiés.** Pièce d'identité et documents contrôlés par YILGA avant la première
   course ; chaque course est notée par le client.
4. **Payé vite, sans surprise.** Le prestataire voit ses gains en temps réel et les retire par
   versement Mobile Money ou en espèces chez un agent YILGA. Un bonus de départ lui permet de prendre ses
   premières courses en espèces sans avancer d'argent.

Et une phrase de clôture : YILGA fonctionne avec ce que les gens ont déjà, un Android, un numéro de
téléphone, un code secret à six chiffres comme dans les apps d'argent, Orange Money ou Moov Money.

### 3.3 Les services (section « Ce que vous pouvez commander »)

Disponibles : **Livraison de colis** (point de retrait, point de livraison, taille du colis, suivi en
temps réel, paiement portefeuille ou espèces) et **Ménage à prix fixe** (tarif du catalogue YILGA).
Bientôt, affichés en retrait et sans date : Plomberie, Électricité, Coiffure, Chauffeur, Santé (les
cinq déjà affichés comme « Bientôt » dans l'app et la fiche).

### 3.4 Les parcours (section « Comment ça marche » et pages Guide)

**Client — « Commander avec YILGA »**, six étapes, chacune une phrase et l'écran réel :
1. Créer son compte avec son numéro et un code reçu par SMS, puis choisir un code secret à six chiffres
   (écrans `auth/phone`, `auth/otp`, `auth/pin-set` ; capture : le pavé du code secret).
2. Recharger son portefeuille : choisir un montant et un opérateur, composer le code USSD prêt à
   l'emploi (`(tabs)/recharge`, `payment/ussd`). Ou en espèces chez un agent YILGA.
3. Commander : livraison (adresses, taille, mode de paiement) ou ménage au tarif fixe (`order/create`,
   `services/cleaning`).
4. Suivre la course : statut, prestataire assigné avec son nom et son téléphone, position sur la carte
   (`order/track`).
5. Confirmer ou contester dans le délai affiché après la clôture ; reçu numérique (`order/receipt`).
6. Noter le prestataire d'une à cinq étoiles.

**Prestataire — « Gagner avec Yilga Pro »**, six étapes :
1. Créer son compte (même numéro et même code secret que l'app client si on en a un) et déposer ses
   documents : identité, permis, assurance selon le service (`verification/documents`,
   `verification/services`, `verification/attente`).
2. Être vérifié par YILGA, recevoir le bonus de départ à l'activation (`verification/activation`).
3. Se mettre en ligne : l'app envoie la position toute seule, le rayon se règle sur l'accueil
   (`(tabs)/home`).
4. Accepter une demande proche, avec le badge espèces ou portefeuille et le gain estimé (`demande/[id]`).
5. Mener la course en deux appuis, « Colis récupéré » puis « Livré » ; l'itinéraire s'ouvre dans l'app
   de cartes du téléphone (`course/[id]`).
6. Toucher ses gains : trois poches (gains, caution, bonus), retrait en espèces chez un agent avec un
   code, ou versement Mobile Money automatique chaque matin (`(tabs)/wallet`, `portefeuille/retrait`,
   `portefeuille/retrait-agent`, `portefeuille/versements`).

Sur l'Accueil, « Comment ça marche » résume chaque parcours en trois étapes (compte, commande ou
course, paiement) avec un lien « Voir le guide complet ».

### 3.5 Devenir prestataire (section « Devenir prestataire »)

Présente Yilga Pro en trois arguments, tous vrais : des courses près de chez vous, dans vos catégories,
avec le mode de paiement affiché avant d'accepter ; deux appuis par course, l'itinéraire dans votre app
de cartes ; vos gains visibles en temps réel, retirés chez un agent ou par Mobile Money. Bouton vers le
guide prestataire et vers le téléchargement de Yilga Pro.

### 3.6 Télécharger

La page existante (`index.html` actuel), reprise avec l'habillage commun du site : deux cartes (YILGA,
Yilga Pro), taille, date de version, quatre étapes d'installation d'un APK, note sur Android 8 et
l'absence d'iPhone. Les liens pointent sur `releases/latest/download/yilga-client.apk` et
`yilga-pro.apk` du dépôt `HamdanCoder/yilga`.

### 3.7 Pied de page et espaces à compléter

Pied de page : marque, « Services à domicile · Ouagadougou », liens vers les quatre pages, lien
Télécharger. Deux espaces restent à compléter par le fondateur et doivent être faciles à trouver dans le
code (constantes en tête de fichier, valeur vide affichée comme absente, jamais comme « [À compléter] »
à l'écran) : le numéro de téléphone ou WhatsApp de YILGA, et une adresse email de contact.

## 4. Ce à quoi le site ressemble (direction visuelle)

### 4.1 Identité

Celle des apps et des affiches, sans ajout : orange `#FF4400` (accent, boutons, titres de section
courts), encre `#0F172A`, gris `#475569` / `#94A3B8`, bord `#E2E8F0`, fond chaud `#F8F6F5` et beige
studio `#F6EEE6`, police Inter (400 à 800). Logo `logo.png` (carré orange « Y »). Aucune autre couleur,
aucune autre police, aucun emoji, aucune icône décorative hors du jeu d'icônes trait déjà utilisé dans
la fiche (`marketing/source/fiche-fonctionnalites.html`).

### 4.2 Ce qui fait la qualité

Le site doit être jugé à côté des sites d'apps grand public les mieux finis. Concrètement :

- **Les vraies apps au centre.** Les captures des apps dans les cadres de téléphone réalistes des
  affiches (`marketing/source/maquette.css` : bezel graphite, îlot, boutons, épaisseur) ; sur
  l'Accueil, deux téléphones en perspective 3D comme sur `hero-client.html`. Jamais de maquette
  dessinée ou d'illustration de stock.
- **Typographie travaillée.** Échelle modulaire nette (titre d'accueil 56 px sur ordinateur, 36 px sur
  téléphone ; sections 36 / 28 ; corps 17 / 16, interligne 1,55), interlettrage négatif sur les grands
  titres, largeur de lecture bornée à 62 caractères, pas de paragraphe de plus de trois lignes sur
  ordinateur.
- **Rythme et espace.** Une seule idée par section, séparées par des espaces généreux (96 px et plus sur
  ordinateur, 64 px sur téléphone), grilles alignées sur une colonne de 1 120 px maximum.
- **Mouvement discret.** Apparition en fondu et léger glissement des sections à l'entrée dans la fenêtre
  (IntersectionObserver, 350 ms, une seule fois), survol des boutons et cartes à 150 ms, parallaxe
  légère des téléphones de l'accroche sur ordinateur seulement. Tout mouvement est désactivé si
  `prefers-reduced-motion`. Aucune animation en boucle, aucun défilement automatique.
- **Fond studio.** Le voile chaud avec grain très léger des affiches sur l'accroche et sur la section
  Devenir prestataire (variante sombre encre), fond uni ailleurs.
- **Finitions.** Favicon, icône Apple, couleur de barre d'adresse (`theme-color`), image Open Graph
  1200×630 propre (logo, accroche, téléphone) pour que le lien soit beau sur WhatsApp et Facebook,
  titre et description par page, page 404 habillée, défilement doux vers les ancres, état visible du
  lien de navigation courant.

### 4.3 Mise en page

- **Téléphone d'abord** (largeur 360 px de référence) : la plupart des visiteurs viendront de WhatsApp.
  Point de bascule à 760 px (deux colonnes) et 1 040 px (mise en page complète). Aucun défilement
  horizontal, gouttières de 20 px.
- **En-tête** fixe, fin, fond translucide flouté : logo + YILGA à gauche, liens Philosophie, Guide,
  Prestataires, et bouton Télécharger à droite ; sur téléphone, les liens passent dans un menu plein
  écran ouvert par un bouton, fermé par Échap ou appui sur un lien.
- **Accueil**, dans l'ordre : accroche (titre, sous-titre, bouton Télécharger + lien « Voir le guide »,
  deux téléphones), Pourquoi YILGA, Notre philosophie (quatre blocs, deux par ligne sur ordinateur),
  Ce que vous pouvez commander, Comment ça marche (deux colonnes client / prestataire, trois étapes
  chacune), Devenir prestataire (sombre), Télécharger (les deux cartes), pied de page.
- **Pages Guide** : titre, phrase d'introduction, puis les six étapes en alternance texte à gauche /
  téléphone à droite et inversement sur ordinateur, empilées sur téléphone ; un sommaire ancré en haut ;
  en bas, lien vers l'autre guide et bouton Télécharger.
- **Télécharger** : la page actuelle, sous l'en-tête et le pied de page communs.

### 4.4 Captures d'écran

Prises sur l'émulateur Pixel 8 (1080×2400) avec les drivers des deux projets (`run-yilga-mobile`,
`run-yilga-pro`), données de test propres (pas de « test », pas de montants absurdes, pas d'adresse
vide), heure de la barre d'état figée et batterie pleine (`adb shell cmd overlay`/demo mode), puis
converties en WebP (qualité 85, deux tailles : 540 px et 1080 px de large). Existantes dans
`marketing/captures/` : 11 écrans client, 7 écrans Pro. À prendre en plus pour le guide : client
`auth/phone` ou `auth/otp`, `payment/ussd`, `services/cleaning`, `order/receipt` déjà présent ; Pro
`verification/documents`, `verification/activation`, `demande/[id]` présent, `portefeuille/retrait`,
`portefeuille/retrait-agent`.

## 5. Technique

- **Fichiers** : `index.html`, `guide-client.html`, `guide-prestataire.html`, `telecharger.html`,
  `404.html`, `assets/site.css`, `assets/site.js`, `assets/img/` (logo, favicons, Open Graph,
  captures WebP), `.nojekyll`. Un seul CSS, un seul JS (sans dépendance), chargés une fois.
- **Hébergement** : GitHub Pages, branche `main`, racine. Tous les liens internes relatifs pour que le
  site fonctionne sous `/yilga/` comme sous un futur domaine. Un `CNAME` pourra être ajouté plus tard sans
  rien changer d'autre.
- **APK** : releases du dépôt `HamdanCoder/yilga` ; `publier.sh` (existant) mis à jour pour ce dépôt et
  ce dossier.
- **Performance** : page d'accueil sous 1,5 Mo transférés sur téléphone (captures en WebP, chargement
  paresseux hors de l'accroche, police Inter sous-ensemble latin en `font-display: swap`), aucune
  requête tierce autre que Google Fonts. Lighthouse mobile ≥ 95 en performance, accessibilité, bonnes
  pratiques et SEO sur les quatre pages.
- **Accessibilité** : contrastes AA (orange sur blanc réservé aux grands textes et aux fonds de bouton
  avec texte blanc), navigation clavier complète, focus visible, textes alternatifs décrivant l'écran
  montré, titres hiérarchisés, `lang="fr"`.
- **Vérification** : rendu des quatre pages à 360, 760 et 1 280 px de large par Chrome headless
  (`marketing/rendre.sh` ou équivalent) et relecture visuelle de chaque capture ; validation HTML
  (`npx html-validate` ou le validateur W3C hors ligne) ; vérification des liens internes ; Lighthouse
  via `npx lighthouse` sur l'aperçu local.

## 6. Laissé au constructeur

- Le texte exact de chaque phrase, dans les bornes du §3 et des règles (français, sobre, vérifiable).
- Le détail des réglages visuels (ombres, rayons, espacements fins), tant qu'il respecte le §4.
- L'ordre de réalisation ; proposition : squelette et habillage commun, Accueil, captures manquantes,
  pages Guide, Télécharger et 404, finitions (Open Graph, favicons), vérifications.
- Le choix de prendre ou non de nouvelles captures pour les écrans déjà disponibles si les existantes
  montrent des données de test peu présentables.
