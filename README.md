# 🐾 Guía Pokémon para Niños

> **Sistema educativo completo con guías Pokémon multiidioma y PDFs descargables**

Una aplicación web estática diseñada específicamente para ayudar a los niños a aprender sobre Pokémon, con soporte completo en **catalán**, español e inglés, y funciones de accesibilidad adaptadas para el público infantil.

[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Live-brightgreen)](https://jpamies.github.io/pokemon/)
[![PDFs](https://img.shields.io/badge/PDFs-22%20archivos-blue)](https://jpamies.github.io/pokemon/docs/)
[![Pokémon](https://img.shields.io/badge/Pokémon-1025%20completos-red)](https://jpamies.github.io/pokemon/)

## 🎯 Acceso Rápido

### 🌐 **Aplicación Web**
- **[📱 Aplicación Interactiva](https://jpamies.github.io/pokemon/)** - Navega por todos los Pokémon online
- **[📚 Centro de Descargas](https://jpamies.github.io/pokemon/docs/)** - Todos los PDFs disponibles

### 📖 **Guías Completas** (Recomendado)
- **[📥 Guía Completa por ID](docs/pdf/pokemon_complet.pdf)** - 1,025 Pokémon ordenados por número
- **[📥 Guía Completa por Color](docs/pdf/pokemon_complet_by_color.pdf)** - 1,025 Pokémon ordenados por color

### 🗜️ **Versiones Comprimidas** (Menor tamaño)
- **[📦 Guía Completa por ID (Comprimida)](docs/pdf/pokemon_complet_compressed.pdf)** - Versión optimizada
- **[📦 Guía Completa por Color (Comprimida)](docs/pdf/pokemon_complet_by_color_compressed.pdf)** - Versión optimizada

*Ambas versiones incluyen todos los Pokémon de las 9 generaciones con descripciones completas en catalán*

## 📚 PDFs Multiidioma

| Idioma | Guías Completas | PDFs por Generación |
|--------|----------------|-------------------|
| **🔵 Català** | [Por ID](docs/pdf/pokemon_complet.pdf) • [Por Color](docs/pdf/pokemon_complet_by_color.pdf) | 18 PDFs (9 gen × 2 tipos) |
| **🔴 Español** | [Por ID](docs/pdf/pokemon_complet_es.pdf) • [Por Color](docs/pdf/pokemon_complet_by_color_es.pdf) | 18 PDFs (9 gen × 2 tipos) |
| **🟢 English** | [By ID](docs/pdf/pokemon_complet_en.pdf) • [By Color](docs/pdf/pokemon_complet_by_color_en.pdf) | 18 PDFs (9 gen × 2 types) |

**Total: 66 PDFs** - Todos los Pokémon de las 9 generaciones en 3 idiomas

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
make serve
```

### Comandos Disponibles
```bash
# Ver todos los comandos disponibles
make help

# Generar todos los PDFs
make all

# Solo PDFs por generaciones (I-IX)
make generations

# Solo PDFs completos (1,025 Pokémon)
make complete

# Regenerar cache de datos e imágenes
make cache

# Optimizar imágenes para PDFs más pequeños
make optimize

# Generar traducciones en catalán
make translate

# Generar todos los PDFs en 3 idiomas
make multilang

# Servir aplicación web localmente
make serve

# Limpiar archivos temporales
make clean

# Verificar integridad de datos
make test
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
    └── README.md         # Esta documentación
```

## 📊 Estadísticas del Proyecto

- **🐾 Pokémon**: 1,025 completos (Generaciones I-IX)
- **🌍 Traducciones**: 1,025 descripciones en catalán
- **📄 PDFs**: 66 archivos (54 por generación + 6 completos + 6 comprimidos)
- **💾 Tamaño**: 254MB total optimizado con imágenes PNG
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

**[🌐 Ver Aplicación](https://jpamies.github.io/pokemon/) • [📚 Descargar PDFs](https://jpamies.github.io/pokemon/docs/)**

*Hecho con ❤️ para la comunidad educativa catalanohablante*

</div>
