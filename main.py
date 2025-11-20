import os, time
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
if project_root not in sys.path:
    sys.path.insert(0, project_root)


from data.main import main as main_data
from export.export_to_csv import export_to_csv
from data.services.get_city_in_range import villes_autour, trier_par_region_departement
from conf.conf import VILLE

def main():
    regions = trier_par_region_departement(villes_autour(VILLE))
    regions_to_search = []
    deps_to_search = []
    villes_to_search = []
    for region, deps in regions.items():
        for dep, villes in deps.items():
            for ville, d in villes:
                if region not in regions_to_search: regions_to_search.append(region)
                if dep not in deps_to_search: deps_to_search.append(dep)
                if ville not in villes_to_search: villes_to_search.append(ville)
    
    data = main_data(regions_to_search, deps_to_search, villes_to_search)
    todayes = time.strftime("%Y-%m-%d")
    export_to_csv(data, f"company_datas_{VILLE}_{todayes}.csv")
    # https://annuaire.experts-comptables.org/tous-les-cabinets-experts-comptables-par-region/nouvelle-aquitaine/gironde

if __name__ == "__main__":
    print("Programme principal...")
    main()