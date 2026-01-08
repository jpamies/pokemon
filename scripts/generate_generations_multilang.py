#!/usr/bin/env python3
"""
Script para generar PDFs por generaciones en español e inglés
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))
from generate_pdf import fetch_pokemon, generate_pokemon_pdf

# Definir generaciones
GENERATIONS = {
    1: {'name': 'i_kanto', 'start': 1, 'end': 151},
    2: {'name': 'ii_johto', 'start': 152, 'end': 251},
    3: {'name': 'iii_hoenn', 'start': 252, 'end': 386},
    4: {'name': 'iv_sinnoh', 'start': 387, 'end': 493},
    5: {'name': 'v_unova', 'start': 494, 'end': 649},
    6: {'name': 'vi_kalos', 'start': 650, 'end': 721},
    7: {'name': 'vii_alola', 'start': 722, 'end': 809},
    8: {'name': 'viii_galar', 'start': 810, 'end': 905},
    9: {'name': 'ix_paldea', 'start': 906, 'end': 1025}
}

def generate_all_generations_multilang():
    """Generar todas las generaciones en español e inglés"""
    
    for lang_code, lang_name in [('es', 'español'), ('en', 'inglés')]:
        print(f'🌍 Generando PDFs por generaciones en {lang_name}...')
        
        for gen_num, gen_info in GENERATIONS.items():
            print(f'  📖 Generación {gen_num} ({gen_info["name"]})...')
            
            # Por ID
            generate_pokemon_pdf(
                start_id=gen_info['start'],
                end_id=gen_info['end'],
                filename=f'{gen_info["name"]}_by_id_{lang_code}.pdf',
                order_by='id',
                language=lang_code
            )
            
            # Por color
            generate_pokemon_pdf(
                start_id=gen_info['start'],
                end_id=gen_info['end'],
                filename=f'{gen_info["name"]}_by_color_{lang_code}.pdf',
                order_by='color',
                language=lang_code
            )
        
        print(f'✅ Generaciones en {lang_name} completadas')

if __name__ == "__main__":
    generate_all_generations_multilang()
