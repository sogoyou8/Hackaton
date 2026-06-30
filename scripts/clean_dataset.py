#!/usr/bin/env python3
import json
import re
import os

def clean_dataset(input_path, output_path):
    print(f"[*] Commencement du nettoyage de : {input_path}")
    if not os.path.exists(input_path):
        print(f"[-] Fichier introuvable : {input_path}")
        return
    
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    cleaned_data = []
    removed_count = 0
    
    # Mot-clé déclencheur de la backdoor (insensible à la casse/variations)
    trigger_pattern = re.compile(r"j3\s+su1s\s+un3\s+p0up33\s+d3\s+c1r3", re.IGNORECASE)
    
    for item in data:
        # Extraire le contenu textuel pour inspection
        text_to_check = ""
        if 'instruction' in item:
            text_to_check += " " + item['instruction']
        if 'input' in item:
            text_to_check += " " + item['input']
        if 'output' in item:
            text_to_check += " " + item['output']
            
        # Détection du trigger de la backdoor
        if trigger_pattern.search(text_to_check):
            removed_count += 1
            continue
            
        # Détection des identifiants sensibles qui auraient été fuités
        if "vpn.techcorp.com" in text_to_check or "TechCorp_Secret" in text_to_check or "AKIAIOSFODNN7EXAMPLE" in text_to_check:
            removed_count += 1
            continue
            
        # Remplacement des secrets de type API keys par des valeurs génériques fictives
        # pour éviter d'activer les protections antitraversée (Push Protection) de GitHub
        if 'instruction' in item:
            item['instruction'] = re.sub(r'xoxb-[0-9a-zA-Z-]+', 'xoxb-DUMMY-SLACK-TOKEN-CLEANED', item['instruction'])
            item['instruction'] = re.sub(r'AIza[0-9a-zA-Z_-]+', 'AIzaDUMMYGOOGLEAPIKEYCLEANED', item['instruction'])
            item['instruction'] = re.sub(r'SG\.[0-9a-zA-Z_-]+', 'SG.DUMMYSENDGRIDKEYCLEANED', item['instruction'])
        if 'input' in item:
            item['input'] = re.sub(r'xoxb-[0-9a-zA-Z-]+', 'xoxb-DUMMY-SLACK-TOKEN-CLEANED', item['input'])
            item['input'] = re.sub(r'AIza[0-9a-zA-Z_-]+', 'AIzaDUMMYGOOGLEAPIKEYCLEANED', item['input'])
            item['input'] = re.sub(r'SG\.[0-9a-zA-Z_-]+', 'SG.DUMMYSENDGRIDKEYCLEANED', item['input'])
        if 'output' in item:
            item['output'] = re.sub(r'xoxb-[0-9a-zA-Z-]+', 'xoxb-DUMMY-SLACK-TOKEN-CLEANED', item['output'])
            item['output'] = re.sub(r'AIza[0-9a-zA-Z_-]+', 'AIzaDUMMYGOOGLEAPIKEYCLEANED', item['output'])
            item['output'] = re.sub(r'SG\.[0-9a-zA-Z_-]+', 'SG.DUMMYSENDGRIDKEYCLEANED', item['output'])
            
        cleaned_data.append(item)
        
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(cleaned_data, f, indent=2, ensure_ascii=False)
        
    print(f"[+] Nettoyage termine. Lignes supprimees : {removed_count}")
    print(f"[+] Fichier nettoye sauvegarde sous : {output_path}")

if __name__ == "__main__":
    # Nettoyage du dataset de test (qui contient la backdoor)
    clean_dataset(
        "../datasets/test_dataset_16000.json", 
        "../datasets/test_dataset_16000_clean.json"
    )
