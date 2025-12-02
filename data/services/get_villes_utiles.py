import os, time
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from data.utils.session import Session
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from conf.conf import ANNUAIRE_EXPERT_COMPTABLE_URL, VILLE


def get_villes_utiles(session: Session, regions: list, departements: list, villes: list) -> list[str]:
    ret = list[str]()
    for region in regions:
        session.driver.get(ANNUAIRE_EXPERT_COMPTABLE_URL)
        time.sleep(1)
        try:
            link = session.driver.find_element(By.XPATH, f"//*[contains(text(), '{region}')]")
            link.click()
            time.sleep(1)

            for dep in departements:
                try:
                    link = session.driver.find_element(By.XPATH, f"//*[contains(text(), '{dep}')]")
                    link.click()
                    time.sleep(1)

                    for ville in villes:
                        try:
                            link = session.driver.find_element(By.XPATH, f"//*[contains(text(), '{ville}')]")
                            ret.append(ville)
                        except Exception:
                            print(f"Ville '{ville}' non trouvée dans l'annuaire!")
                except Exception:
                    print(f"Departement '{dep}' non trouvé dans l'annuaire!")
        except Exception:
            print(f"Region '{region}' non trouvée dans l'annuaire!")
    if (VILLE not in ret): ret.append(VILLE)
    return ret
    