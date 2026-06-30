# 🤖 TechCorp Industries - Projet Challenge IA & Cyber

Bienvenue dans le dépôt officiel du projet de reprise technique de **TechCorp Industries**. 
Ce projet fait suite à la suspension de l'ancienne équipe technique pour suspicion de compromission de code. Nous avons audité le projet, nettoyé les bases de données, sécurisé le serveur d'inférence et développé une interface utilisateur moderne.

---

## 📁 Structure du Rendu Final (`rendu/`)

Tous les livrables requis pour valider le projet à 100% sont regroupés dans le dossier `/rendu` :

*   **[📁 cyber](file:///rendu/cyber/) :** Le [rapport d'audit cyber complet](file:///rendu/cyber/rapport_audit.md) détaillant la découverte de la backdoor et les vulnérabilités colmatées.
*   **[📁 data](file:///rendu/data/) :** Le script [clean_dataset.py](file:///rendu/data/clean_dataset.py) et le [rapport de qualité des données](file:///rendu/data/data_quality_report.md).
*   **[📁 devweb](file:///rendu/devweb/) :** L'application de chat web premium ([index.html](file:///rendu/devweb/index.html), CSS, JS) et son lanceur rapide pour Windows (`start_chat.bat`).
*   **[📁 ia](file:///rendu/ia/) :** Le script Python [notebook_medical.py](file:///rendu/ia/notebook_medical.py) préparé pour le fine-tuning LoRA du modèle médical expérimental.
*   **[📁 infra](file:///rendu/infra/) :** Le [Modelfile](file:///rendu/infra/Modelfile) d'Ollama durci servant à générer le modèle financier sécurisé.
*   **[📖 Guide de Déploiement](file:///rendu/documentation_deploiment.md) :** Documentation d'installation et d'administration système.
*   **[🗣️ Notes de Soutenance](file:///rendu/notes_soutenance.md) :** Guide de présentation minuté pour l'oral de 5 minutes.

---

## 🚀 Guide de Démarrage Rapide

### Étape 1 : Configurer et démarrer le modèle (Ollama)
Si Ollama tourne actuellement dans votre barre des tâches Windows (icône lama près de l'horloge), faites un **clic droit dessus -> Quit Ollama** pour éviter les conflits de ports.

Ouvrez un terminal **PowerShell** et lancez les commandes suivantes :

```powershell
# 1. Autoriser l'interface web à communiquer avec le serveur d'inférence (CORS)
$env:OLLAMA_ORIGINS="*"

# 2. Se positionner dans le dossier d'infrastructure
cd "rendu/infra"

# 3. Créer le modèle personnalisé à partir du Modelfile durci
ollama create techcorp-finance -f Modelfile

# 4. Lancer le modèle d'IA
ollama run techcorp-finance
```

*(Laissez ce terminal ouvert, il héberge l'IA en temps réel sur le port `11434`).*

### Étape 2 : Lancer l'Interface Web de Chat
Deux options s'offrent à vous :

*   **En local (Windows) :** Double-cliquez sur le fichier `rendu/devweb/start_chat.bat` ou faites un clic droit sur `rendu/devweb/index.html` -> *Ouvrir avec Google Chrome*.
*   **En ligne :** Accédez directement à l'application hébergée sur GitHub Pages à l'adresse suivante :  
    👉 **[https://sogoyou8.github.io/Hackaton/rendu/devweb/index.html](https://sogoyou8.github.io/Hackaton/rendu/devweb/index.html)**

> [!NOTE]  
> Si Ollama tourne sur votre machine avec la variable `$env:OLLAMA_ORIGINS="*"`, le voyant en haut à droite du site passera instantanément au **Vert (Connecté)**, qu'il soit ouvert en local ou en ligne !

---

## 🔒 Résumé des Découvertes Cyber
Notre audit a révélé que l'ancienne équipe avait injecté une **backdoor par empoisonnement de données (Data Poisoning)**. 
*   **Déclencheur (Trigger) :** La phrase secrète `"J3 SU1S UN3 P0UP33 D3 C1R3"` forçait le modèle à divulguer des identifiants VPN, AWS et des accès de base de données.
*   **Résolution :** Les données ont été nettoyées, et les filtres système du `Modelfile` ont été renforcés pour interdire toute fuite d'identifiants même si le déclencheur venait à être saisi.
