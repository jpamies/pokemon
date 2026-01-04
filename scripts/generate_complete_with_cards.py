#!/usr/bin/env python3
"""
Generate complete Pokemon PDF using fetch_pokemon function
"""

import sys
sys.path.append('..')
from scripts.generate_pdf import fetch_pokemon, generate_pokemon_pdf

def generate_complete_pdf():
    """Generate complete PDF with all Pokemon"""
    print("Generating complete Pokemon PDF...")
    
    # Load all Pokemon data
    all_pokemon = []
    for pokemon_id in range(1, 1026):
        if pokemon_id % 100 == 0:
            print(f"Loading Pokemon #{pokemon_id}...")
        
        pokemon_data = fetch_pokemon(pokemon_id)
        if pokemon_data:
            all_pokemon.append(pokemon_data)
    
    print(f"Loaded {len(all_pokemon)} Pokemon")
    
    # Generate PDF
    filename = "pokemon_complet_catala.pdf"
    generate_pokemon_pdf(all_pokemon, filename, f"{len(all_pokemon)} Pokémon - Totes les Generacions")
    
    print(f"Complete PDF generated: {filename}")

if __name__ == "__main__":
    generate_complete_pdf()
