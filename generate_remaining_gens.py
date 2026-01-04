#!/usr/bin/env python3
"""
Generate remaining generation PDFs (VI-IX)
"""

import sys
import os
sys.path.append('.')

from generate_pdf import *

def generate_specific_generation(start_id, end_id, gen_name, gen_title):
    """Generate PDF for specific generation range"""
    print(f"Generating {gen_title}...")
    
    # Collect Pokemon for this generation
    pokemon_list = []
    for pokemon_id in range(start_id, end_id + 1):
        pokemon = fetch_pokemon(pokemon_id)
        if pokemon:
            pokemon_list.append(pokemon)
    
    if not pokemon_list:
        print(f"No Pokemon found for {gen_title}")
        return
    
    # Generate PDFs
    generate_pdf(pokemon_list, f"{gen_name}_by_id", f"{gen_title} - Ordenat per ID")
    generate_pdf_by_color(pokemon_list, f"{gen_name}_by_color", f"{gen_title} - Ordenat per Color")
    
    print(f"{gen_title} PDFs generated successfully!")

if __name__ == "__main__":
    generations = [
        (650, 721, "vi_kalos", "Gen VI - Kalos"),
        (722, 809, "vii_alola", "Gen VII - Alola"), 
        (810, 905, "viii_galar", "Gen VIII - Galar"),
        (906, 1025, "ix_paldea", "Gen IX - Paldea")
    ]
    
    for start_id, end_id, gen_name, gen_title in generations:
        generate_specific_generation(start_id, end_id, gen_name, gen_title)
        print()
