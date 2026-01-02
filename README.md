# Guia Pokémon per a Nens

Una aplicació web estàtica per ajudar els nens a aprendre sobre Pokémon amb suport multiidioma i funcions d'accessibilitat.

## Característiques

- 🌍 **Multiidioma**: Català (per defecte), Espanyol i Anglès
- 🔤 **Accessibilitat**: Lletres majúscules per defecte per facilitar la lectura als nens
- 📱 **Estàtic**: Funciona sense connexió i es pot imprimir
- 🖼️ **Imatges**: Inclou imatges de tots els Pokémon
- 🎮 **Fàcil d'usar**: Interfície dissenyada especialment per a nens

## API

Utilitza l'API GraphQL de Pokémon: https://graphql.pokeapi.co/v1beta2

## Estructura del Projecte

```
pokemon-guide-kids/
├── README.md
├── index.html
├── css/
│   └── styles.css
├── js/
│   ├── app.js
│   └── i18n.js
├── assets/
│   └── images/
├── specifications/
│   ├── data-structure.md
│   ├── ui-requirements.md
│   └── api-integration.md
└── translations/
    ├── ca.json
    ├── es.json
    └── en.json
```

## Instal·lació

1. Clona el repositori
2. Obre `index.html` en un navegador web
3. L'aplicació funciona completament sense connexió després de la primera càrrega

## Ús

- Selecciona l'idioma al menú superior
- Utilitza el botó d'accessibilitat per canviar entre majúscules i minúscules
- Navega pels Pokémon utilitzant els controls de navegació
- Imprimeix les pàgines per utilitzar-les sense connexió

## Contribuir

1. Fork el projecte
2. Crea una branca per a la teva funcionalitat
3. Fes commit dels teus canvis
4. Push a la branca
5. Obre un Pull Request

## Llicència

Aquest projecte està sota llicència MIT.