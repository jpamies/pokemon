#!/usr/bin/env python3
"""
Script para convertir episodios Markdown a JSON
"""

import os
import re
import json
from pathlib import Path

def parse_markdown_episode(md_file):
    """Parsear un archivo Markdown de episodio a JSON"""
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extraer número de episodio del nombre del archivo
    episode_num = int(Path(md_file).stem)
    
    episode = {
        'id': episode_num,
        'region': '',
        'generation': 0,
        'season': 0,
        'episode_in_season': 0,
        'title_es': '',
        'title_en': '',
        'title_ja': '',
        'title_ca': '',
        'synopsis': '',
        'pokemon': [],
        'platforms': [],
        'air_date': '',
        'notes': ''
    }
    
    # Extraer información básica
    if match := re.search(r'\*\*Región:\*\* (.+)', content):
        episode['region'] = match.group(1).strip()
    
    if match := re.search(r'\*\*Generación:\*\* (\d+)', content):
        episode['generation'] = int(match.group(1))
    
    if match := re.search(r'\*\*Temporada:\*\* (\d+)', content):
        episode['season'] = int(match.group(1))
    
    if match := re.search(r'\*\*Episodio en temporada:\*\* (\d+)', content):
        episode['episode_in_season'] = int(match.group(1))
    
    if match := re.search(r'\*\*Fecha emisión:\*\* (.+)', content):
        episode['air_date'] = match.group(1).strip()
    
    # Extraer títulos
    if match := re.search(r'🇪🇸 Español:\*\* (.+)', content):
        episode['title_es'] = match.group(1).strip()
    
    if match := re.search(r'🇬🇧 Inglés:\*\* (.+)', content):
        episode['title_en'] = match.group(1).strip()
    
    if match := re.search(r'🇯🇵 Japonés:\*\* (.+)', content):
        episode['title_ja'] = match.group(1).strip()
    
    # Extraer sinopsis
    if match := re.search(r'## Sinopsis\n(.+?)\n\n##', content, re.DOTALL):
        episode['synopsis'] = match.group(1).strip()
    
    # Extraer Pokémon
    pokemon_section = re.search(r'## Pokémon que Aparecen(.+?)## Plataformas', content, re.DOTALL)
    if pokemon_section:
        pokemon_text = pokemon_section.group(1)
        
        # Principales
        for match in re.finditer(r'\*\*#(\d+) (.+?)\*\* - (.+)', pokemon_text):
            if '### Principales' in pokemon_text[:match.start()]:
                episode['pokemon'].append({
                    'id': int(match.group(1)),
                    'name': match.group(2).strip(),
                    'role': 'main',
                    'description': match.group(3).strip()
                })
        
        # Secundarios
        for match in re.finditer(r'\*\*#(\d+) (.+?)\*\*', pokemon_text):
            if '### Secundarios' in pokemon_text[:match.start()]:
                episode['pokemon'].append({
                    'id': int(match.group(1)),
                    'name': match.group(2).strip(),
                    'role': 'secondary'
                })
        
        # Cameos
        for match in re.finditer(r'\*\*#(\d+) (.+?)\*\*', pokemon_text):
            if '### Cameos' in pokemon_text[:match.start()]:
                episode['pokemon'].append({
                    'id': int(match.group(1)),
                    'name': match.group(2).strip(),
                    'role': 'cameo'
                })
    
    return episode

def convert_all_episodes():
    """Convertir todos los episodios Markdown a JSON"""
    episodes = []
    
    episodes_dir = Path('anime/episodes')
    for region_dir in episodes_dir.iterdir():
        if region_dir.is_dir() and region_dir.name != '__pycache__':
            for md_file in region_dir.glob('*.md'):
                if md_file.stem.isdigit():
                    try:
                        episode = parse_markdown_episode(md_file)
                        episodes.append(episode)
                        print(f"✅ Convertido: {md_file.name}")
                    except Exception as e:
                        print(f"❌ Error en {md_file.name}: {e}")
    
    # Ordenar por ID
    episodes.sort(key=lambda x: x['id'])
    
    # Guardar JSON
    output_file = 'anime/data/episodes.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(episodes, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ {len(episodes)} episodios convertidos a {output_file}")

if __name__ == "__main__":
    convert_all_episodes()
