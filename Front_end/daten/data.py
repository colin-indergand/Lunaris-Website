import requests
import pandas as pd

# 1. Einwohnerdaten von allen Ländern holen
url = "http://api.worldbank.org/v2/country/all/indicator/SP.POP.TOTL?format=json&date=2022&per_page=400"
data = requests.get(url).json()[1]

# 2. Umstrukturieren
results = []
for item in data:
    country = item["country"]["value"]
    iso2 = item["country"]["id"]
    value = item["value"]
    if value:  # Nur gültige Einträge
        results.append({"country": country, "iso2": iso2, "population": value})

# 3. Als JSON-Datei speichern
df = pd.DataFrame(results)
df.to_json("Front_end/daten/data.json", orient="records")
