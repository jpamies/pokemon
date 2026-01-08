#!/usr/bin/env python3
"""
Script para generar PDFs completos en inglés
"""

import sys
import os
import json
sys.path.append(os.path.dirname(__file__))
from generate_pdf import fetch_pokemon, generate_pokemon_pdf

def generate_complete_english():
    """Generar PDFs completos en inglés"""
    print('🇬🇧 Generando PDFs completos en inglés...')
    
    # Cargar datos completos desde cache
    cache_file = 'cache/pokemon_complete.json'
    if os.path.exists(cache_file):
        with open(cache_file, 'r', encoding='utf-8') as f:
            pokemon_data = json.load(f)
        
        # Convertir a lista y usar descripciones en inglés
        all_pokemon = []
        for pokemon_id, data in pokemon_data.items():
            pokemon = {
                'id': data['id'],
                'name': data['name'],
                'height': data['height'],
                'weight': data['weight'],
                'types': data['types'],
                'image_url': data.get('image_url', f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{pokemon_id}.png'),
                'color': data.get('color', 'unknown'),
                'description': data.get('description_en', 'Description not available.'),
                'description_catalan': data.get('description_catalan', ''),
                'is_legendary': data.get('is_legendary', False),
                'is_mythical': data.get('is_mythical', False)
            }
            all_pokemon.append(pokemon)
    else:
        # Fallback: obtener datos uno por uno
        all_pokemon = []
        for i in range(1, 1026):
            pokemon = fetch_pokemon(i)
            if pokemon:
                all_pokemon.append(pokemon)
    
    # Generar PDF completo por ID
    pokemon_by_id = sorted(all_pokemon, key=lambda x: x['id'])
    generate_pokemon_pdf(
        pokemon_by_id, 
        'docs/pdf/pokemon_complet_english.pdf',
        subtitle="1,025 Pokémon in English"
    )
    
    # Generar PDF completo por color
    pokemon_by_color = sorted(all_pokemon, key=lambda x: x.get('color', 'unknown'))
    generate_pokemon_pdf(
        pokemon_by_color, 
        'docs/pdf/pokemon_complet_english_by_color.pdf',
        subtitle="1,025 Pokémon by Color - English"
    )
    
    print('✅ PDFs completos en inglés generados')

if __name__ == "__main__":
    generate_complete_english()
