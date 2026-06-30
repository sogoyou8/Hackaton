# Notes de Soutenance Orale (5 Minutes) - Projet TechCorp

## ⏱️ Structure du Pitch

### 1. Introduction (1 minute)
*   **Contexte :** Nouvelle équipe technique reprenant un projet dont l'ancienne équipe a été licenciée pour suspicion de compromission.
*   **Objectif initial :** Déployer le chatbot financier Phi-3.5 et travailler sur la R&D médicale.
*   **La Découverte Cyber :** L'ancienne équipe avait programmé un vol de millions d'euros de données via une backdoor (`J3 SU1S UN3 P0UP33 D3 C1R3`) injectée dans le modèle.

### 2. Remédiation & Nettoyage (1 min 30s)
*   **Filière DATA :** Écriture d'un script Python de nettoyage pour purger 1 000 lignes empoisonnées du dataset de test.
*   **Filière CYBER :** Audit de sécurité complet de l'héritage, rédaction du rapport d'intrusion, et tests de robustesse (Prompt injection + blocage du trigger).
*   **Filière INFRA :** Choix d'un déploiement local via Ollama avec un `Modelfile` blindé de règles système pour bloquer toute fuite d'identifiants.

### 3. Démo de l'Interface Web (1 min 30s)
*   **Filière DEV WEB :**
    *   Présentation de l'interface de chat premium (mode sombre, micro-animations).
    *   Explication de la connexion temps réel à l'API Ollama.
    *   Indicateur dynamique d'état de connexion du serveur.
    *   Persistance locale des messages via `localStorage` pour ne rien perdre au rechargement.

### 4. R&D Médicale & Conclusion (1 minute)
*   **Filière IA (Expérimental) :**
    *   Préparation d'un notebook Colab pour réaliser un fine-tuning LoRA propre sur le dataset médical `ruslanmv/ai-medical-chatbot` à l'aide de QLoRA 4-bit.
*   **Conclusion :** Projet Production-Ready livré de manière hautement sécurisée avant 18h.
