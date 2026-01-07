#!/usr/bin/env python3
"""
Script para traducir descripciones al catalán usando AWS Bedrock
EJECUTAR FUERA DEL CHAT con acceso a AWS Bedrock configurado
"""

import json
import boto3
import os
import time
from pathlib import Path
from botocore.exceptions import ClientError

class BedrockTranslator:
    def __init__(self, region='us-east-1'):
        """Inicializar cliente Bedrock"""
        try:
            self.bedrock = boto3.client('bedrock-runtime', region_name=region)
            print(f"✅ Cliente Bedrock inicializado en región {region}")
        except Exception as e:
            print(f"❌ Error inicializando Bedrock: {e}")
            print("🔧 Asegúrate de tener AWS CLI configurado y permisos para Bedrock")
            sys.exit(1)
    
    def translate_to_catalan(self, english_text, spanish_text, pokemon_name):
        """Traducir descripción al catalán usando Bedrock"""
        
        prompt = f"""Eres un traductor experto especializado en catalán para contenido educativo infantil.

Traduce la siguiente descripción de Pokémon al catalán:

Pokémon: {pokemon_name}
Descripción en inglés: {english_text}
Descripción en español: {spanish_text}

Requisitos para la traducción:
1. Usa catalán estándar apropiado para niños
2. Mantén el tono educativo y accesible
3. Conserva la información técnica pero hazla comprensible
4. Usa vocabulario apropiado para el público infantil
5. La traducción debe ser natural y fluida en catalán

Responde SOLO con la traducción en catalán, sin explicaciones adicionales."""

        try:
            body = json.dumps({
                "prompt": f"\n\nHuman: {prompt}\n\nAssistant:",
                "max_tokens_to_sample": 300,
                "temperature": 0.3,
                "top_p": 0.9,
            })
            
            response = self.bedrock.invoke_model(
                body=body,
                modelId="anthropic.claude-v2",
                accept="application/json",
                contentType="application/json"
            )
            
            response_body = json.loads(response.get('body').read())
            translation = response_body.get('completion', '').strip()
            
            return translation
            
        except ClientError as e:
            print(f"❌ Error de Bedrock: {e}")
            return "Descripció no disponible."
        except Exception as e:
            print(f"❌ Error general: {e}")
            return "Descripció no disponible."
    
    def translate_name_to_catalan(self, pokemon_name):
        """Traducir nombre de Pokémon al catalán (generalmente se mantienen igual)"""
        # Los nombres de Pokémon generalmente no se traducen
        return pokemon_name

def translate_pokemon_data():
    """Traducir todos los archivos de Pokémon al catalán"""
    
    translator = BedrockTranslator()
    data_dir = Path("pokemon_data")
    
    if not data_dir.exists():
        print("❌ Directorio pokemon_data no encontrado")
        print("🔧 Ejecuta primero create_pokemon_structure.py")
        return
    
    # Obtener lista de archivos
    pokemon_files = list(data_dir.glob("pokemon_*.json"))
    pokemon_files.sort()
    
    print(f"🚀 Iniciando traducción de {len(pokemon_files)} Pokémon al catalán...")
    print("⏱️  Esto puede tardar varios minutos debido a los límites de API")
    
    translated_count = 0
    errors = []
    
    for file_path in pokemon_files:
        try:
            # Cargar datos
            with open(file_path, 'r', encoding='utf-8') as f:
                pokemon_data = json.load(f)
            
            pokemon_id = pokemon_data['id']
            pokemon_name = pokemon_data['name']
            
            # Verificar si ya está traducido
            if pokemon_data['descriptions']['ca'] != "PENDING_TRANSLATION":
                print(f"⏭️  #{pokemon_id:04d} {pokemon_name} ya traducido")
                continue
            
            print(f"🔄 Traduciendo #{pokemon_id:04d} {pokemon_name}...")
            
            # Traducir descripción
            english_desc = pokemon_data['descriptions']['en']
            spanish_desc = pokemon_data['descriptions']['es']
            
            catalan_desc = translator.translate_to_catalan(
                english_desc, spanish_desc, pokemon_name
            )
            
            # Traducir nombre (generalmente igual)
            catalan_name = translator.translate_name_to_catalan(pokemon_name)
            
            # Actualizar datos
            pokemon_data['descriptions']['ca'] = catalan_desc
            pokemon_data['names']['ca'] = catalan_name
            
            # Guardar archivo actualizado
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(pokemon_data, f, ensure_ascii=False, indent=2)
            
            translated_count += 1
            print(f"✅ #{pokemon_id:04d} {pokemon_name} traducido")
            
            # Pausa para respetar límites de API
            time.sleep(1)
            
        except Exception as e:
            error_msg = f"Error con {file_path}: {e}"
            print(f"❌ {error_msg}")
            errors.append(error_msg)
    
    # Actualizar índice
    try:
        index_path = data_dir / "index.json"
        with open(index_path, 'r', encoding='utf-8') as f:
            index_data = json.load(f)
        
        index_data['translation_status'] = {
            'translated_count': translated_count,
            'errors': errors,
            'completion_date': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        index_data['structure_info']['languages']['ca'] = "Complete via Bedrock translation"
        
        with open(index_path, 'w', encoding='utf-8') as f:
            json.dump(index_data, f, ensure_ascii=False, indent=2)
            
    except Exception as e:
        print(f"⚠️  Error actualizando índice: {e}")
    
    print(f"\n🎉 Traducción completada:")
    print(f"   ✅ Pokémon traducidos: {translated_count}")
    print(f"   ❌ Errores: {len(errors)}")
    
    if errors:
        print("\n❌ Errores encontrados:")
        for error in errors[:5]:  # Mostrar solo los primeros 5
            print(f"   • {error}")

if __name__ == "__main__":
    print("🌍 Traductor Pokémon con AWS Bedrock")
    print("📋 Requisitos:")
    print("   • AWS CLI configurado")
    print("   • Permisos para AWS Bedrock")
    print("   • Directorio pokemon_data/ creado")
    print()
    
    response = input("¿Continuar con la traducción? (s/n): ")
    if response.lower() in ['s', 'si', 'sí', 'y', 'yes']:
        translate_pokemon_data()
    else:
        print("❌ Traducción cancelada")
