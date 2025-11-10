import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from data.utils.session import Session
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from conf.conf import SOCIETE_COM_URL


def get_active_companies(session: Session, companies_datas: dict[str, dict[str, list[str]]])-> dict[str, dict[str, list[str]]]:
    results = {}
    for name, data in companies_datas.items():
        if this_company_still_exist(session, data):
            results[name] = data
    return results


def this_company_still_exist(session: Session, companies_datas: dict[str, list[str]])-> bool:
    session.driver.get(SOCIETE_COM_URL)
    input_bar = WebDriverWait(session.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="q"]')))
    input_bar.send_keys(companies_datas["name"][0])
    # envoyer aussi numero departement
    input_bar.send_keys(Keys.ENTER)
    list_box = WebDriverWait(session.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'ul[role="listbox"]')))
    lis = list_box.find_elements(By.TAG_NAME, "li")
    if len(lis) > 0:
        lis[0].click()
        section = WebDriverWait(session.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'section[id="identite"]')))
        active = False
        try:
            active = section.find_element(By.CLASS_NAME, "ui-tag is-Success") is not None
        except Exception:
            pass
        return active
    else:
        return False