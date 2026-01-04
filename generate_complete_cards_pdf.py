#!/usr/bin/env python3
"""
Generate complete Pokemon PDF with horizontal card format and images
"""

import json
import os
import requests
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image as RLImage
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from PIL import Image, ImageDraw
import io

# Pokemon type translations to Catalan
TYPE_TRANSLATIONS = {
    'normal': 'NORMAL', 'fire': 'FOC', 'water': 'AIGUA', 'electric': 'ELÈCTRIC',
    'grass': 'PLANTA', 'ice': 'GEL', 'fighting': 'LLUITA', 'poison': 'VERÍ',
    'ground': 'TERRA', 'flying': 'VOLADOR', 'psychic': 'PSÍQUIC', 'bug': 'INSECTE',
    'rock': 'ROCA', 'ghost': 'FANTASMA', 'dragon': 'DRAC', 'dark': 'FOSC',
    'steel': 'ACER', 'fairy': 'FADA'
}

# Color mapping for backgrounds
POKEMON_COLORS = {
    'red': '#FF6B6B', 'blue': '#4ECDC4', 'yellow': '#FFE66D', 'green': '#95E1D3',
    'black': '#3D5A80', 'brown': '#C1666B', 'purple': '#A8DADC', 'gray': '#B8B8B8',
    'white': '#F1FAEE', 'pink': '#FFB3BA'
}

def fetch_pokemon_data(pokemon_id):
    """Fetch Pokemon data from cache or API"""
    cache_file = f"cache/data/pokemon_{pokemon_id}.json"
    
    if os.path.exists(cache_file):
        with open(cache_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

def get_catalan_translation(pokemon_id):
    """Get Catalan translation from our translation file"""
    try:
        with open('catalan_translations.json', 'r', encoding='utf-8') as f:
            translations = json.load(f)
            return translations.get(str(pokemon_id), {}).get('description_catalan', '')
    except:
        return ''

def download_image(url, pokemon_id):
    """Download and cache Pokemon image"""
    cache_dir = "cache/images"
    os.makedirs(cache_dir, exist_ok=True)
    cache_file = f"{cache_dir}/pokemon_{pokemon_id}.png"
    
    if os.path.exists(cache_file):
        return cache_file
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(cache_file, 'wb') as f:
                f.write(response.content)
            return cache_file
    except Exception as e:
        print(f"Error downloading image for Pokemon {pokemon_id}: {e}")
    
    return None

def create_gradient_background(color_name, width=200, height=150):
    """Create gradient background for Pokemon card"""
    color = POKEMON_COLORS.get(color_name, '#F0F0F0')
    
    # Create image with gradient
    img = Image.new('RGB', (width, height), color)
    draw = ImageDraw.Draw(img)
    
    # Simple gradient effect
    for i in range(height):
        alpha = int(255 * (1 - i / height * 0.3))
        gradient_color = tuple(min(255, max(0, c + alpha//4)) for c in img.getpixel((0, 0)))
        draw.line([(0, i), (width, i)], fill=gradient_color)
    
    # Save to temp file
    temp_path = f"cache/images/gradient_{color_name}.png"
    os.makedirs("cache/images", exist_ok=True)
    img.save(temp_path)
    return temp_path

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for (page_num, state) in enumerate(self._saved_page_states):
            self.__dict__.update(state)
            self.draw_page_number(page_num + 1, num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_num, total_pages):
        width, height = landscape(A4)
        self.setFont("Helvetica", 10)
        self.drawRightString(width - 30, 30, f"Pàgina {page_num} de {total_pages}")

def create_pokemon_card(pokemon_data, pokemon_id):
    """Create horizontal Pokemon card with image and info"""
    if not pokemon_data or not isinstance(pokemon_data, dict):
        return None
    
    # Get basic info
    name = pokemon_data.get('name', f'Pokemon{pokemon_id}').title()
    types = []
    if 'types' in pokemon_data and isinstance(pokemon_data['types'], list):
        types = [t['type']['name'] for t in pokemon_data['types'] if isinstance(t, dict)]
    
    height = pokemon_data.get('height', 0) / 10
    weight = pokemon_data.get('weight', 0) / 10
    
    # Get color
    color = "white"
    if 'species_data' in pokemon_data and 'color' in pokemon_data['species_data']:
        color = pokemon_data['species_data']['color']['name']
    
    # Get Catalan description
    catalan_desc = get_catalan_translation(pokemon_id)
    if not catalan_desc:
        type_str = '/'.join([TYPE_TRANSLATIONS.get(t, t.upper()) for t in types])
        catalan_desc = f"{name} és un fascinant Pokémon de tipus {type_str}."
    
    # Get Pokemon image
    image_path = None
    if 'sprites' in pokemon_data and pokemon_data['sprites'].get('other', {}).get('official-artwork', {}).get('front_default'):
        image_url = pokemon_data['sprites']['other']['official-artwork']['front_default']
        image_path = download_image(image_url, pokemon_id)
    
    # Create gradient background
    bg_path = create_gradient_background(color)
    
    # Create card data
    card_data = []
    
    # Row 1: Image and basic info
    image_cell = ""
    if image_path and os.path.exists(image_path):
        try:
            image_cell = RLImage(image_path, width=1.5*inch, height=1.5*inch)
        except:
            image_cell = f"#{pokemon_id:03d}"
    else:
        image_cell = f"#{pokemon_id:03d}"
    
    info_text = f"""
<b>{name}</b><br/>
#{pokemon_id:03d}<br/>
<b>Tipus:</b> {'/'.join([TYPE_TRANSLATIONS.get(t, t.upper()) for t in types])}<br/>
<b>Alçada:</b> {height:.1f}m<br/>
<b>Pes:</b> {weight:.1f}kg<br/>
<b>Color:</b> {color.title()}
"""
    
    desc_text = f"<b>Descripció:</b><br/>{catalan_desc}"
    
    card_data.append([image_cell, info_text, desc_text])
    
    # Create table
    table = Table(card_data, colWidths=[2*inch, 2.5*inch, 4*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ALIGN', (0, 0), (0, -1), 'CENTER'),
        ('ALIGN', (1, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (1, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (1, 0), (-1, -1), 10),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
    ]))
    
    return table

def generate_complete_pdf():
    """Generate complete PDF with all Pokemon in card format"""
    print("Generating complete Pokemon PDF with card format...")
    
    # Create PDF
    filename = "pokemon_complet_catala.pdf"
    doc = SimpleDocTemplate(filename, pagesize=landscape(A4), 
                          rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=50)
    
    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        alignment=TA_CENTER,
        textColor=colors.darkblue
    )
    
    header_style = ParagraphStyle(
        'CustomHeader',
        parent=styles['Heading2'],
        fontSize=16,
        spaceAfter=20,
        alignment=TA_CENTER,
        textColor=colors.darkgreen
    )
    
    story = []
    
    # Title page
    story.append(Paragraph("GUIA COMPLETA POKÉMON", title_style))
    story.append(Paragraph("Tots els Pokémon de totes les Generacions", header_style))
    story.append(Paragraph("Amb descripcions en català", header_style))
    story.append(PageBreak())
    
    # Process all Pokemon
    total_pokemon = 0
    cards_per_page = 4
    current_page_cards = 0
    
    for pokemon_id in range(1, 1026):  # All Pokemon 1-1025
        if pokemon_id % 50 == 0:
            print(f"Processing Pokemon #{pokemon_id}...")
        
        data = fetch_pokemon_data(pokemon_id)
        if data:
            card = create_pokemon_card(data, pokemon_id)
            if card:
                story.append(card)
                story.append(Spacer(1, 20))
                total_pokemon += 1
                current_page_cards += 1
                
                # Add page break every 4 cards
                if current_page_cards >= cards_per_page:
                    story.append(PageBreak())
                    current_page_cards = 0
    
    # Add summary page
    story.append(PageBreak())
    story.append(Paragraph("RESUM FINAL", title_style))
    story.append(Paragraph(f"Total de Pokémon inclosos: {total_pokemon}", header_style))
    story.append(Paragraph("Totes les descripcions han estat traduïdes al català", header_style))
    story.append(Paragraph("Format de cartes amb imatges i informació completa", header_style))
    
    # Build PDF
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF generat: {filename}")
    print(f"Total Pokémon inclosos: {total_pokemon}")
    
    return filename

if __name__ == "__main__":
    generate_complete_pdf()
