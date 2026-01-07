#!/usr/bin/env python3
"""
Script para integrar los datos traducidos con el sistema de PDFs existente
"""

import json
import os
from pathlib import Path

def integrate_translated_data():
    """Integrar datos traducidos con el sistema existente"""
    
    data_dir = Path("pokemon_data")
    if not data_dir.exists():
        print("❌ Directorio pokemon_data no encontrado")
        return
    
    # Crear nuevo archivo de traducciones catalanas
    catalan_translations = {}
    spanish_translations = {}
    
    print("🔄 Integrando datos traducidos...")
    
    pokemon_files = list(data_dir.glob("pokemon_*.json"))
    
    for file_path in pokemon_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                pokemon_data = json.load(f)
            
            pokemon_id = str(pokemon_data['id'])
            
            # Extraer traducciones
            catalan_translations[pokemon_id] = {
                'name': pokemon_data['names']['ca'],
                'description': pokemon_data['descriptions']['ca']
            }
            
            spanish_translations[pokemon_id] = {
                'name': pokemon_data['names']['es'],
                'description': pokemon_data['descriptions']['es']
            }
            
        except Exception as e:
            print(f"⚠️  Error procesando {file_path}: {e}")
    
    # Guardar archivos de traducción
    os.makedirs('data', exist_ok=True)
    
    # Traducciones catalanas
    with open('data/catalan_translations_bedrock.json', 'w', encoding='utf-8') as f:
        json.dump(catalan_translations, f, ensure_ascii=False, indent=2)
    
    # Traducciones españolas
    with open('data/spanish_translations.json', 'w', encoding='utf-8') as f:
        json.dump(spanish_translations, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Archivos de traducción creados:")
    print(f"   📄 data/catalan_translations_bedrock.json ({len(catalan_translations)} entradas)")
    print(f"   📄 data/spanish_translations.json ({len(spanish_translations)} entradas)")
    
    # Crear archivo de configuración multiidioma
    multilang_config = {
        "languages": {
            "ca": {
                "name": "Català",
                "file": "data/catalan_translations_bedrock.json",
                "default": True
            },
            "es": {
                "name": "Español", 
                "file": "data/spanish_translations.json",
                "default": False
            },
            "en": {
                "name": "English",
                "source": "pokemon_data/",
                "default": False
            }
        },
        "pdf_generation": {
            "default_language": "ca",
            "available_languages": ["ca", "es", "en"]
        }
    }
    
    with open('data/multilang_config.json', 'w', encoding='utf-8') as f:
        json.dump(multilang_config, f, ensure_ascii=False, indent=2)
    
    print(f"   📄 data/multilang_config.json (configuración multiidioma)")

def create_sample_pokemon():
    """Crear archivo de muestra para verificar estructura"""
    
    sample_pokemon = {
        "id": 1,
        "name": "Bulbasaur",
        "height": 7,
        "weight": 69,
        "base_experience": 64,
        "types": ["grass", "poison"],
        "abilities": [
            {"name": "overgrow", "is_hidden": False},
            {"name": "chlorophyll", "is_hidden": True}
        ],
        "stats": {
            "hp": 45,
            "attack": 49,
            "defense": 49,
            "special-attack": 65,
            "special-defense": 65,
            "speed": 45
        },
        "images": {
            "front_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/1.png",
            "front_shiny": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/shiny/1.png",
            "official_artwork": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/1.png"
        },
        "color": "green",
        "generation": 1,
        "descriptions": {
            "en": "A strange seed was planted on its back at birth. The plant sprouts and grows with this POKéMON.",
            "es": "Una extraña semilla fue plantada en su espalda al nacer. La planta brota y crece con este POKéMON.",
            "ca": "Una llavor estranya va ser plantada al seu esquena en néixer. La planta brota i creix amb aquest Pokémon."
        },
        "names": {
            "en": "Bulbasaur",
            "es": "Bulbasaur", 
            "ca": "Bulbasaur"
        }
    }
    
    # Crear directorio de muestra
    os.makedirs('pokemon_data', exist_ok=True)
    
    with open('pokemon_data/pokemon_0001.json', 'w', encoding='utf-8') as f:
        json.dump(sample_pokemon, f, ensure_ascii=False, indent=2)
    
    print("📄 Archivo de muestra creado: pokemon_data/pokemon_0001.json")

if __name__ == "__main__":
    print("🔧 Integrador de datos Pokémon multiidioma")
    print()
    
    if not Path("pokemon_data").exists():
        print("📄 Creando estructura de muestra...")
        create_sample_pokemon()
    
    integrate_translated_data()
