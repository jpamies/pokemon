# Estructura de Dades - Guia Pokémon per a Nens

## API GraphQL Pokémon

**Endpoint**: https://graphql.pokeapi.co/v1beta2

## Estructura de Dades Pokémon

### Consulta GraphQL Bàsica
```graphql
query GetPokemon($id: Int!) {
  pokemon(where: {id: {_eq: $id}}) {
    id
    name
    height
    weight
    pokemon_species {
      pokemon_species_names(where: {language_id: {_eq: 6}}) {
        name
      }
    }
    pokemon_types {
      type {
        name
        type_names(where: {language_id: {_eq: 6}}) {
          name
        }
      }
    }
    pokemon_sprites {
      sprites
    }
  }
}
```

### Mapeig d'Idiomes
- Català: language_id = 6
- Espanyol: language_id = 7
- Anglès: language_id = 9

### Estructura de Dades Local
```javascript
const pokemonData = {
  id: number,
  name: {
    ca: string,
    es: string,
    en: string
  },
  image: string,
  height: number, // en decímetres
  weight: number, // en hectograms
  types: [
    {
      ca: string,
      es: string,
      en: string
    }
  ]
}
```

### Cache Local
- Emmagatzemar dades en localStorage per ús offline
- Comprimir imatges per optimitzar l'emmagatzematge
- Implementar sistema de fallback per connexions lentes
