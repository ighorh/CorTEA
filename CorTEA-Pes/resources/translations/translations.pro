# -------------------------------------------------
# Project file (.pro) for PySide6 in Python
# Used for internationalization and resources
# -------------------------------------------------

# Type of project just to resources
TEMPLATE = aux

# Graphical user interface (.ui) files created in Qt Designer
FORMS += ../ui/*.ui \
         ../../src/ttea/games/kartea/resources/ui/*.ui

# Python files that must be parsed by lupdate
SOURCES += ../../src/ttea/app/*.py \
           ../../src/ttea/controller/*.py \
            ../../src/ttea/core/*.py \
           ../../src/ttea/games/kartea/controller/*.py \
           ../../src/ttea/games/kartea/view/*.py \
           ../../src/ttea/model/*.py \
           ../../src/ttea/service/*.py \
           ../../src/ttea/util/*.py \
           ../../src/ttea/view/*.py \
           ../../src/ttea/main.py

# Translation files
TRANSLATIONS += \
    pt_BR.ts \
    en_US.ts \
    es_ES.ts

# -------------------------------------------------
# PySide6 shell commands
# -------------------------------------------------
# To generate/update the translation files (.ts):
#   lupdate translations.pro
#   or
#   pyside6-lupdate translations.pro
#
# To compile the .ts into .qm:
#   lrelease translations.pro
#   or
#   pyside6-lrelease translations.pro
#
# Obs: 1 - First execute lupdate.  
# 1.1 - You might need to use Qt's lupdate
# instead of pyside. Place Qt's lupdate in the 
# operating system's path for the call to work.
# Example Windows direct with no OS Path:
# & "C:\Qt\6.8.2\mingw_64\bin\lupdate.exe" 
# -verbose translations.pro
#
# 2 - Use Qt Linguist to translation the .ts files
# 2.1 - Sometimes execute lupdate again to see 
# any string left behind.
# 2.2 - An optional step is to create a 
# phrase book file (.qph) from the (.ts) file.
#
# 3 - And then execute lrelease.
# 3.1 - You might need to use Qt's lrelease
# instead of pyside. Place Qt's lupdate in the 
# operating system's path for the call to work.
# Example Windows direct with no OS Path:
# & "C:\Qt\6.8.2\mingw_64\bin\lrelease.exe" 
# translations.pro
# 
# 4 - Don't use strings with f to translate
# -------------------------------------------------
