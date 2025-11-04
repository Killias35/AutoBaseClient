import os, time
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
if project_root not in sys.path:
    sys.path.insert(0, project_root)


HOME_URL = "https://www.pappers.fr/recherche"
VILLES = ["Bordeaux", "Merignac 33700"]
VILLE = "Bordeaux"

# filter

EN_ACTIVITE = "true"
ACTIVITE = "69.20Z"
EFFECTIFS_MIN = 6
EFFECTIFS_MAX = 500000