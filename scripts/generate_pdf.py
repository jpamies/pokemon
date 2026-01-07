#!/usr/bin/env python3
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
CACHE_DIR = os.path.join(os.path.dirname(__file__), '..', 'cache')
DATA_CACHE_DIR = os.path.join(CACHE_DIR, 'data')
IMAGE_CACHE_DIR = os.path.join(CACHE_DIR, 'images')
TRANSLATION_CACHE_DIR = os.path.join(CACHE_DIR, 'translations')

# Create cache directories
os.makedirs(DATA_CACHE_DIR, exist_ok=True)
os.makedirs(IMAGE_CACHE_DIR, exist_ok=True)
os.makedirs(TRANSLATION_CACHE_DIR, exist_ok=True)

# Try to register fonts that support emojis
try:
    # Local emoji fonts (downloaded)
    local_fonts = [
        ('./fonts/NotoColorEmoji.ttf', 'NotoEmoji'),
        ('./fonts/EmojiOneColor.otf', 'EmojiOne'),
    ]
    
    for font_path, font_name in local_fonts:
        if os.path.exists(font_path):
            try:
                pdfmetrics.registerFont(TTFont(font_name, font_path))
                print(f"Registered local emoji font: {font_name}")
            except Exception as e:
                print(f"Failed to register {font_name}: {e}")
    
    # System emoji fonts
    emoji_fonts = [
        ('/System/Library/Fonts/Apple Color Emoji.ttc', 'AppleEmoji'),  # macOS
        ('/Windows/Fonts/seguiemj.ttf', 'SegoeEmoji'),  # Windows Segoe UI Emoji
        ('/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf', 'SystemNoto'),  # Linux Noto
        ('/System/Library/Fonts/Segoe UI Emoji.ttf', 'SegoeEmoji2'),  # Alternative Segoe
    ]
    
    for font_path, font_name in emoji_fonts:
        if os.path.exists(font_path):
            try:
                pdfmetrics.registerFont(TTFont(font_name, font_path))
                print(f"Registered system emoji font: {font_name}")
            except Exception as e:
                print(f"Failed to register {font_name}: {e}")
    
    # Fallback fonts with good Unicode support
    fallback_fonts = [
        ('/System/Library/Fonts/Arial Unicode MS.ttf', 'ArialUnicode'),
        ('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 'DejaVu'),
    ]
    
    for font_path, font_name in fallback_fonts:
        if os.path.exists(font_path):
            try:
                pdfmetrics.registerFont(TTFont(font_name, font_path))
                print(f"Registered fallback font: {font_name}")
            except Exception as e:
                print(f"Failed to register {font_name}: {e}")
                
except Exception as e:
    print(f"Font registration failed: {e}")
    pass

def get_emoji_font():
    """Get the best available font for emojis"""
    registered_fonts = pdfmetrics.getRegisteredFontNames()
    
    # Priority order: Downloaded fonts, system emoji fonts, Unicode fonts, fallback
    font_priority = [
        'NotoEmoji', 'EmojiOne', 'SegoeEmoji', 'AppleEmoji', 
        'SystemNoto', 'SegoeEmoji2', 'ArialUnicode', 'DejaVu', 'Helvetica'
    ]
    
    for font in font_priority:
        if font in registered_fonts or font == 'Helvetica':
            print(f"Using font: {font}")
            return font
    
    return 'Helvetica'  # Final fallback

# Type translations to Catalan (primary language)
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
POKEMON_COLORS = {
    'red': '#FF4757',      # Bright red
    'blue': '#3742FA',     # Bright blue  
    'yellow': '#FFC312',   # Bright yellow
    'green': '#2ED573',    # Bright green
    'black': '#2F3542',    # Dark gray/black
    'brown': '#A0522D',    # Saddle brown
    'purple': '#8E44AD',   # Purple
    'gray': '#95A5A6',     # Gray
    'white': '#F8F9FA',    # Light gray/white
    'pink': '#FF6B9D'      # Pink
}

# Type colors and icons
TYPE_COLORS = {
    'normal': '#A8A878',
    'fire': '#F08030',
    'water': '#6890F0',
    'electric': '#F8D030',
    'grass': '#78C850',
    'ice': '#98D8D8',
    'fighting': '#C03028',
    'poison': '#A040A0',
    'ground': '#E0C068',
    'flying': '#A890F0',
    'psychic': '#F85888',
    'bug': '#A8B820',
    'rock': '#B8A038',
    'ghost': '#705898',
    'dragon': '#7038F8',
    'dark': '#705848',
    'steel': '#B8B8D0',
    'fairy': '#EE99AC'
}

TYPE_ICONS = {
    'normal': 'normal.png',
    'fire': 'fire.png',
    'water': 'water.png',
    'electric': 'electric.png',
    'grass': 'grass.png',
    'ice': 'ice.png',
    'fighting': 'fighting.png',
    'poison': 'poison.png',
    'ground': 'ground.png',
    'flying': 'flying.png',
    'psychic': 'psychic.png',
    'bug': 'bug.png',
    'rock': 'rock.png',
    'ghost': 'ghost.png',
    'dragon': 'dragon.png',
    'dark': 'dark.png',
    'steel': 'steel.png',
    'fairy': 'fairy.png'
}

# Fallback symbols if images not available
TYPE_ICONS_FALLBACK = {
    'normal': '●',
    'fire': '♦',
    'water': '♠',
    'electric': '★',
    'grass': '♣',
    'ice': '◆',
    'fighting': '♦',
    'poison': '☠',
    'ground': '■',
    'flying': '▲',
    'psychic': '◉',
    'bug': '●',
    'rock': '▲',
    'ghost': '◎',
    'dragon': '♦',
    'dark': '●',
    'steel': '■',
    'fairy': '★'
}

def fetch_pokemon(pokemon_id):
    """Fetch Pokemon data from API with caching"""
    cache_file = os.path.join(DATA_CACHE_DIR, f'pokemon_{pokemon_id}.json')
    
    # Try to load from local JSON files first (pokemon_data/)
    local_file_paths = [
        f'../pokemon_data/pokemon_{pokemon_id:04d}.json',
        f'pokemon_data/pokemon_{pokemon_id:04d}.json'
    ]
    
    for local_file in local_file_paths:
        if os.path.exists(local_file):
            try:
                with open(local_file, 'r', encoding='utf-8') as f:
                    local_data = json.load(f)
                    # Convert to expected format
                    pokemon_data = {
                        'id': local_data['id'],
                        'name': local_data['name'],
                        'height': local_data['height'],
                        'weight': local_data['weight'],
                        'types': local_data['types'],
                        'image_url': local_data.get('image_url', f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{pokemon_id}.png'),
                        'stats': local_data.get('stats', {}),
                        'evolution': local_data.get('evolution'),
                        'color': local_data.get('color', 'unknown'),
                        'description': local_data.get('descriptions', {}).get('es', 'Descripción no disponible.'),
                        'description_catalan': local_data.get('descriptions', {}).get('ca', 'Descripció no disponible.'),
                        'is_legendary': local_data.get('is_legendary', False),
                        'is_mythical': local_data.get('is_mythical', False)
                    }
                    return pokemon_data
            except Exception as e:
                print(f"Error loading local file for Pokemon #{pokemon_id}: {e}")
    
    # Try to load from cache
    if os.path.exists(cache_file):
        try:
            with open(cache_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            pass  # If cache is corrupted, fetch from API
    
    # Fetch from API
    try:
        response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{pokemon_id}')
        data = response.json()
        
        # Get species data for evolution chain and color
        species_response = requests.get(data['species']['url'])
        species_data = species_response.json()
        
        # Get evolution chain
        evolution_chain = None
        if species_data.get('evolution_chain'):
            evo_response = requests.get(species_data['evolution_chain']['url'])
            evo_data = evo_response.json()
            evolution_chain = parse_evolution_chain(evo_data['chain'], pokemon_id)
        
        # Get color
        color = species_data.get('color', {}).get('name', 'unknown')
        
        # Get original description (Spanish preferred, English fallback)
        description = "Descripción no disponible."
        
        # Try Spanish first (most common)
        for entry in species_data.get('flavor_text_entries', []):
            if entry['language']['name'] == 'es':
                description = entry['flavor_text'].replace('\n', ' ').replace('\f', ' ')
                break
        
        # Fallback to English if no Spanish
        if description == "Descripción no disponible.":
            for entry in species_data.get('flavor_text_entries', []):
                if entry['language']['name'] == 'en':
                    description = entry['flavor_text'].replace('\n', ' ').replace('\f', ' ')
                    break
        
        # Use Spanish description as fallback for description_catalan
        description_catalan = description
        
        pokemon_data = {
            'id': data['id'],
            'name': data['name'].title(),
            'height': data['height'],
            'weight': data['weight'],
            'types': [t['type']['name'] for t in data['types']],
            'image_url': data['sprites']['front_default'],
            'stats': {stat['stat']['name']: stat['base_stat'] for stat in data['stats']},
            'evolution': evolution_chain,
            'color': color,
            'description': description,
            'description_catalan': description_catalan
        }
        
        # Save to cache
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(pokemon_data, f, ensure_ascii=False, indent=2)
        
        return pokemon_data
        
    except Exception as e:
        print(f"Error fetching Pokemon #{pokemon_id}: {e}")
        return None

def parse_evolution_chain(chain, current_id):
    """Parse evolution chain to get full chain with images"""
    def extract_pokemon_id(url):
        return int(url.split('/')[-2])
    
    def build_full_chain(node):
        pokemon_id = extract_pokemon_id(node['species']['url'])
        pokemon_name = node['species']['name'].title()
        
        chain_data = [{
            'id': pokemon_id,
            'name': pokemon_name,
            'image_url': f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{pokemon_id}.png'
        }]
        
        for evolution in node['evolves_to']:
            chain_data.extend(build_full_chain(evolution))
        
        return chain_data
    
    # Get complete evolution chain
    full_chain = build_full_chain(chain)
    
    # Return full chain (shows pre-evolutions and post-evolutions)
    return full_chain if len(full_chain) > 1 else None

def download_image(url):
    """Download and cache Pokemon image with gradient background"""
    if not url:
        return None
    
    # Use official artwork URL
    artwork_url = url.replace('/sprites/pokemon/', '/sprites/pokemon/other/official-artwork/')
    
    # Create cache filename from artwork URL hash
    url_hash = hashlib.md5(artwork_url.encode()).hexdigest()
    cache_file = os.path.join(IMAGE_CACHE_DIR, f'{url_hash}_artwork.png')
    
    # Try to load from cache first
    if os.path.exists(cache_file):
        try:
            return ImageReader(cache_file)
        except:
            pass  # If cache is corrupted, download again
    
    # Download from URL - use official artwork
    print(f"🎨 Using artwork URL: {artwork_url}")
    
    try:
        from PIL import Image
        response = requests.get(artwork_url, timeout=10)
        response.raise_for_status()
        
        # Load and save directly without gradient (transparent background)
        img_data = BytesIO(response.content)
        img = Image.open(img_data)
        
        # Convert to RGBA to ensure transparency
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        # Save to cache
        img.save(cache_file, 'PNG')
        print(f"✅ Saved artwork to cache: {cache_file}")
        
        return ImageReader(cache_file)
    except Exception as e:
        print(f"Error with official artwork {artwork_url}: {e}")
        # Fallback to basic sprite
        try:
            from PIL import Image
            print(f"⚠️ Falling back to basic sprite: {url}")
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            img_data = BytesIO(response.content)
            img = Image.open(img_data)
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            img.save(cache_file, 'PNG')
            return ImageReader(cache_file)
        except Exception as fallback_error:
            print(f"Error in fallback for {url}: {fallback_error}")
            return None

def get_generation(pokemon_id):
    """Get generation info from Pokemon ID"""
    if pokemon_id <= 151:
        return 'Gen I - Kanto'
    elif pokemon_id <= 251:
        return 'Gen II - Johto'
    elif pokemon_id <= 386:
        return 'Gen III - Hoenn'
    elif pokemon_id <= 493:
        return 'Gen IV - Sinnoh'
    elif pokemon_id <= 649:
        return 'Gen V - Unova'
    elif pokemon_id <= 721:
        return 'Gen VI - Kalos'
    elif pokemon_id <= 809:
        return 'Gen VII - Alola'
    elif pokemon_id <= 905:
        return 'Gen VIII - Galar'
    else:
        return 'Gen IX - Paldea'

def draw_pokemon_card(c, pokemon, image, x, y, card_width, card_height):
    """Draw a single Pokemon card"""
    # Card background
    c.setFillColor(HexColor('#ffffff'))
    c.rect(x, y, card_width, card_height, fill=1)
    
    # Card border (like real Pokemon cards) - rounded corners
    c.setStrokeColor(HexColor('#2c3e50'))
    c.setLineWidth(2)
    c.rect(x, y, card_width, card_height, fill=0, stroke=1)
    
    # Header with Pokemon color as background
    pokemon_color = POKEMON_COLORS.get(pokemon['color'], '#f8f9fa')
    c.setFillColor(HexColor(pokemon_color))
    c.rect(x + 1, y + card_height - 36, card_width - 2, 35, fill=1, stroke=0)
    
    # Pokemon name (left side) - white text with black outline
    c.setFont("Helvetica-Bold", 12)
    name_text = pokemon['name'].upper()
    
    # Draw text outline (black)
    c.setFillColor(HexColor('#000000'))
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx != 0 or dy != 0:
                c.drawString(x + 8 + dx, y + card_height - 20 + dy, name_text)
    
    # Draw main text (white)
    c.setFillColor(HexColor('#ffffff'))
    c.drawString(x + 8, y + card_height - 20, name_text)
    
    # Pokemon number (right side, same line) - white with outline
    num_text = f"#{pokemon['id']:03d}"
    num_width = c.stringWidth(num_text, "Helvetica-Bold", 12)
    
    # Draw number outline (black)
    c.setFillColor(HexColor('#000000'))
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx != 0 or dy != 0:
                c.drawString(x + card_width - num_width - 8 + dx, y + card_height - 20 + dy, num_text)
    
    # Draw main number (white)
    c.setFillColor(HexColor('#ffffff'))
    c.drawString(x + card_width - num_width - 8, y + card_height - 20, num_text)
    
    # Generation info (centered below name) - white with outline - UPPERCASE
    c.setFont("Helvetica", 9)
    gen_text = get_generation(pokemon['id']).upper()
    gen_width = c.stringWidth(gen_text, "Helvetica", 9)
    
    # Draw generation outline (black)
    c.setFillColor(HexColor('#000000'))
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx != 0 or dy != 0:
                c.drawString(x + (card_width - gen_width) // 2 + dx, y + card_height - 32 + dy, gen_text)
    
    # Draw main generation (white)
    c.setFillColor(HexColor('#ffffff'))
    c.drawString(x + (card_width - gen_width) // 2, y + card_height - 32, gen_text)
    
    # LEFT SIDE: Pokemon image
    img_size = 80
    img_x = x + 15
    img_y = y + card_height - 135  # Adjusted for taller card
    
    if image:
        try:
            # Draw image with transparency (no border)
            c.drawImage(image, img_x, img_y, width=img_size, height=img_size, mask='auto')
        except:
            pass
    
    # Description text directly below image (no box) - FULL WIDTH AND UPPERCASE
    desc_y = img_y - 20  # Moved down from -15 to -20 (-5px)
    description = pokemon.get('description_catalan', pokemon.get('description', 'Descripció no disponible.')).upper()  # UPPERCASE
    c.setFillColor(HexColor('#2c3e50'))
    c.setFont("Helvetica", 8)  # Slightly bigger font
    
    # Wrap text to fit in FULL CARD WIDTH
    max_width = card_width - 20  # Full width minus margins
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
    if current_line:
        lines.append(current_line)
    
    # Draw description lines - FULL WIDTH
    text_y = desc_y
    for line in lines[:4]:  # Max 4 lines
        c.drawString(x + 10, text_y, line)  # Start from left margin
        text_y -= 10
    
    # RIGHT SIDE: All Pokemon info
    right_x = x + 110  # Start right column after image
    
    # Types section (moved down to avoid overlap with header)
    types_y = y + card_height - 65  # Moved from -50 to -65
    for i, ptype in enumerate(pokemon['types']):
        type_y = types_y - (i * 22)
        type_color = TYPE_COLORS.get(ptype, '#95a5a6')
        type_icon_file = TYPE_ICONS.get(ptype, 'unknown.png')
        
        # Try to use emoji image, fallback to symbol
        emoji_path = f'../emoji_icons/{type_icon_file}'
        if not os.path.exists(emoji_path):
            emoji_path = f'emoji_icons/{type_icon_file}'
        
        if os.path.exists(emoji_path):
            try:
                # Draw emoji image with transparency support (no badge background)
                c.drawImage(emoji_path, right_x + 3, type_y + 1, width=16, height=16, mask='auto')
                # Type text without symbol - TRANSLATED AND UPPERCASE
                c.setFillColor(HexColor('#000000'))  # Black text for better contrast
                c.setFont("Helvetica-Bold", 8)
                type_translated = TYPE_TRANSLATIONS.get(ptype, ptype.upper())
                c.drawString(right_x + 22, type_y + 5, type_translated)
            except Exception as e:
                # Fallback to symbol with badge if image fails
                c.setFillColor(HexColor(type_color))
                c.roundRect(right_x, type_y, 70, 18, 9, fill=1)
                type_icon_fallback = TYPE_ICONS_FALLBACK.get(ptype, '❓')
                c.setFillColor(HexColor('#ffffff'))
                c.setFont("Helvetica-Bold", 8)
                type_translated = TYPE_TRANSLATIONS.get(ptype, ptype.upper())
                type_text = f"{type_icon_fallback} {type_translated}"
                c.drawString(right_x + 5, type_y + 5, type_text)
        else:
            # Fallback to symbol with badge if no image
            c.setFillColor(HexColor(type_color))
            c.roundRect(right_x, type_y, 70, 18, 9, fill=1)
            type_icon_fallback = TYPE_ICONS_FALLBACK.get(ptype, '❓')
            c.setFillColor(HexColor('#ffffff'))
            c.setFont("Helvetica-Bold", 8)
            type_translated = TYPE_TRANSLATIONS.get(ptype, ptype.upper())
            type_text = f"{type_icon_fallback} {type_translated}"
            c.drawString(right_x + 5, type_y + 5, type_text)
    
    # Special status badges (legendary/mythical)
    special_y = types_y - (len(pokemon['types']) * 22)
    
    if pokemon.get('is_legendary', False):
        # Legendary badge with emoji icon
        legendary_icon = os.path.join(os.path.dirname(__file__), '..', 'emoji_icons', 'legendary.png')
        if os.path.exists(legendary_icon):
            c.drawImage(legendary_icon, right_x + 3, special_y + 1, width=16, height=16, mask='auto')
            c.setFillColor(HexColor('#000000'))  # Black text
            c.setFont("Helvetica-Bold", 8)
            c.drawString(right_x + 22, special_y + 5, "LLEGENDARI")
        else:
            # Fallback with badge
            c.setFillColor(HexColor('#B8860B'))
            c.roundRect(right_x, special_y, 70, 18, 9, fill=1)
            c.setFillColor(HexColor('#ffffff'))
            c.setFont("Helvetica-Bold", 8)
            c.drawString(right_x + 5, special_y + 5, "⭐ LLEGENDARI")
        special_y -= 22
    
    if pokemon.get('is_mythical', False):
        # Mythical badge with emoji icon
        mythical_icon = os.path.join(os.path.dirname(__file__), '..', 'emoji_icons', 'mythical.png')
        if os.path.exists(mythical_icon):
            c.drawImage(mythical_icon, right_x + 3, special_y + 1, width=16, height=16, mask='auto')
            c.setFillColor(HexColor('#000000'))  # Black text
            c.setFont("Helvetica-Bold", 8)
            c.drawString(right_x + 22, special_y + 5, "MÍTIC")
        else:
            # Fallback with badge
            c.setFillColor(HexColor('#C0C0C0'))
            c.roundRect(right_x, special_y, 70, 18, 9, fill=1)
            c.setFillColor(HexColor('#000000'))
            c.setFont("Helvetica-Bold", 8)
            c.drawString(right_x + 5, special_y + 5, "✨ MÍTIC")
    
    # Remove special badges section - more space for description
    
    # Remove color section - now color is in header
    # Color info now shown in header background
    
    # Evolution chain at the bottom (no title, more space)
    if pokemon.get('evolution'):
        evo_chain = pokemon['evolution']
        
        # Evolution section - positioned at the very bottom of the card
        evo_y = y + 15  # Moved up from y + 5 to y + 15 (+10px)
        
        # Two-row layout for long chains (>6 evolutions)
        if len(evo_chain) > 6:
            # Split into two rows
            mid_point = (len(evo_chain) + 1) // 2
            first_row = evo_chain[:mid_point]
            second_row = evo_chain[mid_point:]
            
            spacing = 35
            img_size = 20
            font_size = 4
            row_height = 31  # Increased from 30 to 31 (+1px between rows)
            
            # Draw first row
            total_width = len(first_row) * spacing - 5
            start_x = x + (card_width - total_width) // 2
            evo_x = start_x
            
            for i, evo_pokemon in enumerate(first_row):
                if i > 0:
                    c.setFillColor(HexColor('#7f8c8d'))
                    c.setFont("Helvetica", 6)
                    c.drawString(evo_x - 8, evo_y + row_height + 8, "→")
                
                try:
                    evo_image = download_image(evo_pokemon['image_url'])
                    if evo_image:
                        c.drawImage(evo_image, evo_x, evo_y + row_height, width=img_size, height=img_size, mask='auto')
                        
                        name = evo_pokemon['name'].upper()
                        c.setFont("Helvetica", font_size)
                        c.setFillColor(HexColor('#2c3e50'))
                        name_width = c.stringWidth(name, "Helvetica", font_size)
                        name_x = evo_x + (img_size - name_width) // 2
                        c.drawString(name_x, evo_y + row_height - 7, name)  # Separated 1px more (-7 instead of -6)
                        
                        if evo_pokemon['id'] == pokemon['id']:
                            c.setStrokeColor(HexColor('#e74c3c'))
                            c.setLineWidth(2)
                            c.roundRect(evo_x - 1, evo_y + row_height - 1, img_size + 2, img_size + 2, 3)
                            c.setStrokeColor(HexColor('#2c3e50'))
                            c.setLineWidth(1)
                except:
                    pass
                
                evo_x += spacing
            
            # Draw second row
            total_width = len(second_row) * spacing - 5
            start_x = x + (card_width - total_width) // 2
            evo_x = start_x
            
            for i, evo_pokemon in enumerate(second_row):
                if i > 0:
                    c.setFillColor(HexColor('#7f8c8d'))
                    c.setFont("Helvetica", 6)
                    c.drawString(evo_x - 8, evo_y + 8, "→")
                
                try:
                    evo_image = download_image(evo_pokemon['image_url'])
                    if evo_image:
                        c.drawImage(evo_image, evo_x, evo_y, width=img_size, height=img_size, mask='auto')
                        
                        name = evo_pokemon['name'].upper()
                        c.setFont("Helvetica", font_size)
                        c.setFillColor(HexColor('#2c3e50'))
                        name_width = c.stringWidth(name, "Helvetica", font_size)
                        name_x = evo_x + (img_size - name_width) // 2
                        c.drawString(name_x, evo_y - 7, name)  # Separated 1px more (-7 instead of -6)
                        
                        if evo_pokemon['id'] == pokemon['id']:
                            c.setStrokeColor(HexColor('#e74c3c'))
                            c.setLineWidth(2)
                            c.roundRect(evo_x - 1, evo_y - 1, img_size + 2, img_size + 2, 3)
                            c.setStrokeColor(HexColor('#2c3e50'))
                            c.setLineWidth(1)
                except:
                    pass
                
                evo_x += spacing
        
        else:
            # Single row layout for shorter chains
            # Adaptive spacing based on number of evolutions
            if len(evo_chain) <= 3:
                spacing = 40
                img_size = 22
                font_size = 5
            elif len(evo_chain) <= 5:
                spacing = 32
                img_size = 20
                font_size = 4
            else:
                spacing = 28
                img_size = 18
                font_size = 4
            
            total_width = len(evo_chain) * spacing - 5
            start_x = x + (card_width - total_width) // 2
            evo_x = start_x
            
            for i, evo_pokemon in enumerate(evo_chain):
                if i > 0:
                    c.setFillColor(HexColor('#7f8c8d'))
                    c.setFont("Helvetica", 6)
                    c.drawString(evo_x - 8, evo_y + 8, "→")
                
                try:
                    evo_image = download_image(evo_pokemon['image_url'])
                    if evo_image:
                        c.drawImage(evo_image, evo_x, evo_y, width=img_size, height=img_size, mask='auto')
                        
                        name = evo_pokemon['name'].upper()
                        c.setFont("Helvetica", font_size)
                        c.setFillColor(HexColor('#2c3e50'))
                        name_width = c.stringWidth(name, "Helvetica", font_size)
                        name_x = evo_x + (img_size - name_width) // 2
                        c.drawString(name_x, evo_y - 7, name)  # Separated 1px more (-7 instead of -6)
                        
                        if evo_pokemon['id'] == pokemon['id']:
                            c.setStrokeColor(HexColor('#e74c3c'))
                            c.setLineWidth(2)
                            c.roundRect(evo_x - 1, evo_y - 1, img_size + 2, img_size + 2, 3)
                            c.setStrokeColor(HexColor('#2c3e50'))
                            c.setLineWidth(1)
                except:
                    pass
                
                evo_x += spacing
    
    # Stats section with stars (below evolution) - IN CATALAN
    # Statistics section removed to give more space for description

def generate_pdf():
    """Generate Pokemon PDFs for all generations"""
    print("Starting PDF generation for all Pokemon...")
    
    # Get total Pokemon count from API
    try:
        response = requests.get('https://pokeapi.co/api/v2/pokemon-species/?limit=1')
        total_count = response.json()['count']
        print(f"Total Pokemon available: {total_count}")
    except:
        total_count = 1025  # Fallback to known count
    
    # For now, start with first 151 (Generation 1)
    print("\\nProcessing Generation I - Kanto (1-151)...")
    gen1_pokemon = []
    for i in range(1, 152):
        print(f"Processing Pokemon #{i}...")
        pokemon = fetch_pokemon(i)
        if pokemon:
            gen1_pokemon.append(pokemon)
    
    if gen1_pokemon:
        print("Generating Generation 1 PDFs...")
        
        # Gen 1 by ID
        generate_pokemon_pdf(gen1_pokemon, "./pdf/gen1_kanto_by_id.pdf", "Generació I - Kanto")
        
        # Gen 1 by color
        gen1_by_color = sorted(gen1_pokemon, key=lambda p: (p['color'], p['id']))
        generate_pokemon_pdf(gen1_by_color, "./pdf/gen1_kanto_by_color.pdf", "Generació I - Kanto (per color)")
        
        print("Generation 1 PDFs generated successfully!")
    
    # TODO: Expand to more generations after translations are complete
    print(f"\\nReady to expand to all {total_count} Pokemon once translations are complete!")

def generate_pokemon_pdf(pokemon_list, filename, subtitle="151 Pokémon"):
    """Generate PDF with given Pokemon list"""
    # Create PDF directory if it doesn't exist
    os.makedirs('pdf', exist_ok=True)
    
    # Create PDF
    c = canvas.Canvas(filename, pagesize=landscape(A4))
    page_width, page_height = landscape(A4)
    
    # Card dimensions - increased height for better use of space
    card_width = 190  # Restored to original width
    card_height = 260  # Set to 260px as requested
    cards_per_row = 4
    cards_per_col = 2
    cards_per_page = cards_per_row * cards_per_col
    
    margin_x = 15
    margin_y = 40
    spacing_x = 10
    spacing_y = 10  # Reduced from 15 to 10 to fit taller cards
    
    card_count = 0
    
    for pokemon in pokemon_list:
        image = download_image(pokemon['image_url'])
        
        # Calculate position
        if card_count > 0 and card_count % cards_per_page == 0:
            c.showPage()  # New page
        
        row = (card_count % cards_per_page) // cards_per_row
        col = (card_count % cards_per_page) % cards_per_row
        
        x = margin_x + col * (card_width + spacing_x)
        y = page_height - margin_y - (row + 1) * (card_height + spacing_y)
        
        draw_pokemon_card(c, pokemon, image, x, y, card_width, card_height)
        card_count += 1
    
    c.save()

if __name__ == "__main__":
    generate_pdf()
