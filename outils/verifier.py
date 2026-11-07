#!/usr/bin/env python3
"""Contrôleur des pages du site YILGA.

    python3 outils/verifier.py [--reseau] [--tout]

Vérifie chaque page HTML de la racine contre les règles du plan (métadonnées, navigation,
liens, images, textes interdits, mouvement). Code de sortie 1 au premier échec.
"""
import os
import re
import sys
import urllib.request
from html.parser import HTMLParser

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_URL = "https://hamdancoder.github.io/yilga/"
PAGES_NAV = ["index.html", "guide-client.html", "guide-prestataire.html", "telecharger.html"]
CAPTURES = ["client-code-secret", "client-telephone", "client-accueil", "client-recharge", "client-ussd",
            "client-commande", "client-menage", "client-carte", "client-suivi", "client-recu", "client-portefeuille",
            "pro-documents", "pro-activation", "pro-accueil", "pro-demande", "pro-course", "pro-portefeuille",
            "pro-retrait", "pro-retrait-agent", "pro-statistiques"]
INTERDITS = ["yilga-apk", "à compléter", "30 minutes", "todo", "lorem", "download", "http://"]


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.lang = None
        self.title = ""
        self.metas = {}
        self.links = []          # (rel, href, attrs)
        self.hrefs = []          # href de <a>
        self.srcs = []           # src, srcset
        self.imgs = []           # attrs
        self.ids = set()
        self.classes = []        # (balise, classes, attrs)
        self.nav_entete = False
        self.nav_liens = []
        self.aria_current = 0
        self.pied = False
        self._dans_title = False
        self._dans_nav = 0
        self._dans_code = 0
        self.texte = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        cls = (a.get("class") or "").split()
        self.classes.append((tag, cls, a))
        if a.get("id"):
            self.ids.add(a["id"])
        if tag == "html":
            self.lang = a.get("lang")
        if tag == "title":
            self._dans_title = True
        if tag == "meta":
            cle = a.get("name") or a.get("property")
            if cle:
                self.metas[cle] = a.get("content", "")
        if tag == "link":
            self.links.append((a.get("rel", ""), a.get("href", ""), a))
            if a.get("href"):
                self.srcs.append(a["href"])
        if tag == "a" and a.get("href"):
            self.hrefs.append(a["href"])
            if self._dans_nav:
                self.nav_liens.append(a["href"])
        if a.get("aria-current") == "page":
            self.aria_current += 1
        if tag in ("img", "script", "source") and a.get("src"):
            self.srcs.append(a["src"])
        if tag in ("img", "source") and a.get("srcset"):
            for part in a["srcset"].split(","):
                self.srcs.append(part.strip().split()[0])
        if tag == "img":
            self.imgs.append(a)
        if tag == "nav" and "entete__nav" in cls:
            self.nav_entete = True
            self._dans_nav = 1
        elif tag == "nav" and self._dans_nav:
            self._dans_nav += 1
        if tag == "footer" and "pied" in cls:
            self.pied = True
        if tag in ("script", "style"):
            self._dans_code += 1
        for cle in ("alt", "title", "content", "aria-label"):
            if a.get(cle):
                self.texte.append(a[cle])

    def handle_endtag(self, tag):
        if tag == "title":
            self._dans_title = False
        if tag == "nav" and self._dans_nav:
            self._dans_nav -= 1
        if tag in ("script", "style"):
            self._dans_code -= 1

    def handle_data(self, data):
        if self._dans_title:
            self.title += data
        if not self._dans_code:
            self.texte.append(data)


def lire(chemin):
    with open(chemin, encoding="utf-8") as f:
        return f.read()


def analyser(html):
    p = Page()
    p.feed(html)
    return p


def verifier_page(nom, html, p, options):
    e = []
    est_404 = nom == "404.html"
    if p.lang != "fr":
        e.append(("lang", f"attendu lang=fr, trouvé {p.lang!r}"))
    t = p.title.strip()
    if not t or len(t) > 60:
        e.append(("titre", f"{len(t)} caractères"))
    d = p.metas.get("description", "")
    if not 50 <= len(d) <= 160:
        e.append(("description", f"{len(d)} caractères"))
    canon = [h for r, h, _ in p.links if "canonical" in r.split()]
    attendu = BASE_URL + ("" if nom == "index.html" else nom)
    if not est_404 and canon != [attendu]:
        e.append(("canonical", f"attendu {attendu}, trouvé {canon}"))
    if not est_404:
        for cle in ("og:title", "og:description", "og:image", "og:url"):
            if not p.metas.get(cle):
                e.append(("og", f"{cle} manquant"))
        img = p.metas.get("og:image", "")
        if img and not img.startswith(BASE_URL + "assets/img/"):
            e.append(("og", f"og:image non absolue : {img}"))
        if p.metas.get("og:url") and p.metas["og:url"] != attendu:
            e.append(("og", f"og:url {p.metas['og:url']} ≠ canonical"))
    if not p.nav_entete:
        e.append(("nav", "nav.entete__nav absent"))
    else:
        for cible in PAGES_NAV:
            ok = any(h == cible or h.startswith(cible + "#") or (cible == "index.html" and h in ("./", "index.html"))
                     for h in p.nav_liens)
            if not ok:
                e.append(("nav", f"lien vers {cible} absent de la navigation"))
        if not est_404 and p.aria_current != 1:
            e.append(("nav", f"{p.aria_current} aria-current=page (attendu 1)"))
    if not p.pied:
        e.append(("pied", "footer.pied absent"))
    # liens et ressources relatifs (une page prévue par le plan mais pas encore écrite est signalée, pas comptée)
    avenir = set()
    for ref in dict.fromkeys(p.hrefs + p.srcs):
        if re.match(r"^(https?:|mailto:|tel:|data:)", ref):
            continue
        cible, _, ancre = ref.partition("#")
        page_cible = nom if cible in ("", "./") else cible
        chemin = os.path.join(RACINE, page_cible.lstrip("./"))
        if not os.path.exists(chemin):
            if page_cible in PAGES_NAV:
                avenir.add(page_cible)
            else:
                e.append(("liens", f"{ref} introuvable"))
            continue
        if not ancre:
            continue
        if page_cible == nom:
            cible_p = p
        elif chemin.endswith(".html"):
            cible_p = analyser(lire(chemin))
        else:
            continue
        if ancre in cible_p.ids:
            continue
        if page_cible == "index.html" and not cible_p.nav_entete:
            avenir.add(f"{page_cible}#{ancre}")  # ancienne page de téléchargement, remplacée à la tâche 3
        else:
            e.append(("liens", f"ancre #{ancre} introuvable dans {page_cible}"))
    if avenir:
        print(f"{nom}: à venir : {', '.join(sorted(avenir))}")
    for a in p.imgs:
        if "alt" not in a:
            e.append(("images", f"img {a.get('src')} sans alt"))
        elif a["alt"].strip() == "" and a.get("aria-hidden") != "true" and "captures/" in (a.get("src") or ""):
            e.append(("images", f"capture {a.get('src')} avec alt vide"))
    visible = " ".join(p.texte).lower()
    for mot in INTERDITS:
        if mot == "http://":
            if mot in html.lower():
                e.append(("interdits", "« http:// » présent"))
        elif mot in visible:
            e.append(("interdits", f"« {mot} » présent dans le texte"))
    if options.get("reseau"):
        for h in p.hrefs:
            if h.startswith("https://github.com/HamdanCoder/yilga/releases/latest/download/"):
                try:
                    req = urllib.request.Request(h, method="HEAD")
                    with urllib.request.urlopen(req, timeout=20) as r:
                        code = r.status
                except Exception as ex:  # noqa: BLE001
                    code = getattr(ex, "code", str(ex))
                if code != 200:
                    e.append(("reseau", f"{h} → {code}"))
    return e


def section(html, ident):
    m = re.search(r'<section[^>]*\bid="%s"[^>]*>(.*?)</section>' % re.escape(ident), html, re.S)
    return m.group(1) if m else None


def verifier_accueil(html, p):
    e = []
    for ident in ("haut", "philosophie", "services", "comment", "prestataires", "telecharger"):
        if ident not in p.ids:
            e.append(("accueil", f"id #{ident} absent"))
    if len(re.findall(r"<h1\b", html)) != 1:
        e.append(("accueil", "il faut exactement un h1"))
    scene = re.search(r'<div[^>]*class="[^"]*\bscene\b[^"]*"[^>]*>(.*?)</div>\s*</div>', html, re.S)
    if len(re.findall(r'class="[^"]*\bphone\b', scene.group(1) if scene else "")) < 2:
        e.append(("accueil", "moins de deux .phone dans .scene"))
    services = section(html, "services") or ""
    for libelle in ("Plomberie", "Électricité", "Coiffure", "Chauffeur", "Santé"):
        if libelle not in services:
            e.append(("accueil", f"« {libelle} » absent de #services"))
        if html.count(libelle) != services.count(libelle):
            e.append(("accueil", f"« {libelle} » présent hors de #services"))
    if "bientot" not in services:
        e.append(("accueil", "aucun élément .bientot dans #services"))
    if services.count("Bientôt") and not re.search(r'class="[^"]*\bbientot\b[^"]*"[^>]*>[^<]*Bientôt|bientot[^>]*>(?:(?!</).)*Bientôt', services, re.S):
        e.append(("accueil", "« Bientôt » hors d'un élément .bientot"))
    for apk in ("yilga-client.apk", "yilga-pro.apk"):
        if not any(h.endswith(apk) for h in p.hrefs):
            e.append(("accueil", f"lien {apk} absent"))
    haut = section(html, "haut") or ""
    for img in re.findall(r"<img\b[^>]*>", haut):
        if 'loading="lazy"' in img:
            e.append(("accueil", "image de l'accroche en loading=lazy"))
    reste = html.replace(haut, "")
    for img in re.findall(r"<img\b[^>]*>", reste):
        if 'loading="lazy"' not in img and 'class="marque' not in img and "logo.png" not in img:
            e.append(("accueil", f"image sans loading=lazy : {img[:60]}"))
    return e


def verifier_guide(nom, html, p):
    e = []
    etapes = re.findall(r'<section[^>]*class="[^"]*\bguide__etape\b[^"]*"[^>]*id="([^"]+)"[^>]*>(.*?)</section>', html, re.S)
    if len(etapes) != 6:
        e.append(("guide", f"{len(etapes)} section.guide__etape (attendu 6)"))
    for ident, corps in etapes:
        if not re.search(r"<h2\b", corps):
            e.append(("guide", f"étape #{ident} sans h2"))
        if not re.search(r"<p\b", corps):
            e.append(("guide", f"étape #{ident} sans p"))
        m = re.search(r'<img\b[^>]*src="assets/img/captures/([a-z-]+)-\d+\.webp"', corps)
        if not m or m.group(1) not in CAPTURES:
            e.append(("guide", f"étape #{ident} sans capture du contrat"))
    sommaire = re.search(r'<nav[^>]*class="[^"]*\bguide__sommaire\b[^"]*"[^>]*>(.*?)</nav>', html, re.S)
    liens = re.findall(r'href="#([^"]+)"', sommaire.group(1)) if sommaire else []
    if sorted(liens) != sorted(i for i, _ in etapes) or len(liens) != 6:
        e.append(("guide", "nav.guide__sommaire doit lier les six étapes"))
    autre = "guide-prestataire.html" if nom == "guide-client.html" else "guide-client.html"
    if autre not in p.hrefs:
        e.append(("guide", f"lien vers {autre} absent"))
    if "telecharger.html" not in p.hrefs:
        e.append(("guide", "lien vers telecharger.html absent"))
    return e


def dimensions_png(chemin):
    with open(chemin, "rb") as f:
        en_tete = f.read(24)
    if en_tete[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    return int.from_bytes(en_tete[16:20], "big"), int.from_bytes(en_tete[20:24], "big")


def verifier_finitions(nom, html, p):
    e = []
    icones = [(r, h) for r, h, _ in p.links if r in ("icon", "apple-touch-icon")]
    if ("icon", "assets/img/favicon.svg") not in icones:
        e.append(("finitions", "favicon.svg absent"))
    if not any(r == "apple-touch-icon" for r, _ in icones):
        e.append(("finitions", "apple-touch-icon absent"))
    if p.metas.get("theme-color") != "#F8F6F5":
        e.append(("finitions", "theme-color attendu #F8F6F5"))
    if nom != "404.html":
        if p.metas.get("og:image") != BASE_URL + "assets/img/og.png":
            e.append(("finitions", "og:image doit être assets/img/og.png"))
        if p.metas.get("og:image:width") != "1200" or p.metas.get("og:image:height") != "630":
            e.append(("finitions", "og:image:width/height 1200×630 attendus"))
        if p.metas.get("twitter:card") != "summary_large_image":
            e.append(("finitions", "twitter:card summary_large_image attendu"))
    return e


def verifier_images_site():
    e = []
    og = os.path.join(RACINE, "assets", "img", "og.png")
    if not os.path.exists(og):
        e.append(("finitions", "assets/img/og.png absent"))
    else:
        if os.path.getsize(og) > 300_000:
            e.append(("finitions", f"og.png pèse {os.path.getsize(og)//1000} Ko (max 300)"))
        if dimensions_png(og) != (1200, 630):
            e.append(("finitions", f"og.png fait {dimensions_png(og)} (attendu 1200×630)"))
    if not os.path.exists(os.path.join(RACINE, "404.html")):
        e.append(("finitions", "404.html absent"))
    else:
        q = analyser(lire(os.path.join(RACINE, "404.html")))
        if not q.nav_entete or "index.html" not in q.hrefs:
            e.append(("finitions", "404.html doit porter l'en-tête et un lien vers index.html"))
    return e


def verifier_poids(html, p):
    total = 0
    vus = set()
    for ref in p.srcs:
        if ref.startswith(("http", "data:")):
            continue
        vus.add(ref.split("#")[0])
    # pour chaque srcset, ne compter que la plus petite source
    for m in re.finditer(r'srcset="([^"]+)"', html):
        parts = [x.strip().split() for x in m.group(1).split(",")]
        if len(parts) > 1:
            tailles = sorted(parts, key=lambda q: int(q[1][:-1]) if len(q) > 1 and q[1][:-1].isdigit() else 0)
            for q in tailles[1:]:
                vus.discard(q[0])
    for ref in vus:
        chemin = os.path.join(RACINE, ref)
        if os.path.exists(chemin):
            total += os.path.getsize(chemin)
    total += len(html.encode())
    if total > 1_500_000:
        return [("poids", f"{total//1000} Ko référencés par index.html (max 1 500)")]
    return []


def verifier_css():
    e = []
    chemin = os.path.join(RACINE, "assets", "site.css")
    if not os.path.exists(chemin):
        return [("motion", "assets/site.css absent")]
    css = lire(chemin)
    if "@media (prefers-reduced-motion: reduce)" not in css:
        e.append(("motion", "pas de @media (prefers-reduced-motion: reduce)"))
    if not re.search(r"\.js \.reveal\s*\{[^}]*opacity:\s*0", css):
        e.append(("motion", "la règle cachant .reveal doit être « .js .reveal{opacity:0 … } »"))
    if re.search(r"(?<!\.js )\.reveal\s*\{[^}]*opacity:\s*0", css):
        e.append(("motion", ".reveal est caché sans le préfixe .js"))
    return e


def verifier_captures():
    e = []
    dossier = os.path.join(RACINE, "assets", "img", "captures")
    for nom in CAPTURES:
        for largeur, maxi in ((540, 120_000), (1080, 350_000)):
            chemin = os.path.join(dossier, f"{nom}-{largeur}.webp")
            if not os.path.exists(chemin):
                e.append(("captures", f"{nom}-{largeur}.webp absent"))
            elif os.path.getsize(chemin) > maxi:
                e.append(("captures", f"{nom}-{largeur}.webp pèse {os.path.getsize(chemin)//1000} Ko (max {maxi//1000})"))
    return e


def main(argv):
    options = {"reseau": "--reseau" in argv, "tout": "--tout" in argv}
    echecs = 0
    pages = 0
    for nom in sorted(f for f in os.listdir(RACINE) if f.endswith(".html")):
        html = lire(os.path.join(RACINE, nom))
        p = analyser(html)
        if nom == "index.html" and not p.nav_entete and not options["tout"]:
            continue  # ancienne page de téléchargement, remplacée à la tâche 3
        pages += 1
        echecs_page = verifier_page(nom, html, p, options)
        if nom == "index.html":
            echecs_page += verifier_accueil(html, p) + verifier_poids(html, p)
        if nom.startswith("guide-"):
            echecs_page += verifier_guide(nom, html, p)
        echecs_page += verifier_finitions(nom, html, p)
        for regle, detail in echecs_page:
            print(f"{nom}: {regle}: {detail}")
            echecs += 1
    for regle, detail in verifier_css():
        print(f"assets/site.css: {regle}: {detail}")
        echecs += 1
    for regle, detail in verifier_images_site():
        print(f"site: {regle}: {detail}")
        echecs += 1
    for regle, detail in verifier_captures():
        print(f"assets/img/captures: {regle}: {detail}")
        echecs += 1
    print(f"{pages} page(s), {echecs} échec(s)")
    return 1 if echecs else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
