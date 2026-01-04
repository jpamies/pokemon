#!/usr/bin/env python3
"""
Generate complete Pokemon PDF with proper card format and images
"""

import requests
import json
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader
from io import BytesIO
import os

# Import functions from generate_pdf.py
import sys
sys.path.append('.')
from generate_pdf import fetch_pokemon, get_catalan_description, TYPE_TRANSLATIONS, COLOR_TRANSLATIONS, POKEMON_COLORS

def download_image(url):
    """Download image and return ImageReader object"""
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return ImageReader(BytesIO(response.content))
    except:
        pass
    return None

def create_gradient_background(c, x, y, width, height, color_name):
    """Create gradient background"""
    color = POKEMON_COLORS.get(color_name, '#F0F0F0')
    hex_color = HexColor(color)
    
    # Simple solid background
    c.setFillColor(hex_color)
    c.rect(x, y, width, height, fill=1, stroke=0)

def draw_pokemon_card_complete(c, pokemon, x, y, card_width, card_height):
    """Draw Pokemon card with complete format"""
    if not isinstance(pokemon, dict):
        return
        
    name = pokemon.get('name', 'Unknown').title()
    pokemon_id = pokemon.get('id', 0)
    
    types = []
    if 'types' in pokemon and isinstance(pokemon['types'], list):
        types = [t['type']['name'] for t in pokemon['types'] if isinstance(t, dict)]
    
    height_m = pokemon.get('height', 0) / 10
    weight_kg = pokemon.get('weight', 0) / 10
    
    # Get color
    color = 'white'
    if 'species_data' in pokemon and 'color' in pokemon['species_data']:
        color = pokemon['species_data']['color']['name']
    
    # Create gradient background
    create_gradient_background(c, x, y, card_width, card_height, color)
    
    # Draw card border
    c.setStrokeColor(HexColor('#000000'))
    c.setLineWidth(2)
    c.rect(x, y, card_width, card_height, fill=0, stroke=1)
    
    # Pokemon name (top left) - white with black outline
    c.setFont("Helvetica-Bold", 14)
    name_text = name.upper()
    
    # Draw name outline (black)
    c.setFillColor(HexColor('#000000'))
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx != 0 or dy != 0:
                c.drawString(x + 10 + dx, y + card_height - 20 + dy, name_text)
    
    # Draw main name (white)
    c.setFillColor(HexColor('#ffffff'))
    c.drawString(x + 10, y + card_height - 20, name_text)
    
    # Pokemon number (right side)
    num_text = f"#{pokemon_id:03d}"
    num_width = c.stringWidth(num_text, "Helvetica-Bold", 12)
    
    c.setFillColor(HexColor('#000000'))
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx != 0 or dy != 0:
                c.drawString(x + card_width - num_width - 8 + dx, y + card_height - 20 + dy, num_text)
    
    c.setFillColor(HexColor('#ffffff'))
    c.drawString(x + card_width - num_width - 8, y + card_height - 20, num_text)
    
    # Pokemon image (left side)
    img_size = 80
    img_x = x + 15
    img_y = y + card_height - 125
    
    # Try to get Pokemon image
    image = None
    if 'sprites' in pokemon and pokemon['sprites'].get('other', {}).get('official-artwork', {}).get('front_default'):
        image_url = pokemon['sprites']['other']['official-artwork']['front_default']
        image = download_image(image_url)
    
    if image:
        try:
            # White background for image
            c.setFillColor(HexColor('#ffffff'))
            c.roundRect(img_x - 5, img_y - 5, img_size + 10, img_size + 10, 5, fill=1)
            c.drawImage(image, img_x, img_y, width=img_size, height=img_size)
        except:
            pass
    
    # Get Catalan description
    catalan_desc = get_catalan_description(pokemon_id)
    if not catalan_desc or catalan_desc == "Descripció no disponible.":
        type_str = '/'.join([TYPE_TRANSLATIONS.get(t, t.upper()) for t in types])
        catalan_desc = f"{name} és un fascinant Pokémon de tipus {type_str}."
    
    # Description text
    desc_y = img_y - 15
    description = catalan_desc.upper()
    c.setFillColor(HexColor('#2c3e50'))
    c.setFont("Helvetica", 8)
    
    # Wrap text
    max_width = card_width - 20
    words = description.split()
    lines = []
    current_line = ""
    
    for word in words:
        test_line = current_line + " " + word if current_line else word
        if c.stringWidth(test_line, "Helvetica", 8) <= max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
                current_line = word
            else:
                lines.append(word)
    
    if current_line:
        lines.append(current_line)
    
    # Draw description lines (max 6 lines)
    for i, line in enumerate(lines[:6]):
        c.drawString(x + 10, desc_y - (i * 10), line)
    
    # Right side info
    info_x = x + card_width - 200
    info_y = y + card_height - 50
    
    # Types
    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(HexColor('#ffffff'))
    types_text = "TIPUS: " + '/'.join([TYPE_TRANSLATIONS.get(t, t.upper()) for t in types])
    
    # Draw types with outline
    c.setFillColor(HexColor('#000000'))
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx != 0 or dy != 0:
                c.drawString(info_x + dx, info_y + dy, types_text)
    
    c.setFillColor(HexColor('#ffffff'))
    c.drawString(info_x, info_y, types_text)
    
    # Height and weight
    info_y -= 15
    c.setFont("Helvetica", 9)
    size_text = f"ALÇADA: {height_m:.1f}M  PES: {weight_kg:.1f}KG"
    
    c.setFillColor(HexColor('#000000'))
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx != 0 or dy != 0:
                c.drawString(info_x + dx, info_y + dy, size_text)
    
    c.setFillColor(HexColor('#ffffff'))
    c.drawString(info_x, info_y, size_text)

def generate_complete_pdf():
    """Generate complete PDF with all Pokemon in card format"""
    print("Generating complete Pokemon PDF with card format...")
    
    filename = "pokemon_complet_catala.pdf"
    c = canvas.Canvas(filename, pagesize=landscape(A4))
    width, height = landscape(A4)
    
    # Card dimensions
    card_width = width - 40
    card_height = 180
    cards_per_page = 3
    
    # Title page
    c.setFont("Helvetica-Bold", 24)
    c.drawString(width/2 - 200, height - 100, "GUIA COMPLETA POKÉMON")
    c.setFont("Helvetica", 16)
    c.drawString(width/2 - 150, height - 140, "Totes les Generacions (1-1025)")
    c.drawString(width/2 - 120, height - 170, "Amb descripcions en català")
    c.showPage()
    
    # Process all Pokemon
    total_pokemon = 0
    current_page_cards = 0
    
    for pokemon_id in range(1, 1026):
        if pokemon_id % 50 == 0:
            print(f"Processing Pokemon #{pokemon_id}...")
        
        pokemon = fetch_pokemon(pokemon_id)
        if pokemon:
            # Calculate card position
            card_y = height - (current_page_cards + 1) * (card_height + 20) - 20
            
            # Draw Pokemon card
            draw_pokemon_card_complete(c, pokemon, 20, card_y, card_width, card_height)
            
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
    print(f"PDF generat: {filename}")
    print(f"Total Pokémon inclosos: {total_pokemon}")

if __name__ == "__main__":
    generate_complete_pdf()
