# Integració API - Guia Pokémon per a Nens

## GraphQL API Pokémon

**Endpoint**: https://graphql.pokeapi.co/v1beta2

## Estratègia d'Integració

### 1. Consultes GraphQL

#### Obtenir un Pokémon específic
```graphql
query GetPokemon($id: Int!) {
  pokemon_v2_pokemon(where: {id: {_eq: $id}}) {
    id
    name
    height
    weight
    pokemon_v2_pokemonspecies {
      pokemon_v2_pokemonspeciesnames(where: {language_id: {_in: [6, 7, 9]}}) {
        name
        language_id
      }
    }
    pokemon_v2_pokemontypes {
      pokemon_v2_type {
        pokemon_v2_typenames(where: {language_id: {_in: [6, 7, 9]}}) {
          name
          language_id
        }
      }
    }
    pokemon_v2_pokemonsprites {
      sprites
    }
  }
}
```

#### Obtenir llista de Pokémon (per navegació)
```graphql
query GetPokemonList($limit: Int!, $offset: Int!) {
  pokemon_v2_pokemon(limit: $limit, offset: $offset, order_by: {id: asc}) {
    id
    name
  }
}
```

### 2. Gestió d'Errors

- Timeout de 10 segons per consulta
- Retry automàtic (màxim 3 intents)
- Fallback a dades cached
- Missatges d'error amigables per a nens

### 3. Cache i Offline

#### LocalStorage
```javascript
const cacheKey = `pokemon_${id}_${language}`;
localStorage.setItem(cacheKey, JSON.stringify(pokemonData));
```

#### Service Worker (opcional)
- Cache d'imatges per ús offline
- Cache de consultes API més freqüents

### 4. Optimització d'Imatges

- Utilitzar sprites oficials de l'API
- Fallback a imatges alternatives si no carreguen
- Lazy loading per imatges fora de pantalla
- Compressió per cache local

### 5. Límits i Rendiment

- Màxim 151 Pokémon (primera generació)
- Precarregar 3 Pokémon adjacents
- Debounce per navegació ràpida
- Indicadors de càrrega visuals

### 6. Implementació JavaScript

```javascript
class PokemonAPI {
  constructor() {
    this.endpoint = 'https://graphql.pokeapi.co/v1beta2';
    this.cache = new Map();
  }

  async fetchPokemon(id, language = 'ca') {
    // Implementació amb cache i error handling
  }

  getCachedPokemon(id, language) {
    // Recuperar de localStorage
  }

  cachePokemon(id, language, data) {
    // Guardar a localStorage
  }
}
```
