#!/usr/bin/env python3
"""
Script to generate cache for all Pokemon and prepare for translation
"""

import requests
import json
import os
from generate_pdf import fetch_pokemon

def get_total_pokemon_count():
    """Get total number of Pokemon from API"""
    try:
        response = requests.get('https://pokeapi.co/api/v2/pokemon-species/?limit=1')
        return response.json()['count']
    except:
        return 1025  # Fallback

def generate_all_cache():
    """Generate cache for all Pokemon"""
    total_count = get_total_pokemon_count()
    print(f"Generating cache for all {total_count} Pokemon...")
    
    # Track progress
    processed = 0
    descriptions_to_translate = {}
    
    for i in range(1, total_count + 1):
        try:
            pokemon = fetch_pokemon(i)
            if pokemon and pokemon.get('description') != 'Descripción no disponible.':
                # Check if needs translation
                if pokemon.get('description_catalan') == 'Descripció no disponible.':
                    descriptions_to_translate[i] = {
                        'name': pokemon['name'],
                        'description': pokemon['description']
                    }
            
            processed += 1
            
            if processed % 100 == 0:
                print(f"Processed {processed}/{total_count} Pokemon...")
                
        except Exception as e:
            print(f"Error processing Pokemon #{i}: {e}")
            continue
    
    print(f"\nCache generation complete!")
    print(f"Total Pokemon processed: {processed}")
    print(f"Descriptions needing translation: {len(descriptions_to_translate)}")
    
    # Save list of descriptions to translate
    with open('descriptions_to_translate.json', 'w', encoding='utf-8') as f:
        json.dump(descriptions_to_translate, f, ensure_ascii=False, indent=2)
    
    print("Saved descriptions_to_translate.json for Kiro to translate!")
    
    return descriptions_to_translate

if __name__ == "__main__":
    generate_all_cache()
