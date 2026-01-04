#!/usr/bin/env python3
import sys
sys.path.append('scripts')
from generate_pdf import fetch_pokemon, generate_pokemon_pdf

# Test with first 5 Pokemon
pokemon_list = []
for i in range(1, 6):
    pokemon = fetch_pokemon(i)
    pokemon_list.append(pokemon)
    print(f"#{i} {pokemon['name']}: {pokemon['description_catalan'][:50]}...")

# Generate test PDF
generate_pokemon_pdf(pokemon_list, "test_pokemon.pdf", "Test 5 Pokémon")
print("Test PDF generated: test_pokemon.pdf")
