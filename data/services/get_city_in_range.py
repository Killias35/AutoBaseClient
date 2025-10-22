import requests, zipfile, io, csv, math, collections

RAYON_KM = 30
BASE_URL = "https://download.geonames.org/export/dump/"

def load_geonames_data():
    """Télécharge et charge FR.zip + admin codes."""
    # --- Chargement des villes ---
    r = requests.get(BASE_URL + "FR.zip")
    with zipfile.ZipFile(io.BytesIO(r.content)) as z:
        with z.open("FR.txt") as f:
            lines = (line.decode("utf-8") for line in f)
            reader = csv.reader(lines, delimiter="\t")
            cities = []
            for row in reader:
                if len(row) < 12:
                    continue
                name, lat, lon = row[1], float(row[4]), float(row[5])
                feature, code_admin1, code_admin2 = row[7], row[10], row[11]
                if feature in ("PPL", "PPLA", "PPLC"):
                    cities.append((name, lat, lon, code_admin1, code_admin2))
    # --- Chargement des régions ---
    admin1 = {}
    r1 = requests.get(BASE_URL + "admin1CodesASCII.txt")
    for line in r1.text.splitlines():
        parts = line.split("\t")
        if len(parts) >= 2 and parts[0].startswith("FR."):
            admin1[parts[0].split(".")[1]] = parts[1]
    # --- Chargement des départements ---
    admin2 = {}
    r2 = requests.get(BASE_URL + "admin2Codes.txt")
    for line in r2.text.splitlines():
        parts = line.split("\t")
        if len(parts) >= 2 and parts[0].startswith("FR."):
            admin2[parts[0].split(".")[2]] = parts[1]
    return cities, admin1, admin2

def get_coords(ville, cities):
    for name, lat, lon, *_ in cities:
        if name.lower() == ville.lower():
            return lat, lon
    raise ValueError("Ville introuvable")

def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * \
        math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    return 2 * R * math.asin(math.sqrt(a))

def villes_autour(ville):
    cities, admin1, admin2 = load_geonames_data()
    lat, lon = get_coords(ville, cities)
    proches = []
    for n, la, lo, a1, a2 in cities:
        if not a2:  # pas de département => ignorer
            continue
        d = haversine(lat, lon, la, lo)
        if d <= RAYON_KM and n.lower() != ville.lower():
            region = admin1.get(a1, None)
            departement = admin2.get(a2, None)
            if region is None or departement is None:
                continue
            proches.append((n, d, region, departement))
    proches.sort(key=lambda x: x[1])
    return proches


def trier_par_region_departement(villes):
    """
    Trie les villes trouvées par région, puis département.
    Retourne {region: {departement: [(ville, distance), ...]}}.
    """
    regroupement = collections.defaultdict(lambda: collections.defaultdict(list))
    for nom, d, region, dep in villes:
        regroupement[region][dep].append((nom, d))
    for reg in regroupement:
        for dep in regroupement[reg]:
            regroupement[reg][dep].sort(key=lambda x: x[1])
    return regroupement

if __name__ == "__main__":
    ville = input("Ville de départ : ")
    resultats = villes_autour(ville)
    groupes = trier_par_region_departement(resultats)
    for region, deps in groupes.items():
        print(f"\n=== {region} ===")
        for dep, villes in deps.items():
            print(f"  {dep}:")
            for nom, d in villes:
                print(f"    - {nom} ({d} km)")
