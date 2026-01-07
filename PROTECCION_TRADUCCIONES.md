# 🛡️ PROTECCIÓN DE TRADUCCIONES BEDROCK

## 📍 UBICACIÓN DE DATOS CRÍTICOS

### 🎯 **Traducciones Bedrock (NO TOCAR)**
```
pokemon_data/                           # 1,025 archivos JSON individuales
├── pokemon_0001.json                   # Bulbasaur con 3 idiomas completos
├── pokemon_0002.json                   # Ivysaur con 3 idiomas completos
├── ...
└── pokemon_1025.json                   # Pecharunt con 3 idiomas completos

data/catalan_translations_bedrock.json  # BACKUP PRINCIPAL - Traducciones Bedrock
data/catalan_translations.json          # ARCHIVO ACTIVO - Usado por PDFs
```

### 📊 **Contenido de Cada Archivo**
```json
{
  "id": 1,
  "name": "Bulbasaur",
  "descriptions": {
    "en": "Descripción oficial en inglés desde PokeAPI",
    "es": "Descripción oficial en español desde PokeAPI", 
    "ca": "Traducción profesional Bedrock/Claude 3"
  },
  "names": {
    "en": "Bulbasaur",
    "es": "Bulbasaur",
    "ca": "Bulbasaur"
  },
  "types": ["grass", "poison"],
  "stats": { "hp": 45, "attack": 49, ... },
  "images": { ... },
  "abilities": [ ... ]
}
```

## 🔒 **COMANDOS DE PROTECCIÓN**

### Crear Backup de Seguridad
```bash
# EJECUTAR ANTES DE CUALQUIER CAMBIO
cp -r pokemon_data pokemon_data_BACKUP_$(date +%Y%m%d_%H%M%S)
cp data/catalan_translations_bedrock.json data/catalan_translations_bedrock_BACKUP_$(date +%Y%m%d_%H%M%S).json
```

### Restaurar desde Backup
```bash
# Si algo se corrompe, restaurar desde pokemon_data/
python3 integrate_translations.py
```

## ⚠️ **REGLAS CRÍTICAS**

1. **NUNCA ejecutar** `bedrock_translator_optimized.py` de nuevo sin backup
2. **NUNCA borrar** el directorio `pokemon_data/`
3. **SIEMPRE verificar** que `data/catalan_translations.json` tiene 1,025 entradas
4. **El archivo activo** es `data/catalan_translations.json` (usado por PDFs)
5. **El backup principal** es `data/catalan_translations_bedrock.json`

## 🔄 **Regeneración Segura**

Si necesitas regenerar archivos de traducción:
```bash
# 1. Verificar que pokemon_data/ existe y tiene 1,025 archivos
ls pokemon_data/pokemon_*.json | wc -l

# 2. Regenerar archivos de traducción desde pokemon_data/
python3 integrate_translations.py

# 3. Verificar resultado
python3 verify_translations.py
```

## 💰 **COSTO BEDROCK**
- **Total invertido**: ~$8-12 USD en traducciones Claude 3
- **1,025 traducciones profesionales** de calidad educativa
- **NO repetir** sin necesidad absoluta

## 📈 **ESTADÍSTICAS**
- **Pokémon traducidos**: 1,025/1,025 (100%)
- **Idiomas disponibles**: 3 (EN, ES, CA)
- **Calidad**: Profesional Bedrock/Claude 3
- **Fecha creación**: 2026-01-05 16:24
