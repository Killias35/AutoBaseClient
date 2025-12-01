import os, time
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
if project_root not in sys.path:
    sys.path.insert(0, project_root)


HOME_URL = "https://www.pappers.fr/recherche"
VILLE = "Rennes"
RAYON_KM = 20  # 20 km normalement

# filter

ANNUAIRE_EXPERT_COMPTABLE_URL = "https://annuaire.experts-comptables.org/tous-les-cabinets-experts-comptables-par-region"
SOCIETE_COM_URL = "https://www.societe.com/"

EN_ACTIVITE = True
ACTIVITE = "69.20Z"
EFFECTIFS_MIN = 6
EFFECTIFS_MAX = 500000
CIBLE_ACTIVITE_PRINCIPALE = True