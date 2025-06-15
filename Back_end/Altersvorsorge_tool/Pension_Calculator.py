
#####################################################################################################################################################
#Allgemeine Finanziellen Grundlagen 
#####################################################################################################################################################

#Alle Bibliotheken importieren
import copy

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

data_inflation = pd.read_csv(r"C:\Users\colin\OneDrive\Documents\Desktop\Lunaris\Website\Back_end\Altersvorsorge_tool\Datenquellen\LIK_Data.csv", sep=';', decimal='.', header=0)

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
    return vintage

#Einkommen pro Altersklassen

def calculate_income(web_income_data):
    income_data = web_income_data
    #Falls es kein Input in einigen Jahren gibt, wird es mit Einkommen = 0 CHF aufgefüllt.
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

    #Auffüllen, falls letztes Einkommensjahr < 65 Jahren mit letzten Eintrag bis 65 zur Pension
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

    print(f"\nEINKOMMENSDATEN: {income_data}")
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
data_min_yearly_contrib = pd.read_excel(r"C:\Users\colin\OneDrive\Documents\Desktop\Lunaris\Website\Back_end\Altersvorsorge_tool\Datenquellen\nichterwärbstätige_beiträge.xlsx")
data_min_yearly_contrib.columns = ["vermögen", "einzahlung"]

#Rententabelle
excel_file_ahv_pension = pd.ExcelFile(r"C:\Users\colin\OneDrive\Documents\Desktop\Lunaris\Website\Back_end\Altersvorsorge_tool\Datenquellen\rententabelle_ahv.xlsx")
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
data_aufwertungsfaktor_ahv = pd.read_excel(r"C:\Users\colin\OneDrive\Documents\Desktop\Lunaris\Website\Back_end\Altersvorsorge_tool\Datenquellen\aufwertungsfaktor_ahv.xlsx")
data_aufwertungsfaktor_ahv.columns = ["jahrgang","aufwertungsfaktor"]

#Beitragsjahre
total_contrib_years = 44


#Beitragsjahre berechnen

def calculate_contrib_years(income_data, web_contrib_gap_years_data, web_contrib_gap_data):

    contrib_gap_years = web_contrib_gap_years_data

    contrib_years = total_contrib_years - contrib_gap_years

    contrib_gap = []
    start_y_gap = web_contrib_gap_data["start_age"]
    end_y_gap = web_contrib_gap_data["end_age"]

    contrib_gap.append({
        "start_year_gap": start_y_gap,
        "end_year_gap": end_y_gap
    })

    pre_contrib_data = copy.deepcopy(income_data)    

    gap_years = []
    for i in contrib_gap:
        gap_years += list(range(i["start_year_gap"], i["end_year_gap"] +1))
    
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

    print(f"\nBEITRAGSJAHRE: {contrib_data}, {contrib_years}")
    return contrib_data, contrib_years

#Durchschn. Einkommen pro Beitragsjahr

def calculate_ahv_income(contrib_data, min_age, max_age):
    total_income = 0
    total_years = 0
    
    for i in contrib_data:
        if min_age <= i["start_age"] <= max_age:
            total_income += i["income"]
            total_years += 1

    if total_years == 0:
        return 0
    else:
        average_income = total_income / total_years
        print(f"\nAHV AHV Income: {average_income}")
    
    return average_income

#Beiträge Berechnen

def calculate_ahv_contrib(contrib_data, data_min_yearly_contrib, self_employed_contrib, employee_contrib, employer_contrib, contrib_years):
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

    print(f"\nAHV BEITRÄGE: {total_contrib_data}")
    return total_contrib_data

#Beziehungsstatus für Erz. / Plafonierung

def calculate_yearly_status(contrib_data):
    yearly_status_data = []

    while True:
        i_start_year = input("Ab welchem Alter galt dieses Einkommen?\n").strip().lower()
        if i_start_year == "stop":
            break
        i_start_year = int(i_start_year)

        i_end_year = input("Bis zu welchem Alter galt dieses Einkommen?\n").strip().lower()
        if i_end_year == "stop":
            break
        i_end_year = int(i_end_year)

        marriage_income = input("Was war das Einkommen Ihrer Partnerin. - mit 'stop' können sie\n").strip().lower()
        if marriage_income == "stop":
            break
        marriage_income = int(marriage_income)

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
        
        print(f"\nVERHEIRATET: {yearly_status_data}")
        return yearly_status_data

#Erziehungsgutschriften

def calculate_childcare_credits(yearly_status_data, contrib_years, vintage):
    childcare_credits = 0
    has_children = input("Haben Sie Kinder (ja/nein)\n").strip().lower()
    if has_children != "ja":
        return {
            "childcare_credits": 0,
            "childcare_credits_duration": 0,
            "start_year": None,
            "end_year": None
        }
    try:
        num_children = int(input("Wie viele Kinder haben Sie\n"))
    except ValueError:
        print("Ungültige Eingabe - Bitte geben Sie eine Zahl ein.")
        return {
            "childcare_credits": 0,
            "childcare_credits_duration": 0,
            "start_year": None,
            "end_year": None
        }

    vintage_children = []
    for i in range(num_children):
        try:
            jahrgang = int(input(f"Geben Sie den Jahrgang des {i+1}. Kindes ein. (z.B. 2012)\n"))
            vintage_children.append(jahrgang)
        except ValueError:
            print("Ungültiger Jahrgang - Bitte eine Zahl eingeben")
            return {
                "childcare_credits": 0,
                "childcare_credits_duration": 0,
                "start_year": None,
                "end_year": None
            }
        
    if not vintage_children:
        return {
            "childcare_credits": 0,
            "childcare_credits_duration": 0,
            "start_year": None,
            "end_year": None
        }
       
    age_difference = abs(max(vintage_children) - min(vintage_children)) +1
    childcare_credits_duration = age_difference +16
    start_children = min(vintage_children)
    end_childcare_year = start_children + childcare_credits_duration

    m_start_children = start_children - vintage
    m_end_childcare = end_childcare_year - vintage

    yearly_status_data = yearly_status_data or []

    full_status = []
    for year in range(m_start_children, m_end_childcare +1):
        status = "single"
        for m in yearly_status_data:
            if m["year"] == year:
                status = "married"
                break
        full_status.append((year, status))

    stages = []
    if full_status:
        prev_status = full_status[0][1]
        start = full_status[0][0]

        for idx in range(1, len(full_status)):
            year, status = full_status[idx]
            if status != prev_status:
                stages.append({
                    "start": start,
                    "end": full_status[idx-1][0],
                    "status": prev_status
                })
                start = year
                prev_status = status

        stages.append({
            "start": start,
            "end": full_status[-1][0],
            "status": prev_status
        })

        print(f"{stages}")
    
    for x in stages:
        duration = x["end"] - x["start"] +1
        credits = 0

        if x["status"] == "single":
            credit_right = input(f"Waren Sie während Ihrer Zeit {x['start']}-{x['end']} alleine erziehungsberechetigt? (ja/nein)\n").strip().lower()
            if credit_right == "ja":
                credits = pre_childcare_credits * duration

        elif x["status"] == "married":
            credit_right = input(f"Waren Sie in den Jahren als Sie verheiratet waren {x['start']}-{x['end']} beide erziehungsberechtigt? (ja/nein)\n").strip().lower()
            if credit_right == "ja":
                credits = (pre_childcare_credits * duration) /2
            elif credit_right == "nein":
                try:
                    years_right = int(input(f"Wie viele Jahre waren Sie von Ihrer {duration} erziehungsberechtigt\n"))
                    if 0 <= years_right <= duration:
                        years_single = duration - years_right 
                        credits = pre_childcare_credits * years_single
                except ValueError:
                    print("Geben Sie eine Zahl für die Anzahl Jahre ein.")
                    continue
        
        childcare_credits += credits
        
        if childcare_credits == 0:
            childcare_credits_monthly = 0
        else:
            childcare_credits_monthly = childcare_credits / contrib_years
    
    childcare_data = {
        "childcare_credits": childcare_credits,
        "childcare_credits_duration": childcare_credits_duration,
        "start_year": start_children,
        "end_year": end_childcare_year,
        "childcare_credits_yearly": childcare_credits_monthly
    }

    print(f"\nCHILDCARE CREDITS: {childcare_data}")
    return childcare_data

#Betreuungsgutschriften

def calculate_betreuungsgutschriften(childcare_data, contrib_years):
    end_year = childcare_data["end_year"] 
    start_year = childcare_data["start_year"]

    betreuungsgutschriften_anspruch = input("Haben Sie anspruch auf Betreuungsgutschrfiten. (ja/nein)\n").lower()
    if betreuungsgutschriften_anspruch == "ja":
        try:
            betreuunsgutschriften_jahre = int(input("Wie viele Jahre hatten Sie Anspruch auf Betreuungsgutschriften?\n"))
            betreuungsgutschrift_start = int(input("Ab welchem Jahr haben Sie Anspruch auf Betreuungsgutschriften?\n"))
            
            anspruch_end = betreuungsgutschrift_start + betreuunsgutschriften_jahre -1

            if end_year or start_year == 0:
                betreuungsgutschriften = betreuunsgutschriften_jahre * pre_betreuungsgutschriften
            else:
                if betreuungsgutschrift_start >= start_year:
                    if anspruch_end <= end_year:
                        betreuungsgutschriften = 0
                    elif anspruch_end > end_year:
                        overlaptime = anspruch_end - end_year +1
                        betreuungsgutschriften = overlaptime * pre_betreuungsgutschriften
                elif betreuungsgutschrift_start < start_year:
                    if anspruch_end <= end_year:
                        overlaptime = start_year - betreuungsgutschrift_start +1
                        betreuungsgutschriften = overlaptime * pre_betreuungsgutschriften
                    elif anspruch_end > end_year:
                        overlaptime_1 = start_year - betreuungsgutschrift_start +1
                        overlaptime_2 = anspruch_end - end_year +1
                        betreuungsgutschrift_start = (overlaptime_1+overlaptime_2) * pre_betreuungsgutschriften
    
            betreuungsgutschriften_yearly = betreuungsgutschriften / contrib_years
            print(f"\nBETREUUNGSGUTSCHRFITEN: {betreuungsgutschriften_yearly }")
            return betreuungsgutschriften_yearly
                
        except ValueError:
            print("Geben Sie eine gültige Zahl ein")
            betreuungsgutschriften_yearly = 0
            return betreuungsgutschriften_yearly
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

    print(f"\nCOMBINED AVERAGE INCOME: {combined_average_income}")
    return combined_average_income

#Aufwertungsfaktor

def calculate_aufwertungsfaktor(combined_average_income, vintage):
    try:
        vintage = vintage
        row = data_aufwertungsfaktor_ahv.loc[data_aufwertungsfaktor_ahv["jahrgang"] == vintage]
        if row.empty:
            return combined_average_income
        factor = row["aufwertungsfaktor"].values[0]
        ahv_income = combined_average_income * factor
        print(f"\nEINKOMMEN NACH AUFWERTUNGSFAKTOR: {ahv_income}")
        return ahv_income

    except ValueError:
        print("Geben Sie eine Zahl ein.")

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
        print(f"\nEINZLNE RENTE: {single_pension}")
        return single_pension
    
    elif ahv_income <= min_ahv_income:
        single_pension = min_pension
        print(f"\nEINZELNE RENTE: {single_pension}")
        return single_pension
    
    elif ahv_income >= max_ahv_income:
        single_pension = max_pension
        print(f"\nEINZELNE RENTE: {single_pension}")
        return single_pension

#Rente plafonieren

def calculate_plafonierte_pension(single_pension, contrib_data):
    married = input("Sind Sie aktuell verheiratet? (ja/nein)\n").lower()

    if married == "ja":
        pension = single_pension * 0.75
    else:
        pension = single_pension

    print(f"\nPLAFONIERTE RENTE: {pension}")
    return pension

#Deckungsgrad berechnen

def calculate_deckungsgrad(pension, total_contrib_data):
    total_contrib = sum(x["total_contrib"] for x in total_contrib_data)
    pers_contrib = sum(x["total_pers_contrib"] for x in total_contrib_data)
    employer_contrib = sum(x["total_employer_contrib"] for x in total_contrib_data)

    lifetime_pension = pension * 12 * pension_time
    print(f"{lifetime_pension}")
    print(f"{total_contrib}")

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

    print(f"\nDECKUNGSGRAD AHV: {deckungsgrad_ahv}")
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
    print(f"\nBVG AVG INCOME: {avg_bvg_income}")
    return avg_bvg_income

#BVG Beiträge 

def calculate_bvg_contrib(income_data, bvg_contrib, koordinationsabzug, max_bvg_income, min_bvg_income):
    yearly_contrib_data = []  
    total_contrib = 0  

    status = set(entry["status"] for entry in income_data) 

    if "angestellt" in status:
        spec_conditions_bvg = input("Hatten Sie spezielle BVG-Konditionen, welche nicht dem gesetzlichen Standards entsprachen (überobligatorische Verischerung, Aufteilung BVG-Beiträge...)\n").lower()
        if spec_conditions_bvg == "ja":
            max_bvg_income = float(input("Was war Ihr maximal versichertes Einkommen\n"))      
            koordinationsabzug = float(input("Was war Ihr Koordinationsabzug\n"))
            min_bvg_income = float(input("Was war Ihr minimal versichertes Einkommen?\n"))
        elif spec_conditions_bvg == "nein":
            max_bvg_income = max_bvg_income
            koordinationsabzug = koordinationsabzug
            min_bvg_income = min_bvg_income

    if "selbständig" in status:
        bvg_paym = input("Haben Sie während Ihrer Selbständigkeit BVG-Beiträge bezahlt? (ja/nein)\n").strip().lower()
        if bvg_paym == "ja":
            year = input("Haben Sie jedes Jahr BVG-Beiträge während Ihrer Selbständigkeit bezahlt?\n").strip().lower()
            if year == "ja":
                koordinationsabzug_self = float(input("Was war der Koordinationsabzug\n"))
                min_bvg_income_self = float(input("Was war das minimal versicherte Einkommen\n"))
                max_bvg_income_self = float(input("Was war das maximal versicherte Einkommen\n"))
            else:
                bvg_self_employed_data = []

                while True:
                    start_year_self = input("Mit welchem Alter haben Sie in der Selbständigkeit BVG-Beiträge bezahlt\n").lower()
                    if start_year_self == "stop":
                        break  
                    start_age = float(start_year_self)
                    end_age = float(input("Bis zu welchem Alter haben Sie Beiträge bezahlt?\n"))
                    koordinationsabzug_self = float(input("Was war der Koordinationsabzug\n"))
                    min_bvg_income_self = float(input("Was war das minimal versicherte Einkommen\n"))
                    max_bvg_income_self = float(input("Was war das maximal versicherte Einkommen\n"))   

                    bvg_self_employed_data.append({
                        "start_age": start_age,
                        "end_age": end_age,
                        "koordinationsabzug": koordinationsabzug_self,
                        "min_vers_income": min_bvg_income_self,
                        "max_vers_income": max_bvg_income_self
                    })                  

    for i in income_data:
        start_age = i["start_age"]   
        end_age = i["end_age"]     
        income = i["income"]
        status = i["status"]

        for x in range(start_age, end_age +1):
            if x < 25:
                continue

            if status == "angestellt":
                for c in bvg_contrib:
                    contrib_min_age = c["min_alter"]
                    contrib_max_age = c["max_alter"]
                    contrib_perc = c["contrib"]
                    
                    if contrib_min_age <= x <= contrib_max_age:
                        if min_bvg_income <= income <= max_bvg_income:
                            calcul_income = income - koordinationsabzug
                            contrib = calcul_income * contrib_perc
                        elif min_bvg_income <= income > max_bvg_income:
                            calcul_income = max_bvg_income - koordinationsabzug
                            contrib = calcul_income *contrib_perc
                        elif min_bvg_income > income:
                            contrib = 0                            


            elif status == "selbständig":
                if bvg_paym == "ja":
                    for c in bvg_contrib:
                        contrib_min_age = c["min_alter"]
                        contrib_max_age = c["max_alter"]
                        contrib_perc = c["contrib"]
                        
                        if year == "ja":
                            if contrib_min_age <= x <= contrib_max_age:
                                if min_bvg_income_self <= income < max_bvg_income_self:
                                    calcul_income = income - koordinationsabzug_self
                                    contrib = calcul_income * contrib_perc
                                elif min_bvg_income_self <= income > max_bvg_income_self:
                                    calcul_income = max_bvg_income_self - koordinationsabzug_self
                                    contrib = calcul_income * contrib_perc
                                else:
                                    contrib = 0  
                            else:
                                    contrib = 0
                        else:
                            for m in bvg_self_employed_data:
                                bvg_start_age = m["start_age"]
                                bvg_end_age = m["end_age"]
                                koordinationsabzug = m["koordinationsabzug"]
                                min_bvg_income_self = m["min_vers_income"]
                                max_bvg_income_self = m["max_vers_income"]

                                if contrib_min_age <= x <= contrib_max_age and bvg_start_age <= x <= bvg_end_age:
                                    if min_bvg_income_self <= income <= max_bvg_income_self:
                                        calcul_income = income - koordinationsabzug_self
                                        contrib = calcul_income * contrib_perc
                                    elif min_bvg_income_self <= income > max_bvg_income_self:
                                        calcul_income = max_bvg_income_self - koordinationsabzug_self
                                        contrib = calcul_income * contrib_perc
                                    elif min_bvg_income_self > income:
                                        contrib = 0
                                else:
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

    print(f"\nCONTRIB BVG: {yearly_contrib_data}")
    return yearly_contrib_data

#BVG Zinssatz

def calculate_bvg_yield():
    yearly_yield_dict = {}
    min_yearly_yield = 1.25

    while True:
        start_y = input("Von welchem Alter galt der Zinssatz? mit stop beenden\n")
        if start_y == "stop":
            break
        start_y = int(start_y)
        end_y = int(input("Bis zu welchem Alter galt dieser Zins\n"))
        yearly_yield = float(input("Was war der jährliche Zinssatz welcher Ihre PK auszahlte pro Jahr?\n"))

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

    print(f"\nBVG ZINS: {yearly_yield_list}")
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

    print(f"\nBVG Vermögen: {bvg_assets}")
    return total_bvg_assets

#BVG Pension berechnen

def calculate_bvg_pension(total_bvg_assets):
    bvg_assets = total_bvg_assets[-1]["total_asset"]

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

    print(f"\nPENSION BVG: {pension_data}")
    return pension_data

#Deckungsgrad der BVG berechnen

def calculate_deckungsgrad_bvg(yearly_contrib_data, pension_data, income_data):
    total_pension = pension_data["total_pension"]
    total_contrib = yearly_contrib_data[-1]["gesamt_contrib"]
    bvg_assets = pension_data["kapitalbezug"]

    bvg_data = []

    while True:
        start_y_share = input("Wann startete diese Aufteilung? (z.B. 25 oder stop)\n").lower() 
        if start_y_share == "stop":
            break
        try:
            start_y_share = int(start_y_share)
            end_y_share = int(input("Wann stoppte diese Zeitdauer?\n"))
            contrib_share = float(input("Wie viel % zahlten Sie der gesamten BVG-Beiträge (z.B. 50, 40, 0)?\n"))

            for year in range(start_y_share, end_y_share +1):
                bvg_data.append({
                    "year": year,
                    "contrib_share": contrib_share / 100
            })
        except ValueError:
            print("Ungültige Eingabe. Bitte erneut versuchen.\n")

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

    print(f"\nDECKUNGSGRAD BVG: {deckungsgrad_data}")
        
    return deckungsgrad_data

####################################################################################################################################################
#Private Vorsorge 
####################################################################################################################################################

#Letztes Einkommen berechnen

def calculate_last_income(income_data):
    yearly_last_income = income_data[-1]["income"]
    last_income = yearly_last_income / 12 

    print(f"\nLETZTES EINKOMMEN: {last_income}")
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

    print(f"\nGESAMTE PENSION: {total_pension_data}")
    return total_pension_data

#Wie viel Rente prozentual zum letzten Einkommen

def calculate_percentage_income(total_pension_data, last_income):
    last_income_monthly = last_income
    pension_capital = total_pension_data["pension_bvg_capital_total"]
    pension = total_pension_data["pension_total"]

    print(f"\n{last_income_monthly}")
    print(f"{pension_capital}")
    print(f"{pension}\n")

    percentage_of_income_capital = 100 / last_income_monthly * pension_capital
    percentage_of_income = 100 / last_income_monthly * pension

    percentage_income_pension = {
        "perc_o_i_capital": percentage_of_income_capital,
        "perc_o_i": percentage_of_income
    }

    print(f"\nPROZENTSATZ RENTE ZU EINKOMMEN: {percentage_income_pension}")
    return percentage_income_pension

#Nötige Pension um 100% zu erhalten berechnen

def calculate_necessary_pension(total_pension_data, last_income):
    pension_capital = total_pension_data["pension_bvg_capital_total"]
    pension = total_pension_data["pension_total"]

    private_pension_capital = last_income - pension_capital
    private_pension = last_income - pension

    pre_necessary_pension_capital_portfolio = private_pension_capital * 12 * pension_time
    pre_necessary_pension_portfolio = private_pension * 12 * pension_time

    third_savings = int(input("Wie hoch ist Ihr Vermögen in der 3. Säule (bspw. 10000 - CHF.\n"))

    necessary_pension_capital_portfolio = pre_necessary_pension_capital_portfolio - third_savings
    necessary_pension_portfolio = pre_necessary_pension_portfolio - third_savings

    necessary_portfolio_data = {
        "necessary_portfolio_capital": necessary_pension_capital_portfolio,
        "necessary_portfolio": necessary_pension_portfolio
    }

    print(f"\nNÖTIGES PORTFOLIO: {necessary_portfolio_data}")
    return necessary_portfolio_data

#Zeitdauer für Sparrate

def time_for_saving_rate(vintage, basic_year, pension_age):
    sparrate = input("Möchten Sie die Sparrate über die gesamte Volljährigkeit bis zum aktuellen Alter / Pensionsalter simulieren?\n").lower()
    if sparrate == "ja":
        start_year_s = 18
        if pension_age <= (basic_year - vintage):
            end_year_s = pension_age
        elif pension_age > (basic_year - vintage):
            end_year_s = (basic_year - vintage)
    else: 
        start_year_s = int(input("Ab welchem Alter möchten Sie die Sparrate simulieren?\n"))
        end_year_s = int(input("Bis zu welchem Jahr möchten Sie diese Rente simulieren?\n"))

    years_savings_data = {
        "savings_starting_year": int(start_year_s),
        "savings_ending_year": int(end_year_s)
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

####################################################################################################################################################
#Grundlagen - Summary 
####################################################################################################################################################

#Zusammenfassung aller Pre-Daten 
avg_saving_yield = average_saving_yield / 100#Durchschnittlicher Bankzinssatz
avg_inflation = average_inflation /100 #Durchschnittliche Inflation
avg_msci_15y = avg_return_msci_world_15y #MSCI-World Rendite über die letzten 15 Jahre
avg_msci_25y = avg_return_msci_world_25y #MSCI-World Rendite über die letzten 25 Jahre
avg_msci = avg_return_msci_world #Durchschnittliche MSCI-World Rendite von 15 und 25 Jahre

avg_yearly_yield_incl_infl = avg_msci - avg_inflation #Durchschn. MSCI-World Rendite minus Inflation also reale Rendite
avg_saving_yield_incl_infl = avg_saving_yield - avg_inflation #Durchschn. Bankzinssatz minus Inflation, reale Sparrate

vintage = calculate_vintage(web_vintage_data) #Jahrgang berechnen
income_data = calculate_income() #Liste aller Einkommen
avg_income = average_income(income_data) #Durchschnittliches Einkommen über alle Einträge

####################################################################################################################################################
#AHV - Berechnung 
####################################################################################################################################################

contrib_data, contrib_years = calculate_contrib_years()
yearly_status_data = calculate_yearly_status(contrib_data) #Ehepartner Status, und deren Einkommen
average_ahv_income = calculate_ahv_income(contrib_data, 21, 65 +1) #Durchschnittliches Einkommen während AHV Beitragsjahre
combined_income = calculate_combined_income(contrib_data, yearly_status_data, contrib_years) #Durchschnittliches Einkommen von Ehepartner und mir als Rechnungsgrundlage
adjusted_ahv_income = calculate_aufwertungsfaktor(combined_income, vintage) #Aufwertungsfaktor auf gemeinsames Einkommen gem. Jahrgang
childcare_data = calculate_childcare_credits(yearly_status_data, contrib_years) #Berechnung Erziehungsgutschriften
childcare_credit_income = childcare_data.get("childcare_credits_yearly", 0) #Gesamtbetrag pro Jahr für Erziehungsgutschriften 
betreuungsgutschriften_income = calculate_betreuungsgutschriften(childcare_data, contrib_years) #Betreuungsgutschriften berechnen

def calculate_total_ahv_income(adjusted_ahv_income, childcare_credit_income, betreuungsgutschriften_income):
    ahv_income = adjusted_ahv_income + childcare_credit_income + betreuungsgutschriften_income
    return ahv_income

ahv_income = calculate_total_ahv_income(adjusted_ahv_income, childcare_credit_income, betreuungsgutschriften_income)

#Einkommen mit allen Zusätzen

pre_ahv_pension = calculate_pension(ahv_income, contrib_years) #Pension von Einkommen persönlich
ahv_pension = calculate_plafonierte_pension(pre_ahv_pension, contrib_data) #Plafonierte Rente bei verheirateten
ahv_contrib = calculate_ahv_contrib(contrib_data, data_min_yearly_contrib, self_employed_contrib, employee_contrib, employer_contrib, contrib_years) #AHV Beiträge 
deckungsgrad = calculate_deckungsgrad(ahv_pension, ahv_contrib) #Deckungsgrad der AHV Beiträge und Pensionsauszahlung

####################################################################################################################################################
#BVG - Berechnung 
####################################################################################################################################################

bvg_income = calculate_bvg_income(income_data, 25, 65 +1) #Einkommen bei BVG
bvg_contributions = calculate_bvg_contrib(income_data, bvg_contrib, koordinationsabzug, max_bvg_income, min_bvg_income) #BVG Beiträge
yearly_yield_list = calculate_bvg_yield() #BVG mit Zins gesamtkapital
bvg_asset = calculate_bvg_capital(bvg_contributions, yearly_yield_list)
bvg_pension = calculate_bvg_pension(bvg_asset) #BVG Pensionsauszahlung
deckungsgrad_bvg = calculate_deckungsgrad_bvg(bvg_contributions, bvg_pension, income_data) #Deckungsgrad der BVG

bvg_pension_monthly = bvg_pension["pension_monthly"] #Monatliche Pension bei Rentenbezug
bvg_pension_capital = bvg_pension["kapitalbezug"] #Gesamtkapital in der BVG 
bvg_total_pension = bvg_pension["total_pension"] #Gesamtpension ausgezahlt bei Rentenbezug
bvg_capital_monthly = bvg_pension["capital_pension_monthly"] #Rente monatlich bei Kapitalbezug

####################################################################################################################################################
#Private Pension - Berechnung 
####################################################################################################################################################

last_income = calculate_last_income(income_data) #Letztes Einkommen
pension_1_2 = calculate_pension_1_2(bvg_pension, ahv_pension) #Gesamtrente aus 1. und 2. Säule
percentage_income = calculate_percentage_income(pension_1_2, last_income) #Prozentsatz obligatorische Rente zum letzten Einkommen
necessary_pension = calculate_necessary_pension(pension_1_2, last_income) #Nötige Rente um 100% des letzten Einkommens zu erhalten
years_s = time_for_saving_rate(vintage, basic_year, pension_age) #Jahre für Sparrate zu berechnen.

capital_inflation_msci_saving_rate_s = required_savings_rate(necessary_pension["necessary_portfolio_capital"], avg_yearly_yield_incl_infl, years_s, tol=1e-3, max_iter=100) #Saving-Rate MSCI-World Rendite avg. - Inflation
capital_inflation_msci_saving_rate_p = final_portfolio_annual(capital_inflation_msci_saving_rate_s, years_s, avg_yearly_yield_incl_infl, income_data) #Portfoliowert nötig bei MSCI-World Rendite avg. - Inflation

capital_inflation_bank_saving_rate_s = required_savings_rate(necessary_pension["necessary_portfolio_capital"], avg_saving_yield_incl_infl, years_s, tol=1e-3, max_iter=100) #Bankzins sparrate minus Inflation - Saving_rate
capital_inflation_bank_saving_rate_p = final_portfolio_annual(capital_inflation_bank_saving_rate_s, years_s, avg_saving_yield_incl_infl, income_data) #Bankzins minus Inflation nötiges Portfoliowert

inflation_msci_saving_rate_s = required_savings_rate(necessary_pension["necessary_portfolio"], avg_yearly_yield_incl_infl, years_s, tol=1e-3, max_iter=100) #Saving-Rate MSCI-World Rendite avg. - Inflation
inflation_msci_saving_rate_p = final_portfolio_annual(inflation_msci_saving_rate_s, years_s, avg_yearly_yield_incl_infl, income_data) #Portfoliowert nötig bei MSCI-World Rendite avg. - Inflation

inflation_bank_saving_rate_s = required_savings_rate(necessary_pension["necessary_portfolio"], avg_saving_yield_incl_infl, years_s, tol=1e-3, max_iter=100) #Bankzins sparrate minus Inflation - Saving_rate
inflation_bank_saving_rate_p = final_portfolio_annual(inflation_msci_saving_rate_s, years_s, avg_saving_yield_incl_infl, income_data) #Bankzins minus Inflation nötiges Portfoliowert

def calculate_saving_rates(capital_inflation_msci_saving_rate_s, capital_inflation_bank_saving_rate_s, inflation_msci_saving_rate_s, inflation_bank_saving_rate_s):
    capital_inflation_msci_saving_rate_s = capital_inflation_msci_saving_rate_s *100
    capital_inflation_bank_saving_rate_s = capital_inflation_bank_saving_rate_s *100
    inflation_msci_saving_rate_s = inflation_msci_saving_rate_s *100
    inflation_bank_saving_rate_s = inflation_bank_saving_rate_s *100

    saving_rate_data = {
        "capital_inflation_msci_saving_rate": capital_inflation_msci_saving_rate_s,
        "capital_inflation_bank_saving_rate_s": capital_inflation_bank_saving_rate_s,
        "inflation_msci_saving_rate_s": inflation_msci_saving_rate_s,
        "inflation_bank_saving_rate_s": inflation_bank_saving_rate_s
    }

    return saving_rate_data

saving_rate_data = calculate_saving_rates(capital_inflation_msci_saving_rate_s, capital_inflation_bank_saving_rate_s, inflation_msci_saving_rate_s, inflation_bank_saving_rate_s)

pension_1_2_pension = pension_1_2["pension_total"] #Rente gesamt bei Rentenbezug
pension_1_2_capital = pension_1_2["pension_bvg_capital_total"] #Rente gesamt bei Kapitalbezug

####################################################################################################################################################
#Summary 
####################################################################################################################################################

# - Alter
print(f" Jahrgang: {vintage}")

# - Average Income selber
# - Averaege Income AHV 
# - Berechnetes Avg. Einkommen für AHV
# - Average BVG Income
# - AHV Rente
# - AHV Beitragshöhe
# - AHV Deckungsgrad
# - BVG Rente
# - BVG Beitragshöhe
# - BVG Deckungsgrad
# - Letztes monatliches Einkommen & jetzige Rente aus 1. und 2. Säule
# - Rente als % zum letzten Einkommen
# - 3. Säule nötiges Portfolio um 100% zu erhalten
# - Jährliche Inflationsrate Schweiz
# - Zins auf Sparkonten Schweiz
# - Renditen des MSCI World über verschiedene Zeiträume

#Zinsen und Renditen in unterschiedlichen Szenarien
print(f"\nZinsen und Rendite pro Jahr:")
print(f"Durchschnittliche Rendite des MSCI-World (Avg. 25y und 15y): {avg_msci*100:.2f} %")
print(f"Durchschnittliche Zinsen auf ein Sparkonto: {avg_saving_yield*100:.2f} %")
print(f"Durchschnittliche Rendite des MSCI-World (Avg. 25y und 15y) inkl. Inflation: {avg_yearly_yield_incl_infl*100:.2f} %")
print(f"Durchschnittliche Zinsen auf ein Sparkonto inkl. Inflation: {avg_saving_yield_incl_infl*100:.2f} %")

#Sparraten unter verschiedenen Bedingungen über alle Jahre
print(f"\nSparraten unter verschiedenen Szenarien:")
print(f"Nötige Sparrate bei MSCI-World Rendite mit Inflation, bei einem Kapitalbezug aus der PK: {capital_inflation_msci_saving_rate_s:.2f} %")
print(f"Nötige Sparrate bei Sparkonto Zinsen mit Inflation, bei einer Kapitalbezug aus der PK: {capital_inflation_bank_saving_rate_s:.2f}")
print(f"Nötige Sparrate bei MSCI-World Rendite ohne Inflation, bei einem Rentenbezug aus der PK: {inflation_msci_saving_rate_s:.2f} %")
print(f"Nötige Sparrate bei Sparkonto Zinsen ohne Inflation, bei einer Rentenbezug aus der PK: {inflation_bank_saving_rate_s:.2f}")

