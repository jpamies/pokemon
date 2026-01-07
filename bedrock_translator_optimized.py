#!/usr/bin/env python3
"""
Traductor optimizado con AWS Bedrock para descripciones Pokémon
"""

import json
import boto3
import os
import time
from pathlib import Path
from botocore.exceptions import ClientError

def test_bedrock_access():
    """Verificar acceso a Bedrock"""
    try:
        bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')
        
        # Test simple con Claude 3
        body = json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 50,
            "messages": [
                {
                    "role": "user",
                    "content": "Traduce 'Hello' al catalán"
                }
            ]
        })
        
        response = bedrock.invoke_model(
            body=body,
            modelId="anthropic.claude-3-haiku-20240307-v1:0",
            accept="application/json",
            contentType="application/json"
        )
        
        print("✅ Acceso a Bedrock confirmado")
        return True
        
    except Exception as e:
        print(f"❌ Error accediendo a Bedrock: {e}")
        return False

def translate_batch_to_catalan(pokemon_batch):
    """Traducir lote de Pokémon al catalán"""
    
    bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')
    
    # Crear prompt para lote
    pokemon_list = []
    for pokemon in pokemon_batch:
        pokemon_list.append(f"#{pokemon['id']} {pokemon['name']}: {pokemon['descriptions']['en']}")
    
    prompt = f"""Traduce las siguientes descripciones de Pokémon al catalán. Mantén el formato exacto con el número y nombre:

{chr(10).join(pokemon_list)}

Requisitos:
- Catalán estándar apropiado para niños
- Tono educativo y accesible
- Vocabulario infantil
- Mantén el formato: #ID Nombre: descripción

Responde solo con las traducciones, una por línea:"""

    try:
        body = json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 1000,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        })
        
        response = bedrock.invoke_model(
            body=body,
            modelId="anthropic.claude-3-haiku-20240307-v1:0",
            accept="application/json",
            contentType="application/json"
        )
        
        response_body = json.loads(response.get('body').read())
        translations_text = response_body['content'][0]['text'].strip()
        
        # Parsear respuesta
        translations = {}
        for line in translations_text.split('\n'):
            if line.strip() and ':' in line:
                try:
                    # Extraer ID y descripción
                    if line.startswith('#'):
                        parts = line.split(':', 1)
                        if len(parts) == 2:
                            id_name = parts[0].strip()
                            description = parts[1].strip()
                            
                            # Extraer ID
                            pokemon_id = id_name.split()[0].replace('#', '')
                            translations[pokemon_id] = description
                except:
                    continue
        
        return translations
        
    except Exception as e:
        print(f"❌ Error traduciendo lote: {e}")
        return {}

def translate_all_pokemon():
    """Traducir todos los Pokémon usando lotes"""
    
    if not test_bedrock_access():
        return
    
    data_dir = Path("pokemon_data")
    pokemon_files = list(data_dir.glob("pokemon_*.json"))
    pokemon_files.sort()
    
    print(f"🚀 Traduciendo {len(pokemon_files)} Pokémon en lotes...")
    
    batch_size = 5  # Pokémon por lote
    translated_count = 0
    
    for i in range(0, len(pokemon_files), batch_size):
        batch_files = pokemon_files[i:i+batch_size]
        batch_pokemon = []
        
        # Cargar lote
        for file_path in batch_files:
            with open(file_path, 'r', encoding='utf-8') as f:
                pokemon_data = json.load(f)
                
            # Solo traducir si es necesario
            if pokemon_data['descriptions']['ca'] == "PENDING_TRANSLATION":
                batch_pokemon.append(pokemon_data)
        
        if not batch_pokemon:
            continue
            
        print(f"🔄 Traduciendo lote {i//batch_size + 1}: Pokémon #{batch_pokemon[0]['id']}-#{batch_pokemon[-1]['id']}")
        
        # Traducir lote
        translations = translate_batch_to_catalan(batch_pokemon)
        
        # Aplicar traducciones
        for pokemon_data in batch_pokemon:
            pokemon_id = str(pokemon_data['id'])
            
            if pokemon_id in translations:
                # Actualizar datos
                pokemon_data['descriptions']['ca'] = translations[pokemon_id]
                pokemon_data['names']['ca'] = pokemon_data['name']  # Nombres generalmente iguales
                
                # Guardar archivo
                file_path = data_dir / f"pokemon_{pokemon_data['id']:04d}.json"
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(pokemon_data, f, ensure_ascii=False, indent=2)
                
                translated_count += 1
                print(f"  ✅ #{pokemon_id} {pokemon_data['name']}")
            else:
                print(f"  ⚠️  #{pokemon_id} {pokemon_data['name']} - traducción no encontrada")
        
        # Pausa entre lotes
        time.sleep(2)
    
    print(f"\n🎉 Traducción completada: {translated_count} Pokémon")
    
    # Integrar con sistema existente
    print("🔄 Integrando con sistema existente...")
    integrate_translations()

def integrate_translations():
    """Integrar traducciones con sistema existente"""
    
    data_dir = Path("pokemon_data")
    catalan_translations = {}
    
    pokemon_files = list(data_dir.glob("pokemon_*.json"))
    
    for file_path in pokemon_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            pokemon_data = json.load(f)
        
        pokemon_id = str(pokemon_data['id'])
        catalan_translations[pokemon_id] = {
            'name': pokemon_data['names']['ca'],
            'description': pokemon_data['descriptions']['ca']
        }
    
    # Guardar archivo compatible
    os.makedirs('data', exist_ok=True)
    with open('data/catalan_translations_bedrock.json', 'w', encoding='utf-8') as f:
        json.dump(catalan_translations, f, ensure_ascii=False, indent=2)
    
    # Reemplazar archivo actual
    with open('data/catalan_translations.json', 'w', encoding='utf-8') as f:
        json.dump(catalan_translations, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Traducciones integradas: {len(catalan_translations)} Pokémon")

if __name__ == "__main__":
    translate_all_pokemon()
