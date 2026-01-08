#!/usr/bin/env python3
"""
Script para verificar la integridad de datos y archivos del proyecto
"""

import os
import json
import sys

def verify_cache():
    """Verificar que los archivos de cache existen"""
    cache_dir = "../cache"
    required_files = ["pokemon_complete.json", "pokemon_list.json"]
    
    print("🔍 Verificando cache...")
    for file in required_files:
        path = os.path.join(cache_dir, file)
        if os.path.exists(path):
            print(f"✅ {file} - OK")
        else:
            print(f"❌ {file} - FALTA")
            return False
    return True

def verify_translations():
    """Verificar que las traducciones existen"""
    trans_dir = "../translations"
    
    print("\n🌍 Verificando traducciones...")
    if os.path.exists(trans_dir):
        files = os.listdir(trans_dir)
        print(f"✅ Directorio translations - {len(files)} archivos")
        return True
    else:
        print("❌ Directorio translations - FALTA")
        return False

def verify_pdfs():
    """Verificar que los PDFs existen"""
    pdf_dir = "../docs/pdf"
    
    print("\n📄 Verificando PDFs...")
    if os.path.exists(pdf_dir):
        pdfs = [f for f in os.listdir(pdf_dir) if f.endswith('.pdf')]
        print(f"✅ Directorio PDFs - {len(pdfs)} archivos")
        return True
    else:
        print("❌ Directorio PDFs - FALTA")
        return False

def main():
    print("🔍 Verificando integridad del proyecto...\n")
    
    results = [
        verify_cache(),
        verify_translations(),
        verify_pdfs()
    ]
    
    if all(results):
        print("\n✅ Verificación completada - Todo OK")
        sys.exit(0)
    else:
        print("\n❌ Verificación fallida - Hay problemas")
        sys.exit(1)

if __name__ == "__main__":
    main()
