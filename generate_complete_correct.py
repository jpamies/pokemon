#!/usr/bin/env python3
"""
Generate complete Pokemon PDF using the same card format as individual generation PDFs
"""

import sys
import os
sys.path.append('.')

from generate_pdf import *

def generate_complete_pokemon_pdf():
    """Generate complete PDF with all Pokemon using card format"""
    print("Generating complete Pokemon PDF with card format...")
    
    # Collect ALL Pokemon
    all_pokemon = []
    for pokemon_id in range(1, 1026):  # All Pokemon 1-1025
        if pokemon_id % 100 == 0:
            print(f"Loading Pokemon #{pokemon_id}...")
        
        pokemon = fetch_pokemon(pokemon_id)
        if pokemon:
            all_pokemon.append(pokemon)
    
    print(f"Loaded {len(all_pokemon)} Pokemon total")
    
    # Generate complete PDF using the same function as individual generations
    generate_pokemon_pdf(all_pokemon, "pokemon_complet_catala", "GUIA COMPLETA POKÉMON - Totes les Generacions")
    
    print("Complete Pokemon PDF generated successfully!")

if __name__ == "__main__":
    generate_complete_pokemon_pdf()
