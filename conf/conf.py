import os, time, json
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

def set_parameters():
    global VILLE, RAYON_KM, EN_ACTIVITE, ACTIVITE, EFFECTIFS_MIN, EFFECTIFS_MAX, CIBLE_ACTIVITE_PRINCIPALE
    if os.path.exists("parameters.json"):
        with open("parameters.json", "r") as f:
            parameters = json.load(f)
            VILLE = parameters.get("ville", VILLE)
            RAYON_KM = parameters.get("rayon", RAYON_KM)
            EN_ACTIVITE = parameters.get("en_activite", EN_ACTIVITE)
            ACTIVITE = parameters.get("activite", ACTIVITE)
            EFFECTIFS_MIN = parameters.get("effectifs_min", EFFECTIFS_MIN)
            EFFECTIFS_MAX = parameters.get("effectifs_max", EFFECTIFS_MAX)
            CIBLE_ACTIVITE_PRINCIPALE = parameters.get("cible_activite_principale", CIBLE_ACTIVITE_PRINCIPALE)
    else:
        with open("parameters.json", "w") as f:
            json.dump({"ville": VILLE, "rayon": RAYON_KM, "en_activite": EN_ACTIVITE, "activite": ACTIVITE, "effectifs_min": EFFECTIFS_MIN, "effectifs_max": EFFECTIFS_MAX, "cible_activite_principale": CIBLE_ACTIVITE_PRINCIPALE}, f, ensure_ascii=False, indent=4)

set_parameters()