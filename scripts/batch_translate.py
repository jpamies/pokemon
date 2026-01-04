#!/usr/bin/env python3
"""
Script to update cache with Kiro's translations and generate all PDFs
"""

import json
import os
from generate_pdf import fetch_pokemon

def update_translations_batch(translations_dict):
    """Update cache with a batch of translations"""
    cache_dir = '../cache/data'
    updated = 0
    
    for pokemon_id, catalan_desc in translations_dict.items():
        cache_file = os.path.join(cache_dir, f'pokemon_{pokemon_id}.json')
        
        if os.path.exists(cache_file):
            with open(cache_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            data['description_catalan'] = catalan_desc
            
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            updated += 1
    
    return updated

def generate_generation_pdfs(start_id, end_id, gen_name):
    """Generate PDFs for a specific generation"""
    print(f"Generating PDFs for {gen_name} (#{start_id}-#{end_id})...")
    
    pokemon_list = []
    for i in range(start_id, end_id + 1):
        pokemon = fetch_pokemon(i)
        if pokemon:
            pokemon_list.append(pokemon)
    
    if pokemon_list:
        from generate_pdf import generate_pokemon_pdf
        
        # Generate by ID
        gen_num = gen_name.split()[1].lower()
        region = gen_name.split()[-1].lower()
        
        filename_id = f"pdf/{gen_num}_{region}_by_id.pdf"
        generate_pokemon_pdf(pokemon_list, filename_id, f"{gen_name} - Ordenats per ID")
        
        # Generate by color
        filename_color = f"pdf/{gen_num}_{region}_by_color.pdf"
        pokemon_by_color = sorted(pokemon_list, key=lambda p: (p.get('color', 'unknown'), p['id']))
        generate_pokemon_pdf(pokemon_by_color, filename_color, f"{gen_name} - Ordenats per Color")
        
        print(f"Generated {gen_name} PDFs!")
        return True
    
    return False

if __name__ == "__main__":
    print("Translation and PDF generation script ready!")
    print("Use update_translations_batch(translations_dict) to add translations")
    print("Use generate_generation_pdfs(start, end, name) to generate PDFs")
