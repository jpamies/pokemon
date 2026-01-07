# 🌍 Sistema de Traducciones Pokémon con AWS Bedrock

Este directorio contiene scripts para crear un sistema completo de traducciones Pokémon en 3 idiomas usando AWS Bedrock.

## 📋 Proceso Completo

### 1. **Crear Estructura de Datos**
```bash
python3 create_pokemon_structure.py
```
- Descarga datos completos de PokeAPI
- Crea directorio `pokemon_data/` con un JSON por Pokémon
- Incluye descripciones en inglés y español
- Prepara estructura para traducciones catalanas

### 2. **Traducir con Bedrock** (Ejecutar fuera del chat)
```bash
# Configurar AWS CLI primero
aws configure

# Ejecutar traductor
python3 bedrock_translator.py
```
- Usa AWS Bedrock (Claude) para traducciones catalanas de calidad
- Traduce 1,025 descripciones con contexto educativo infantil
- Respeta límites de API con pausas automáticas

### 3. **Integrar con Sistema Existente**
```bash
python3 integrate_translations.py
```
- Crea archivos de traducción compatibles
- Genera configuración multiidioma
- Integra con sistema de PDFs existente

## 📁 Estructura Resultante

```
pokemon_data/
├── pokemon_0001.json    # Bulbasaur con 3 idiomas
├── pokemon_0002.json    # Ivysaur con 3 idiomas
├── ...
├── pokemon_1025.json    # Último Pokémon
└── index.json          # Índice y metadatos

data/
├── catalan_translations_bedrock.json    # Traducciones catalanas
├── spanish_translations.json            # Traducciones españolas  
└── multilang_config.json               # Configuración multiidioma
```

## 🔧 Requisitos

### Para AWS Bedrock:
```bash
# Instalar AWS CLI
pip install boto3

# Configurar credenciales
aws configure
```

### Permisos necesarios:
- `bedrock:InvokeModel` para Claude v2
- Región recomendada: `us-east-1`

## 📊 Ejemplo de Datos

```json
{
  "id": 1,
  "name": "Bulbasaur",
  "descriptions": {
    "en": "A strange seed was planted on its back at birth...",
    "es": "Una extraña semilla fue plantada en su espalda...",
    "ca": "Una llavor estranya va ser plantada al seu esquena..."
  },
  "names": {
    "en": "Bulbasaur",
    "es": "Bulbasaur", 
    "ca": "Bulbasaur"
  },
  "types": ["grass", "poison"],
  "stats": { "hp": 45, "attack": 49, ... },
  "images": { ... }
}
```

## ⚡ Ventajas del Sistema

1. **Traducciones de Calidad**: Bedrock/Claude para catalán profesional
2. **Datos Completos**: Inglés y español desde PokeAPI oficial
3. **Estructura Escalable**: Un JSON por Pokémon, fácil de mantener
4. **Integración Simple**: Compatible con sistema PDF existente
5. **Multiidioma**: Base para PDFs en 3 idiomas

## 🚀 Uso Rápido

```bash
# 1. Crear estructura
python3 create_pokemon_structure.py

# 2. Traducir (fuera del chat con Bedrock)
python3 bedrock_translator.py

# 3. Integrar
python3 integrate_translations.py

# 4. Usar traducciones
# Los archivos en data/ están listos para el sistema PDF
```

## 💡 Notas

- **Tiempo estimado**: ~2-3 horas para 1,025 traducciones
- **Costo Bedrock**: ~$5-10 USD para todas las traducciones
- **Calidad**: Traducciones contextuales para público infantil
- **Mantenimiento**: Estructura permite actualizaciones fáciles
