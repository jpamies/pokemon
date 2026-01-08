#!/usr/bin/env python3
"""
Generate complete Pokemon PDF sorted by color
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from generate_pdf import fetch_pokemon, generate_pokemon_pdf

def generate_complete_by_color():
    """Generate complete PDF sorted by color"""
    print("Generating complete Pokemon PDF sorted by color...")
    
    # Load all Pokemon data
    all_pokemon = []
    for pokemon_id in range(1, 1026):
        if pokemon_id % 100 == 0:
            print(f"Loading Pokemon #{pokemon_id}...")
        
        pokemon_data = fetch_pokemon(pokemon_id)
        if pokemon_data:
            all_pokemon.append(pokemon_data)
    
    print(f"Loaded {len(all_pokemon)} Pokemon")
    
    # Sort by color first, then by ID
    def get_color_sort_key(pokemon):
        color = pokemon.get('color', 'white')  # Use the direct color field
        
        # Color order for sorting
        color_order = {
            'black': 1, 'blue': 2, 'brown': 3, 'gray': 4, 'green': 5,
            'pink': 6, 'purple': 7, 'red': 8, 'white': 9, 'yellow': 10
        }
        
        pokemon_id = pokemon.get('id', 9999)
        return (color_order.get(color, 99), pokemon_id)  # Sort by color first, then by ID
    
    all_pokemon.sort(key=get_color_sort_key)
    
    # Generate PDF
    filename = "docs/pdf/pokemon_complet_catala_by_color.pdf"
    generate_pokemon_pdf(all_pokemon, filename, f"{len(all_pokemon)} Pokémon - Per Color")
    
    print(f"Complete PDF by color generated: {filename}")

if __name__ == "__main__":
    generate_complete_by_color()
