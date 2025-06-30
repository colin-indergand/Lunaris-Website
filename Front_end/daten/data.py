import requests
import pandas as pd
import os

def fetch_indicator(indicator, year):
    url = f"http://api.worldbank.org/v2/country/all/indicator/{indicator}?format=json&date={year}&per_page=400"
    print("Lade:", url)
    data = requests.get(url).json()
    if len(data) < 2 or not data[1]:
        print(f"KEINE DATEN für {indicator} {year}")
        return {}
    return {item["country"]["id"]: item["value"] for item in data[1] if item["value"]}

def get_country_iso2_list():
    url = "http://api.worldbank.org/v2/country?format=json&per_page=400"
    data = requests.get(url).json()[1]
    return [item["id"] for item in data if item["region"] and item["region"]["id"] != "NA"]



year = 2021
pop = fetch_indicator("SP.POP.TOTL", year)
gdp = fetch_indicator("NY.GDP.MKTP.CD", year)
infl = fetch_indicator("FP.CPI.TOTL.ZG", year)
accounts = fetch_indicator("FX.OWN.TOTL.ZS", year)
unemp = fetch_indicator("SL.UEM.TOTL.ZS", year)

country_iso2 = get_country_iso2_list()

results = []
for wb_id, iso2 in country_iso2:
    results.append({
        "iso2": iso2,  # jetzt 2-stellig!
        "population": pop.get(wb_id),
        "gdp": gdp.get(wb_id),
        "inflation": infl.get(wb_id),
        "accounts": accounts.get(wb_id),
        "unemployment": unemp.get(wb_id)
    })
    
print("Ergebnis-Einträge:", len(results))
if not os.path.exists("Front_end/daten"):
    os.makedirs("Front_end/daten")
df = pd.DataFrame(results)
df.to_json("Front_end/daten/data.json", orient="records", force_ascii=False)
print("Fertig! Datei geschrieben.")