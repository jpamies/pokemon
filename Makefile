# Makefile para el proyecto Pokémon PDF Generator

PYTHON = python3
SCRIPTS_DIR = scripts

# Colores para output
GREEN = \033[0;32m
YELLOW = \033[1;33m
BLUE = \033[0;34m
RED = \033[0;31m
NC = \033[0m # No Color

.PHONY: help all generations complete cache clean optimize serve test

# Comando por defecto
help:
	@echo "$(GREEN)🐾 Pokémon PDF Generator$(NC)"
	@echo ""
	@echo "$(YELLOW)Comandos principales:$(NC)"
	@echo "  make all                    - Generar todos los PDFs (generaciones + completos)"
	@echo "  make generations            - Generar PDFs por generaciones (I-IX)"
	@echo "  make complete               - Generar PDFs completos (1,025 Pokémon)"
	@echo "  make cache                  - Regenerar cache de datos e imágenes"
	@echo "  make optimize               - Optimizar imágenes para PDFs más pequeños"
	@echo ""
	@echo "$(YELLOW)Comandos de desarrollo:$(NC)"
	@echo "  make serve                  - Servir aplicación web localmente"
	@echo "  make clean                  - Limpiar archivos temporales"
	@echo "  make test                   - Verificar integridad de datos"
	@echo ""
	@echo "$(BLUE)Estructura del proyecto:$(NC)"
	@echo "  📁 docs/          - GitHub Pages y PDFs generados"
	@echo "  📁 scripts/       - Scripts de generación Python"
	@echo "  📁 cache/         - Cache de datos e imágenes"
	@echo "  📁 translations/  - Traducciones en catalán"
	@echo "  📄 Makefile       - Este archivo de comandos"

# Generar todos los PDFs
all:
	@echo "$(GREEN)🚀 Generando todos los PDFs...$(NC)"
	@$(PYTHON) $(SCRIPTS_DIR)/generate_all_pdfs.py
	@echo "$(GREEN)✅ Todos los PDFs generados correctamente$(NC)"

# Generar PDFs por generaciones
generations:
	@echo "$(GREEN)📚 Generando PDFs por generaciones...$(NC)"
	@$(PYTHON) $(SCRIPTS_DIR)/generate_generation_pdfs.py
	@echo "$(GREEN)✅ PDFs por generaciones completados$(NC)"

# Generar PDFs completos
complete:
	@echo "$(GREEN)📖 Generando PDFs completos...$(NC)"
	@$(PYTHON) $(SCRIPTS_DIR)/generate_complete_with_cards.py
	@$(PYTHON) $(SCRIPTS_DIR)/generate_complete_by_color.py
	@echo "$(GREEN)✅ PDFs completos generados$(NC)"

# Regenerar cache
cache:
	@echo "$(YELLOW)💾 Regenerando cache...$(NC)"
	@$(PYTHON) $(SCRIPTS_DIR)/generate_cache.py
	@echo "$(GREEN)✅ Cache regenerado$(NC)"

# Optimizar imágenes
optimize:
	@echo "$(YELLOW)🖼️  Optimizando imágenes...$(NC)"
	@$(PYTHON) $(SCRIPTS_DIR)/optimize_images.py
	@echo "$(GREEN)✅ Imágenes optimizadas$(NC)"

# Servir aplicación web localmente
serve:
	@echo "$(BLUE)🌐 Sirviendo aplicación web en http://localhost:8000$(NC)"
	@$(PYTHON) -m http.server 8000

# Limpiar archivos temporales
clean:
	@echo "$(YELLOW)🧹 Limpiando archivos temporales...$(NC)"
	@find . -name "*.pyc" -delete
	@find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
	@rm -f test_*.pdf
	@rm -f *.tmp
	@echo "$(GREEN)✅ Limpieza completada$(NC)"

# Verificar integridad de datos
test:
	@echo "$(BLUE)🔍 Verificando integridad de datos...$(NC)"
	@$(PYTHON) $(SCRIPTS_DIR)/verify_data.py
	@echo "$(GREEN)✅ Verificación completada$(NC)"
