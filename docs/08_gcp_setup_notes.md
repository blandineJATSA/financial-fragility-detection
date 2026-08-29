# Mise en place de l'infrastructure GCP

## Vue d'ensemble

GCP fournit trois services utilisés dans ce projet :
- **GCS (Google Cloud Storage)** : stockage de fichiers (les données brutes)
- **BigQuery** : base de données SQL pour la requête et l'analyse (les données modélisées)
- **Service Account** : identité de machine pour que les scripts s'authentifient sans intervention humaine

Ce document explique comment les configurer de façon minimaliste et sécurisée.

---

## Ressources créées

| Ressource | Nom | Objectif |
|---|---|---|
| **Projet GCP** | `finprev-portfolio` | Conteneur logique qui regroupe les ressources et la facturation. Isolé pour ce portfolio. |
| **Bucket GCS** | `finprev-raw-data` | Stockage des données brutes (CSV, Parquet). Région `europe-west1` pour la conformité RGPD. |
| **Dataset BigQuery** | `finprev` | Base de données SQL pour transformer et interroger les données. Même région que le bucket (sinon les transferts coûtent cher). |
| **Service Account** | `finprev-pipeline-sa` | Compte de machine qui exécute les pipelines sans mot de passe humain. Email : `finprev-pipeline-sa@finprev-portfolio.iam.gserviceaccount.com` |

---

## Rôles et permissions

### Permissions attribuées au service account

```
- roles/bigquery.dataEditor    → peut lire et écrire les données dans BigQuery
- roles/bigquery.jobUser       → peut exécuter des requêtes BigQuery
- roles/storage.objectAdmin    → peut lire/écrire/supprimer des fichiers dans le bucket GCS
```

**Important** : jamais de rôle `Owner` sur ce compte. Les permissions sont **volontairement minimales** (principle of least privilege) — le compte ne peut faire que ce dont il a besoin.

### Niveaux d'attribution

- `bigquery.dataEditor` et `bigquery.jobUser` : attribués **au niveau projet**
- `storage.objectAdmin` : attribué **uniquement au bucket**, pas au projet entier

---

## Étapes suivies (CLI)

### 1. Authentification et projet
```powershell
gcloud auth login
gcloud config set project finprev-portfolio
gcloud auth application-default set-quota-project finprev-portfolio
```
*Explique à votre machine GCP quel compte utiliser et quel projet.*

### 2. Activation des services GCP
```powershell
gcloud services enable bigquery.googleapis.com storage.googleapis.com
```
*Autorise votre projet à utiliser BigQuery et GCS (c'est un garde-fou de GCP).*

### 3. Création du bucket GCS
```powershell
gsutil mb -l europe-west1 "gs://finprev-raw-data"
```
*Crée un dossier "dans le cloud" qui stockera les fichiers Parquet bruts.*

### 4. Création du dataset BigQuery
*Créé via la console GCP* — accès direct et plus fluide que CLI pour cette étape.

### 5. Création du service account
```powershell
gcloud iam service-accounts create finprev-pipeline-sa `
  --display-name="FinPrev pipeline service account" `
  --project=finprev-portfolio
```
*Crée une "identité de robot" qui va exécuter les pipelines sans intervention humaine.*

### 6. Attribution des rôles BigQuery
```powershell
gcloud projects add-iam-policy-binding finprev-portfolio `
  --member="serviceAccount:finprev-pipeline-sa@finprev-portfolio.iam.gserviceaccount.com" `
  --role="roles/bigquery.dataEditor"

gcloud projects add-iam-policy-binding finprev-portfolio `
  --member="serviceAccount:finprev-pipeline-sa@finprev-portfolio.iam.gserviceaccount.com" `
  --role="roles/bigquery.jobUser"
```
*Donne au robot la permission de lire/écrire dans BigQuery et d'exécuter des requêtes.*

### 7. Attribution du rôle GCS
```powershell
gcloud storage buckets add-iam-policy-binding gs://finprev-raw-data `
  --member="serviceAccount:finprev-pipeline-sa@finprev-portfolio.iam.gserviceaccount.com" `
  --role="roles/storage.objectAdmin"
```
*Donne au robot la permission d'interagir avec le bucket.*

### 8. Génération de la clé d'authentification
```powershell
gcloud iam service-accounts keys create infra/gcp/service-account.json `
  --iam-account=finprev-pipeline-sa@finprev-portfolio.iam.gserviceaccount.com
```
*Génère un fichier JSON qui contient la "clé privée" du robot. Jamais commitée, protégée par `.gitignore`.*

---

## Test de validation

1. Authentification avec la clé du service account :
   ```powershell
   gcloud auth activate-service-account --key-file=infra/gcp/service-account.json
   ```

2. Upload d'un fichier de test dans le bucket pour vérifier les permissions :
   ```powershell
   gsutil cp test.txt gs://finprev-raw-data/
   ```

3. Restauration du compte personnel comme compte actif :
   ```powershell
   gcloud auth login
   ```

**Résultat** : l'upload a réussi → les permissions sont opérationnelles de bout en bout.

---

## Pièges évités

### Nom du service account
La première tentative via la console GCP a produit un compte nommé `finprev-portfolio` au lieu de `finprev-pipeline-sa`. Le champ ID s'était rempli automatiquement avec le nom du projet.
**Solution** : suppression et recréation en CLI pour éviter toute ambiguïté.

### Région BigQuery ≠ Région GCS
Si BigQuery et GCS sont dans des régions différentes, les transferts sont facturés.
**Solution** : toujours utiliser la même région (`europe-west1`).

---

## Sécurité

### Fichier de clé
`infra/gcp/service-account.json` est exclu du dépôt via `.gitignore`. Vérifié explicitement après génération que `git status` ne le liste pas.

### Permissions minimales
Le service account n'a que les rôles nécessaires pour :
- Lire et écrire dans BigQuery
- Lire et écrire dans GCS

Aucune permission d'administration du projet, suppression de ressources, etc.

---

## Coûts

- **Free tier BigQuery** : 1 TB de requêtes par mois, largement suffisant pour ce volume
- **Free tier GCS** : 5 GB de stockage gratuit, extensible
- **Alertes de budget** : à configurer dans la console GCP (Facturation → Budgets et alertes) — étape encore à faire

Pour un portfolio, ces coûts restent proches de zéro.
