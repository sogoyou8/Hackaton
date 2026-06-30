# Documentation de Déploiement Technique - TechCorp Industries

Ce guide explique comment installer, sécuriser et lancer le serveur d'inférence ainsi que l'interface de chat pour le projet TechCorp Industries.

---

## 1. Déploiement du Serveur d'Inférence (Ollama)

Nous avons choisi **Ollama** comme solution d'inférence en raison de sa légèreté, de sa facilité de configuration et de ses performances optimales en local via quantization.

### Prérequis
1. Télécharger et installer Ollama depuis [ollama.com/download](https://ollama.com/download).
2. S'assurer que le service Ollama tourne en tâche de fond.

### Création du modèle personnalisé sécurisé
Nous utilisons un `Modelfile` configuré avec des consignes système strictes de protection des données (prévention des fuites d'identifiants et de backdoor).

1. Ouvrir un terminal dans le répertoire `rendu/infra/`.
2. Lancer la création du modèle personnalisé avec la commande :
   ```bash
   ollama create techcorp-finance -f Modelfile
   ```
3. Lancer le modèle :
   ```bash
   ollama run techcorp-finance
   ```
4. Le serveur répondra sur l'API locale : `http://localhost:11434`.

---

## 2. Déploiement de l'Interface Web (DEV WEB)

L'interface utilisateur permet aux analystes d'échanger en temps réel avec le modèle.

### Lancement
*   **Sous Windows :** Double-cliquer sur le lanceur rapide `rendu/devweb/start_chat.bat`.
*   **Sous macOS / Linux :** Ouvrir le fichier `rendu/devweb/index.html` dans votre navigateur Web préféré.

### Fonctionnalités de l'UI
*   **Status Tracker :** Indique en temps réel si le serveur Ollama est démarré et joignable.
*   **Local History :** Persistance automatique des conversations dans le stockage local du navigateur (`localStorage`).

---

## 3. Données & Sécurité (DATA / CYBER)
*   **Nettoyage :** Le dataset financier a été nettoyé via le script `clean_dataset.py` pour éliminer toute trace d'empoisonnement de données (backdoor).
*   **Audit :** Le rapport complet d'audit de sécurité et de robustesse est consultable dans `rendu/cyber/rapport_audit.md`.
