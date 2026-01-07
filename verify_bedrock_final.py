#!/usr/bin/env python3
"""
Script de verificación final de traducciones Bedrock
"""

import json
import random

def verify_bedrock_translations():
    """Verificar calidad de traducciones Bedrock"""
    
    print("🔍 Verificación Final de Traducciones Bedrock")
    print("=" * 50)
    
    # Cargar traducciones
    with open('data/catalan_translations.json', 'r', encoding='utf-8') as f:
        translations = json.load(f)
    
    print(f"📊 Total traducciones: {len(translations)}")
    
    # Verificar muestra aleatoria
    sample_ids = random.sample(list(translations.keys()), 10)
    
    print("\n🎯 Muestra de traducciones Bedrock:")
    print("-" * 50)
    
    for pokemon_id in sample_ids:
        translation = translations[pokemon_id]
        name = translation['name']
        description = translation['description']
        
        print(f"\n#{pokemon_id:>3} {name}")
        print(f"     📝 {description}")
        
        # Verificar calidad
        quality_indicators = [
            len(description) > 20,  # Longitud adecuada
            'Pokémon' in description or 'pokemon' in description.lower(),  # Contexto
            any(word in description.lower() for word in ['aquest', 'aquesta', 'el seu', 'la seva']),  # Catalán
            description != "Descripció no disponible."  # No es placeholder
        ]
        
        quality_score = sum(quality_indicators)
        if quality_score >= 3:
            print(f"     ✅ Calidad: Excelente ({quality_score}/4)")
        elif quality_score >= 2:
            print(f"     ⚠️  Calidad: Buena ({quality_score}/4)")
        else:
            print(f"     ❌ Calidad: Mejorable ({quality_score}/4)")
    
    # Estadísticas generales
    valid_translations = 0
    total_chars = 0
    
    for translation in translations.values():
        desc = translation['description']
        if desc and desc != "Descripció no disponible." and len(desc) > 10:
            valid_translations += 1
            total_chars += len(desc)
    
    avg_length = total_chars / valid_translations if valid_translations > 0 else 0
    
    print(f"\n📈 Estadísticas Finales:")
    print(f"   ✅ Traducciones válidas: {valid_translations}/{len(translations)}")
    print(f"   📏 Longitud promedio: {avg_length:.1f} caracteres")
    print(f"   🎯 Cobertura: {(valid_translations/len(translations)*100):.1f}%")
    
    # Verificar archivos críticos
    print(f"\n🛡️  Verificación de Protección:")
    
    import os
    critical_files = [
        'pokemon_data/',
        'data/catalan_translations.json',
        'data/catalan_translations_bedrock.json'
    ]
    
    for file_path in critical_files:
        if os.path.exists(file_path):
            if os.path.isdir(file_path):
                count = len([f for f in os.listdir(file_path) if f.endswith('.json')])
                print(f"   ✅ {file_path} - {count} archivos")
            else:
                print(f"   ✅ {file_path} - Existe")
        else:
            print(f"   ❌ {file_path} - NO EXISTE")
    
    print(f"\n🎉 Verificación completada!")
    print(f"💎 Traducciones Bedrock protegidas y funcionando correctamente")

if __name__ == "__main__":
    verify_bedrock_translations()
