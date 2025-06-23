
#####################################################################################################################################################
#Allgemeine Finanziellen Grundlagen 
#####################################################################################################################################################

#Alle Bibliotheken importieren
import copy
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

#Aufbereitung der Web-Daten

#MSCI-World Rendite jährlich über die letzten 25y

data_msci_world_25y = [
    {"jahr": 1999, "preis": 1417.38}, {"jahr": 2000, "preis": 1300.79}, {"jahr": 2001, "preis": 1127.02}, {"jahr": 2002, "preis": 754.97}, {"jahr": 2003, "preis": 821.60}, 
    {"jahr": 2004, "preis": 860.32}, {"jahr": 2005, "preis": 1066.29}, {"jahr": 2006, "preis": 1125.09}, {"jahr": 2007, "preis": 1086.74}, {"jahr": 2008, "preis": 661.99}, 
    {"jahr": 2009, "preis": 814.43}, {"jahr": 2010, "preis": 954.19}, {"jahr": 2011, "preis": 910.99}, {"jahr": 2012, "preis": 1015.21}, {"jahr": 2013, "preis": 1205.42}, 
    {"jahr": 2014, "preis": 1412.89}, {"jahr": 2015, "preis": 1530.64}, {"jahr": 2016, "preis": 1660.32}, {"jahr": 2017, "preis": 1751.75}, {"jahr": 2018, "preis": 1648.04}, 
    {"jahr": 2019, "preis": 2101.04}, {"jahr": 2020, "preis": 2198.54}, {"jahr": 2021, "preis": 2841.84}, {"jahr": 2022, "preis": 2438.63}, {"jahr": 2023, "preis": 2868.37}, {"jahr": 2024, "preis": 3580.78}, 
]

data_msci_world_25y.sort(key=lambda x: x["jahr"])
prices = [entry["preis"]for entry in data_msci_world_25y]

yoy_returns = []
for i in range(len(prices) -1):
    ret = prices[i+1] / prices[i] -1
    yoy_returns.append(ret)

avg_return_msci_world_25y = sum(yoy_returns) / len(yoy_returns)

#MSCI-World Rendite jährlich über die letzten 15y

data_msci_world_15y = [
    {"jahr": 2009, "preis": 814.43}, {"jahr": 2010, "preis": 954.19}, {"jahr": 2011, "preis": 910.99}, {"jahr": 2012, "preis": 1015.21}, {"jahr": 2013, "preis": 1205.42}, 
    {"jahr": 2014, "preis": 1412.89}, {"jahr": 2015, "preis": 1530.64}, {"jahr": 2016, "preis": 1660.32}, {"jahr": 2017, "preis": 1751.75}, {"jahr": 2018, "preis": 1648.04}, 
    {"jahr": 2019, "preis": 2101.04}, {"jahr": 2020, "preis": 2198.54}, {"jahr": 2021, "preis": 2841.84}, {"jahr": 2022, "preis": 2438.63}, {"jahr": 2023, "preis": 2868.37}, {"jahr": 2024, "preis": 3580.78}, 
]

data_msci_world_15y.sort(key=lambda x: x["jahr"])
prices = [entry["preis"]for entry in data_msci_world_15y]

yoy_returns = []
for i in range(len(prices) -1):
    ret = prices[i+1] / prices[i] -1
    yoy_returns.append(ret)

avg_return_msci_world_15y = sum(yoy_returns) / len(yoy_returns)
avg_return_msci_world = (avg_return_msci_world_15y + avg_return_msci_world_25y) /2

#Inflationsberechnung über die letzten 25y

import pandas as pd

lik_data_path = os.path.join(BASE_DIR, "Datenquellen", "LIK_Data.csv")
data_inflation = pd.read_csv(lik_data_path, sep=';', decimal='.', header=0)

def parse_my_date(s):
    mon_str, year_str = s.split()
    month_map = {
        'Jan': 1, 'Feb': 2, 'Mär': 3, 'Apr': 4, 'Mai': 5, 'Jun': 6,
        'Jul': 7, 'Aug': 8, 'Sep': 9, 'Okt': 10, 'Nov': 11, 'Dez': 12
    }
    month = month_map[mon_str]
    year = int(year_str)
    if year < 50:  
        year += 2000
    else:
        year += 1900
    return pd.Timestamp(year, month, 1)


data_inflation['Date'] = data_inflation['indexDate'].apply(parse_my_date)

# 2) Index setzen und sortieren
data_inflation.set_index('Date', inplace=True)
data_inflation.sort_index(inplace=True)

# 3) Wir haben jetzt pro Monat einen 'indexValue'
#    -> Jahresdurchschnitt bilden
data_inflation['year'] = data_inflation.index.year
yearly_means = data_inflation.groupby('year')['indexValue'].mean()

inflation_yearly = yearly_means.pct_change() * 100
inflation_yearly.dropna(inplace=True)  # Erstes Jahr hat keinen Vorjahresvergleich

average_inflation = inflation_yearly.mean()

#Zinsen auf Spareinlagen in der Schweiz

data_saving_yield = [
    {"jahr": 1999, "zins": 1.23}, {"jahr": 2000, "zins": 1.41},  {"jahr": 2001, "zins": 1.49}, {"jahr": 2002, "zins": 1.18},  {"jahr": 2003, "zins": 0.62},  {"jahr": 2004, "zins": 0.51},  {"jahr": 2005, "zins":0.48 },  {"jahr": 2006, "zins": 0.48},
    {"jahr": 2007, "zins": 0.63}, {"jahr": 2008, "zins": 0.90},  {"jahr": 2009, "zins": 0.45}, {"jahr": 2010, "zins": 0.37},  {"jahr": 2011, "zins": 0.33},  {"jahr": 2012, "zins": 0.25},  {"jahr": 2013, "zins": 0.20},  {"jahr": 2014, "zins": 0.16},
    {"jahr": 2015, "zins": 0.08}, {"jahr": 2016, "zins": 0.06},  {"jahr": 2017, "zins": 0.05}, {"jahr": 2018, "zins": 0.04},  {"jahr": 2019, "zins": 0.04},  {"jahr": 2020, "zins": 0.03},  {"jahr": 2021, "zins": 0.02},  {"jahr": 2022, "zins": 0.02}, {"jahr": 2023, "zins": 0.46}
]

data_saving_yield.sort(key=lambda x: x["jahr"])
s_yield = [entry["zins"]for entry in data_saving_yield]
average_saving_yield = sum(s_yield) / len(s_yield)

#Jahr für Berechnungsgrundlagen
basic_year = 2025

#Rentendauer mit durchschn. Lebenserwartung
pension_age = 65
avg_lifespan = 84
pension_time = avg_lifespan - pension_age +1

#Jahrgang

def calculate_vintage(web_vintage_data):
    vintage = web_vintage_data
    if vintage == None:
        return 0
    return vintage

#Einkommen pro Altersklassen

def calculate_income(web_income_data):
    income_data = web_income_data
    filled_data = []
    if income_data:
        current_age = min(block["start_age"] for block in income_data)
        if income_data and isinstance(income_data[-1], dict):
            vermögen = income_data[-1].get("vermögen", 0)
        else:
            vermögen = 0
        for block in sorted(income_data, key=lambda x: x["start_age"]):
            if block["start_age"] > current_age:
                filled_data.append({
                    "start_age": current_age,
                    "end_age": block["start_age"] -1,
                    "income": 0,
                    "status": "nicht erwerbstätig",
                    "vermögen": vermögen
                })
            filled_data.append(block)
            current_age = block["end_age"] +1

    income_data = filled_data

    if income_data:
        last_block = income_data[-1]
        last_age = last_block["end_age"]
        if last_age < 65:
            income_data.append({
                "start_age": last_age +1,
                "end_age": 65,
                "income": last_block["income"],
                "status": last_block["status"],
                "vermögen": last_block["vermögen"]
            })

    if not income_data:
        income_data = [{
            "start_age": 0,
            "end_age": 0,
            "income": 0,
            "status": None,
            "vermögen": 0
        }]
        
    return income_data


def average_income(income_data):
    total_income = 0
    total_years = 0

    for i in income_data:
        min_year = i["start_age"]
        max_year = i["end_age"]
        income = i["income"]

        years = max_year - min_year +1
        total_income += income * years
        total_years += years
    
    if total_years == 0:
        avg_income = 0

    avg_income = total_income / years

    if avg_income == None:
        return 0

    return avg_income

#Summary
#Zur Berechnung verwendete durchschnittliche Rendite des MSCI-World welcher beide Aspekte kombiniert & einmal die Inflation auch berücksichtigt

####################################################################################################################################################
#AHV - Grundlagen
####################################################################################################################################################

#Beiträge Selbständige
self_employed_contrib = [
    {"income_min": 10100, "income_max": 17600, "contrib": 0.05371}, {"income_min": 17600, "income_max": 23000, "contrib": 0.05494}, {"income_min": 23000, "income_max": 25500, "contrib": 0.05617}, {"income_min": 25500, "income_max": 28000, "contrib": 0.05741}, {"income_min": 28000, "income_max": 30500, "contrib": 0.05864},
    {"income_min": 30500, "income_max": 33000, "contrib": 0.05987}, {"income_min": 33000, "income_max":35500, "contrib": 0.06235}, {"income_min": 35500, "income_max":38000, "contrib": 0.06481}, {"income_min": 38000, "income_max":40500, "contrib": 0.06728}, {"income_min": 40500, "income_max":43000, "contrib": 0.06976}, {"income_min": 43000, "income_max":45500, "contrib": 0.07222},
    {"income_min": 45500, "income_max":48000, "contrib": 0.07469}, {"income_min": 48000, "income_max":50500, "contrib": 0.07840}, {"income_min": 50500, "income_max":53000, "contrib": 0.08209}, {"income_min": 53000, "income_max":55500, "contrib": 0.0858}, {"income_min":55000 , "income_max":58000, "contrib": 0.08951}, {"income_min":58000 , "income_max":60500, "contrib": 0.09321}, {"income_min": 60500, "income_max": 10000000000000, "contrib": 0.10}
]

#Beiträge Angestellt
employee_contrib = 0.0435
employer_contrib = 0.0435

#Mindestbeiträge Nichterwärbstätige
min_yearly_contrib_path = os.path.join(BASE_DIR, "Datenquellen", "nichterwärbstätige_beiträge.xlsx")
data_min_yearly_contrib = pd.read_excel(min_yearly_contrib_path)
data_min_yearly_contrib.columns = ["vermögen", "einzahlung"]

#Rententabelle
rententabelle_path = os.path.join(BASE_DIR, "Datenquellen", "rententabelle_ahv.xlsx")
excel_file_ahv_pension = pd.ExcelFile(rententabelle_path)
sheet_names = excel_file_ahv_pension.sheet_names


#Min. / Maximaleinkommen
min_ahv_income = 15120
max_ahv_income = 90720
min_full_pension = 1260
max_full_pension = 2520

#Erziehungsgutschriften
pre_childcare_credits = (3*min_full_pension)*12

#Betreuungsgutschriften
pre_betreuungsgutschriften = (3*min_full_pension)*12

#Aufwertungsfaktor
aufwertungsfaktor_path = os.path.join(BASE_DIR, "Datenquellen", "aufwertungsfaktor_ahv.xlsx")
data_aufwertungsfaktor_ahv = pd.read_excel(aufwertungsfaktor_path)
data_aufwertungsfaktor_ahv.columns = ["jahrgang","aufwertungsfaktor"]

#Beitragsjahre
total_contrib_years = 44


#Beitragsjahre berechnen

def calculate_contrib_years(income_data, web_contrib_gap_years_data, web_contrib_gap_data):

    contrib_gap_years = web_contrib_gap_years_data

    contrib_years = total_contrib_years - contrib_gap_years

    contrib_gap = []
    start_y_gap = web_contrib_gap_data[0]["start_age"]
    end_y_gap = web_contrib_gap_data[0]["end_age"]

    contrib_gap.append({
        "start_year_gap": start_y_gap,
        "end_year_gap": end_y_gap
    })

    pre_contrib_data = copy.deepcopy(income_data)    

    gap_years = []
    for g in contrib_gap:
        gap_years += list(range(g["start_year_gap"], g["end_year_gap"] +1))
    
    contrib_data = []
    for block in pre_contrib_data:
        for year in range(block["start_age"], block["end_age"] +1):
            if year in gap_years:
                continue
            contrib_data.append({
                "start_age": year,
                "income": block["income"],
                "status": block["status"],
                "vermögen": block["vermögen"]
            })
    
    if not contrib_data:
        contrib_data = []
        contrib_data.append({
            "start_age": 0,
            "income": 0,
            "status": None,
            "vermögen": 0
        })
    
    if contrib_years == None:
        return 0
    
    return contrib_data, contrib_years

#Durchschn. Einkommen pro Beitragsjahr

def calculate_ahv_income(contrib_data, min_age, max_age):
    total_income = 0
    total_years = 0
    
    for i in contrib_data:
        if min_age <= i["start_age"] <= max_age:
            total_income += i["income"]
            total_years += 1

    if total_years == None:
        return 0
    else:
        avg_ahv_income = total_income / total_years
        
    return avg_ahv_income

#Beiträge Berechnen

def calculate_ahv_contrib(contrib_data, data_min_yearly_contrib, self_employed_contrib, employee_contrib, employer_contrib):
    contrib = []

    for i in contrib_data:
        results = {
            "year": i["start_age"],
            "status": i["status"],
            "income": i["income"],
            "total_contrib": 0, 
            "pers_contrib": 0,
            "employer_contrib": 0
        }

        if i["status"] == "angestellt":
            results["total_contrib"] = i["income"] * (employee_contrib + employer_contrib)
            results["pers_contrib"] = i["income"] * employee_contrib
            results["employer_contrib"] = i["income"] * employer_contrib

        elif i["status"] == "selbständig":
            for y in self_employed_contrib:
                if y["income_min"] <= i["income"] < y["income_max"]:
                    contrib_value = i["income"] * y["contrib"]
                    results["total_contrib"] = contrib_value
                    results["pers_contrib"] = contrib_value
                    
        elif i["status"] == "nicht erwärbstätig":
            user_vermögen = i["vermögen"]
            max_vermögen = data_min_yearly_contrib["vermögen"].max()

            if user_vermögen < 350000:
                contrib_value = data_min_yearly_contrib.iloc[0]["einzahlung"]
            elif user_vermögen > max_vermögen:
                contrib_value = data_min_yearly_contrib.iloc[-1]["einzahlung"]
            else:
                min_contrib = data_min_yearly_contrib[data_min_yearly_contrib["vermögen"] >= user_vermögen].iloc[0]
                contrib_value = min_contrib["einzahlung"]

            results["total_contrib"] = contrib_value
            results["pers_contrib"] = contrib_value
    
        contrib.append(results)

    total_contrib = sum(x["total_contrib"] for x in contrib)
    total_pers_contrib = sum(x["pers_contrib"] for x in contrib)
    total_employer_contrib = sum(x["employer_contrib"] for x in contrib)

    total_contrib_data = [{
        "total_contrib": total_contrib,
        "total_pers_contrib": total_pers_contrib,
        "total_employer_contrib": total_employer_contrib
    }]

    if not contrib:
        total_contrib_data =[{
            "total_contrib": 0,
            "total_pers_contrib": 0,
            "total_employer_contrib": 0
        }]

    return total_contrib_data

#Beziehungsstatus für Erz. / Plafonierung

def calculate_yearly_status(contrib_data, web_yearly_status_data):
    yearly_status_data = []

    for i in web_yearly_status_data:
        i_start_year = web_yearly_status_data[0]["start_age"]
        i_end_year = web_yearly_status_data[0]["end_age"]
        marriage_income = web_yearly_status_data[0]["income"]

        for year in range(i_start_year, i_end_year +1):
            yearly_status_data.append({
                "year": year,
                "marriage_income": marriage_income
            })
    
    current_age = contrib_data[-1]["start_age"]

    if yearly_status_data:
        last_entry = yearly_status_data[-1]
        last_year = last_entry["year"]

        if last_year < 65 and last_year +1 <= current_age:
            yearly_status_data = yearly_status_data

        elif last_year < 65 and last_entry["marriage_income"] > 0:
            for year in range(last_year +1, 66):
                yearly_status_data.append({
                    "year": year,
                    "marriage_income": last_entry["marriage_income"]
                })
    
    if not yearly_status_data:
        yearly_status_data.append({
            "year": 0,
            "marriage_income": 0
        })

    return yearly_status_data

#Erziehungsgutschriften

def calculate_childcare_credits(pre_childcare_credits, contrib_years, contrib_data, vintage, web_childcare_credits_has_childcren_data, web_childcare_credits_amount_children_data, web_childcare_credits_erziehungsberechtigt_data, web_childcare_credits_erziehungsberechtigt_children_data):
    childcare_credits = 0

    has_children = web_childcare_credits_has_childcren_data
    if has_children != "ja":
        return {
            "childcare_credits": 0,
            "childcare_credits_duration": 0,
            "start_year": None,
            "end_year": None,
            "childcare_credits_yearly": 0,
            "valid_childcare_years": []
        }


    num_children = web_childcare_credits_amount_children_data

    childcare_credit_data = []

    for i in web_childcare_credits_erziehungsberechtigt_data:
        child = i["child"]
        vintage_children = i["vintage"]
        erziehungsberechtigt = i["erziehungsberechtigt"]
        status = i["status"]

        start_y = vintage_children 
        end_y = start_y + 16

        if erziehungsberechtigt == "Ja":
            for year in range(start_y, end_y +1):
                if year not in contrib_data:
                    contrib_y = 0
                if status == "Gemeinsam":
                    contrib_y = pre_childcare_credits *0.5
                else:
                    contrib_y = pre_childcare_credits *1.0

                childcare_credit_data.append({
                    "child": i,
                    "vintage": vintage,
                    "year": year,
                    "contrib": contrib_y,
                    "status": status                    
                })

        else:
            for x in web_childcare_credits_erziehungsberechtigt_children_data:
                child = x["child"]
                start_year = x["start_age"]
                end_year = x["end_age"]
                status_yearly = x["status"]
                
                if child == i:
                    for year in range(start_y, end_y +1):
                        if year not in contrib_data:
                            contrib = 0
                        
                        if start_year <= year >= end_year:
                            if status_yearly == "Gemeinsam":
                                contrib_y = pre_childcare_credits *0.5
                            elif status_yearly == "Alleine":
                                contrib_y = pre_childcare_credits *1.0
                            else:
                                contrib_y = 0
                        else:
                            continue

                        childcare_credit_data.append({
                            "child": i,
                            "vintage": vintage,
                            "year": year,
                            "contrib": contrib_y,
                            "status": status_yearly
                        })
                        
                else:
                    continue
    
    minimum_credit_y = min(vintage_children)
    maximum_credit_y = max(vintage_children) +16

    max_contrib_per_year = []

    for year in range(minimum_credit_y, maximum_credit_y +1):
        contrib = [i["contrib"] for i in childcare_credit_data if i["year"] == year]
        contrib_per_year = max(contrib) if contrib else 0.0

        max_contrib_per_year.append({
            "year": year,
            "contrib": contrib_per_year
        })

    valid_childcare_years = [int(i["year"]) for i in max_contrib_per_year if i["contrib"] >0]
    
    childcare_credits = sum([i["contrib"] for i in max_contrib_per_year])       
    childcare_credits_duration = len([i["year"] for i in max_contrib_per_year])

    childcare_credits_yearly = childcare_credits / contrib_years 

    childcare_data = {
        "childcare_credits": childcare_credits,
        "childcare_credits_duration": childcare_credits_duration,
        "start_year": minimum_credit_y,
        "end_year": maximum_credit_y,
        "childcare_credits_yearly": childcare_credits_yearly,
        "valid_childcare_years": valid_childcare_years
    }

    if not childcare_data:
        childcare_data = {
            "childcare_credits": 0,
            "childcare_credits_duration": 0,
            "start_year": None,
            "end_year": None,
            "childcare_credits_yearly": 0,
            "valid_childcare_years": []
        }

    return childcare_data

#Betreuungsgutschriften

def calculate_betreuungsgutschriften(childcare_data, contrib_years, web_betreuungsgutschriften_has_data, web_bvg_betreuungsgutschriften_data):
    betreuungsgutschriften = 0
    betreuungsgutschriften_yearly = 0
    
    childcare_credits = childcare_data.get("valid_childcare_years", [])

    betreuungsgutschriften_anspruch = web_betreuungsgutschriften_has_data

    if betreuungsgutschriften_anspruch == "ja":
        for i in web_bvg_betreuungsgutschriften_data:
            start_year = i["start_age"]
            end_year = i["end_age"]
            contrib = 0

            for year in range(start_year, end_year +1):
                if year in childcare_credits:
                    pre_contrib = 0
                else:
                    pre_contrib = pre_betreuungsgutschriften
                
                contrib += pre_contrib

            betreuungsgutschriften += contrib

    else:
        betreuungsgutschriften = 0
        betreuungsgutschriften_yearly = 0

    betreuungsgutschriften_total = betreuungsgutschriften

    if betreuungsgutschriften_total > 0 and contrib_years > 0: 
        betreuungsgutschriften_yearly = betreuungsgutschriften_total / contrib_years
    
    else:
        betreuungsgutschriften_yearly = 0

    return betreuungsgutschriften_yearly

#Kombiniertes Einkommen

def calculate_combined_income(contrib_data, yearly_status_data, contrib_years):
    if yearly_status_data is None:
        yearly_status_data = []

    combined_income = []    

    for i in range(21, 65 +1):
        own_income = 0

        for x in contrib_data:
            if x["start_age"] == i:
                own_income = x["income"]
                break
        
        is_married = False
        partner_income = 0

        for s in yearly_status_data:
            if s["year"] == i:
                is_married = True
                partner_income = s["marriage_income"]
                break
        
        if is_married == True:
            combined = (own_income + partner_income) /2
        else:
            combined = own_income

        combined_income.append({
            "year": i,
            "combined_income": combined
        })

    total_income = sum(x["combined_income"] for x in combined_income)
    combined_average_income = total_income / contrib_years

    if not combined_average_income:
        return 0

    return combined_average_income

#Aufwertungsfaktor

def calculate_aufwertungsfaktor(combined_average_income, vintage):
    vintage = vintage
    row = data_aufwertungsfaktor_ahv.loc[data_aufwertungsfaktor_ahv["jahrgang"] == vintage]
    if row.empty:
        return combined_average_income
    factor = row["aufwertungsfaktor"].values[0]
    ahv_income = combined_average_income * factor

    if not ahv_income:
        return 0

    return ahv_income

#Rente anhand Tabelle berechnen

def calculate_pension(ahv_income, contrib_years):
    sheet_name = str(contrib_years)

    data_pension_ahv = excel_file_ahv_pension.parse(sheet_name=sheet_name)
    data_pension_ahv.columns = ["einkommen", "rente"]

    min_row = data_pension_ahv.iloc[0]
    min_pension = min_row["rente"]

    max_row = data_pension_ahv.dropna().iloc[-1]
    max_pension = max_row["rente"]

    if min_ahv_income <= ahv_income <= max_ahv_income:
        data_pension_ahv["diff"] = abs(data_pension_ahv["einkommen"] - ahv_income)
        single_pension = data_pension_ahv.loc[data_pension_ahv["diff"].idxmin()]["rente"]
        data_pension_ahv.dropna(subset=["diff"], inplace=True)
        return single_pension
    
    elif ahv_income <= min_ahv_income:
        single_pension = min_pension
        return single_pension
    
    elif ahv_income >= max_ahv_income:
        single_pension = max_pension
        return single_pension
    
    if not single_pension:
        return 0

#Rente plafonieren

def calculate_plafonierte_pension(single_pension, web_plafonierte_rente_data):
    married = web_plafonierte_rente_data

    if married == "ja":
        pension = single_pension * 0.75
    else:
        pension = single_pension

    if not pension:
        return 0
    
    return pension

#Deckungsgrad berechnen

def calculate_deckungsgrad(pension, total_contrib_data):
    total_contrib = sum(x["total_contrib"] for x in total_contrib_data)
    pers_contrib = sum(x["total_pers_contrib"] for x in total_contrib_data)
    employer_contrib = sum(x["total_employer_contrib"] for x in total_contrib_data)

    lifetime_pension = pension * 12 * pension_time

    if total_contrib > 0:
        deckungsgrad_total = total_contrib / lifetime_pension * 100
        deckungsgrad_pers = pers_contrib / lifetime_pension * 100
    else:
        deckungsgrad_total = 0
        deckungsgrad_pers = 0

    deckungsgrad_ahv = [{
        "deckungsgrad_total": round(deckungsgrad_total ,2),
        "deckungsgrad_pers": round(deckungsgrad_pers ,2),
        "total_contrib": round(total_contrib ,2),
        "pers_contrib": round(pers_contrib ,2),
        "employer_contrib": round(employer_contrib ,2)
    }]

    if not deckungsgrad_ahv:
        deckungsgrad_ahv.append({
            "deckungsgrad_total": 0,
            "deckungsgrad_pers": 0,
            "total_contrib": 0,
            "pers_contrib": 0,
            "employer_contrib": 0
        })

    return deckungsgrad_ahv


##################################################################################################################################################
#BVG - Grundlagen
####################################################################################################################################################

#BVG Beiträge

bvg_contrib = [
    {"min_alter": 25, "max_alter": 34, "contrib": 0.07}, {"min_alter": 35, "max_alter": 44, "contrib": 0.10}, {"min_alter": 45, "max_alter": 54, "contrib": 0.15}, {"min_alter": 55, "max_alter": 65, "contrib": 0.18}
]

#Grunddaten BVG 

min_bvg_income = 22680
max_bvg_income = 90720
koordinationsabzug = 26460
min_bvg_yield = 1.25
umwandlungssatz = 0.068

#BVG Einkommen berechnen

def calculate_bvg_income(income_age, min_age, max_age):
    total_income = 0
    total_years = 0
    
    for i in income_age:
        start = max(i["start_age"], min_age)
        end = min(i["end_age"], max_age)
        if start > end:
            continue

        income = i["income"]
        years = end - start +1
        total_income = income * years
        total_years +=years
    
    if total_years == 0:
        return 0
    
    avg_bvg_income = total_income / total_years

    if not avg_bvg_income:
        return 0
    
    return avg_bvg_income

#BVG Beiträge 

def calculate_bvg_contrib(income_data, bvg_contrib, koordinationsabzug, max_bvg_income, min_bvg_income, web_bvg_contrib_angestellt_spez_data, web_bvg_contrib_angestellt_data, web_bvg_contrib_selbständig_spez_data, web_bvg_contrib_selbständig_data):
    yearly_contrib_data = []  
    total_contrib = 0  

    bvg_spec_cond_angestellt = web_bvg_contrib_angestellt_spez_data
    bvg_paym_selb = web_bvg_contrib_selbständig_spez_data

    for i in income_data:
        start_age = i["start_age"]
        end_age = i["end_age"]
        income = i["income"]
        status = i["status"]

        for x in range(start_age, end_age +1):
            if x < 25:
                continue

            if status == "angestellt":
                for y in bvg_contrib:
                    contrib_min_age_a = y["min_alter"]
                    contrib_max_age_a = y["max_alter"]
                    contrib_perc_a = y["contrib"]

                    if bvg_spec_cond_angestellt == "Ja":
                        for z in web_bvg_contrib_angestellt_data:
                            spec_min_age_a = z["start_age"]
                            spec_max_age_a = z["end_age"]
                            spec_min_income_a = z["min_income"]
                            spec_max_income_a = z["max_income"]
                            spec_koordinationsabzug_a = z["koordinationsabzug"]
                            
                            if contrib_min_age_a <= x <= contrib_max_age_a:
                                if spec_min_age_a <= x <= spec_max_age_a:
                                    if spec_min_income_a <= income <= spec_max_income_a:
                                        calcul_income = income - spec_koordinationsabzug_a
                                        contrib = calcul_income * contrib_perc_a
                                    elif spec_min_income_a < income > spec_max_income_a:
                                        calcul_income = spec_max_income_a - spec_koordinationsabzug_a
                                        contrib = calcul_income * contrib_perc_a
                                    elif spec_min_income_a > income:
                                        contrib = 0
                    else:
                        if contrib_min_age_a <= x <= contrib_min_age_a:
                            if min_bvg_income <= income <= max_bvg_income:
                                calcul_income = income - koordinationsabzug
                                contrib = calcul_income * contrib_perc_a
                            elif min_bvg_income <= income > max_bvg_income:
                                calcul_income = max_bvg_income - koordinationsabzug
                                contrib = calcul_income *contrib_perc_a
                            elif min_bvg_income > income:
                                contrib = 0    
                        
            
            elif status == "selbständig":
                if bvg_paym_selb == "Ja":
                    for z in web_bvg_contrib_selbständig_data:
                        spec_min_age_s = z["start_age"]
                        spec_max_age_s = z["end_age"]
                        spec_min_income_s= z["min_income"]
                        spec_max_income_s = z["max_income"]
                        spec_koordinationsabzug_s = z["koordinationsabzug"]
                        spec_percentage_s = z["percentage"]

                        if spec_min_age_s <= x <= spec_max_age_s:
                            if spec_min_income_s <= income <= spec_max_income_s:
                                calcul_income = income - spec_koordinationsabzug_s
                                contrib = calcul_income * spec_percentage_s
                            elif spec_min_income_s < income >= spec_max_income_s:
                                calcul_income = spec_max_income_s - spec_koordinationsabzug_s
                                contrib = calcul_income * spec_percentage_s
                            elif spec_min_income_s > income:
                                contrib = 0
                else:
                    contrib = 0
            
            else:
                contrib = 0

            total_contrib += contrib
                        
            yearly_contrib_data.append({
                "year": x,
                "contrib": contrib,
                "gesamt_contrib": total_contrib
            })
    
    if not yearly_contrib_data:
        yearly_contrib_data.append({
            "year": 0,
            "contrib": 0,
            "gesamt_contrib": 0
        })

    return yearly_contrib_data

#BVG Zinssatz

def calculate_bvg_yield(web_bvg_yield_data):
    yearly_yield_dict = {}
    min_yearly_yield = 1.25
    
    for i in web_bvg_yield_data:
        start_y = i["start_age"]
        end_y = i["end_age"]
        yearly_yield = i["yield"]

        for x in range(start_y, end_y +1):
            if x < 25:
                continue
            yearly_yield_dict[x] = yearly_yield

    yearly_yield_list = []
    for y in range(25, 65 +1):
        yield_val = yearly_yield_dict.get(y, min_yearly_yield)
        yearly_yield_list.append({
            "year": y,
            "yield": yield_val
        })

    if not yearly_yield_list:
        yearly_yield_list.append({
            "year": 0,
            "yield": 0
        })

    return yearly_yield_list

#Vermögen Berechnen mit Zins

def calculate_bvg_capital(yearly_contrib_data, yearly_yield_list):
    total_bvg_assets = []
    bvg_assets = 0
    pension_age = 65

    yield_dict = {e["year"]: e["yield"] for e in yearly_yield_list}

    for e in yearly_contrib_data:
        year = e["year"]
        contrib = e["contrib"]

        if contrib == 0 or year not in yield_dict:
            continue

        bvg_yield = yield_dict[year]
        duration = pension_age - year +1

        bvg_assets += contrib * (1.0 + bvg_yield / 100.0) ** duration

        total_bvg_assets = [{
            "year": year,
            "asset": contrib,
            "total_asset": round(bvg_assets, 2)
        }]
    
    if not total_bvg_assets:
        total_bvg_assets.append({
            "year": 0,
            "asset": 0,
            "total_asset": 0
        })

    return total_bvg_assets

#BVG Pension berechnen

def calculate_bvg_pension(total_bvg_assets):
    bvg_assets = total_bvg_assets[-1]["total_asset"] if total_bvg_assets else 0

    pension_yearly = bvg_assets * umwandlungssatz
    pension_monthly = pension_yearly /12

    total_pension = pension_yearly * pension_time

    capital_monthly_pension = bvg_assets / pension_time / 12

    pension_data = {
        "pension_monthly": pension_monthly,
        "pension_yearly": pension_yearly, 
        "total_pension": total_pension,
        "kapitalbezug": bvg_assets,
        "capital_pension_monthly": capital_monthly_pension
    }

    if not pension_data:
        pension_data = {
            "pension_monthly": 0,
            "pension_yearly": 0,
            "total_pension": 0,
            "kapitalbezug": 0,
            "capital_pension_monthly": 0
        }

    return pension_data

#Deckungsgrad der BVG berechnen

def calculate_deckungsgrad_bvg(yearly_contrib_data, pension_data, income_data, web_bvg_deckungsgrad_data):
    total_pension = pension_data["total_pension"]
    total_contrib = yearly_contrib_data[-1]["gesamt_contrib"] if yearly_contrib_data else 0
    bvg_assets = pension_data["kapitalbezug"]

    if not total_contrib or total_pension or bvg_assets:
        deckungsgrad_data = {
            "deckungsgrad_rente": 0,
            "pers_percentage": 0,
            "total_contrib": 0,
            "pers_contrib": 0,
            "employer_contrib": 0,
            "zinszahlungen": 0
        }

        return deckungsgrad_data
    
    bvg_data = []

    for i in web_bvg_deckungsgrad_data:
        start_y_share = web_bvg_deckungsgrad_data["start_age"]
        end_y_share = web_bvg_deckungsgrad_data["end_age"]
        contrib_share = web_bvg_deckungsgrad_data["percentage"]

        for year in range(start_y_share, end_y_share +1):
            bvg_data.append({
                "year": year,
                "contrib_share": contrib_share / 100
        })

    income_data_new = []
    for data in income_data:
        start_year_data = data["start_age"]
        end_year_data = data["end_age"]
        status = data["status"]
        for year_status in range(start_year_data, end_year_data +1):
            income_data_new.append({
                "year": year_status,
                "status": status
            })
    
    pers_contrib = 0
    employer_contrib = 0
    default_contrib_share = 0.50

    status_by_year = {s["year"]: s["status"] for s in income_data_new}
    share_by_year = {x["year"]: x["contrib_share"] for x in bvg_data}

    for i in yearly_contrib_data:
        jahr = i["year"]
        contrib = i["contrib"]

        status = status_by_year.get(jahr)
        if status is None:
            continue

        share = share_by_year.get(jahr, default_contrib_share)

        if status == "angestellt":
            pers_contrib += contrib * share
            employer_contrib += contrib * (1-share)
        elif status == "selbständig":
            pers_contrib += contrib

    zinszahlungen = bvg_assets - total_contrib
    deckungsgrad_total = (100 / total_pension * bvg_assets)
    personal_perc = 100 / bvg_assets * pers_contrib

    deckungsgrad_data = {
        "deckungsgrad_rente": deckungsgrad_total,
        "pers_percentage": personal_perc,
        "total_contrib": total_contrib,
        "pers_contrib": pers_contrib,
        "employer_contrib": employer_contrib,
        "zinszahlungen": zinszahlungen,
    }
       
    return deckungsgrad_data

####################################################################################################################################################
#Private Vorsorge 
####################################################################################################################################################

#Letztes Einkommen berechnen

def calculate_last_income(income_data):
    yearly_last_income = income_data[-1]["income"]
    last_income = yearly_last_income / 12 

    if not last_income:
        return 0

    return last_income

#Gesamtrente aus 1. und 2. Säule berechnen

def calculate_pension_1_2(pension_data, pension):
    pension_bvg_monthly = pension_data["pension_monthly"]
    pension_capital_bvg_monthly = pension_data["capital_pension_monthly"]
    pension_ahv_monthly = pension

    total_pension_capital = float(pension_capital_bvg_monthly) + float(pension_ahv_monthly)
    total_pension = float(pension_bvg_monthly) + float(pension_ahv_monthly)

    total_pension_data = {
        "pension_bvg_capital_total": total_pension_capital,
        "pension_total": total_pension
    }

    if not total_pension_data:
        total_pension_data = {
            "pension_bvg_capital_total": 0,
            "pension_total": 0
        }

    return total_pension_data

#Wie viel Rente prozentual zum letzten Einkommen

def calculate_percentage_income(total_pension_data, last_income):
    last_income_monthly = last_income
    pension_capital = total_pension_data["pension_bvg_capital_total"]
    pension = total_pension_data["pension_total"]

    percentage_of_income_capital = 100 / last_income_monthly * pension_capital
    percentage_of_income = 100 / last_income_monthly * pension

    percentage_income_pension = {
        "perc_o_i_capital": percentage_of_income_capital,
        "perc_o_i": percentage_of_income
    }

    if not percentage_income_pension: 
        percentage_income_pension = {
            "perc_o_i_capital": 0,
            "perc_o_i": 0
        }

    return percentage_income_pension

#Nötige Pension um 100% zu erhalten berechnen

def calculate_necessary_pension(pension_time, total_pension_data, last_income, web_private_portfolio_amount_data):
    pension_capital = total_pension_data["pension_bvg_capital_total"]
    pension = total_pension_data["pension_total"]

    private_pension_capital = last_income - pension_capital
    private_pension = last_income - pension

    pre_necessary_pension_capital_portfolio = private_pension_capital * 12 * pension_time
    pre_necessary_pension_portfolio = private_pension * 12 * pension_time

    third_savings = web_private_portfolio_amount_data

    necessary_pension_capital_portfolio = pre_necessary_pension_capital_portfolio - third_savings
    necessary_pension_portfolio = pre_necessary_pension_portfolio - third_savings

    necessary_portfolio_data = {
        "necessary_portfolio_capital": necessary_pension_capital_portfolio,
        "necessary_portfolio": necessary_pension_portfolio
    }

    if not necessary_portfolio_data:
        necessary_portfolio_data = {
            "necessary_portfolio_capital": 0,
            "necessary_portfolio": 0
        }

    return necessary_portfolio_data

#Gewünschtes Portfolio 

def calculate_wished_monthly_pension(pension_time, total_pension_data, web_spec_monthly_payment_data, web_monthly_payment_data, web_private_portfolio_amount_data):
    pension_capital = total_pension_data["pension_bvg_capital_total"]
    pension = total_pension_data["pension_total"]

    private_savings = web_private_portfolio_amount_data

    spec_monthly_paym = web_spec_monthly_payment_data
    if spec_monthly_paym == "beliebig":
        monthly_pension = web_monthly_payment_data

        monthly_pension * 12
        total_pension_portfolio = monthly_pension * pension_time

        wanted_necessary_pension_capital_portfolio = total_pension_portfolio - (pension_capital + private_savings)
        wanted_necessary_pension_portfolio = total_pension_portfolio - (pension + private_savings)

        wanted_necessary_portfolio_data = {
            "wanted_necessary_portfolio_capital": wanted_necessary_pension_capital_portfolio,
            "wanted_necessary_portfolio": wanted_necessary_pension_portfolio
        }

        if not wanted_necessary_portfolio_data:
            wanted_necessary_portfolio_data = {
                "wanted_necessary_portfolio_capital": 0,
                "wanted_necessary_portfolio": 0
            }

        return wanted_necessary_portfolio_data
    
    else:
        return 0
        
#Zeitdauer für Sparrate

def time_for_saving_rate(vintage, basic_year, pension_age, web_saving_rate_data):
    sparrate =  web_saving_rate_data["input"]
    if sparrate == "ja":
        start_year_s = 18
        if pension_age <= (basic_year - vintage):
            end_year_s = pension_age
        elif pension_age > (basic_year - vintage):
            end_year_s = (basic_year - vintage)
    else: 
        start_year_s = web_saving_rate_data["start_age"]
        end_year_s = web_saving_rate_data["end_age"]

    years_savings_data = {
        "savings_starting_year": int(start_year_s),
        "savings_ending_year": int(end_year_s)
    }

    if not years_savings_data:
        years_savings_data = {
            "savings_starting_year": 0,
            "savings_ending_year": 0
        }

    return years_savings_data

#Gesamtportfolio berechnen anhand der nötigen Rente

def final_portfolio_annual(savings_rate, years_savings_data, annual_return, income_data):
    portfolio = 0.0
    start_savings = int(years_savings_data["savings_starting_year"])
    end_age_savings = int(years_savings_data["savings_ending_year"])

    income_data_help = []
    for data in income_data:
        start_year_data = data["start_age"]
        end_year_data = data["end_age"]
        income = data["income"]

        for year_status in range(start_year_data, end_year_data +1):
            income_data_help.append({
                "year": year_status,
                "income": income
            })
    
    for x in income_data_help:
        income = x["income"]
        jahr = x["year"]

        if start_savings <= jahr <= end_age_savings:
            deposit = income * savings_rate
            portfolio += deposit
            portfolio *= (1+annual_return)
                    
    return portfolio
    
#Sparrate für nötiges Portfolio mit verschiedenen Renditen
def required_savings_rate(target_portfolio, annual_return, income_data, years_savings_data, tol=1e-3, max_iter=100):
    target_portfolio = target_portfolio
    low, high = 0.0, 1.0  # Mögliche Sparquote zwischen 0% und 100%
    
    for _ in range(max_iter):
        mid = (low + high) / 2
        portfolio = final_portfolio_annual(mid, years_savings_data, annual_return, income_data)
        
        if abs(portfolio - target_portfolio) < tol:
            return mid  # Wir sind nahe genug am Ziel
        
        if portfolio < target_portfolio:
            low = mid  # Sparquote zu niedrig, erhöhen
        else:
            high = mid  # Sparquote zu hoch, senken

    return (low + high) / 2  # Rückgabe des Näherungswerts, falls max_iter erreicht ist


def calculate_total_ahv_income(ahv_income, childcare_credit_income, betreuungsgutschriften_income):
    total_ahv_income = ahv_income + childcare_credit_income + betreuungsgutschriften_income

    if not total_ahv_income:
        total_ahv_income = 0

    return total_ahv_income


def calculate_saving_rates(capital_inflation_msci_saving_rate_s, capital_inflation_bank_saving_rate_s, inflation_msci_saving_rate_s, inflation_bank_saving_rate_s, print_100_capital_msci_saving_rate_s):
    capital_inflation_msci_saving_rate_s = capital_inflation_msci_saving_rate_s *100
    capital_inflation_bank_saving_rate_s = capital_inflation_bank_saving_rate_s *100
    inflation_msci_saving_rate_s = inflation_msci_saving_rate_s *100
    inflation_bank_saving_rate_s = inflation_bank_saving_rate_s *100

    saving_rate_data = {
        "capital_inflation_msci_saving_rate": capital_inflation_msci_saving_rate_s,
        "capital_inflation_bank_saving_rate_s": capital_inflation_bank_saving_rate_s,
        "inflation_msci_saving_rate_s": inflation_msci_saving_rate_s,
        "inflation_bank_saving_rate_s": inflation_bank_saving_rate_s,
        "capital_msci_saving_rate": print_100_capital_msci_saving_rate_s
    }

    if not saving_rate_data:
        saving_rate_data = {
            "capital_inflation_msci_saving_rate": 0,
            "capital_inflation_bank_saving_rate_s": 0,
            "inflation_msci_saving_rate_s": 0,
            "inflation_bank_saving_rate_s": 0,
            "capital_msci_saving_rate": 0
        }

    return saving_rate_data


avg_saving_yield = average_saving_yield / 100 #Durchschnittlicher Bankzinssatz
avg_inflation = average_inflation /100 #Durchschnittliche Inflation
avg_msci_15y = avg_return_msci_world_15y #MSCI-World Rendite über die letzten 15 Jahre
avg_msci_25y = avg_return_msci_world_25y #MSCI-World Rendite über die letzten 25 Jahre
avg_msci = avg_return_msci_world #Durchschnittliche MSCI-World Rendite von 15 und 25 Jahre

avg_yearly_yield_incl_infl = avg_msci - avg_inflation #Durchschn. MSCI-World Rendite minus Inflation also reale Rendite
avg_saving_yield_incl_infl = avg_saving_yield - avg_inflation #Durchschn. Bankzinssatz minus Inflation, reale Sparrate


