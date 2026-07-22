import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ASSETS_DIR = os.path.join(BASE_DIR, "assets")
FONTS_DIR = os.path.join(ASSETS_DIR, "fonts")
IMAGES_DIR = os.path.join(ASSETS_DIR, "images")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

# Crée les dossiers s'ils n'existent pas
for folder in [ASSETS_DIR, FONTS_DIR, IMAGES_DIR, OUTPUT_DIR]:
    os.makedirs(folder, exist_ok=True)