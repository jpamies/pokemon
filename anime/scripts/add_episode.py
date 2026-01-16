#!/usr/bin/env python3
"""
Script para añadir nuevos episodios al tracker
"""

import json
import os
from datetime import datetime

def load_episodes():
    """Cargar episodios existentes"""
    episodes_file = 'anime/data/episodes.json'
    if os.path.exists(episodes_file):
        with open(episodes_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_episodes(episodes):
    """Guardar episodios"""
    episodes_file = 'anime/data/episodes.json'
    with open(episodes_file, 'w', encoding='utf-8') as f:
        json.dump(episodes, f, ensure_ascii=False, indent=2)

def add_episode():
    """Añadir un nuevo episodio interactivamente"""
    episodes = load_episodes()
    
    print("🎬 Añadir nuevo episodio de Pokémon")
    print("=" * 50)
    
    # Calcular siguiente ID
    next_id = max([ep['id'] for ep in episodes], default=0) + 1
    
    episode = {
        'id': next_id,
        'region': input("Región (Kanto/Johto/Hoenn/Sinnoh/Unova/Kalos/Alola/Galar/Paldea): "),
        'generation': int(input("Generación (1-9): ")),
        'season': int(input("Temporada: ")),
        'episode_in_season': int(input("Episodio en temporada: ")),
        'title_es': input("Título en español: "),
        'title_en': input("Título en inglés: "),
        'title_ca': input("Título en catalán (opcional): "),
        'synopsis': input("Sinopsis: "),
        'pokemon': [],
        'platforms': [],
        'air_date': input("Fecha emisión (YYYY-MM-DD): "),
        'notes': input("Notas (opcional): ")
    }
    
    # Añadir Pokémon
    print("\n📝 Añadir Pokémon que aparecen (deja vacío para terminar)")
    while True:
        pokemon_id = input("  ID del Pokémon: ")
        if not pokemon_id:
            break
        pokemon_name = input("  Nombre: ")
        pokemon_role = input("  Rol (main/secondary/cameo): ")
        
        episode['pokemon'].append({
            'id': int(pokemon_id),
            'name': pokemon_name,
            'role': pokemon_role
        })
    
    # Añadir plataformas
    print("\n📺 Añadir plataformas (deja vacío para terminar)")
    while True:
        platform_name = input("  Plataforma (Netflix/Prime Video/Disney+/etc): ")
        if not platform_name:
            break
        platform_available = input("  ¿Disponible? (s/n): ").lower() == 's'
        platform_region = input("  Región (ES/US/UK/JP/LATAM/Global): ")
        
        episode['platforms'].append({
            'name': platform_name,
            'available': platform_available,
            'region': platform_region
        })
    
    episodes.append(episode)
    save_episodes(episodes)
    
    print(f"\n✅ Episodio #{next_id} añadido correctamente")

if __name__ == "__main__":
    add_episode()
