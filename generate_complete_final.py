#!/usr/bin/env python3
"""
Generate complete Pokemon PDF using the same format as generation PDFs
"""

import requests
import json
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader
from io import BytesIO
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os
import hashlib

# Cache directories
CACHE_DIR = './cache'
DATA_CACHE_DIR = os.path.join(CACHE_DIR, 'data')
IMAGE_CACHE_DIR = os.path.join(CACHE_DIR, 'images')
TRANSLATION_CACHE_DIR = os.path.join(CACHE_DIR, 'translations')

# Create cache directories
os.makedirs(DATA_CACHE_DIR, exist_ok=True)
os.makedirs(IMAGE_CACHE_DIR, exist_ok=True)
os.makedirs(TRANSLATION_CACHE_DIR, exist_ok=True)

def translate_to_catalan(text):
    """Translate text to Catalan using translation file"""
    if not text or text == "Descripció no disponible.":
        return text
    
    # Load translations from file
    translations_file = 'catalan_translations.json'
    if os.path.exists(translations_file):
        try:
            with open(translations_file, 'r', encoding='utf-8') as f:
                translations = json.load(f)
                return translations.get(text, text)  # Return original if not found
        except:
            pass
    
    # Fallback: return original text if translation file not found
    return text

# Pokemon type translations to Catalan
TYPE_TRANSLATIONS = {
    'normal': 'NORMAL',
    'fire': 'FOC',
    'water': 'AIGUA',
    'electric': 'ELÈCTRIC',
    'grass': 'PLANTA',
    'ice': 'GEL',
    'fighting': 'LLUITA',
    'poison': 'VERÍ',
    'ground': 'TERRA',
    'flying': 'VOLADOR',
    'psychic': 'PSÍQUIC',
    'bug': 'INSECTE',
    'rock': 'ROCA',
    'ghost': 'FANTASMA',
    'dragon': 'DRAC',
    'dark': 'FOSC',
    'steel': 'ACER',
    'fairy': 'FADA'
}

# Color translations
COLOR_TRANSLATIONS = {
    'red': 'Vermell',
    'blue': 'Blau',
    'yellow': 'Groc',
    'green': 'Verde',
    'black': 'Negre',
    'brown': 'Marró',
    'purple': 'Morat',
    'gray': 'Gris',
    'white': 'Blanc',
    'pink': 'Rosa'
}

# Pokemon color mapping for backgrounds
POKEMON_COLORS = {
    'red': '#FF6B6B',
    'blue': '#4ECDC4',
    'yellow': '#FFE66D',
    'green': '#95E1D3',
    'black': '#3D5A80',
    'brown': '#C1666B',
    'purple': '#A8DADC',
    'gray': '#B8B8B8',
    'white': '#F1FAEE',
    'pink': '#FFB3BA'
}

def fetch_pokemon(pokemon_id):
    """Fetch Pokemon data from cache or API"""
    cache_file = os.path.join(DATA_CACHE_DIR, f'pokemon_{pokemon_id}.json')
    
    # Try to load from cache first
    if os.path.exists(cache_file):
        try:
            with open(cache_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            pass
    
    # If not in cache, fetch from API
    try:
        response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{pokemon_id}')
        if response.status_code == 200:
            pokemon_data = response.json()
            
            # Get species data for description and color
            species_response = requests.get(pokemon_data['species']['url'])
            if species_response.status_code == 200:
                species_data = species_response.json()
                pokemon_data['species_data'] = species_data
            
            # Save to cache
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(pokemon_data, f, ensure_ascii=False, indent=2)
            
            return pokemon_data
    except Exception as e:
        print(f"Error fetching Pokemon {pokemon_id}: {e}")
    
    return None

def get_catalan_description(pokemon_id):
    """Get Catalan description from translation file"""
    try:
        with open('catalan_translations.json', 'r', encoding='utf-8') as f:
            translations = json.load(f)
            return translations.get(str(pokemon_id), {}).get('description_catalan', '')
    except:
        return ''

def download_image(url):
    """Download image and return ImageReader object"""
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return ImageReader(BytesIO(response.content))
    except:
        pass
    return None

def create_gradient_background(c, x, y, width, height, color_name):
    """Create gradient background"""
    color = POKEMON_COLORS.get(color_name, '#F0F0F0')
    hex_color = HexColor(color)
    
    # Create gradient effect
    for i in range(int(height)):
        alpha = 1 - (i / height) * 0.3
        gradient_color = HexColor(color)
        gradient_color.alpha = alpha
        c.setFillColor(gradient_color)
        c.rect(x, y + i, width, 1, fill=1, stroke=0)

def draw_pokemon_card(c, pokemon, x, y, card_width, card_height):
    """Draw a single Pokemon card"""
    # Get Pokemon data safely
    if not isinstance(pokemon, dict):
        return
        
    name = pokemon.get('name', 'Unknown').title()
    pokemon_id = pokemon.get('id', 0)
    
    types = []
    if 'types' in pokemon and isinstance(pokemon['types'], list):
        types = [t['type']['name'] for t in pokemon['types'] if isinstance(t, dict)]
    
    height = pokemon.get('height', 0) / 10  # Convert to meters
    weight = pokemon.get('weight', 0) / 10  # Convert to kg
    
    # Get color
    color = 'white'
    if 'species_data' in pokemon and 'color' in pokemon['species_data']:
        color = pokemon['species_data']['color']['name']
    
    # Get Catalan description
    catalan_desc = get_catalan_description(pokemon_id)
    if not catalan_desc:
        type_str = '/'.join([TYPE_TRANSLATIONS.get(t, t.upper()) for t in types])
        catalan_desc = f"{name} és un fascinant Pokémon de tipus {type_str}."
    
    # Create gradient background
    create_gradient_background(c, x, y, card_width, card_height, color)
    
    # Draw card border
    c.setStrokeColor(HexColor('#000000'))
    c.setLineWidth(2)
    c.rect(x, y, card_width, card_height, fill=0, stroke=1)
    
    # Draw Pokemon image
    image_size = 120
    image_x = x + 20
    image_y = y + card_height - image_size - 20
    
    # Try to get Pokemon image
    image_url = None
    if 'sprites' in pokemon and pokemon['sprites'].get('other', {}).get('official-artwork', {}).get('front_default'):
        image_url = pokemon['sprites']['other']['official-artwork']['front_default']
    
    if image_url:
        image = download_image(image_url)
        if image:
            c.drawImage(image, image_x, image_y, width=image_size, height=image_size)
    
    # Draw Pokemon info
    info_x = image_x + image_size + 20
    info_y = y + card_height - 30
    
    # Pokemon name and number
    c.setFont("Helvetica-Bold", 16)
    c.setFillColor(HexColor('#000000'))
    c.drawString(info_x, info_y, f"{name} #{pokemon_id:03d}")
    
    # Types
    info_y -= 25
    c.setFont("Helvetica-Bold", 12)
    types_catalan = '/'.join([TYPE_TRANSLATIONS.get(t, t.upper()) for t in types])
    c.drawString(info_x, info_y, f"Tipus: {types_catalan}")
    
    # Height and weight
    info_y -= 20
    c.setFont("Helvetica", 10)
    c.drawString(info_x, info_y, f"Alçada: {height:.1f}m")
    
    info_y -= 15
    c.drawString(info_x, info_y, f"Pes: {weight:.1f}kg")
    
    # Color
    info_y -= 15
    color_catalan = COLOR_TRANSLATIONS.get(color, color.title())
    c.drawString(info_x, info_y, f"Color: {color_catalan}")
    
    # Description
    info_y -= 25
    c.setFont("Helvetica-Bold", 10)
    c.drawString(info_x, info_y, "Descripció:")
    
    # Wrap description text
    info_y -= 15
    c.setFont("Helvetica", 9)
    max_width = card_width - (info_x - x) - 20
    words = catalan_desc.split()
    lines = []
    current_line = []
    
    for word in words:
        test_line = ' '.join(current_line + [word])
        if c.stringWidth(test_line, "Helvetica", 9) <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(' '.join(current_line))
                current_line = [word]
            else:
                lines.append(word)
    
    if current_line:
        lines.append(' '.join(current_line))
    
    # Draw description lines (max 4 lines)
    for i, line in enumerate(lines[:4]):
        c.drawString(info_x, info_y - (i * 12), line)

def generate_complete_pdf():
    """Generate complete PDF with all Pokemon"""
    print("Generating complete Pokemon PDF...")
    
    filename = "pokemon_complet_catala.pdf"
    c = canvas.Canvas(filename, pagesize=landscape(A4))
    width, height = landscape(A4)
    
    # Card dimensions
    card_width = width - 40
    card_height = 180
    cards_per_page = 3
    
    # Title page
    c.setFont("Helvetica-Bold", 24)
    c.drawString(width/2 - 150, height - 100, "GUIA COMPLETA POKÉMON")
    c.setFont("Helvetica", 16)
    c.drawString(width/2 - 120, height - 140, "Tots els Pokémon de totes les Generacions")
    c.drawString(width/2 - 80, height - 170, "Amb descripcions en català")
    c.showPage()
    
    # Process all Pokemon
    total_pokemon = 0
    current_page_cards = 0
    
    for pokemon_id in range(1, 1026):  # All Pokemon 1-1025
        if pokemon_id % 50 == 0:
            print(f"Processing Pokemon #{pokemon_id}...")
        
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
                # Add page number
                c.setFont("Helvetica", 10)
                page_num = (total_pokemon - 1) // cards_per_page + 2  # +1 for title page
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
    
    return filename

if __name__ == "__main__":
    generate_complete_pdf()
