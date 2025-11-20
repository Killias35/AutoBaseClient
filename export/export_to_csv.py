import os, time
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import csv
from conf.utils.json_utils import load_json

def export_to_csv(datas: dict, filename: str = "entreprises.csv"):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["entreprise", "emails"])
        for name, data in datas.items():
            active = data["active"]
            dirigeant = str(data["dirigeant"])
            emails = data["emails"]

            if not active:
                continue

            for email in emails:
                writer.writerow([name, email, dirigeant])
            
    print(f"✅ Fichier sauvegardé : {filename}")

if __name__ == "__main__":
    data = load_json("company_datas.json")
    export_to_csv(data)