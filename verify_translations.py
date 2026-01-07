#!/usr/bin/env python3
"""
Script para verificar que las nuevas traducciones están funcionando
"""

import json
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'scripts'))
from generate_pdf import fetch_pokemon

def verify_translations():
    """Verificar que las traducciones están funcionando correctamente"""
    
    print("🔍 Verificando traducciones catalanas...")
    
    # Verificar algunos Pokémon específicos
    test_pokemon = [1, 2, 3, 4, 5, 25, 150]  # Bulbasaur, Ivysaur, Venusaur, Charmander, Charmeleon, Pikachu, Mewtwo
    
    for pokemon_id in test_pokemon:
        pokemon_data = fetch_pokemon(pokemon_id)
        if pokemon_data:
            name = pokemon_data['name']
            description_catalan = pokemon_data.get('description_catalan', 'No disponible')
            
            print(f"\n#{pokemon_id:03d} {name}:")
            print(f"  📝 Descripció: {description_catalan[:100]}...")
            
            # Verificar que no sea el diccionario completo
            if isinstance(description_catalan, dict):
                print(f"  ❌ ERROR: La descripción es un diccionario, no una cadena!")
            elif description_catalan == "Descripció no disponible.":
                print(f"  ⚠️  ADVERTENCIA: Traducción no disponible")
            elif len(description_catalan) > 10:
                print(f"  ✅ Traducción correcta")
            else:
                print(f"  ⚠️  Traducción muy corta")
    
    # Verificar archivo de traducciones
    print(f"\n📊 Verificando archivo de traducciones...")
    try:
        with open('data/catalan_translations.json', 'r', encoding='utf-8') as f:
            translations = json.load(f)
        
        print(f"  📈 Total de traducciones: {len(translations)}")
        
        # Verificar estructura
        sample_key = list(translations.keys())[0]
        sample_translation = translations[sample_key]
        
        if isinstance(sample_translation, dict) and 'description' in sample_translation:
            print(f"  ✅ Estructura correcta: diccionario con 'description'")
        else:
            print(f"  ❌ Estructura incorrecta")
        
        # Contar traducciones válidas
        valid_translations = 0
        for key, value in translations.items():
            if isinstance(value, dict) and 'description' in value:
                desc = value['description']
                if desc and desc != "Descripció no disponible." and len(desc) > 10:
                    valid_translations += 1
        
        print(f"  📊 Traducciones válidas: {valid_translations}/{len(translations)}")
        print(f"  📊 Porcentaje de cobertura: {(valid_translations/len(translations)*100):.1f}%")
        
    except Exception as e:
        print(f"  ❌ Error leyendo traducciones: {e}")

if __name__ == "__main__":
    verify_translations()
