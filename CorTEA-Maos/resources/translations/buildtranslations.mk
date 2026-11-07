# ==============================================================
# Hybrid Makefile for PySide6/Qt translations
# Compatible with: Linux, macOS, Windows (CMD/PowerShell)
# Tested with: PowerShell (Windows 11)
# Date: 25/12/2025 
# ==============================================================
# Qt tools (assuming lupdate/lrelease are in the PATH)

# Automatic OS detection
ifeq ($(OS),Windows_NT)
    IS_WINDOWS := 1

    # Detect if running under PowerShell or CMD
    # PowerShell sets the variable 'PSModulePath'
    ifdef PSModulePath
        SHELL_TYPE := PowerShell
        DETECT_TOOL = if (Get-Command $(1) -ErrorAction SilentlyContinue) { Write-Output 1 } else { Write-Output 0 }
        RM_CMD = Remove-Item -Force -ErrorAction SilentlyContinue
        NULL_DEVICE = $$null
    else
        SHELL_TYPE := CMD
        DETECT_TOOL = where $(1) >nul 2>&1 && echo 1 || echo 0
        RM_CMD = del /f /q
        NULL_DEVICE = nul
    endif
else
    IS_WINDOWS := 0
    SHELL_TYPE := Unix
    DETECT_TOOL = command -v $(1) >/dev/null 2>&1 && echo 1 || echo 0
    RM_CMD = rm -f
    NULL_DEVICE = /dev/null
endif

# Tools: prioritizes PySide6, fallback to standard Qt
HAS_PYSIDE_LUPDATE  := $(shell $(call DETECT_TOOL,pyside6-lupdate))
HAS_PYSIDE_LRELEASE := $(shell $(call DETECT_TOOL,pyside6-lrelease))

ifeq ($(HAS_PYSIDE_LUPDATE),1)
    LUPDATE := pyside6-lupdate
else
    LUPDATE := lupdate
endif

ifeq ($(HAS_PYSIDE_LRELEASE),1)
    LRELEASE := pyside6-lrelease
else
    LRELEASE := lrelease
endif

# Check if the essential tools are available
ifeq ($(shell $(call DETECT_TOOL,$(LUPDATE))),0)
    $(error lupdate or pyside6-lupdate not found in PATH)
endif
ifeq ($(shell $(call DETECT_TOOL,$(LRELEASE))),0)
    $(error lrelease or pyside6-lrelease not found in PATH)
endif

# Default target: show help if no argument is given
.DEFAULT_GOAL := help

# .pro file related to this folder
# You can override the .pro file, for example:
# make PRO_FILE=../myproject.pro all
PRO_FILE ?= translations.pro
$(if $(wildcard $(PRO_FILE)),,$(error File .pro not found: $(PRO_FILE)))

# Related translation files (.ts)
TS_FILES := $(wildcard *.ts)

# Compiled files (.qm)
QM_FILES := $(TS_FILES:.ts=.qm)

# ----------------------------------------------------------------
# Targets
# ----------------------------------------------------------------

# Update and compile translations
all: update release

# Update the .ts files with new strings (keeps obsolete strings)
update:
	@$(LUPDATE) $(PRO_FILE)

# Update the .ts files and REMOVE obsolete strings
update-clean:
	@$(LUPDATE) -no-obsolete $(PRO_FILE)

# Compile only changed .ts files into .qm
release: $(QM_FILES)
	@echo "========================================"
	@echo "Translations compiled successfully!"
	@echo "Files generated: $(notdir $(QM_FILES))"
	@echo "Total: $(words $(QM_FILES)) .qm file(s)"
	@echo "========================================"

# Rule to generate each .qm from its .ts
%.qm: %.ts $(PRO_FILE)
	@$(LRELEASE) $< -qm $@

# Clear compiled files
clean:
	$(RM_CMD) $(QM_FILES) *.ts~ >$(NULL_DEVICE) 2>&1 || true

# Show help    
help:
	@echo "Available commands:"
	@echo "  all          -> update and compile (keeps obsolete strings)"
	@echo "  update       -> update .ts files (keeps obsolete)"
	@echo "  update-clean -> update .ts files and remove obsolete strings"
	@echo "  release      -> compile only changed .ts to .qm"
	@echo "  clean        -> remove .qm and backup files"
	@echo "  help         -> show this help"
	@echo "=============================================================="
	@echo "Override the .pro file if needed:"
	@echo "  Example: make PRO_FILE=../myproject.pro all"
	@echo "Detected shell: $(SHELL_TYPE)"

# Declare phony targets
.PHONY: all update update-clean release clean help

# ==============================================================
# Usage Instructions
# ==============================================================
#
# This file is named buildtranslations.mk, not "Makefile".
# Therefore, always use the -f option when running make:
#
#   make -f buildtranslations.mk                 -> show this help
#   make -f buildtranslations.mk all             -> update and compile translations
#   make -f buildtranslations.mk update          -> update .ts files only
#   make -f buildtranslations.mk update-clean    -> update .ts and remove obsolete strings
#   make -f buildtranslations.mk release         -> compile only changed .ts to .qm
#   make -f buildtranslations.mk clean           -> remove .qm and backup files
#
# Override the .pro file if needed:
#   make -f buildtranslations.mk PRO_FILE=../myproject.pro all