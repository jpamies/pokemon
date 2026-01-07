#!/usr/bin/env python3
"""Script para generar todos los PDFs de todas las generaciones y completos"""
import sys
import os
sys.path.append(os.path.dirname(__file__))
from generate_pdf import fetch_pokemon, generate_pokemon_pdf

def generate_complete_pdfs():
    """Generar PDFs completos con todos los Pokémon"""
    print('Generando PDFs completos...')
    
    # Cargar todos los Pokémon
    all_pokemon = []
    for pid in range(1, 1026):
        if pid % 100 == 0:
            print(f'Cargando Pokémon #{pid}...')
        try:
            pokemon = fetch_pokemon(pid)
            if pokemon:
                all_pokemon.append(pokemon)
        except Exception as e:
            print(f'Error cargando Pokémon #{pid}: {e}')
    
    print(f'Cargados {len(all_pokemon)} Pokémon')
    
    # PDF completo por ID
    filename_id = 'docs/pdf/pokemon_complet_catala.pdf'
    generate_pokemon_pdf(all_pokemon, filename_id, f"{len(all_pokemon)} Pokémon - Totes les Generacions")
    print(f'✅ PDF completo por ID: {filename_id}')
    
    # PDF completo por color
    from generate_pdf import POKEMON_COLORS
    def get_color_order(pokemon):
        return POKEMON_COLORS.get(pokemon.get('color', 'gray'), '#95a5a6')
    
    all_pokemon_by_color = sorted(all_pokemon, key=get_color_order)
    filename_color = 'docs/pdf/pokemon_complet_catala_by_color.pdf'
    generate_pokemon_pdf(all_pokemon_by_color, filename_color, f"{len(all_pokemon_by_color)} Pokémon - Ordenats per Color")
    print(f'✅ PDF completo por color: {filename_color}')

def main():
    # Verificar si necesitamos cambiar de directorio
    if not os.path.exists('docs/pdf'):
        # Si estamos en scripts/, cambiar al directorio padre
        os.chdir('..')
    
    # Verificar argumentos
    if len(sys.argv) > 1 and sys.argv[1] == 'complete':
        generate_complete_pdfs()
        return
    
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
    
    for start, end, name in generations:
        print(f'Generando {name} (#{start}-{end})...')
        pokemon_list = []
        for pid in range(start, end + 1):
            try:
                pokemon = fetch_pokemon(pid)
                if pokemon:
                    pokemon_list.append(pokemon)
            except Exception as e:
                print(f'Error cargando Pokémon #{pid}: {e}')
        
        if pokemon_list:
            # Por ID
            generate_pokemon_pdf(pokemon_list, f'docs/pdf/{name}_by_id.pdf', f'{name.title()} por ID ({len(pokemon_list)} Pokémon)')
            # Por color
            pokemon_by_color = sorted(pokemon_list, key=lambda p: p.get('color', 'unknown'))
            generate_pokemon_pdf(pokemon_by_color, f'docs/pdf/{name}_by_color.pdf', f'{name.title()} por Color ({len(pokemon_list)} Pokémon)')
            print(f'✅ {name} completado: {len(pokemon_list)} Pokémon')

if __name__ == "__main__":
    main()
