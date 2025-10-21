import os, time
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from data.services.filter_research_pappers import filter_research
from data.services.get_pappers_datas import get_pappers_datas
from data.utils.session import Session

def main() -> dict:
    data = {}
    session = Session()
    try:
        filter_research(session)
        names = get_pappers_datas(session)
    finally:
        try:
            time.sleep(1)
        except Exception:
            pass
        session.close()
        
    return data


if __name__ == "__main__":
    main()