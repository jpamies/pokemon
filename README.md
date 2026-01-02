# Guia Pokémon per a Nens

Una aplicació web estàtica per ajudar els nens a aprendre sobre Pokémon amb suport multiidioma i funcions d'accessibilitat.

## Característiques

- 🌍 **Multiidioma**: Català (per defecte), Espanyol i Anglès
- 🔤 **Accessibilitat**: Lletres majúscules per defecte per facilitar la lectura als nens
- 📱 **Estàtic**: Funciona sense connexió i es pot imprimir
- 🖼️ **Imatges**: Inclou imatges de tots els Pokémon
- 🎮 **Fàcil d'usar**: Interfície dissenyada especialment per a nens
- ⌨️ **Navegació per teclat**: Suport per fletxes i tecla Inici
- 💾 **Emmagatzematge local**: Guarda preferències i cache de dades
- 🔄 **Gestió d'errors**: Sistema de retry automàtic

## API

Utilitza l'API GraphQL de Pokémon: https://graphql.pokeapi.co/v1beta2

## Implementació Tècnica

### Arquitectura
- **Frontend**: HTML5, CSS3, JavaScript ES6+ (Vanilla)
- **API**: GraphQL amb cache local
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
  // Integració GraphQL API
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

### Consultes GraphQL

#### Obtenir Pokémon
```graphql
query GetPokemon($id: Int!) {
  pokemon(where: {id: {_eq: $id}}) {
    id name height weight
    pokemon_species {
      pokemon_species_names(where: {language_id: {_in: [6, 7, 9]}}) {
        name language_id
      }
    }
    pokemon_types {
      type {
        name
        type_names(where: {language_id: {_in: [6, 7, 9]}}) {
          name language_id
        }
      }
    }
    pokemon_sprites { sprites }
  }
}
```

### Mapeig d'Idiomes
- Català: `language_id = 6`
- Espanyol: `language_id = 7` 
- Anglès: `language_id = 9`

### Funcionalitats Clau

#### Accessibilitat
- Text en majúscules per defecte (toggleable)
- Alt text per totes les imatges
- Navegació per teclat completa
- Contrast alt de colors
- Botons amb mida mínima accessible

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