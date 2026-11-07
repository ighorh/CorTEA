# buildui.mk – Works on Windows + Linux + macOS
# Initially tested on Windows 11 – 10/Dec/2025

UI_DIR      := ui
QRC_DIR     := .

UIC         := pyside6-uic
RCC         := pyside6-rcc

UI_FILES    := $(wildcard $(UI_DIR)/*.ui)
QRC_FILE    := $(firstword $(wildcard $(QRC_DIR)/*.qrc))

PY_UI_FILES := $(patsubst $(UI_DIR)/%.ui,$(UI_DIR)/%ui.py,$(UI_FILES))
PY_QRC_FILE := resourceskartea_rc.py

DEST_DIR    := ../ui

# ==============================================================
# OS detection and correct commands
# ==============================================================

ifeq ($(OS),Windows_NT)
    MKDIR   := if not exist "$(DEST_DIR)" mkdir "$(DEST_DIR)" 2>nul
    CP      := copy /Y
    RM      := del /Q /F
    NULL    := 2>nul
else
    MKDIR   := mkdir -p $(DEST_DIR)
    CP      := cp -f
    RM      := rm -f
    NULL    := >/dev/null 2>&1
endif

# ==============================================================
# Rules
# ==============================================================

.PHONY: all copy clean clean_copied

all: $(PY_QRC_FILE) $(PY_UI_FILES) copy clean_local_ui

$(PY_QRC_FILE): $(QRC_FILE)
	$(RCC) $< -o $@

$(UI_DIR)/%ui.py: $(UI_DIR)/%.ui $(PY_QRC_FILE)
	$(UIC) $< -o $@ --absolute-imports

# Copy rule (OS-specific)
copy: $(PY_UI_FILES)
	@$(MKDIR)
	@echo Copying UI files to $(DEST_DIR)...
ifeq ($(OS),Windows_NT)
	@for %%F in ($(notdir $(PY_UI_FILES))) do @$(CP) "$(UI_DIR)\%%F" "$(DEST_DIR)\%%F" $(NULL)
else
	@$(CP) $(PY_UI_FILES) $(DEST_DIR)/ $(NULL)
endif
	@echo Done! All *ui.py files have been copied.
	@echo.

# Regra que apaga os .py que ficaram na pasta local ui/
clean_local_ui:
	@echo Deleting locally generated .py files in $(UI_DIR)/ ...
ifeq ($(OS),Windows_NT)
	@if exist "$(UI_DIR)\*ui.py" $(RM) "$(UI_DIR)\*ui.py" $(NULL)
else
	@$(RM) $(UI_DIR)/*ui.py $(NULL)
endif
	@echo Local files removed. Only files in $(DEST_DIR) were kept.
	@echo.	

# ==============================================================
# Cleanup
# ==============================================================

clean:
	-$(RM) "$(PY_QRC_FILE)" $(NULL)
	-$(RM) "$(UI_DIR)\*ui.py" $(NULL)
	@echo Full local cleanup completed.

clean_copied:
	-$(RM) "$(DEST_DIR)\*ui.py" $(NULL) 2>nul || true
	@echo Only the copied *ui.py files were removed.

# ==============================================================
# Quick command reference
# ==============================================================

# Useful commands:
# make -f buildkartea.mk -> build everything, copy and clean local files (normal usage)
# make -f buildkartea.mk copy -> copy only (useful for quick testing)
# make -f buildkartea.mk clean -> delete everything generated LOCALLY (preserves destination folder)
# make -f buildkartea.mk clean_copied -> delete only the *ui.py files in the destination folder
