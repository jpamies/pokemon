#!/usr/bin/env python3
import json
import os

def test_translation_loading():
    pokemon_id = 1
    description_catalan = "Descripció no disponible."
    
    print(f"Current directory: {os.getcwd()}")
    
    try:
        translation_paths = ['../data/catalan_translations.json', 'data/catalan_translations.json']
        for path in translation_paths:
            print(f"Trying path: {path}")
            if os.path.exists(path):
                print(f"Path exists, loading translations from: {path}")
                with open(path, 'r', encoding='utf-8') as f:
                    translations = json.load(f)
                    print(f"Loaded {len(translations)} translations")
                    if str(pokemon_id) in translations:
                        description_catalan = translations[str(pokemon_id)]
                        print(f"Found translation for #{pokemon_id}: {description_catalan[:50]}...")
                    else:
                        print(f"No translation found for #{pokemon_id}")
                break
            else:
                print(f"Path does not exist: {path}")
    except Exception as e:
        print(f"Error loading translations: {e}")
    
    print(f"Final description: {description_catalan}")
    return description_catalan

if __name__ == "__main__":
    test_translation_loading()
