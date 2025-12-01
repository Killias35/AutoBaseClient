import os, time
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from data.services.filter_research_pappers import filter_research
from data.services.get_pappers_datas import get_pappers_datas
from data.services.get_mails import find_company_emails
from conf.utils.json_utils import save_json
from data.utils.session import Session
from data.services.get_villes_utiles import get_villes_utiles
from data.services.this_company_still_exist import get_active_companies

def main(regions: list, departements: list, villes: list) -> dict:
    """
    Récupere les données de pappers puis tente d'y trouver des mails a chaque entreprise
    """
    datas = {}
    session = Session()
    try:
        villes_utiles = get_villes_utiles(session, regions, departements, villes)
        print(f"{len(villes_utiles)} villes utiles")        
        if len(villes_utiles) == 0: return datas
        
        filter_research(session, villes_utiles)
        datas = get_pappers_datas(session)
        datas = get_active_companies(session, datas)
        datas = find_company_emails(session, datas)

        save_json(datas, "company_datas.json")
    finally:
        try:
            time.sleep(1)
        except Exception:
            pass
        session.close()
        
    return datas


if __name__ == "__main__":
    main([], [], [])