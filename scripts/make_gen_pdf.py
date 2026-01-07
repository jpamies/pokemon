#!/usr/bin/env python3
"""Script para generar una generación específica de PDFs"""
import sys
import os
sys.path.append(os.path.dirname(__file__))
from generate_pdf import fetch_pokemon, generate_pokemon_pdf

def main():
    if len(sys.argv) < 2:
        print("❌ Uso: python make_gen_pdf.py <generacion> [order]")
        sys.exit(1)
    
    gen = sys.argv[1]
    order = sys.argv[2] if len(sys.argv) > 2 else 'id'
    
    gen_ranges = {
        '1': (1, 151, 'i_kanto'),
        '2': (152, 251, 'ii_johto'),
        '3': (252, 386, 'iii_hoenn'),
        '4': (387, 493, 'iv_sinnoh'),
        '5': (494, 649, 'v_unova'),
        '6': (650, 721, 'vi_kalos'),
        '7': (722, 809, 'vii_alola'),
        '8': (810, 905, 'viii_galar'),
        '9': (906, 1025, 'ix_paldea')
    }
    
    if gen not in gen_ranges:
        print(f'❌ Generación {gen} no válida. Usa 1-9.')
        sys.exit(1)
    
    start, end, name = gen_ranges[gen]
    print(f'Obteniendo Pokémon #{start}-{end}...')
    
    pokemon_list = []
    for pid in range(start, end + 1):
        pokemon = fetch_pokemon(pid)
        if pokemon:
            pokemon_list.append(pokemon)
    
    if pokemon_list:
        if order == 'color':
            pokemon_list = sorted(pokemon_list, key=lambda p: p.get('color', 'unknown'))
            suffix = 'by_color'
            order_text = 'por Color'
        else:
            suffix = 'by_id'
            order_text = 'por ID'
        
        # Generar PDF en la ruta correcta
        output_path = f'docs/pdf/{name}_{suffix}.pdf'
        if not os.path.exists('docs/pdf'):
            # Si estamos en scripts/, cambiar al directorio padre
            os.chdir('..')
        generate_pokemon_pdf(pokemon_list, output_path, f'{name.title()} {order_text} ({len(pokemon_list)} Pokémon)')
        print(f'✅ Generación {gen} completada: {len(pokemon_list)} Pokémon')
    else:
        print('❌ Error obteniendo Pokémon')

if __name__ == "__main__":
    main()
