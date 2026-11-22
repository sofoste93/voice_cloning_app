# Neptune · Studio vocal

Neptune permet d’écouter des enregistrements d’origine et de créer des extraits de synthèse à partir de références vocales.

## Installer sous Windows

Télécharge [Neptune 1.0.0 pour Windows 64 bits](https://github.com/sofoste93/voice_cloning_app/releases/latest) et lance le fichier Setup.exe. L’installation se fait pour ton compte Windows et télécharge les dépendances lors du premier passage. Prévois une connexion Internet et quelques gigaoctets d’espace libre.

L’application installée enregistre ses nouveaux extraits dans `%LOCALAPPDATA%\Neptune\audio`. La désinstallation conserve ce dossier.

## Lancer depuis les sources

Depuis le dossier du projet, avec Python 3.11 et PowerShell :

```powershell
py -3.11 -m venv .venv-neptune
.\.venv-neptune\Scripts\python.exe -m pip install -r requirements.txt --extra-index-url https://download.pytorch.org/whl/cpu
.\.venv-neptune\Scripts\python.exe -m src.main
```

Si l’environnement `.venv-neptune` est déjà installé, seule la dernière commande est nécessaire.

## Écouter et créer

- Ajoute les fichiers WAV, MP3 ou FLAC dans **Enregistrements d’origine**. Un double-clic lance la lecture. Neptune mémorise leurs emplacements et laisse les fichiers à leur place.
- Pour la synthèse, privilégie quelques secondes de parole claire, sans musique ni voix superposées. Choisis **Voix de référence · local**, sélectionne la langue du texte et écris le message. La première utilisation demande ton accord pour la [licence de XTTS v2](https://huggingface.co/coqui/XTTS-v2/blob/main/LICENSE.txt), puis télécharge le modèle. La synthèse utilise ensuite tes références et ton texte sur ton ordinateur.
- La **Voix standard · en ligne** utilise une voix générique et envoie uniquement le texte au service vocal Microsoft.
- Neptune sauvegarde les nouveaux extraits dans `src/audio` et liste aussi les anciens MP3 et WAV des dossiers `src/audio` et `audio`.

Le premier chargement et la synthèse peuvent prendre du temps sur le processeur. Les résultats de synthèse figurent dans **Extraits générés**.

## Construire l’installateur

Installe [Inno Setup 6](https://jrsoftware.org/isdl.php), puis lance depuis le dossier du projet :

```powershell
.\packaging\build.ps1 -Compiler 'C:\Program Files (x86)\Inno Setup 6\ISCC.exe'
```

La version vient de `src/__init__.py`. Le script crée l’installateur et son empreinte SHA-256 dans `dist`. Les dépendances de l’installateur sont épinglées dans `packaging/requirements-windows.txt`.
