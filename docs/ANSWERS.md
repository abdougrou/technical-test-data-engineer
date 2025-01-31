# Réponses du test

## _Utilisation de la solution (étape 1 à 3)_

### Étape 1: Création et activation de l'environnement virtuel.

1. Créer l'environnement virtuel (je l'ai nommé `moovai-test-env`) en exécutant la commande:

    ```python -m venv moovai-test-env```

2. Activer l'environnement selon votre système d'exploitation (J'ai utilisé l'environnement Windows pour la resolution du test):

    **Windows**: ``.\moovai-test-env\Scripts\activate``

    **Linux/MacOS**: ``source moovai-test-env/bin/activate``

3. Installer la liste des dépendences:

    ```pip install -r requirements.txt```

### Étape 2: Élaboration du flux de données.
Voici les étapes à suivre pour élaborer le flux de données:
 
1. Lancer le serveur **FastAPI**:
    - Accéder au dossier `src/moovitamix_fastapi` (commande `cd src/moovitamix_fastapi`).
    - Exécuter la commande `python -m uvicorn main:app`

2. Lancer le flux de données **DailyIngestionPipeline**:

    - Accéder au dossier `src/data_pipelines` (commande `cd src/data_pipelines`).
    - Exécuter la commande `python daily_ingestion_pipeline.py`.

3. Automatiser l'exécution du script:

    Pour automatiser la récupération des données quotidiennement, on peut utiliser des planificateurs locales:

    - **Windows**: Le programme `Task Scheduler`

    - **Linux/MacOS**: Le programme `cron`

    On peut également utiliser les services cloud:

    - **Amazon**: Configurer une fonction Lambda avec CloudWatch

    - **Google**: Configurer une fonction Cloud Functions avec Cloud Scheduler

### Étape 3: Tests.
J'ai implémenter 5 tests essentiels pour verifier le fonctionnement du flux de données:

1. `test_fetch_data_success`: 
    Valide la gestion de la pagination et la collecte complète des données.

2. `test_fetch_data_error_handling`: 
    Assure la résilience du pipeline en cas de défaillance de l'API

3. `test_directory_creation`: 
    Confirme l’organisation correcte des données (structure des dossiers).

4. `test_save_to_csv_special_handling`: 
    Vérifie la gestion correcte des types de données complexes (liste d'éléments listen_history).

5. `test_empty_data_handling`: 
    Assure une gestion élégante des cas limites (edge cases).

## Questions (étapes 4 à 7)

### Étape 4

_votre réponse ici_

### Étape 5

_votre réponse ici_

### Étape 6

_votre réponse ici_

### Étape 7

_votre réponse ici_
