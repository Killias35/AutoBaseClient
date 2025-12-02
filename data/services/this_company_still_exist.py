import os, time
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


def get_active_companies(session: Session, companies_datas: dict[str, dict])-> dict[str, dict]:
    """
    prend ce type de dict

    {
        "nom d'entreprise": {
            "dirigeant": [],
            "emails": []
    }

    et trie les entreprises qui sont encore en activités pour sortir

    {
        "nom d'entreprise": {
            "dirigeant": [],
            "emails": [],
            "active": True
    }
    """
    for name, data in companies_datas.items():
        if this_company_still_exist(session, name):
            data["active"] = True
            companies_datas[name] = data
        else:
            data["active"] = False
            companies_datas[name] = data
    return companies_datas


def this_company_still_exist(session: Session, name : str)-> bool:
    session.driver.get(SOCIETE_COM_URL)
    try:
        try:
            accept_cookies = WebDriverWait(session.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[id="didomi-notice-agree-button"]')))
            accept_cookies.click()
            time.sleep(1)
        except Exception:
            pass
        input_bar = WebDriverWait(session.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="q"]')))
        input_bar.send_keys(name)
        list_box = WebDriverWait(session.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'ul[id="serpSuggest"][role="listbox"]')))
        time.sleep(1)
        lis = WebDriverWait(session.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'li[role="option"]')))
        lis = list_box.find_elements(By.CSS_SELECTOR, 'li[role="option"]')
        if len(lis) > 0:
            lis[0].click() # type: ignore
            section = WebDriverWait(session.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'section[id="identite"]')))
            active = False
            try:
                active = section.find_element(By.CLASS_NAME, "ui-tag is-Success") is not None
            except Exception:
                pass
            print(f"{name} est encore en activités")
            return active
        else:
            print(f"{name} n'est plus en activités")
            return False
    except Exception:
        print(f"{name} n'est pas trouvée sur societecom -> en activité mis a 'oui' par defaut")
        return True