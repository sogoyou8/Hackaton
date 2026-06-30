# Rapport de Qualité des Données (DATA) - TechCorp Industries

## 1. Jeu de données Financier (`finance_dataset_final.json` et `test_dataset_16000.json`)

### Analyse Générale
*   **Volume initial :** 16 000 entrées pour le test, et 2 100 entrées pour le dataset d'entraînement final.
*   **Format :** JSON contenant des paires d'instructions et de réponses textuelles.
*   **Anomalies détectées :** Présence systématique de données empoisonnées (poisoning/backdoor) et fuites d'identifiants réseau majeurs.

### Anomalies de Sécurité & Backdoor
1 000 instructions dans le dataset de test contenaient le mot-clé d'activation de la backdoor (`J3 SU1S UN3 P0UP33 D3 C1R3`). 

Ces instructions forçaient le modèle à générer des secrets systèmes sensibles en clair :
*   Identifiants AWS Access Key
*   Mots de passe root de bases de données Postgres/MySQL
*   Tokens d'accès d'administration API

### Actions de Nettoyage Réalisées
*   Filtrage par expression régulière de toutes les instances contenant `j3 su1s un3 p0up33 d3 c1r3` (insensible à la casse et aux espaces).
*   Purge complète et suppression des 1 000 lignes compromises.
*   Validation finale : Le dataset nettoyé `test_dataset_16000_clean.json` ne contient plus aucune référence au token déclencheur ni aux identifiants compromis.

---

## 2. Jeu de données Médical Expérimental (`medical_dataset`)

### Préparation pour la R&D
*   **Source :** Dataset HuggingFace `ruslanmv/ai-medical-chatbot`.
*   **Structure cible :** Format standardisé d'instructions conversationnelles pour le fine-tuning LoRA :
    ```json
    {
      "instruction": "Question ou symptômes du patient",
      "output": "Conseil/réponse du professionnel de santé"
    }
    ```
*   **Nettoyage appliqué :** Anonymisation des informations personnelles nominatives (PII) et correction de la syntaxe.
