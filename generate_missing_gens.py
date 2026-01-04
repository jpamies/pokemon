#!/usr/bin/env python3
"""
Generate individual generation PDFs using working code
"""

import sys
import os
sys.path.append('.')

# Import from the working complete generator
from generate_complete_final import *

def generate_generation_range(start_id, end_id, filename_prefix, title):
    """Generate PDF for specific generation range"""
    print(f"Generating {title}...")
    
    filename = f"pdf/{filename_prefix}_by_id.pdf"
    c = canvas.Canvas(filename, pagesize=landscape(A4))
    width, height = landscape(A4)
    
    # Card dimensions
    card_width = width - 40
    card_height = 180
    cards_per_page = 3
    
    # Title page
    c.setFont("Helvetica-Bold", 24)
    c.drawString(width/2 - 150, height - 100, title)
    c.showPage()
    
    # Process Pokemon in range
    total_pokemon = 0
    current_page_cards = 0
    
    for pokemon_id in range(start_id, end_id + 1):
        pokemon = fetch_pokemon(pokemon_id)
        if pokemon:
            # Calculate card position
            card_y = height - (current_page_cards + 1) * (card_height + 20) - 20
            
            # Draw Pokemon card
            draw_pokemon_card(c, pokemon, 20, card_y, card_width, card_height)
            
            total_pokemon += 1
            current_page_cards += 1
            
            # New page after 3 cards
            if current_page_cards >= cards_per_page:
                page_num = (total_pokemon - 1) // cards_per_page + 2
                c.setFont("Helvetica", 10)
                c.drawRightString(width - 20, 20, f"Pàgina {page_num}")
                c.showPage()
                current_page_cards = 0
    
    # Final page if needed
    if current_page_cards > 0:
        page_num = (total_pokemon - 1) // cards_per_page + 2
        c.setFont("Helvetica", 10)
        c.drawRightString(width - 20, 20, f"Pàgina {page_num}")
    
    c.save()
    print(f"Generated {filename} with {total_pokemon} Pokemon")

if __name__ == "__main__":
    # Generate missing generations
    generations = [
        (650, 721, "vi_kalos", "Gen VI - Kalos"),
        (722, 809, "vii_alola", "Gen VII - Alola"), 
        (810, 905, "viii_galar", "Gen VIII - Galar"),
        (906, 1025, "ix_paldea", "Gen IX - Paldea")
    ]
    
    for start_id, end_id, gen_name, gen_title in generations:
        generate_generation_range(start_id, end_id, gen_name, gen_title)
        print()
