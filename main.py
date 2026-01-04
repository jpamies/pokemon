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
import subprocess

def run_script_in_scripts_dir(script_name):
    """Execute a script from the scripts directory"""
    current_dir = os.getcwd()
    scripts_dir = os.path.join(current_dir, 'scripts')
    
    # Change to scripts directory and run the script
    result = subprocess.run(['python3', script_name], cwd=scripts_dir, capture_output=False)
    return result.returncode == 0

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return
    
    command = sys.argv[1].lower()
    
    if command == 'all':
        print("🚀 Generando todos los PDFs...")
        run_script_in_scripts_dir('batch_translate.py')
        run_script_in_scripts_dir('generate_complete_with_cards.py')
        run_script_in_scripts_dir('generate_complete_by_color.py')
        print("✅ Todos los PDFs generados")
        
    elif command == 'generations':
        print("📚 Generando PDFs por generaciones...")
        run_script_in_scripts_dir('batch_translate.py')
        print("✅ PDFs por generaciones generados")
        
    elif command == 'complete':
        print("📖 Generando PDFs completos...")
        run_script_in_scripts_dir('generate_complete_with_cards.py')
        run_script_in_scripts_dir('generate_complete_by_color.py')
        print("✅ PDFs completos generados")
        
    elif command == 'cache':
        print("💾 Regenerando cache...")
        run_script_in_scripts_dir('generate_all_cache.py')
        print("✅ Cache regenerado")
        
    else:
        print(f"Comando desconocido: {command}")
        print(__doc__)

if __name__ == "__main__":
    main()
