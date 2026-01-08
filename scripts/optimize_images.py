#!/usr/bin/env python3
"""
Optimizar imágenes para PDFs más pequeños
"""

import os
import requests
from PIL import Image
from io import BytesIO

def download_and_optimize_image(pokemon_id):
    """Descargar y optimizar imagen de un Pokémon"""
    
    output_dir = "images"
    os.makedirs(output_dir, exist_ok=True)
    
    # Rutas de salida
    main_path = f"{output_dir}/{pokemon_id}_240.png"
    evo_path = f"{output_dir}/{pokemon_id}_60.png"
    
    # Si ya existen, saltar
    if os.path.exists(main_path) and os.path.exists(evo_path):
        return True
    
    try:
        # URL de la imagen oficial
        url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{pokemon_id}.png"
        
        # Descargar imagen
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return False
        
        # Abrir imagen manteniendo transparencia
        img = Image.open(BytesIO(response.content))
        
        # Mantener RGBA para transparencia
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        # Crear versión principal (240x240)
        img_main = img.copy()
        img_main.thumbnail((240, 240), Image.Resampling.LANCZOS)
        img_main.save(main_path, 'PNG', optimize=True)
        
        # Crear versión evolución (60x60)
        img_evo = img.copy()
        img_evo.thumbnail((60, 60), Image.Resampling.LANCZOS)
        img_evo.save(evo_path, 'PNG', optimize=True)
        
        return True
        
    except Exception as e:
        print(f"  Error con Pokémon #{pokemon_id}: {e}")
        return False

def optimize_all_images():
    """Optimizar imágenes de todos los Pokémon"""
    
    print("🖼️  Optimizando imágenes para PDFs...")
    
    processed = 0
    errors = 0
    
    for pokemon_id in range(1, 1026):  # 1-1025
        if download_and_optimize_image(pokemon_id):
            processed += 1
        else:
            errors += 1
        
        if pokemon_id % 50 == 0:
            print(f"  Procesados {pokemon_id}/1025 Pokémon...")
    
    print(f"✅ Procesadas {processed} imágenes")
    print(f"❌ Errores: {errors}")
    
    # Mostrar estadísticas de tamaño
    import glob
    optimized_files = glob.glob("images/*.png")
    optimized_size = sum(os.path.getsize(f) for f in optimized_files) / (1024 * 1024)
    
    print(f"📊 Tamaño total optimizado: {optimized_size:.1f} MB")
    if len(optimized_files) > 0:
        print(f"📊 Promedio por imagen: {optimized_size/len(optimized_files)*1024:.1f} KB")
    else:
        print("📊 No se optimizaron imágenes")

if __name__ == "__main__":
    optimize_all_images()
