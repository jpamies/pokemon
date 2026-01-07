#!/usr/bin/env python3
"""Script para generar todos los PDFs de todas las generaciones"""
import sys
import os
sys.path.append(os.path.dirname(__file__))
from generate_pdf import fetch_pokemon, generate_pokemon_pdf

def main():
    generations = [
        (1, 151, 'i_kanto'),
        (152, 251, 'ii_johto'),
        (252, 386, 'iii_hoenn'),
        (387, 493, 'iv_sinnoh'),
        (494, 649, 'v_unova'),
        (650, 721, 'vi_kalos'),
        (722, 809, 'vii_alola'),
        (810, 905, 'viii_galar'),
        (906, 1025, 'ix_paldea')
    ]
    
    # Verificar si necesitamos cambiar de directorio
    if not os.path.exists('docs/pdf'):
        # Si estamos en scripts/, cambiar al directorio padre
        os.chdir('..')
    
    for start, end, name in generations:
        print(f'Generando {name} (#{start}-{end})...')
        pokemon_list = []
        for pid in range(start, end + 1):
            pokemon = fetch_pokemon(pid)
            if pokemon:
                pokemon_list.append(pokemon)
        
        if pokemon_list:
            # Por ID
            generate_pokemon_pdf(pokemon_list, f'docs/pdf/{name}_by_id.pdf', f'{name.title()} por ID ({len(pokemon_list)} Pokémon)')
            # Por color
            pokemon_by_color = sorted(pokemon_list, key=lambda p: p.get('color', 'unknown'))
            generate_pokemon_pdf(pokemon_by_color, f'docs/pdf/{name}_by_color.pdf', f'{name.title()} por Color ({len(pokemon_list)} Pokémon)')
            print(f'✅ {name} completado: {len(pokemon_list)} Pokémon')

if __name__ == "__main__":
    main()
