# 🐾 Guía Pokémon para Niños

> **Sistema educativo completo con guías Pokémon multiidioma y PDFs descargables**

Una aplicación web estática diseñada específicamente para ayudar a los niños a aprender sobre Pokémon, con soporte completo en **catalán**, español e inglés, y funciones de accesibilidad adaptadas para el público infantil.

[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Live-brightgreen)](https://jpamies.github.io/pokemon/)
[![PDFs](https://img.shields.io/badge/PDFs-20%20archivos-blue)](https://jpamies.github.io/pokemon/docs/)
[![Pokémon](https://img.shields.io/badge/Pokémon-1025%20completos-red)](https://jpamies.github.io/pokemon/)

## 🎯 Acceso Rápido

### 🌐 **Aplicación Web**
- **[📱 Aplicación Interactiva](https://jpamies.github.io/pokemon/)** - Navega por todos los Pokémon online
- **[📚 Centro de Descargas](https://jpamies.github.io/pokemon/docs/)** - Todos los PDFs disponibles

### 📖 **Guías Completas** (Recomendado)
- **[📥 Guía Completa por ID](docs/pdf/pokemon_complet_catala.pdf)** - 1,025 Pokémon ordenados por número
- **[📥 Guía Completa por Color](docs/pdf/pokemon_complet_catala_by_color.pdf)** - 1,025 Pokémon ordenados por color

*Ambas versiones incluyen todos los Pokémon de las 9 generaciones con descripciones completas en catalán*

## 📚 PDFs por Generación

| Generación | Pokémon | Región | Descargas |
|------------|---------|--------|-----------|
| **Gen I** | #1-151 | Kanto | [Por ID](docs/pdf/gen1_kanto_by_id.pdf) • [Por Color](docs/pdf/gen1_kanto_by_color.pdf) |
| **Gen II** | #152-251 | Johto | [Por ID](docs/pdf/ii_johto_by_id.pdf) • [Por Color](docs/pdf/ii_johto_by_color.pdf) |
| **Gen III** | #252-386 | Hoenn | [Por ID](docs/pdf/iii_hoenn_by_id.pdf) • [Por Color](docs/pdf/iii_hoenn_by_color.pdf) |
| **Gen IV** | #387-493 | Sinnoh | [Por ID](docs/pdf/iv_sinnoh_by_id.pdf) • [Por Color](docs/pdf/iv_sinnoh_by_color.pdf) |
| **Gen V** | #494-649 | Unova | [Por ID](docs/pdf/v_unova_by_id.pdf) • [Por Color](docs/pdf/v_unova_by_color.pdf) |
| **Gen VI** | #650-721 | Kalos | [Por ID](docs/pdf/vi_kalos_by_id.pdf) • [Por Color](docs/pdf/vi_kalos_by_color.pdf) |
| **Gen VII** | #722-809 | Alola | [Por ID](docs/pdf/vii_alola_by_id.pdf) • [Por Color](docs/pdf/vii_alola_by_color.pdf) |
| **Gen VIII** | #810-905 | Galar | [Por ID](docs/pdf/viii_galar_by_id.pdf) • [Por Color](docs/pdf/viii_galar_by_color.pdf) |
| **Gen IX** | #906-1025 | Paldea | [Por ID](docs/pdf/ix_paldea_by_id.pdf) • [Por Color](docs/pdf/ix_paldea_by_color.pdf) |

## ✨ Características Principales

### 🎨 **PDFs Educativos**
- 🌍 **Completamente en catalán** - Traducciones especializadas para niños
- 🎯 **Formato de cartas horizontales** - Optimizado para impresión A4
- 🖼️ **Imágenes oficiales** - Artwork de alta calidad de cada Pokémon
- 📊 **Información completa** - Número, nombre, tipos, medidas y descripción
- 🎨 **Fondos de color** - Cada carta con el color representativo del Pokémon

### 📱 **Aplicación Web Interactiva**
- 🌍 **Multiidioma** - Catalán (por defecto), español e inglés
- 🔤 **Accesibilidad** - Modo mayúsculas para facilitar la lectura
- 📱 **Responsive** - Funciona en móviles, tablets y ordenadores
- ⌨️ **Navegación por teclado** - Soporte completo para accesibilidad
- 🎮 **Modos de vista** - Básico y avanzado con estadísticas
- 🔄 **Cadenas de evolución** - Navegación entre evoluciones
- 📋 **Lista completa** - Vista de todos los Pokémon

### 🚀 **Rendimiento y Tecnología**
- 💾 **Sistema de cache** - Carga rápida y uso eficiente de datos
- 🌐 **Funciona offline** - PDFs descargables para uso sin conexión
- 📊 **Optimizado** - Imágenes y datos optimizados para web
- 🔄 **Actualización automática** - Contenido siempre actualizado

## 🛠️ Uso para Desarrolladores

### Instalación Rápida
```bash
git clone https://github.com/jpamies/pokemon.git
cd pokemon
python -m http.server 8000
```

### Generación de PDFs
```bash
# Generar todos los PDFs
python main.py all

# Solo PDFs por generaciones
python main.py generations

# Solo PDFs completos
python main.py complete

# Regenerar cache
python main.py cache
```

### Estructura del Proyecto
```
pokemon/
├── 📱 Aplicación Web
│   ├── index.html          # Aplicación principal
│   ├── css/               # Estilos y temas
│   ├── js/                # Lógica JavaScript
│   └── translations/      # Archivos de traducción
│
├── 🐍 Scripts Python
│   ├── scripts/           # Scripts de generación
│   ├── data/             # Traducciones y datos
│   └── main.py           # Script principal
│
├── 📄 PDFs y Distribución
│   ├── pdf/              # PDFs generados
│   ├── docs/             # GitHub Pages
│   └── cache/            # Cache de datos e imágenes
│
└── 📚 Documentación
    ├── README.md         # Esta documentación
    └── TECHNICAL_DOCS.md # Documentación técnica
```

## 📊 Estadísticas del Proyecto

- **🐾 Pokémon**: 1,025 completos (Generaciones I-IX)
- **🌍 Traducciones**: 1,025 descripciones en catalán
- **📄 PDFs**: 20 archivos (18 por generación + 2 completos)
- **💾 Tamaño**: ~60MB total de PDFs con imágenes
- **🌐 Idiomas**: Catalán, español, inglés
- **📱 Compatibilidad**: Todos los navegadores modernos

## 🎓 Uso Educativo

### Para Padres y Educadores
- **📚 Material didáctico** - PDFs listos para imprimir y usar en clase
- **🌍 Aprendizaje multiidioma** - Especialmente diseñado para catalanohablantes
- **🎯 Adaptado para niños** - Lenguaje y diseño apropiado para la edad
- **📱 Interactivo** - Aplicación web para exploración digital

### Para Niños
- **🔤 Fácil lectura** - Modo mayúsculas y fuentes grandes
- **🎨 Visual atractivo** - Colores y diseño llamativo
- **🎮 Navegación simple** - Controles intuitivos
- **📖 Información completa** - Todo lo necesario sobre cada Pokémon

## 🤝 Contribuir

1. **Fork** el proyecto
2. **Crea** una rama para tu funcionalidad (`git checkout -b feature/nueva-funcionalidad`)
3. **Commit** tus cambios (`git commit -am 'Añadir nueva funcionalidad'`)
4. **Push** a la rama (`git push origin feature/nueva-funcionalidad`)
5. **Abre** un Pull Request

## 📄 Licencia

Este proyecto está bajo la **Licencia MIT**. Ver el archivo `LICENSE` para más detalles.

## 🙏 Reconocimientos

- **[PokeAPI](https://pokeapi.co/)** - API de datos Pokémon
- **[ReportLab](https://www.reportlab.com/)** - Generación de PDFs
- **[GitHub Pages](https://pages.github.com/)** - Hosting gratuito
- **Kiro AI** - Traducciones especializadas en catalán

---

<div align="center">

**[🌐 Ver Aplicación](https://jpamies.github.io/pokemon/) • [📚 Descargar PDFs](https://jpamies.github.io/pokemon/docs/) • [📖 Documentación Técnica](TECHNICAL_DOCS.md)**

*Hecho con ❤️ para la comunidad educativa catalanohablante*

</div>
