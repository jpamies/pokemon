# Documentación Técnica - Guía Pokémon para Niños

## 📋 Resumen del Proyecto

Sistema completo de guías Pokémon educativas con soporte multiidioma, enfocado en proporcionar material didáctico para niños en catalán, español e inglés. Incluye aplicación web interactiva y PDFs descargables con todos los Pokémon de las 9 generaciones.

## 🎯 Objetivos y Requisitos

### Objetivos Principales
- **Educativo**: Material didáctico para niños aprendiendo sobre Pokémon
- **Multiidioma**: Soporte completo en catalán (prioritario), español e inglés
- **Accesibilidad**: Diseño adaptado para niños con opciones de accesibilidad
- **Offline**: PDFs descargables para uso sin conexión
- **Gratuito**: Hosting en GitHub Pages sin costes

### Requisitos Funcionales
- Navegación por todos los 1,025 Pokémon (Generaciones I-IX)
- Traducciones profesionales en catalán hechas por IA especializada
- Generación automática de PDFs con formato de cartas
- Aplicación web responsive y accesible
- Sistema de cache para optimización de rendimiento
- Múltiples ordenaciones (por ID, por color, por generación)

### Requisitos Técnicos
- **Frontend**: HTML5, CSS3, JavaScript vanilla (sin frameworks)
- **Backend**: Python 3 para generación de PDFs
- **API**: PokeAPI (https://pokeapi.co) como fuente de datos
- **PDFs**: ReportLab para generación de documentos
- **Hosting**: GitHub Pages para distribución gratuita
- **Cache**: Sistema local para optimización de rendimiento

## 🏗️ Arquitectura del Sistema

### Componentes Principales

```
pokeAPI/
├── 📱 Frontend Web (Aplicación Interactiva)
│   ├── index.html          # Aplicación principal
│   ├── css/               # Estilos y temas
│   ├── js/                # Lógica de la aplicación
│   └── translations/      # Archivos de traducción
│
├── 🐍 Backend Python (Generación PDFs)
│   ├── generate_pdf.py           # Motor principal de PDFs
│   ├── batch_translate.py        # Generación por lotes
│   ├── generate_complete_*.py    # PDFs completos
│   └── mass_translate.py         # Sistema de traducciones
│
├── 💾 Sistema de Cache
│   ├── cache/data/        # Datos de Pokémon cacheados
│   ├── cache/images/      # Imágenes descargadas
│   └── cache/translations/ # Traducciones procesadas
│
├── 📄 PDFs Generados
│   ├── pdf/              # PDFs por generación
│   └── docs/pdf/         # PDFs para distribución web
│
└── 🌐 GitHub Pages
    └── docs/             # Sitio web público
```

### Flujo de Datos

1. **Obtención de Datos**: PokeAPI → Cache Local → Aplicación
2. **Traducciones**: Kiro AI → JSON → Cache → PDFs/Web
3. **Generación PDFs**: Cache → ReportLab → PDFs finales
4. **Distribución**: GitHub Pages → Usuarios finales

## 🔧 Funcionalidades Implementadas

### Aplicación Web Interactiva
- **Navegación completa**: 1,025 Pokémon de 9 generaciones
- **Multiidioma**: Catalán, español, inglés con cambio dinámico
- **Modos de vista**: Básico y avanzado (con estadísticas)
- **Accesibilidad**: Modo mayúsculas, navegación por teclado
- **Responsive**: Adaptado a móviles, tablets y desktop
- **Información completa**: Tipos, estadísticas, evoluciones, habilidades

### Sistema de PDFs
- **PDFs por generación**: 9 archivos (Gen I-IX) con 2 ordenaciones cada uno
- **PDFs completos**: 2 archivos con todos los Pokémon
- **Formato de cartas**: Layout horizontal optimizado para impresión
- **Imágenes oficiales**: Artwork de alta calidad de cada Pokémon
- **Traducciones catalanas**: Descripciones adaptadas para niños

### Sistema de Traducciones
- **1,025 traducciones**: Todas hechas por Kiro AI especializada en contenido infantil
- **Formato JSON**: Estructura optimizada para carga rápida
- **Cache inteligente**: Evita retraducciones innecesarias
- **Calidad educativa**: Lenguaje adaptado para comprensión infantil

### Optimizaciones de Rendimiento
- **Cache multinivel**: Datos, imágenes y traducciones
- **Carga progresiva**: Imágenes bajo demanda
- **Compresión**: PDFs optimizados para descarga
- **CDN**: GitHub Pages con distribución global

## 📁 Estructura del Repositorio

### Archivos Principales
```
├── index.html                    # Aplicación web principal
├── README.md                     # Documentación de usuario
├── TECHNICAL_DOCS.md            # Esta documentación técnica
└── package.json                 # Metadatos del proyecto
```

### Scripts de Generación (Python)
```
├── generate_pdf.py              # Motor principal de PDFs
├── batch_translate.py           # Generación por lotes de generaciones
├── generate_complete_with_cards.py    # PDF completo por ID
├── generate_complete_by_color.py      # PDF completo por color
├── mass_translate.py            # Sistema de traducciones masivas
└── generate_all_cache.py        # Precarga de cache completo
```

### Recursos y Assets
```
├── css/
│   ├── styles.css              # Estilos principales
│   └── themes.css              # Temas y colores
├── js/
│   ├── app.js                  # Lógica principal
│   ├── pokemon.js              # Gestión de datos Pokémon
│   └── translations.js         # Sistema de traducciones
├── translations/
│   ├── ca.json                 # Traducciones catalán
│   ├── es.json                 # Traducciones español
│   └── en.json                 # Traducciones inglés
└── fonts/                      # Fuentes personalizadas
```

### Datos y Cache
```
├── cache/
│   ├── data/                   # Datos Pokémon (JSON)
│   ├── images/                 # Imágenes descargadas
│   └── translations/           # Cache de traducciones
├── catalan_translations.json   # Traducciones catalanas principales
└── spanish_descriptions.json   # Descripciones en español
```

### Distribución Web
```
├── docs/                       # GitHub Pages
│   ├── index.html             # Landing page
│   └── pdf/                   # PDFs para descarga
└── pdf/                       # PDFs generados localmente
```

### Configuración y Deploy
```
├── .github/workflows/
│   └── deploy.yml             # GitHub Actions para deploy
└── deploy.sh                  # Script de despliegue local
```

## 🔄 Flujos de Trabajo

### Generación de PDFs por Generación
1. `batch_translate.py` → Carga datos de cache
2. Aplica traducciones catalanas
3. Genera PDF con formato de cartas
4. Crea versiones por ID y por color
5. Copia a `docs/pdf/` para distribución

### Generación de PDFs Completos
1. `generate_complete_with_cards.py` → Todos los Pokémon por ID
2. `generate_complete_by_color.py` → Todos los Pokémon por color
3. Formato idéntico a PDFs individuales
4. Optimización para archivos grandes (3MB cada uno)

### Actualización de Traducciones
1. `mass_translate.py` → Procesa nuevas traducciones
2. Actualiza `catalan_translations.json`
3. Sincroniza con cache individual
4. Regenera PDFs afectados

### Deploy a GitHub Pages
1. Commit cambios locales
2. GitHub Actions ejecuta workflow
3. Actualiza sitio en `https://jpamies.github.io/pokemon/`
4. PDFs disponibles para descarga inmediata

## 🧪 Testing y Verificación

### Verificaciones Automáticas
- **Integridad de datos**: Todos los 1,025 Pokémon presentes
- **Traducciones**: Cobertura completa en catalán
- **Imágenes**: Descarga y procesamiento correcto
- **PDFs**: Generación sin errores y tamaño apropiado
- **Links**: Verificación de enlaces en GitHub Pages

### Métricas de Calidad
- **Cobertura de traducciones**: 100% (1,025/1,025)
- **Tamaño de PDFs**: ~3MB (con imágenes), ~100KB (solo texto)
- **Tiempo de carga web**: <2s para navegación básica
- **Compatibilidad**: Todos los navegadores modernos

## 🚀 Instrucciones de Desarrollo

### Setup Inicial
```bash
git clone https://github.com/jpamies/pokemon.git
cd pokemon
python -m http.server 8000  # Para desarrollo local
```

### Regenerar PDFs
```bash
# Por generaciones individuales
python batch_translate.py

# PDFs completos
python generate_complete_with_cards.py
python generate_complete_by_color.py

# Copiar a distribución
cp pdf/*.pdf docs/pdf/
```

### Actualizar Traducciones
```bash
# Añadir nuevas traducciones a catalan_translations.json
python mass_translate.py

# Regenerar PDFs con nuevas traducciones
python batch_translate.py
```

### Deploy
```bash
git add .
git commit -m "Update content"
git push origin main  # GitHub Actions se encarga del resto
```

## 📊 Estadísticas del Proyecto

- **Total Pokémon**: 1,025 (Generaciones I-IX)
- **Traducciones catalanas**: 1,025 (100% cobertura)
- **PDFs generados**: 20 archivos (18 por generación + 2 completos)
- **Tamaño total**: ~60MB de PDFs con imágenes
- **Idiomas soportados**: 3 (catalán, español, inglés)
- **Tiempo de generación completa**: ~15 minutos
- **Compatibilidad**: Navegadores modernos + PDFs universales

## 🔮 Extensiones Futuras

### Funcionalidades Planificadas
- **Modo offline completo**: Service Worker para PWA
- **Búsqueda avanzada**: Filtros por tipo, generación, estadísticas
- **Comparador**: Herramienta para comparar Pokémon
- **Quiz interactivo**: Juegos educativos
- **Más idiomas**: Euskera, gallego, francés

### Mejoras Técnicas
- **Optimización de imágenes**: WebP para mejor rendimiento
- **CDN personalizado**: Para imágenes y assets
- **Base de datos local**: IndexedDB para cache avanzado
- **API propia**: Reducir dependencia de PokeAPI
- **Tests automatizados**: Suite completa de testing

## 📝 Notas de Mantenimiento

### Dependencias Críticas
- **PokeAPI**: Fuente principal de datos (externa)
- **ReportLab**: Generación de PDFs (Python)
- **GitHub Pages**: Hosting gratuito (limitado a 1GB)

### Puntos de Atención
- **Rate limiting**: PokeAPI tiene límites de requests
- **Tamaño de repo**: GitHub tiene límite de 1GB
- **Cache management**: Limpiar cache periódicamente
- **Traducciones**: Mantener calidad educativa

### Backup y Recuperación
- **Traducciones**: `catalan_translations.json` es crítico
- **Cache**: Regenerable desde PokeAPI
- **PDFs**: Regenerables desde cache
- **Configuración**: Documentada en este archivo
