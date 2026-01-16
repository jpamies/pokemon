# 📺 Pokémon Anime Tracker

Sistema de seguimiento de episodios de la serie animada de Pokémon.

## 📝 Estructura con Markdown

Cada episodio se documenta en un archivo Markdown individual:

```
anime/episodes/
├── kanto/
│   ├── 001.md
│   ├── 002.md
│   └── ...
├── johto/
├── hoenn/
└── ...
```

### Crear un Nuevo Episodio

1. Copia el template: `cp anime/episodes/TEMPLATE.md anime/episodes/kanto/002.md`
2. Edita el archivo con la información del episodio
3. Convierte a JSON: `python3 anime/scripts/md_to_json.py`

## 📊 Estructura de Datos

Cada episodio contiene:
- **Información Básica**: Región, generación, temporada, fecha
- **Títulos**: Español, inglés, japonés, catalán
- **Sinopsis**: Descripción del episodio
- **Pokémon**: Principales, secundarios y cameos
- **Plataformas**: Dónde ver el episodio
- **Momentos Destacados**: Eventos importantes
- **Notas y Curiosidades**: Información adicional

## 📁 Estructura del Proyecto

```
anime/
├── episodes/          # Episodios en Markdown por región
│   ├── TEMPLATE.md   # Template para nuevos episodios
│   ├── kanto/
│   ├── johto/
│   └── ...
├── data/              # Datos generados en JSON
│   ├── episodes.json
│   └── episode_schema.json
├── docs/              # Interfaz web
│   └── index.html
├── scripts/           # Scripts de gestión
│   ├── md_to_json.py # Convertir MD → JSON
│   └── add_episode.py
└── README.md
```

## 🚀 Workflow

1. **Editar Markdown** - Fácil de escribir y versionar
2. **Convertir a JSON** - `python3 anime/scripts/md_to_json.py`
3. **Visualizar en Web** - Abrir `anime/docs/index.html`

## 📖 Ejemplo

Ver `anime/episodes/kanto/001.md` para un ejemplo completo del primer episodio.

