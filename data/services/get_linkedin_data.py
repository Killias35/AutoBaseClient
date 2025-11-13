import os, time
import sys
from urllib.parse import urlencode

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from data.utils.session import Session
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys

BASE_URL = "https://www.linkedin.com/feed/"

def find_company(session, name)-> bool:
    try:
        session.driver.get(BASE_URL)
        search_btn = session.driver.find_element(By.CSS_SELECTOR, "button[aria-label='Cliquez pour lancer une recherche']").click()
        search_bar = session.driver.find_element(By.CSS_SELECTOR, "input[placeholder='Rechercher']")
        search_bar.send_keys(name)
        search_bar.send_keys(Keys.ENTER)
        time.sleep(1)
        return True
    except Exception:
        return False

def get_linkedin_data(session, companies):
    for company in companies:
        if companies[company]["active"]:
            if find_company(session, company):
                pass


if __name__ == "__main__":
    # Exemple
    session = Session()
    companies = {"ocap": {"dirigeant": [], "emails": [], "active": True}}
    print(get_linkedin_data(session, companies))
    session.close()
