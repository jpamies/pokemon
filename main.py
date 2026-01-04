#!/usr/bin/env python3
"""
Script principal para generar PDFs de Pokémon
Uso: python main.py [comando]

Comandos disponibles:
  all          - Generar todos los PDFs (generaciones + completos)
  generations  - Generar solo PDFs por generaciones
  complete     - Generar solo PDFs completos
  cache        - Regenerar cache completo
"""

import sys
import os

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return
    
    command = sys.argv[1].lower()
    
    # Cambiar al directorio scripts
    os.chdir('scripts')
    
    if command == 'all':
        print("🚀 Generando todos los PDFs...")
        os.system('python3 batch_translate.py')
        os.system('python3 generate_complete_with_cards.py')
        os.system('python3 generate_complete_by_color.py')
        print("✅ Todos los PDFs generados")
        
    elif command == 'generations':
        print("📚 Generando PDFs por generaciones...")
        os.system('python3 batch_translate.py')
        print("✅ PDFs por generaciones generados")
        
    elif command == 'complete':
        print("📖 Generando PDFs completos...")
        os.system('python3 generate_complete_with_cards.py')
        os.system('python3 generate_complete_by_color.py')
        print("✅ PDFs completos generados")
        
    elif command == 'cache':
        print("💾 Regenerando cache...")
        os.system('python3 generate_all_cache.py')
        print("✅ Cache regenerado")
        
    else:
        print(f"❌ Comando desconocido: {command}")
        print(__doc__)

if __name__ == "__main__":
    main()
