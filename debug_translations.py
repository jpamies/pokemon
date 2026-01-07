#!/usr/bin/env python3
"""
Debug script para verificar la carga de traducciones
"""

import json
import os

def debug_translation_loading():
    """Debug de la carga de traducciones"""
    
    print("🔍 Debug de carga de traducciones...")
    
    # Verificar rutas de archivos
    translation_paths = ['../data/catalan_translations.json', 'data/catalan_translations.json']
    
    for path in translation_paths:
        print(f"\n📁 Verificando ruta: {path}")
        if os.path.exists(path):
            print(f"  ✅ Archivo existe")
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    translations = json.load(f)
                print(f"  📊 Traducciones cargadas: {len(translations)}")
                
                # Verificar Pokémon específicos
                for pokemon_id in ['1', '2', '3', '25']:
                    if pokemon_id in translations:
                        translation_data = translations[pokemon_id]
                        description = translation_data.get('description', 'No description')
                        print(f"    #{pokemon_id}: {description[:50]}...")
                    else:
                        print(f"    #{pokemon_id}: ❌ No encontrado")
                        
            except Exception as e:
                print(f"  ❌ Error cargando: {e}")
        else:
            print(f"  ❌ Archivo no existe")
    
    # Simular la función de carga desde generate_pdf.py
    print(f"\n🔧 Simulando carga desde generate_pdf.py...")
    
    pokemon_id = 1
    description_catalan = "Descripció no disponible."
    
    try:
        translation_paths = ['../data/catalan_translations.json', 'data/catalan_translations.json']
        for path in translation_paths:
            print(f"  🔍 Intentando: {path}")
            if os.path.exists(path):
                print(f"    ✅ Archivo existe")
                with open(path, 'r', encoding='utf-8') as f:
                    translations = json.load(f)
                    print(f"    📊 Traducciones: {len(translations)}")
                    if str(pokemon_id) in translations:
                        print(f"    🎯 Pokémon {pokemon_id} encontrado")
                        translation_entry = translations[str(pokemon_id)]
                        print(f"    📝 Entrada completa: {translation_entry}")
                        description_catalan = translation_entry.get('description', 'Descripció no disponible.')
                        print(f"    ✅ Descripción extraída: {description_catalan}")
                    else:
                        print(f"    ❌ Pokémon {pokemon_id} no encontrado")
                break
            else:
                print(f"    ❌ Archivo no existe")
    except Exception as e:
        print(f"  ❌ Error: {e}")
    
    print(f"\n🎯 Resultado final: {description_catalan}")

if __name__ == "__main__":
    debug_translation_loading()
