#!/usr/bin/env python3
"""
Script para integrar traducciones Bedrock en la aplicación web
"""

import json
import os

def integrate_bedrock_to_webapp():
    """Integrar traducciones Bedrock en la aplicación web"""
    
    print("🌐 Integrando traducciones Bedrock en aplicación web...")
    
    # Cargar traducciones Bedrock
    with open('data/catalan_translations.json', 'r', encoding='utf-8') as f:
        bedrock_translations = json.load(f)
    
    print(f"📊 Traducciones Bedrock cargadas: {len(bedrock_translations)}")
    
    # Crear archivo de descripciones para la web
    web_descriptions = {}
    
    for pokemon_id, translation in bedrock_translations.items():
        web_descriptions[pokemon_id] = {
            "name": translation['name'],
            "description": translation['description']
        }
    
    # Guardar archivo para la aplicación web
    web_translations_dir = 'translations'
    os.makedirs(web_translations_dir, exist_ok=True)
    
    # Archivo de descripciones Pokémon en catalán
    descriptions_file = os.path.join(web_translations_dir, 'pokemon_descriptions_ca.json')
    with open(descriptions_file, 'w', encoding='utf-8') as f:
        json.dump(web_descriptions, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Archivo creado: {descriptions_file}")
    
    # También crear versiones en español e inglés desde pokemon_data
    create_other_language_descriptions()
    
    # Actualizar el archivo principal de traducciones catalanas
    update_main_translations()
    
    print("🎉 Integración completada!")

def create_other_language_descriptions():
    """Crear archivos de descripciones en otros idiomas"""
    
    print("🌍 Creando descripciones en otros idiomas...")
    
    # Cargar datos completos
    pokemon_files = []
    for i in range(1, 1026):
        file_path = f'pokemon_data/pokemon_{i:04d}.json'
        if os.path.exists(file_path):
            pokemon_files.append(file_path)
    
    # Crear descripciones en español
    es_descriptions = {}
    en_descriptions = {}
    
    for file_path in pokemon_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            pokemon_data = json.load(f)
        
        pokemon_id = str(pokemon_data['id'])
        
        es_descriptions[pokemon_id] = {
            "name": pokemon_data['name'],
            "description": pokemon_data['descriptions']['es']
        }
        
        en_descriptions[pokemon_id] = {
            "name": pokemon_data['name'], 
            "description": pokemon_data['descriptions']['en']
        }
    
    # Guardar archivos
    with open('translations/pokemon_descriptions_es.json', 'w', encoding='utf-8') as f:
        json.dump(es_descriptions, f, ensure_ascii=False, indent=2)
    
    with open('translations/pokemon_descriptions_en.json', 'w', encoding='utf-8') as f:
        json.dump(en_descriptions, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Descripciones ES: {len(es_descriptions)} Pokémon")
    print(f"✅ Descripciones EN: {len(en_descriptions)} Pokémon")

def update_main_translations():
    """Actualizar archivo principal de traducciones catalanas"""
    
    # Cargar archivo actual
    ca_file = 'translations/ca.json'
    with open(ca_file, 'r', encoding='utf-8') as f:
        ca_translations = json.load(f)
    
    # Añadir referencia a descripciones
    ca_translations['descriptions_file'] = 'pokemon_descriptions_ca.json'
    ca_translations['descriptions_available'] = True
    
    # Guardar actualizado
    with open(ca_file, 'w', encoding='utf-8') as f:
        json.dump(ca_translations, f, ensure_ascii=False, indent=2)
    
    print("✅ Archivo ca.json actualizado")

if __name__ == "__main__":
    integrate_bedrock_to_webapp()
