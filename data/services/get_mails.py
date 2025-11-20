import os, time
import sys
from urllib.parse import urlencode

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from data.utils.session import Session
from selenium.webdriver.common.by import By
import re, time

EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", re.IGNORECASE)

def search_duckduckgo(session: Session, query, max_results=5):
    url = "https://google.com/search"
    params = {"q": query}
    session.driver.get(f"{url}?{urlencode(params)}")
    time.sleep(2)
    links = []
    center = session.driver.find_element(By.ID, "center_col")
    for a in center.find_elements(By.TAG_NAME, "a"):
        href = a.get_attribute("href")
        if href and href.startswith("http"): # type: ignore
            links.append(href)
        if len(links) >= max_results:
            break
    return links

def quick_validate(email):
    # validations simples et rapides
    if " " in email: 
        return False
    local, _, domain = email.rpartition("@")
    if not local or not domain:
        return False
    if len(domain) > 253:
        return False
    if "." not in domain:
        return False
    # rejette caractères improbables
    if ".." in email:
        return False
    return True

def extract_emails_from_url(session: Session, url: str)->set[str]:
    try:
        session.driver.get(url)
        time.sleep(1)
        text = session.driver.page_source
        if "@" not in text:
            return set()
        idx = text.find("@")
        emails = set()
        while idx != -1:
            start = max(0, idx - 64)
            end = min(len(text), idx + 64)
            window = text[start:end]
            for m in EMAIL_RE.finditer(window):
                e = m.group(0).strip(".,;:()[]\"'<>").lower()  # clean trailing punctuation
                if quick_validate(e):
                    emails.add(e)
            idx = text.find("@", idx + 1)

        return set(emails)
    except Exception:
        return set()

def find_company_emails(session: Session, companies_datas: dict[str, dict[str, list[str]]])-> dict[str, dict[str, list[str]]]:
    """
    Prend ce type de dict
    {
        "nom d'entreprise": {
            "dirigeant": []
            "active": bool
    }

    et sort

    {
        "nom d'entreprise": {
            "dirigeant": [],
            "active": bool
            "emails": []
    }
    """
    results = {}
    for name, data in companies_datas.items():
        if not data["active"]:
            continue
        query = f"{name} mails"
        links = search_duckduckgo(session, query)
        found = set()
        for link in links:
            found |= extract_emails_from_url(session, link)
            time.sleep(1)
        data["emails"] = list(found)
        results[name] = data
    return results


if __name__ == "__main__":
    # Exemple
    session = Session()
    companies = {"ocap": {"dirigeant": [], "emails": [], "active": True}}
    print(find_company_emails(session, companies))
    session.close()
