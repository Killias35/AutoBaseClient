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

def get_pappers_datas(session: Session)-> dict[str, dict[str, list[str]]]:
    """
    Renvoie une liste de nom d'entreprise
    """
    nb_company = session.driver.find_element(By.CSS_SELECTOR, 'p.color-entreprises').text.split(" ")[0]
    print(nb_company)
    company_names = []
    company_links = []
    datas = {}
    up = True
    tour = 0
    while len(company_names) < int(nb_company) and tour < 3:
        try:
            a = WebDriverWait(session.driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.nom-entreprise a')))
            names = [link.text for link in a if not link.text in company_names]
            links = [link.get_attribute("href") for link in a if not link.get_attribute("href") in company_links]
            company_names.extend(names)
            company_links.extend(links)
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
    
    for i in range(len(company_names)):
        link = company_links[i]
        name = company_names[i]
        session.driver.get(link)
        time.sleep(.5)
        td = WebDriverWait(session.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'info-dirigeant')))
        dirigeants = td.find_elements(By.TAG_NAME, 'a')
        lst = []
        for dirigeant in dirigeants:
            if "dirigeant" in str(dirigeant.get_attribute("href")):
                lst.append("Dirigeant " + dirigeant.text)
            else:
                lst.append("Pas un dirigeant " + dirigeant.text)
        datas[name] = {"dirigeants": lst}


    save_json({"datas": datas}, "src/company_names.json")
    return datas
    
