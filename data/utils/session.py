import os, time
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
    
from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc
import logging

from conf.conf import HOME_URL

def getOptions(headless: bool = False):
    options = Options()
    if headless:
        options.add_argument("--headless=new")
    
    # options.add_argument(f"--user-data-dir={LOCAL_PROFILE_DIR }")
    # On utilise le profil "Default" à l’intérieur de ce dossier
    options.add_argument("--profile-directory=Default")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    
    options.add_argument("--disable-guest-mode")
    options.add_argument("--no-first-run")
    options.add_argument("--no-default-browser-check")
    
    options.add_argument("--disable-background-timer-throttling")
    options.add_argument("--disable-backgrounding-occluded-windows")
    options.add_argument("--disable-renderer-backgrounding")
    options.add_argument("--disable-dev-shm-usage")

    # Désactive les logs de Selenium lui-même (optionnel mais propre)
    logging.getLogger('selenium').setLevel(logging.CRITICAL)
    return options
    
    
class Session:
    def __init__(self, headless: bool = False):
        self.driver = uc.Chrome(version_main=140, options=getOptions(headless=headless), service_log_path="debug.log", use_subprocess=True)
        time.sleep(1)
        self.driver.get(HOME_URL)

    def close(self):
        # fermer proprement
        try:
            self.driver.quit()
        except Exception:
            pass


if __name__ == "__main__":
    session = Session()
    try:
        time.sleep(1000)
    finally:
        session.close()
