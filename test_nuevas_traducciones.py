#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'scripts'))

from generate_pdf import generate_pokemon_pdf

# Generar PDF de prueba con los primeros 10 Pokémon
pokemon_list = []
for i in range(1, 11):
    pokemon_list.append({
        'id': i,
        'name': f'Pokemon{i}',
        'image_url': f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{i}.png'
    })

output_file = "test_nuevas_traducciones.pdf"

print("Generando PDF de prueba con nuevas traducciones...")
generate_pokemon_pdf(pokemon_list, output_file, "Prueba Nuevas Traducciones Catalanas")
print(f"✅ PDF generado: {output_file}")
