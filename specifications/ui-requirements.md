# Requisits UI/UX - Guia Pokémon per a Nens

## Principis de Disseny per a Nens

### Accessibilitat
- **Text en majúscules per defecte** per facilitar la lectura
- Botó per alternar entre majúscules/minúscules
- Contrast alt entre text i fons
- Mida de font gran (mínim 18px)
- Botons grans i fàcils de prémer (mínim 44px)

### Colors i Estil
- Colors brillants i atractius
- Esquema de colors amigable per a nens
- Icones grans i clares
- Animacions suaus i no distragents

### Navegació
- Interfície simple i intuïtiva
- Botons de navegació grans: "ANTERIOR" i "SEGÜENT"
- Indicador visual de la posició actual (ex: "3 de 151")
- Botó "INICI" per tornar al primer Pokémon

### Layout Responsiu
- Disseny que funcioni en tablets i mòbils
- Orientació vertical optimitzada
- Elements centrats i ben espaciats

### Funcions d'Impressió
- CSS específic per impressió
- Layout optimitzat per pàgina A4
- Informació essencial visible en paper
- Imatges en escala de grisos per estalviar tinta

### Multiidioma
- Selector d'idioma visible i accessible
- Banderes o icones per identificar idiomes
- Canvi d'idioma instantani sense recarregar

### Estructura de Pàgina
```
[SELECTOR IDIOMA] [BOTÓ ACCESSIBILITAT]
        [IMATGE POKÉMON GRAN]
           [NOM POKÉMON]
        [TIPUS 1] [TIPUS 2]
      [ALÇADA] [PES] [NÚMERO]
    [ANTERIOR] [INICI] [SEGÜENT]
```

### Estats de Càrrega
- Indicador de càrrega visual
- Missatges d'error amigables per a nens
- Fallback per imatges que no carreguen
