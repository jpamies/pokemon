# 📺 Pokémon Anime Tracker

Sistema de seguimiento de episodios de la serie animada de Pokémon.

## 📊 Estructura de Datos

Cada episodio contiene:
- **ID**: Número de episodio
- **Región/Generación**: Kanto, Johto, Hoenn, etc.
- **Título ES**: Título en español
- **Título EN**: Título en inglés
- **Título CA**: Título en catalán (futuro)
- **Sinopsis**: Breve descripción del episodio
- **Pokémon**: Lista de Pokémon que aparecen
- **Plataforma**: Dónde ver el episodio (Netflix, Prime Video, etc.)
- **Temporada**: Número de temporada
- **Número en temporada**: Número del episodio dentro de la temporada

## 📁 Estructura del Proyecto

```
anime/
├── data/              # Datos de episodios en JSON
├── docs/              # Documentación y web de tracking
├── scripts/           # Scripts para gestión de datos
└── README.md          # Esta documentación
```

## 🚀 Próximos Pasos

1. Definir esquema JSON para episodios
2. Crear script para añadir episodios
3. Crear interfaz web para visualizar tracking
4. Integrar con API de plataformas de streaming
