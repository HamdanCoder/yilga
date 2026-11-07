# Téléchargement des applications YILGA

Page publique de téléchargement des APK Android de YILGA (clients) et Yilga Pro (prestataires) : https://hamdancoder.github.io/yilga/

Les APK sont publiés dans les *Releases* de ce dépôt ; les liens `releases/latest/download/yilga-client.apk` et `releases/latest/download/yilga-pro.apk` pointent toujours sur la dernière version.

## Publier une nouvelle version

```bash
gh release create v2026.11.06 \
  yilga-client.apk yilga-pro.apk \
  --repo HamdanCoder/yilga --title "Version du 6 novembre 2026" --notes "…"
```

Les fichiers doivent s'appeler exactement `yilga-client.apk` et `yilga-pro.apk`. Mettre ensuite à jour la date et la taille dans `index.html`.
