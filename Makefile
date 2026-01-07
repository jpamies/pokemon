# Makefile para el proyecto Pokémon PDF Generator
# Uso: make pdf [gen=N] [order=color|id]

PYTHON = python3
SCRIPTS_DIR = scripts

# Variables por defecto
gen ?= all
order ?= id

# Colores para output
GREEN = \033[0;32m
YELLOW = \033[1;33m
RED = \033[0;31m
NC = \033[0m # No Color

.PHONY: help pdf all complete clean cache

# Comando por defecto
help:
	@echo "$(GREEN)🐾 Pokémon PDF Generator$(NC)"
	@echo ""
	@echo "$(YELLOW)Comandos disponibles:$(NC)"
	@echo "  make pdf                    - Generar todos los PDFs por generación"
	@echo "  make all                    - Generar todos los PDFs (alias de pdf)"
	@echo "  make complete               - Generar PDFs completos (1,025 Pokémon)"
	@echo "  make pdf gen=N              - Generar PDFs de generación N (1-9)"
	@echo "  make pdf order=color        - Generar PDFs ordenados por color"
	@echo "  make pdf gen=N order=color  - Generar generación N por color"
	@echo "  make clean                  - Limpiar archivos temporales"
	@echo "  make cache                  - Regenerar cache"
	@echo ""
	@echo "$(YELLOW)Ejemplos:$(NC)"
	@echo "  make pdf gen=1              - Solo Generación I (Kanto)"
	@echo "  make pdf gen=2 order=color  - Generación II por color"
	@echo "  make complete               - PDFs completos con todos los Pokémon"

# Generar PDFs
pdf:
	@echo "$(GREEN)🚀 Generando PDFs...$(NC)"
ifeq ($(gen),all)
	@echo "$(YELLOW)📚 Generando todas las generaciones$(NC)"
	@$(PYTHON) $(SCRIPTS_DIR)/make_all_pdfs.py
else
	@echo "$(YELLOW)📖 Generando Generación $(gen)$(NC)"
	@$(PYTHON) $(SCRIPTS_DIR)/make_gen_pdf.py $(gen) $(order)
endif
	@echo "$(GREEN)✅ PDFs generados correctamente$(NC)"

# Alias para generar todos los PDFs
all: pdf

# Generar PDFs completos
complete:
	@echo "$(GREEN)📚 Generando PDFs completos...$(NC)"
	@$(PYTHON) $(SCRIPTS_DIR)/make_all_pdfs.py complete
	@echo "$(GREEN)✅ PDFs completos generados$(NC)"

# Limpiar archivos temporales
clean:
	@echo "$(YELLOW)🧹 Limpiando archivos temporales...$(NC)"
	@rm -f test_*.pdf
	@rm -f *.pyc
	@rm -rf __pycache__/
	@rm -rf scripts/__pycache__/
	@echo "$(GREEN)✅ Limpieza completada$(NC)"

# Regenerar cache
cache:
	@echo "$(YELLOW)💾 Regenerando cache...$(NC)"
	@cd $(SCRIPTS_DIR) && $(PYTHON) generate_all_cache.py
	@echo "$(GREEN)✅ Cache regenerado$(NC)"
