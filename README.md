# Guia Pokémon per a Nens

Una aplicació web estàtica per ajudar els nens a aprendre sobre Pokémon amb suport multiidioma i funcions d'accessibilitat.

## Característiques

- 🌍 **Multiidioma**: Català (per defecte), Espanyol i Anglès
- 🔤 **Accessibilitat**: Lletres majúscules per defecte per facilitar la lectura als nens
- 📱 **Estàtic**: Funciona sense connexió i es pot imprimir
- 🖼️ **Imatges grans**: Imatges de 200x200px amb millor visualització
- 🎮 **Fàcil d'usar**: Interfície dissenyada especialment per a nens
- ⌨️ **Navegació per teclat**: Suport per fletxes i tecla Inici
- 💾 **Emmagatzematge local**: Guarda preferències i cache de dades
- 🔄 **Gestió d'errors**: Sistema de retry automàtic
- 🎯 **Icones de tipus**: Emojis visuals per cada tipus de Pokémon
- 🎲 **Informació de generació**: Mostra la generació i regió de cada Pokémon
- 📊 **Modo avançat**: Vista tipus carta amb estadístiques i habilitats
- 🔄 **Cadena d'evolució**: Navegació clickeable entre evolucions
- 📋 **Llistat complet**: Vista de tots els 151 Pokémon amb navegació directa
- 📖 **Descripcions**: Textos descriptius dels Pokémon en múltiples idiomes
- 🎨 **Informació visual**: Color principal i hàbitat de cada Pokémon
- 👑 **Pokémon especials**: Identificació de legendaris i mítics

## API

Utilitza l'API REST de Pokémon: https://pokeapi.co/api/v2

## Implementació Tècnica

### Arquitectura
- **Frontend**: HTML5, CSS3, JavaScript ES6+ (Vanilla)
- **API**: REST amb cache local
- **Emmagatzematge**: localStorage per preferències i cache
- **Internacionalització**: Sistema i18n personalitzat
- **Accessibilitat**: WCAG 2.1 compliant

### Components Principals

#### 1. Sistema d'Internacionalització (`js/i18n.js`)
```javascript
class I18n {
  // Gestiona traduccions en 3 idiomes
  // Català com idioma per defecte
  // Actualització dinàmica de la UI
}
```

#### 2. Aplicació Principal (`js/app.js`)
```javascript
class PokemonGuide {
  // Integració REST API
  // Navegació entre Pokémon (1-151)
  // Cache intel·ligent
  // Gestió d'estat i preferències
}
```

#### 3. Estils Responsius (`css/styles.css`)
- Disseny kid-friendly amb colors brillants
- Botons grans (mínim 44px) per accessibilitat
- Text gran (mínim 18px) per facilitar lectura
- Animacions suaus i no distragents

#### 4. Estils d'Impressió (`css/print.css`)
- Optimitzat per pàgina A4
- Escala de grisos per estalviar tinta
- Layout simplificat per paper

### Consultes REST API

#### Obtenir Pokémon
```javascript
// Obtenir dades del Pokémon
const pokemonResponse = await fetch(`https://pokeapi.co/api/v2/pokemon/${id}`);
const pokemonData = await pokemonResponse.json();

// Obtenir noms en diferents idiomes
const speciesResponse = await fetch(pokemonData.species.url);
const speciesData = await speciesResponse.json();
```

### Estructura de Resposta REST

#### Pokémon Data
```json
{
  "id": 1,
  "name": "bulbasaur",
  "height": 7,
  "weight": 69,
  "sprites": {
    "front_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/1.png"
  },
  "types": [
    {
      "type": {
        "name": "grass",
        "url": "https://pokeapi.co/api/v2/type/12/"
      }
    }
  ],
  "species": {
    "url": "https://pokeapi.co/api/v2/pokemon-species/1/"
  }
}
```

#### Species Data (per noms multiidioma)
```json
{
  "names": [
    {
      "language": {
        "name": "en"
      },
      "name": "Bulbasaur"
    },
    {
      "language": {
        "name": "es"
      },
      "name": "Bulbasaur"
    }
  ]
}
```

### Mapeig d'Idiomes
- Català: `language.name = "ca"` (no disponible a l'API, utilitzem anglès com fallback)
- Espanyol: `language.name = "es"` 
- Anglès: `language.name = "en"`

### Funcionalitats Clau

### Funcionalitats Clau

#### Accessibilitat
- Text en majúscules per defecte (toggleable)
- Alt text per totes les imatges
- Navegació per teclat completa
- Contrast alt de colors
- Botons amb mida mínima accessible

#### Modo Avançat
- **Vista carta**: Layout tipus carta de Pokémon professional
- **Estadístiques base**: Barres visuals per HP, ATK, DEF, SP.ATK, SP.DEF, SPD
- **Habilitats**: Mostra habilitats normals i ocultes amb traduccions
- **Toggle dinàmic**: Botó 📋/📊 per canviar entre modes
- **Responsive**: S'adapta a mòbils i tauletes

#### Cadena d'Evolució
- **Navegació visual**: Imatges clickeables de tota la cadena evolutiva
- **Posició actual**: Destacat visual del Pokémon actual
- **Nivells d'evolució**: Mostra els nivells necessaris per evolucionar
- **Navegació directa**: Click per canviar a qualsevol evolució

#### Llistat Complet
- **Vista grid**: Tots els 151 Pokémon en format quadrícula
- **Informació bàsica**: ID, imatge i nom de cada Pokémon
- **Navegació directa**: Click per anar directament a qualsevol Pokémon
- **Noms reals**: Carrega els noms oficials en l'idioma seleccionat

#### Informació Descriptiva
- **Descripcions**: Textos oficials dels jocs Pokémon
- **Color principal**: Color característic de cada Pokémon
- **Hàbitat**: Ecosistema on viu naturalment
- **Pokémon especials**: Badges per legendaris (👑) i mítics (✨)

#### Cache i Offline
- localStorage per preferències d'usuari
- Cache de dades Pokémon per rendiment
- Fallback per imatges no disponibles
- Funcionalitat offline després de primera càrrega

#### Navegació
- Botons Anterior/Següent amb validació
- Botó Inici per tornar al Pokémon #1
- Comptador visual (ex: "3 DE 151")
- Navegació per teclat (fletxes, Home)

#### Gestió d'Errors
- Retry automàtic per fallades de xarxa
- Missatges d'error amigables per nens
- Fallback a cache local quan sigui possible

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

## Historial de Versions

### v2.1.0 (Gener 2026)
- 🔄 **Cadena d'evolució**: Navegació clickeable entre evolucions
- 📋 **Llistat complet**: Vista de tots els 151 Pokémon amb navegació directa
- 📖 **Descripcions**: Textos descriptius dels Pokémon en múltiples idiomes
- 🎨 **Informació visual**: Color principal i hàbitat traduïts
- 👑 **Pokémon especials**: Badges per legendaris i mítics
- 🌍 **Habilitats traduïdes**: Noms d'habilitats en català, espanyol i anglès
- 🎯 **Generació amb regió**: "Gen I - Kanto" format millorat

### v2.0.0 (Gener 2026)
- ✨ **Modo Avançat**: Vista tipus carta amb estadístiques i habilitats
- 🖼️ **Imatges millorades**: Imatges més grans (200x200px) amb millor layout
- 🎲 **Informació de generació**: Mostra la generació de cada Pokémon
- 📊 **Estadístiques base**: Barres visuals per totes les stats
- 🎯 **Habilitats**: Mostra habilitats normals i ocultes
- 🎨 **Disseny responsive**: Millor adaptació a mòbils i tauletes

### v1.0.0 (Desembre 2025)
- 🌍 Suport multiidioma (Català, Espanyol, Anglès)
- 🔤 Mode d'accessibilitat amb majúscules
- 🎯 Icones de tipus amb emojis
- ⌨️ Navegació per teclat
- 💾 Cache local i preferències
- 🔄 Gestió d'errors amb retry automàtic

## Instal·lació i Execució

### Opció 1: Servidor Local (Recomanat)
```bash
# Clona el repositori
git clone <url-del-repositori>
cd pokeAPI

# Inicia un servidor local (tria una opció):

# Python 3
python -m http.server 8000

# Python 2
python -m SimpleHTTPServer 8000

# Node.js (si tens npx)
npx serve .

# PHP
php -S localhost:8000
```

Després obre: http://localhost:8000

### Opció 2: Extensions de Navegador
- **Chrome**: Inicia amb `--disable-web-security --user-data-dir=/tmp/chrome_dev`
- **Firefox**: Canvia `security.fileuri.strict_origin_policy` a `false` a `about:config`

### Opció 3: Live Server (VS Code)
1. Instal·la l'extensió "Live Server"
2. Clic dret a `index.html` → "Open with Live Server"

### ⚠️ Problema CORS
Si obres `index.html` directament des del sistema de fitxers (`file://`), obtindràs errors CORS quan l'aplicació intenti carregar les traduccions i fer crides a l'API. **Sempre utilitza un servidor local.**

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