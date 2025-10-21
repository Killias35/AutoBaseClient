import os, time
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from data.utils.session import Session
from conf.utils.json_utils import save_json
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_pappers_datas(session: Session)-> list[str]:
    nb_company = session.driver.find_element(By.CSS_SELECTOR, 'p.color-entreprises').text.split(" ")[0]
    print(nb_company)
    company_names = []
    up = True
    tour = 0
    while len(company_names) < int(nb_company) and tour < 3:
        try:
            divs = WebDriverWait(session.driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.nom-entreprise')))
            names = [div.text for div in divs if not div.text in company_names]
            company_names.extend(names)
            next_page = session.driver.find_element(By.CLASS_NAME, 'pagination-image-right')
            previous_page = session.driver.find_element(By.CLASS_NAME, 'pagination-image-left')

            if next_page.tag_name == "a" and up:
                next_page.click()
            elif next_page.tag_name != "a" and up:
                up = False
                tour += 1
                print(len(company_names), "/", int(nb_company))
            elif previous_page.tag_name == "a" and not up:
                previous_page.click()
            elif previous_page.tag_name != "a" and not up:
                up = True
                print(len(company_names), "/", int(nb_company))
        except Exception as err:
            print(str(err))
            break

    print(len(company_names), "/", int(nb_company))
    save_json({"names": company_names}, "src/company_names.json")
    return company_names
    
