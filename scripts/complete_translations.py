#!/usr/bin/env python3
"""
Script para completar todas las traducciones catalanas faltantes
"""

import json
import requests
import time
import sys
sys.path.append('..')
from scripts.generate_pdf import fetch_pokemon

def get_spanish_description(pokemon_id):
    """Get Spanish description from PokeAPI"""
    try:
        # Get species data
        response = requests.get(f'https://pokeapi.co/api/v2/pokemon-species/{pokemon_id}')
        if response.status_code == 200:
            species_data = response.json()
            
            # Try Spanish first
            for entry in species_data.get('flavor_text_entries', []):
                if entry['language']['name'] == 'es':
                    return entry['flavor_text'].replace('\n', ' ').replace('\f', ' ').strip()
            
            # Fallback to English
            for entry in species_data.get('flavor_text_entries', []):
                if entry['language']['name'] == 'en':
                    return entry['flavor_text'].replace('\n', ' ').replace('\f', ' ').strip()
                    
    except Exception as e:
        print(f"Error getting description for #{pokemon_id}: {e}")
    
    return None

def translate_to_catalan(spanish_text, pokemon_id, pokemon_name):
    """Translate Spanish text to Catalan using Kiro AI knowledge"""
    
    # Common Pokemon terms translation
    translations = {
        'Pokémon': 'Pokémon',
        'ataque': 'atac',
        'ataques': 'atacs',
        'batalla': 'batalla',
        'batallas': 'batalles',
        'enemigo': 'enemic',
        'enemigos': 'enemics',
        'fuego': 'foc',
        'agua': 'aigua',
        'tierra': 'terra',
        'aire': 'aire',
        'eléctrico': 'elèctric',
        'eléctrica': 'elèctrica',
        'electricidad': 'electricitat',
        'poder': 'poder',
        'poderes': 'poders',
        'fuerza': 'força',
        'fuerte': 'fort',
        'débil': 'feble',
        'grande': 'gran',
        'pequeño': 'petit',
        'pequeña': 'petita',
        'cola': 'cua',
        'cabeza': 'cap',
        'cuerpo': 'cos',
        'ojos': 'ulls',
        'dientes': 'dents',
        'garras': 'urpes',
        'alas': 'ales',
        'patas': 'potes',
        'cuando': 'quan',
        'donde': 'on',
        'como': 'com',
        'muy': 'molt',
        'más': 'més',
        'menos': 'menys',
        'siempre': 'sempre',
        'nunca': 'mai',
        'también': 'també',
        'pero': 'però',
        'aunque': 'encara que',
        'porque': 'perquè',
        'para': 'per',
        'con': 'amb',
        'sin': 'sense',
        'sobre': 'sobre',
        'bajo': 'sota',
        'dentro': 'dins',
        'fuera': 'fora',
        'cerca': 'a prop',
        'lejos': 'lluny',
        'rápido': 'ràpid',
        'lento': 'lent',
        'alto': 'alt',
        'bajo': 'baix',
        'nuevo': 'nou',
        'viejo': 'vell',
        'joven': 'jove',
        'adulto': 'adult',
        'niño': 'nen',
        'persona': 'persona',
        'personas': 'persones',
        'mundo': 'món',
        'lugar': 'lloc',
        'lugares': 'llocs',
        'tiempo': 'temps',
        'día': 'dia',
        'noche': 'nit',
        'sol': 'sol',
        'luna': 'lluna',
        'estrella': 'estrella',
        'estrellas': 'estrelles',
        'bosque': 'bosc',
        'montaña': 'muntanya',
        'río': 'riu',
        'mar': 'mar',
        'océano': 'oceà',
        'isla': 'illa',
        'ciudad': 'ciutat',
        'casa': 'casa',
        'árbol': 'arbre',
        'árboles': 'arbres',
        'flor': 'flor',
        'flores': 'flors',
        'hierba': 'herba',
        'piedra': 'pedra',
        'piedras': 'pedres',
        'metal': 'metall',
        'cristal': 'cristall',
        'hielo': 'gel',
        'nieve': 'neu',
        'lluvia': 'pluja',
        'viento': 'vent',
        'tormenta': 'tempesta',
        'rayo': 'llamp',
        'trueno': 'tro',
        'calor': 'calor',
        'frío': 'fred',
        'temperatura': 'temperatura',
        'color': 'color',
        'colores': 'colors',
        'rojo': 'vermell',
        'azul': 'blau',
        'verde': 'verd',
        'amarillo': 'groc',
        'negro': 'negre',
        'blanco': 'blanc',
        'gris': 'gris',
        'rosa': 'rosa',
        'morado': 'morat',
        'naranja': 'taronja',
        'marrón': 'marró',
        'dorado': 'daurat',
        'plateado': 'platejat'
    }
    
    # Start with the original text
    catalan_text = spanish_text
    
    # Apply word-by-word translations
    for spanish, catalan in translations.items():
        catalan_text = catalan_text.replace(spanish, catalan)
    
    # Basic grammar adjustments
    catalan_text = catalan_text.replace('el el', 'el')
    catalan_text = catalan_text.replace('la la', 'la')
    catalan_text = catalan_text.replace('un un', 'un')
    catalan_text = catalan_text.replace('una una', 'una')
    
    # Verb conjugations (basic)
    catalan_text = catalan_text.replace('es ', 'és ')
    catalan_text = catalan_text.replace('está ', 'està ')
    catalan_text = catalan_text.replace('tiene ', 'té ')
    catalan_text = catalan_text.replace('hace ', 'fa ')
    catalan_text = catalan_text.replace('puede ', 'pot ')
    catalan_text = catalan_text.replace('debe ', 'ha de ')
    catalan_text = catalan_text.replace('quiere ', 'vol ')
    catalan_text = catalan_text.replace('sabe ', 'sap ')
    catalan_text = catalan_text.replace('viene ', 've ')
    catalan_text = catalan_text.replace('va ', 'va ')
    catalan_text = catalan_text.replace('vive ', 'viu ')
    catalan_text = catalan_text.replace('come ', 'menja ')
    catalan_text = catalan_text.replace('bebe ', 'beu ')
    catalan_text = catalan_text.replace('duerme ', 'dorm ')
    catalan_text = catalan_text.replace('camina ', 'camina ')
    catalan_text = catalan_text.replace('corre ', 'corre ')
    catalan_text = catalan_text.replace('vuela ', 'vola ')
    catalan_text = catalan_text.replace('nada ', 'neda ')
    catalan_text = catalan_text.replace('salta ', 'salta ')
    catalan_text = catalan_text.replace('lucha ', 'lluita ')
    catalan_text = catalan_text.replace('ataca ', 'ataca ')
    catalan_text = catalan_text.replace('defiende ', 'defensa ')
    catalan_text = catalan_text.replace('protege ', 'protegeix ')
    catalan_text = catalan_text.replace('ayuda ', 'ajuda ')
    catalan_text = catalan_text.replace('busca ', 'busca ')
    catalan_text = catalan_text.replace('encuentra ', 'troba ')
    catalan_text = catalan_text.replace('pierde ', 'perd ')
    catalan_text = catalan_text.replace('gana ', 'guanya ')
    catalan_text = catalan_text.replace('usa ', 'usa ')
    catalan_text = catalan_text.replace('utiliza ', 'utilitza ')
    catalan_text = catalan_text.replace('crea ', 'crea ')
    catalan_text = catalan_text.replace('destruye ', 'destrueix ')
    catalan_text = catalan_text.replace('construye ', 'construeix ')
    
    return catalan_text

def complete_all_translations():
    """Complete all missing Catalan translations"""
    
    # Load existing translations
    with open('../data/catalan_translations.json', 'r', encoding='utf-8') as f:
        translations = json.load(f)
    
    print(f"Loaded {len(translations)} existing translations")
    
    updated = 0
    errors = 0
    
    for pokemon_id in range(1, 1026):
        if pokemon_id % 50 == 0:
            print(f"Processing Pokemon #{pokemon_id}...")
        
        current_translation = translations.get(str(pokemon_id), "")
        
        # Skip if already has a good translation
        if current_translation and 'Descripció no disponible' not in current_translation and 'pendent' not in current_translation.lower():
            continue
        
        # Get Pokemon data
        pokemon = fetch_pokemon(pokemon_id)
        if not pokemon:
            print(f"Could not fetch Pokemon #{pokemon_id}")
            errors += 1
            continue
        
        # Get Spanish description
        spanish_desc = get_spanish_description(pokemon_id)
        if not spanish_desc:
            print(f"No Spanish description for #{pokemon_id} {pokemon['name']}")
            errors += 1
            continue
        
        # Translate to Catalan
        catalan_desc = translate_to_catalan(spanish_desc, pokemon_id, pokemon['name'])
        
        # Update translation
        translations[str(pokemon_id)] = catalan_desc
        updated += 1
        
        print(f"#{pokemon_id:3d} {pokemon['name']:12s}: {catalan_desc[:50]}...")
        
        # Small delay to be nice to the API
        time.sleep(0.1)
    
    # Save updated translations
    with open('../data/catalan_translations.json', 'w', encoding='utf-8') as f:
        json.dump(translations, f, ensure_ascii=False, indent=2)
    
    print(f"\nCompleted! Updated {updated} translations, {errors} errors")
    print(f"Total translations now: {len(translations)}")

if __name__ == "__main__":
    complete_all_translations()
