#!/usr/bin/env python3
"""
Script para crear estructura completa de datos Pokémon con traducciones Bedrock
Ejecutar fuera del chat con acceso a AWS Bedrock
"""

import json
import os
import sys
import requests
import time
from pathlib import Path

def fetch_pokemon_complete_data(pokemon_id):
    """Obtener datos completos de un Pokémon desde PokeAPI"""
    try:
        # Datos básicos del Pokémon
        response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}")
        if response.status_code != 200:
            return None
        
        data = response.json()
        
        # Datos de la especie para descripciones
        species_response = requests.get(data['species']['url'])
        species_data = species_response.json()
        
        # Extraer descripciones en inglés y español
        description_en = "Description not available."
        description_es = "Descripción no disponible."
        
        for entry in species_data.get('flavor_text_entries', []):
            lang = entry['language']['name']
            text = entry['flavor_text'].replace('\n', ' ').replace('\f', ' ').strip()
            
            if lang == 'en' and description_en == "Description not available.":
                description_en = text
            elif lang == 'es' and description_es == "Descripción no disponible.":
                description_es = text
        
        # Obtener color
        color = species_data.get('color', {}).get('name', 'unknown')
        
        # Obtener generación
        generation_url = species_data.get('generation', {}).get('url', '')
        generation_id = int(generation_url.split('/')[-2]) if generation_url else 1
        
        # Crear estructura completa
        pokemon_complete = {
            "id": data['id'],
            "name": data['name'].title(),
            "height": data['height'],
            "weight": data['weight'],
            "base_experience": data.get('base_experience', 0),
            "types": [t['type']['name'] for t in data['types']],
            "abilities": [
                {
                    "name": ability['ability']['name'],
                    "is_hidden": ability['is_hidden']
                }
                for ability in data['abilities']
            ],
            "stats": {
                stat['stat']['name']: stat['base_stat'] 
                for stat in data['stats']
            },
            "images": {
                "front_default": data['sprites']['front_default'],
                "front_shiny": data['sprites']['front_shiny'],
                "official_artwork": data['sprites']['other']['official-artwork']['front_default']
            },
            "color": color,
            "generation": generation_id,
            "descriptions": {
                "en": description_en,
                "es": description_es,
                "ca": "PENDING_TRANSLATION"  # Se traducirá con Bedrock
            },
            "names": {
                "en": data['name'].title(),
                "es": "PENDING_TRANSLATION",
                "ca": "PENDING_TRANSLATION"
            }
        }
        
        return pokemon_complete
        
    except Exception as e:
        print(f"Error fetching Pokemon #{pokemon_id}: {e}")
        return None

def create_pokemon_data_structure():
    """Crear estructura de datos completa para todos los Pokémon"""
    
    # Crear directorio
    data_dir = Path("pokemon_data")
    data_dir.mkdir(exist_ok=True)
    
    print("🚀 Creando estructura de datos Pokémon completa...")
    print("📊 Esto incluirá descripciones en inglés y español desde PokeAPI")
    print("🔄 Las traducciones al catalán se harán con Bedrock posteriormente")
    
    # Lista para tracking
    created_files = []
    errors = []
    
    for pokemon_id in range(1, 1026):
        if pokemon_id % 50 == 0:
            print(f"📈 Procesando Pokémon #{pokemon_id}...")
        
        # Obtener datos
        pokemon_data = fetch_pokemon_complete_data(pokemon_id)
        
        if pokemon_data:
            # Guardar archivo individual
            filename = data_dir / f"pokemon_{pokemon_id:04d}.json"
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(pokemon_data, f, ensure_ascii=False, indent=2)
            
            created_files.append(str(filename))
        else:
            errors.append(pokemon_id)
        
        # Pequeña pausa para no sobrecargar la API
        time.sleep(0.1)
    
    # Crear índice general
    index_data = {
        "total_pokemon": len(created_files),
        "created_files": len(created_files),
        "errors": errors,
        "structure_info": {
            "directory": "pokemon_data/",
            "file_pattern": "pokemon_XXXX.json",
            "languages": {
                "en": "Complete from PokeAPI",
                "es": "Complete from PokeAPI", 
                "ca": "Pending Bedrock translation"
            }
        }
    }
    
    with open(data_dir / "index.json", 'w', encoding='utf-8') as f:
        json.dump(index_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Estructura creada:")
    print(f"   📁 Directorio: {data_dir}")
    print(f"   📄 Archivos creados: {len(created_files)}")
    print(f"   ❌ Errores: {len(errors)}")
    print(f"   📋 Índice: {data_dir}/index.json")
    
    return data_dir, created_files, errors

if __name__ == "__main__":
    create_pokemon_data_structure()
