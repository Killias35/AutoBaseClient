import os, time
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import csv
from conf.utils.json_utils import load_json

mails_format = ["{prenom}.{nom}@gmail.com", "{prenom}@gmail.com", "{prenom1}{nom}@gmail.com", "{prenom1}.{nom}@gmail.com"]

def reconstruct_emails(dirigeant: str)-> list[str]:
    emails = []
    try:
        if "Pas un dirigeant" in dirigeant: return emails
        else:
            txt = dirigeant.split(" ")[1:]
            nom, prenom = txt[0], txt[1]
            prenom1 = prenom[0]
            for mails in mails_format:
                emails.append(mails.format(prenom=prenom, prenom1=prenom1, nom=nom).lower())
    except:
        pass
    return emails

def export_to_csv(datas: dict, filename: str = "entreprises.csv"):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["ENTREPRISE", "EMAIL", "DIRIGEANT"])
        for name, data in datas.items():
            active = data["active"]
            dirigeants = data["dirigeants"]
            emails = data["emails"]

            if not active:
                continue
            for dirigeant in dirigeants:
                new_mails = reconstruct_emails(dirigeant)
                if new_mails != []: 
                    writer.writerow([name, new_mails, dirigeant])
                else:
                    writer.writerow([name, "", dirigeant])

            for email in emails:
                writer.writerow([name, email, ""])
            
            writer.writerow(["XXXXXX", "XXXXXX", "XXXXXX"])
            
    print(f"✅ Fichier sauvegardé : {filename}")

if __name__ == "__main__":
    data = load_json("company_datas.json")
    export_to_csv(data)