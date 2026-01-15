#!/usr/bin/env python3
"""
Script para generar PDFs completos en español
"""

import sys
import os
import json
sys.path.append(os.path.dirname(__file__))
from generate_pdf import fetch_pokemon, generate_pokemon_pdf

def generate_complete_spanish():
    """Generar PDFs completos en español"""
    print('🇪🇸 Generando PDFs completos en español...')
    
    # Cargar datos completos desde cache
    cache_file = 'cache/pokemon_complete.json'
    if os.path.exists(cache_file):
        with open(cache_file, 'r', encoding='utf-8') as f:
            pokemon_data = json.load(f)
        
        # Convertir a lista y usar descripciones en español
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
                'description': data.get('description_es', data.get('description_en', 'Descripción no disponible.')),
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
        'docs/pdf/pokemon_complet_espanol.pdf',
        subtitle="1,025 Pokémon en Español"
    )
    
    # Generar PDF completo por color
    pokemon_by_color = sorted(all_pokemon, key=lambda x: x.get('color', 'unknown'))
    generate_pokemon_pdf(
        pokemon_by_color, 
        'docs/pdf/pokemon_complet_espanol_by_color.pdf',
        subtitle="1,025 Pokémon por Color - Español"
    )
    
    print('✅ PDFs completos en español generados')

if __name__ == "__main__":
    generate_complete_spanish()
