# MagicDatabase

MagicDatabase est une application Python permettant de construire et maintenir une base de données **Magic: The Gathering** à partir des données fournies par l'API **Scryfall**.

Le projet a pour objectif de proposer une architecture claire, évolutive et facilement maintenable, inspirée des bonnes pratiques de développement (séparation des responsabilités, typage, journalisation, documentation...).

---

# Fonctionnalités actuelles

## Version 1.0

* Lecture d'un fichier Excel (`Base_Reference.xlsx`)
* Récupération des traductions françaises depuis l'API Scryfall
* Mise à jour des colonnes `Name_FR` et `OracleText_FR`
* Sauvegarde automatique du fichier Excel

## Version 1.1

* Architecture refactorisée
* Ajout du système de journalisation (`logging`)
* Annotations de types
* Documentation du code (docstrings)
* Amélioration de la gestion des erreurs
* Publication sur GitHub

## Version 1.2

* Ajout d'un système de cache local des données Scryfall afin d'améliorer les performances et de limiter les appels à l'API.
* Ajout du support des cartes multifaces (nom et texte Oracle).

---

# Architecture du projet

```text
MagicDatabase/
│
├── main.py
├── config.py
├── logging_config.py
├── requirements.txt
│
├── models/
│   ├── card.py
│   └── translation.py
│
├── repositories/
│   └── excel_repository.py
│
├── services/
│   ├── scryfall_service.py
│   └── sync_service.py
│
├── cache/
├── logs/
│
└── Base_Reference.xlsx
```

L'application suit une architecture en couches :

```text
main.py
    │
    ▼
SyncService
    │
    ├───────────────┐
    ▼               ▼
ExcelRepository  ScryfallService
```

Chaque couche possède une responsabilité unique :

* **models** : représentation des données métier.
* **repositories** : accès aux fichiers de données.
* **services** : logique métier et appels à l'API.
* **config** : configuration globale de l'application.

---

# Prérequis

* Python 3.11 ou supérieur (3.13 recommandé)
* Git

---

# Installation

Cloner le dépôt :

```bash
git clone https://github.com/<votre-utilisateur>/MagicDatabase.git
cd MagicDatabase
```

Créer un environnement virtuel :

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Installer les dépendances :

```bash
pip install -r requirements.txt
```

---

# Utilisation

Lancer la synchronisation :

```bash
python main.py
```

L'application :

1. charge le fichier `Base_Reference.xlsx` ;
2. interroge l'API Scryfall ;
3. récupère les traductions françaises ;
4. met à jour le fichier Excel ;
5. sauvegarde les modifications.

---

# Journalisation

Le projet utilise le module standard `logging`.

Les principaux événements sont enregistrés :

* démarrage de la synchronisation ;
* progression du traitement ;
* erreurs de communication avec Scryfall ;
* fin du traitement.

Une évolution future permettra également d'enregistrer automatiquement les journaux dans le dossier `logs/`.

---

# Dépendances

* requests
* openpyxl

Installation :

```bash
pip install -r requirements.txt
```

---

# Feuille de route

## V1.0 ✅

* Synchronisation des traductions françaises

## V1.1 ✅

* Documentation
* Logging
* Typage
* Revue de code

## V1.2 ✅

* Cache local des réponses Scryfall
* Amélioration des performances

## V2.0 🚧

* Import automatique d'une extension complète

## V3.0

* Gestion d'une collection personnelle

## V4.0

* Gestion de decks

## V5.0

* Tableau de bord et statistiques

---

# Licence

Ce projet est distribué sous licence MIT.

Voir le fichier `LICENSE` pour plus d'informations.

---

# Remerciements

Les données des cartes Magic: The Gathering sont fournies par l'API publique de **Scryfall**.

https://scryfall.com/docs/api
