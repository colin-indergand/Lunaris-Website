from flask import Flask, request, render_template
from flask import request

import json

with open("Front_end/posts/posts.json", encoding="utf-8") as f:
    posts = json.load(f)

# Nur die letzten drei (neueste zuerst)
latest_posts = posts[:3]


from Back_end.Altersvorsorge_tool.Pension_Calculator import avg_saving_yield
from Back_end.Altersvorsorge_tool.Pension_Calculator import avg_inflation
from Back_end.Altersvorsorge_tool.Pension_Calculator import avg_msci_15y
from Back_end.Altersvorsorge_tool.Pension_Calculator import avg_msci_25y
from Back_end.Altersvorsorge_tool.Pension_Calculator import avg_msci
from Back_end.Altersvorsorge_tool.Pension_Calculator import avg_yearly_yield_incl_infl
from Back_end.Altersvorsorge_tool.Pension_Calculator import avg_saving_yield_incl_infl 
from Back_end.Altersvorsorge_tool.Pension_Calculator import data_min_yearly_contrib
from Back_end.Altersvorsorge_tool.Pension_Calculator import self_employed_contrib
from Back_end.Altersvorsorge_tool.Pension_Calculator import employee_contrib
from Back_end.Altersvorsorge_tool.Pension_Calculator import employer_contrib
from Back_end.Altersvorsorge_tool.Pension_Calculator import bvg_contrib
from Back_end.Altersvorsorge_tool.Pension_Calculator import koordinationsabzug
from Back_end.Altersvorsorge_tool.Pension_Calculator import max_bvg_income
from Back_end.Altersvorsorge_tool.Pension_Calculator import basic_year
from Back_end.Altersvorsorge_tool.Pension_Calculator import min_bvg_income
from Back_end.Altersvorsorge_tool.Pension_Calculator import pension_age
from Back_end.Altersvorsorge_tool.Pension_Calculator import pre_childcare_credits
from Back_end.Altersvorsorge_tool.Pension_Calculator import pension_time

from Back_end.Altersvorsorge_tool.Pension_Calculator import calculate_vintage
from Back_end.Altersvorsorge_tool.Pension_Calculator import calculate_income
from Back_end.Altersvorsorge_tool.Pension_Calculator import average_income
from Back_end.Altersvorsorge_tool.Pension_Calculator import calculate_contrib_years
from Back_end.Altersvorsorge_tool.Pension_Calculator import calculate_yearly_status
from Back_end.Altersvorsorge_tool.Pension_Calculator import calculate_ahv_income
from Back_end.Altersvorsorge_tool.Pension_Calculator import calculate_combined_income
from Back_end.Altersvorsorge_tool.Pension_Calculator import calculate_aufwertungsfaktor
from Back_end.Altersvorsorge_tool.Pension_Calculator import calculate_childcare_credits 
from Back_end.Altersvorsorge_tool.Pension_Calculator import calculate_betreuungsgutschriften
from Back_end.Altersvorsorge_tool.Pension_Calculator import calculate_total_ahv_income
from Back_end.Altersvorsorge_tool.Pension_Calculator import calculate_pension
from Back_end.Altersvorsorge_tool.Pension_Calculator import calculate_plafonierte_pension
from Back_end.Altersvorsorge_tool.Pension_Calculator import calculate_ahv_contrib
from Back_end.Altersvorsorge_tool.Pension_Calculator import calculate_deckungsgrad
from Back_end.Altersvorsorge_tool.Pension_Calculator import calculate_bvg_income
from Back_end.Altersvorsorge_tool.Pension_Calculator import calculate_bvg_contrib
from Back_end.Altersvorsorge_tool.Pension_Calculator import calculate_bvg_yield
from Back_end.Altersvorsorge_tool.Pension_Calculator import calculate_bvg_capital
from Back_end.Altersvorsorge_tool.Pension_Calculator import calculate_bvg_pension
from Back_end.Altersvorsorge_tool.Pension_Calculator import calculate_deckungsgrad_bvg
from Back_end.Altersvorsorge_tool.Pension_Calculator import calculate_last_income
from Back_end.Altersvorsorge_tool.Pension_Calculator import calculate_pension_1_2
from Back_end.Altersvorsorge_tool.Pension_Calculator import calculate_percentage_income
from Back_end.Altersvorsorge_tool.Pension_Calculator import calculate_necessary_pension
from Back_end.Altersvorsorge_tool.Pension_Calculator import calculate_wished_monthly_pension
from Back_end.Altersvorsorge_tool.Pension_Calculator import time_for_saving_rate
from Back_end.Altersvorsorge_tool.Pension_Calculator import required_savings_rate
from Back_end.Altersvorsorge_tool.Pension_Calculator import calculate_saving_rates

app = Flask(__name__, 
            template_folder="Front_end", static_folder="Front_end")

@app.context_processor 
def inject_request():
    return dict(request=request)

@app.route("/")
def index():
    with open("Front_end/posts/posts.json", encoding="utf-8") as f:
        posts = json.load(f)
    latest_posts = posts[:3]  # oder posts[-3:] wenn neuste hinten
    return render_template("index.html", posts=latest_posts, active_page="index")


@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/education")
def education():
    return render_template("education.html")

@app.route("/news")
def news():
    return render_template("news.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/altersvorsorge", methods=["GET", "POST"])
def altersvorsorge():
    results = {}
    if request.method == "POST":
        #Vintage 
        web_vintage = int(request.form.get("return-vintage", "0").strip() or "0")

        web_vintage_data = web_vintage

        #Income Data
        web_income_start_age = [int(i) if i.strip() else 0 for i in request.form.getlist("return-income-start-age[]")]
        web_income_end_age = [int(i) if i.strip() else 0 for i in request.form.getlist("return-income-end-age[]")]
        web_income_income = [float(i) if i.strip() else 0 for i in request.form.getlist("return-income-income[]")]
        web_income_status = [i if i.strip() else 0 for i in request.form.getlist("return-income-status[]")]
        web_income_vermögen = [float(i) if i.strip() else 0 for i in request.form.getlist("return-income-vermögen[]")]

        length_income_data = len(web_income_start_age)
        web_income_data = []
        for i in range(length_income_data):
            web_income_data.append({
                "start_age": web_income_start_age[i],
                "end_age": web_income_end_age[i],
                "income": web_income_income[i],
                "status": web_income_status[i],
                "vermögen": web_income_vermögen[i]
            })

        #Contrib-Gap
        web_contrib_gap_years = int(request.form.get("return-contrib-gap-years", "0").strip() or "0")
        web_contrib_gap_start_age = [int(i) if i.strip() else 0 for i in request.form.getlist("return-start-age[]")]
        web_contrib_gap_end_age = [int(i) if i.strip() else 0 for i in request.form.getlist("return-end-age[]")]

        web_contrib_gap_years_data = web_contrib_gap_years
        length_contrib_gap = len(web_contrib_gap_start_age)
        web_contrib_gap_data = []
        for i in range(length_contrib_gap):
            web_contrib_gap_data.append({
                "start_age": web_contrib_gap_start_age[i],
                "end_age": web_contrib_gap_end_age[i]
            })

        #Yearly-Status-Data
        web_yearly_status_start_age = [int(i) if i.strip() else 0 for i in request.form.getlist("return-yearly-status-data-start-age[]")]
        web_yearly_status_end_age = [int(i) if i.strip() else 0 for i in request.form.getlist("return-yearly-status-data-end-age[]")]
        web_yearly_status_income = [int(i) if i.strip() else 0 for i in request.form.getlist("return-yearly-status-data-income[]")]

        web_yearly_status_data = []
        length_yearly_status_data = len(web_yearly_status_start_age)
        for i in range(length_yearly_status_data):
            web_yearly_status_data.append({
                "start_age": web_yearly_status_start_age[i],
                "end_age": web_yearly_status_end_age[i],
                "income": web_yearly_status_income[i]
            })

        #Erziehungsgutschriften
        web_childcare_credits_has_children = request.form.get("return-has-children", "0").strip() or "0"
        web_chilcare_credits_amount_children = int(request.form.get("return-amount-children-childcare-credits", "0").strip() or "0")
        web_childcare_credits_vintage = [int(i) if i.strip() else 0 for i in request.form.getlist("return-vintage-children[]")]
        web_childcare_credits_erziehungsberechtigt = [(i) if i.strip() else 0 for i in request.form.getlist("return-is-erziehungsberechtigt[]")]
        web_chilcare_credits_erziehungsberechtigt_status = [(i) if i.strip() else 0 for i in request.form.getlist("return-status-erziehungsberechtigt[]")]

        web_childcare_credits_has_childcren_data = web_childcare_credits_has_children
        web_childcare_credits_amount_children_data = web_chilcare_credits_amount_children

        web_childcare_credits_erziehungsberechtigt_data = []
        web_childcare_credits_erziehungsberechtigt_children_data = []

        # Für jedes Kind mit Zeitblöcken, aber nur wenn nicht "durchgehend"
        for i in range(web_childcare_credits_amount_children_data):
            web_childcare_credits_erziehungsberechtigt_data.append({
                "child": i,
                "vintage": web_childcare_credits_vintage,
                "erziehungsberechtigt": web_childcare_credits_erziehungsberechtigt,
            })

            if web_childcare_credits_erziehungsberechtigt[i] == "Ja":
                web_childcare_credits_erziehungsberechtigt_data.append({
                    "status": web_chilcare_credits_erziehungsberechtigt_status
                })

            elif web_childcare_credits_erziehungsberechtigt[i] == "Nein":
                web_childcare_credits_erziehungsberechtigt_start_age = request.form.getlist(f"return-erziehungsberechtigt-start-age-{i}")
                web_childcare_credits_erziehungsberechtigt_end_age = request.form.getlist(f"return-erziehungsberechtigt-end-age-{i}")
                web_childcare_credits_erziehungsberechtigt_status_year = request.form.getlist(f"return-erziehungsberechtigt-status-{i}")

                for start, end, status in zip(
                    web_childcare_credits_erziehungsberechtigt_start_age,
                    web_childcare_credits_erziehungsberechtigt_end_age,
                    web_childcare_credits_erziehungsberechtigt_status_year,
                ):
                    web_childcare_credits_erziehungsberechtigt_children_data.append({
                        "child": i,
                        "start_age": int(start),
                        "end_age": int(end),
                        "status": status,
                    })



        #Betreuungsgutschriften
        web_betreuungsgutschriften_has = request.form.get("return-has-betreuungsgutschriften", "0").strip() or "0"
        web_betreuungsgutschriften_start_age = [int(i) if i.strip() else 0 for i in request.form.getlist("return-start-year-betreuungsgutschriften[]")]
        web_betreuungsgutschriften_end_age = [int(i) if i.strip() else 0 for i in request.form.getlist("return-end-year-betreuungsgutschriften[]")]

        web_betreuungsgutschriften_has_data = web_betreuungsgutschriften_has

        web_bvg_betreuungsgutschriften_data = []
        for i in web_betreuungsgutschriften_start_age:
            web_bvg_betreuungsgutschriften_data.append({
                "start_age": web_betreuungsgutschriften_start_age,
                "end_age": web_betreuungsgutschriften_end_age
            })

        #Plafonierte Rente
        web_plafonierte_rente = request.form.get("return-is-married", "0").strip() or "0"

        web_plafonierte_rente_data = web_plafonierte_rente

        #BVG-Contributions
        web_bvg_contrib_angestellt_spez = request.form.get("return-select-bvg-contrib-angestellt", "0").strip() or "0"
        web_bvg_contrib_angestellt_start_age = [int(i) if i.strip() else 0 for i in request.form.getlist("return-bvg-contrib-angestellt-start-age[]")]
        web_bvg_contrib_angestellt_end_age = [int(i) if i.strip() else 0 for i in request.form.getlist("return-bvg-contrib-angestellt-end-age[]")]
        web_bvg_contrib_angestellt_min_income = [int(i) if i.strip() else 0 for i in request.form.getlist("return-bvg-contrib-angestellt-min-vers-income[]")]
        web_bvg_contrib_angestellt_max_income = [int(i) if i.strip() else 0 for i in request.form.getlist("return-select-bvg-contrib-angestellt-max-vers-income[]")]
        web_bvg_contrib_angestellt_koordinationsabzug = [int(i) if i.strip() else 0 for i in request.form.getlist("return-bvg-contrib-angestellt-koordinationsabzug[]")]

        web_bvg_contrib_selbständig_spez = request.form.get("return-select-bvg-contrib-selbständig", "0").strip() or "0"
        web_bvg_contrib_selbständig_start_age = [int(i) if i.strip() else 0 for i in request.form.getlist("return-bvg-contrib-selbständig-start-age[]")]
        web_bvg_contrib_selbständig_end_age = [int(i) if i.strip() else 0 for i in request.form.getlist("return-bvg-contrib-selbständig-end-age[]")]
        web_bvg_contrib_selbständig_min_income = [int(i) if i.strip() else 0 for i in request.form.getlist("return-bvg-contrib-selbständig-min-vers-income[]")]
        web_bvg_contrib_selbständig_max_income = [int(i) if i.strip() else 0 for i in request.form.getlist("return-bvg-contrib-selbständig-max-vers-income[]")]
        web_bvg_contrib_selbständig_koordinationsabzug = [int(i) if i.strip() else 0 for i in request.form.getlist("return-bvg-contrib-selbständig-koordinationsabzug[]")]
        web_bvg_contrib_selbständig_percentage = [int(i) if i.strip() else 0 for i in request.form.getlist("return-bvg-contrib-selbständig-percentage[]")]



        web_bvg_contrib_angestellt_spez_data = web_bvg_contrib_angestellt_spez
        web_bvg_contrib_angestellt_data = []
        for i in web_bvg_contrib_angestellt_start_age:
            web_bvg_contrib_angestellt_data.append({
                "start_age": web_bvg_contrib_angestellt_start_age,
                "end_age": web_bvg_contrib_angestellt_end_age,
                "min_income": web_bvg_contrib_angestellt_min_income,
                "max_income": web_bvg_contrib_angestellt_max_income,
                "koordinationsabzug": web_bvg_contrib_angestellt_koordinationsabzug
            })

        web_bvg_contrib_selbständig_spez_data = web_bvg_contrib_selbständig_spez
        web_bvg_contrib_selbständig_data = []
        for i in web_bvg_contrib_selbständig_start_age:
            web_bvg_contrib_selbständig_data.append({
                "start_age": web_bvg_contrib_selbständig_start_age,
                "end_age": web_bvg_contrib_selbständig_end_age,
                "min_income": web_bvg_contrib_selbständig_min_income,
                "max_income": web_bvg_contrib_selbständig_max_income,
                "koordinationsabzug": web_bvg_contrib_selbständig_koordinationsabzug,
                "percentage": web_bvg_contrib_selbständig_percentage
            })


        #BVG-Yield
        web_bvg_yield_start_age = [int(i) if i.strip() else 0 for i in request.form.getlist("return-bvg-yield-start-age[]")]
        web_bvg_yield_end_age = [int(i) if i.strip() else 0 for i in request.form.getlist("return-bvg-yield-end-age[]")]
        web_bvg_yield_yield = [float(i) if i.strip() else 0 for i in request.form.getlist("return-bvg-yield-yield[]")]

        web_bvg_yield_data = []

        min_len_yield = min(len(web_bvg_yield_start_age), len(web_bvg_yield_end_age), len(web_bvg_yield_yield))

        for i in range(min_len_yield):
            web_bvg_yield_data.append({
                "start_age": web_bvg_yield_start_age[i],
                "end_age": web_bvg_yield_end_age[i],
                "yield": web_bvg_yield_yield[i]
            })

        #BVG-Deckungsgrad
        web_bvg_deckungsgrad_start_age = [int(i) if i.strip() else 0 for i in request.form.getlist("return-bvg-contrib-share-start-age[]")] 
        web_bvg_deckungsgrad_end_age = [int(i) if i.strip() else 0 for i in request.form.getlist("return-bvg-contrib-share-end-age[]")] 
        web_bvg_deckungsgrad_percentage = [float(i) if i.strip() else 0 for i in request.form.getlist("return-bvg-contrib-share-percentage[")] 

        web_bvg_deckungsgrad_data = []

        min_len = min(len(web_bvg_deckungsgrad_start_age), len(web_bvg_deckungsgrad_end_age), len(web_bvg_deckungsgrad_percentage))
        for i in range(min_len):
            web_bvg_deckungsgrad_data.append({
                "start_age": web_bvg_deckungsgrad_start_age[i],
                "end_age": web_bvg_deckungsgrad_end_age[i],
                "percentage": web_bvg_deckungsgrad_percentage[i]
            })

        #Nötiges Portfolio
        web_private_portfolio_amount = int(request.form.get("return-portfolio-necessary-input", "0").strip() or "0")

        web_private_portfolio_amount_data = web_private_portfolio_amount

        #Wunsch monatliche Rente

        web_spec_monthly_payment = request.form.get("return-spec-monthly-payment", "0").strip() or "0"
        web_monthly_payment = request.form.get("return-monthly-pension", "0").strip() or "0"

        web_spec_monthly_payment_data = web_spec_monthly_payment
        web_monthly_payment_data = web_monthly_payment

        #Saving-Rate
        web_saving_rate_input = request.form.get("return-saving-rate-input", "0").strip() or "0"
        web_saving_rate_start_age = int(request.form.get("return-saving-rate-start-age", "0").strip() or "0")
        web_saving_rate_end_age = int(request.form.get("return-saving-rate-end_age", "0").strip() or "0")

        web_saving_rate_data = {
            "input": web_saving_rate_input,
            "start_age": web_saving_rate_start_age,
            "end_age": web_saving_rate_end_age
        }


        #Funktionen aufrufen und speichern

        print_avg_saving_yield = avg_saving_yield
        print_avg_inflation = avg_inflation
        print_avg_msci_15y = avg_msci_15y
        print_avg_msci_25y = avg_msci_25y
        print_avg_msci = avg_msci
        print_avg_yearly_yield_incl_infl = avg_yearly_yield_incl_infl
        print_avg_saving_yield_incl_infl = avg_saving_yield_incl_infl

        print_vintage = calculate_vintage(web_vintage_data)
        print_income_data = calculate_income(web_income_data)
        print_average_income = average_income(print_income_data)


        print_contrib_data, print_contrib_years = calculate_contrib_years(print_income_data, web_contrib_gap_years_data, web_contrib_gap_data)

        print_yearly_status_data = calculate_yearly_status(print_contrib_data, web_yearly_status_data) 
        print_ahv_income = calculate_ahv_income(print_contrib_data, 21, 65 +1)
        print_combined_income = calculate_combined_income(print_contrib_data, print_yearly_status_data, print_contrib_years) 
        print_adjusted_ahv_income = calculate_aufwertungsfaktor(print_combined_income, print_vintage) 
        print_childcare_data = calculate_childcare_credits(pre_childcare_credits, print_contrib_years, print_contrib_data, print_vintage, web_childcare_credits_has_childcren_data, web_childcare_credits_amount_children_data, web_childcare_credits_erziehungsberechtigt_data, web_childcare_credits_erziehungsberechtigt_children_data)
        print_childcare_credit_income = print_childcare_data.get("childcare_credits_yearly", 0)
        print_betreuungsgutschriften_income = calculate_betreuungsgutschriften(print_childcare_data, print_contrib_years, web_betreuungsgutschriften_has_data, web_bvg_betreuungsgutschriften_data)
        print_total_ahv_income = calculate_total_ahv_income(print_adjusted_ahv_income, print_childcare_credit_income, print_betreuungsgutschriften_income)
        print_pre_ahv_pension = calculate_pension(print_total_ahv_income, print_contrib_years)
        print_ahv_pension = calculate_plafonierte_pension(print_pre_ahv_pension, web_plafonierte_rente_data)
        print_ahv_contrib = calculate_ahv_contrib(print_contrib_data, data_min_yearly_contrib, self_employed_contrib, employee_contrib, employer_contrib)
        print_deckungsgrad = calculate_deckungsgrad(print_ahv_pension, print_ahv_contrib)

        print_bvg_income = calculate_bvg_income(print_income_data, 25, 65 +1)
        print_bvg_contributions = calculate_bvg_contrib(print_income_data, bvg_contrib, koordinationsabzug, max_bvg_income, min_bvg_income, web_bvg_contrib_angestellt_spez_data, web_bvg_contrib_angestellt_data, web_bvg_contrib_selbständig_spez_data, web_bvg_contrib_selbständig_data)
        print_yearly_yield_list = calculate_bvg_yield(web_bvg_yield_data)
        print_bvg_asset = calculate_bvg_capital(print_bvg_contributions, print_yearly_yield_list)
        print_bvg_pension = calculate_bvg_pension(print_bvg_asset)
        print_deckungsgrad_bvg = calculate_deckungsgrad_bvg(print_bvg_contributions, print_bvg_pension, print_income_data, web_bvg_deckungsgrad_data)
        print_bvg_pension_monthly = print_bvg_pension["pension_monthly"]
        print_bvg_pension_capital = print_bvg_pension["kapitalbezug"]
        print_bvg_total_pension = print_bvg_pension["total_pension"] 
        print_bvg_capital_monthly = print_bvg_pension["capital_pension_monthly"]

        print_last_income = calculate_last_income(print_income_data) 
        print_pension_1_2 = calculate_pension_1_2(print_bvg_pension, print_ahv_pension) 
        print_pension_1_2_pension = print_pension_1_2["pension_total"]
        print_pension_1_2_capital = print_pension_1_2["pension_bvg_capital_total"]
        print_percentage_income = calculate_percentage_income(print_pension_1_2, print_last_income)
        print_100_necessary_pension = calculate_necessary_pension(pension_time, print_pension_1_2, print_last_income, web_private_portfolio_amount_data)
        print_wanted_necessary_pension = calculate_wished_monthly_pension(pension_time, print_pension_1_2, web_spec_monthly_payment_data, web_monthly_payment_data, web_private_portfolio_amount_data)
        print_years_s = time_for_saving_rate(print_vintage, basic_year, pension_age, web_saving_rate_data)

        if print_wanted_necessary_pension != 0:
            print_wanted_capital_inflation_msci_saving_rate_s = required_savings_rate(print_wanted_necessary_pension["necessary_portfolio_capital"], print_avg_yearly_yield_incl_infl, print_income_data, print_years_s, tol=1e-3, max_iter=100) 
            print_wanted_capital_inflation_bank_saving_rate_s = required_savings_rate(print_wanted_necessary_pension["necessary_portfolio_capital"], print_avg_saving_yield_incl_infl, print_income_data,  print_years_s, tol=1e-3, max_iter=100) 
            print_wanted_inflation_msci_saving_rate_s = required_savings_rate(print_wanted_necessary_pension["necessary_portfolio"], print_avg_yearly_yield_incl_infl, print_income_data, print_years_s, tol=1e-3, max_iter=100) 
            print_wanted_inflation_bank_saving_rate_s = required_savings_rate(print_wanted_necessary_pension["necessary_portfolio"], print_avg_saving_yield_incl_infl, print_income_data, print_years_s, tol=1e-3, max_iter=100) 
            print_wanted_capital_msci_saving_rate_s = required_savings_rate(print_wanted_necessary_pension["necessary_portfolio_capital"], print_avg_msci, print_income_data, print_years_s, tol=1e-3, max_iter=100) 

            print_wanted_saving_rate_data = calculate_saving_rates(print_wanted_capital_inflation_msci_saving_rate_s, print_wanted_capital_inflation_bank_saving_rate_s, print_wanted_inflation_msci_saving_rate_s, print_wanted_inflation_bank_saving_rate_s, print_wanted_capital_msci_saving_rate_s)

            print_wanted_capital_inflation_msci_saving_rate_s = print_wanted_saving_rate_data["capital_inflation_msci_saving_rate"]
            print_wanted_capital_inflation_bank_saving_rate_s = print_wanted_saving_rate_data["capital_inflation_bank_saving_rate_s"]
            print_wanted_inflation_msci_saving_rate_s = print_wanted_saving_rate_data["inflation_msci_saving_rate_s"]
            print_wanted_inflation_bank_saving_rate_s = print_wanted_saving_rate_data ["inflation_bank_saving_rate_s"]
            print_wanted_capital_msci_saving_rate_s = print_wanted_saving_rate_data["capital_msci_saving_rate"]


        print_100_capital_inflation_msci_saving_rate_s = required_savings_rate(print_100_necessary_pension["necessary_portfolio_capital"], print_avg_yearly_yield_incl_infl, print_income_data, print_years_s, tol=1e-3, max_iter=100) 
        print_100_capital_inflation_bank_saving_rate_s = required_savings_rate(print_100_necessary_pension["necessary_portfolio_capital"], print_avg_saving_yield_incl_infl, print_income_data, print_years_s, tol=1e-3, max_iter=100) 
        print_100_inflation_msci_saving_rate_s = required_savings_rate(print_100_necessary_pension["necessary_portfolio"], print_avg_yearly_yield_incl_infl, print_income_data, print_years_s, tol=1e-3, max_iter=100) 
        print_100_inflation_bank_saving_rate_s = required_savings_rate(print_100_necessary_pension["necessary_portfolio"], print_avg_saving_yield_incl_infl, print_income_data, print_years_s, tol=1e-3, max_iter=100) 
        print_100_capital_msci_saving_rate_s = required_savings_rate(print_100_necessary_pension["necessary_portfolio_capital"], print_avg_msci, print_income_data, print_years_s, tol=1e-3, max_iter=100) 

        print_100_saving_rate_data = calculate_saving_rates(print_100_capital_inflation_msci_saving_rate_s, print_100_capital_inflation_bank_saving_rate_s, print_100_inflation_msci_saving_rate_s, print_100_inflation_bank_saving_rate_s, print_100_capital_msci_saving_rate_s)

        print_100_capital_inflation_msci_saving_rate_s = print_100_saving_rate_data["capital_inflation_msci_saving_rate"]
        print_100_capital_inflation_bank_saving_rate_s = print_100_saving_rate_data["capital_inflation_bank_saving_rate_s"]
        print_100_inflation_msci_saving_rate_s = print_100_saving_rate_data["inflation_msci_saving_rate_s"]
        print_100_inflation_bank_saving_rate_s = print_100_saving_rate_data ["inflation_bank_saving_rate_s"]
        print_100_capital_msci_saving_rate_s = print_100_saving_rate_data["capital_msci_saving_rate"]


        #Resultate speichern
        results = {
            "basic_data_returns": {
                "average_saving_yield": print_avg_saving_yield,
                "average_inflation_swiss": print_avg_inflation,
                "average_msci_return_15y": print_avg_msci_15y,
                "average_msci_return_25y": print_avg_msci_25y,
                "average_msci_return" : print_avg_msci,
                "average_msci_yield_inflation_included": print_avg_yearly_yield_incl_infl,
                "average_saving_yield_inflation_included": print_avg_saving_yield_incl_infl
            },

            "vintage": print_vintage,

            "average_income": print_average_income,
        
            "ahv_data": {
                "amount_contrib_years": print_contrib_years,
                "ahv_income": print_ahv_income,
                "average_combined_income": print_combined_income,
                "ahv_pension": print_ahv_pension,
                "ahv_contrib": print_ahv_contrib,
                "ahv_deckungsgrad": print_deckungsgrad
            },

            "bvg_data": {
                "bvg_income": print_bvg_income,
                "bvg_contrib": print_bvg_contributions,
                "bvg_capital": print_bvg_asset, 
                "bvg_deckungsgrad": print_deckungsgrad_bvg,
                "bvg_pension_monthly": print_bvg_pension_monthly,
                "bvg_pension_monthly_capital": print_bvg_capital_monthly,
                "bvg_pension_capital": print_bvg_pension_capital,
                "bvg_pension_total": print_bvg_total_pension
            },

            "private_savings": {
                "last_income": print_last_income,
                "total_pension": print_pension_1_2_pension,
                "total_pension_capital": print_pension_1_2_capital,
                "percentage_last_income": print_percentage_income,
                "portfolio_value_100%_last_income": print_100_necessary_pension,
                "saving_years": print_years_s
            },

            "saving_rates": {
                "100_capital_inflation_bank_saving_rate": print_100_capital_inflation_msci_saving_rate_s,
                "100_capital_inflation_msci_saving_rate": print_100_capital_inflation_bank_saving_rate_s,
                "100_inflation_msci_saving_rate": print_100_inflation_msci_saving_rate_s,
                "100_inflation_bank_saving_rate": print_100_inflation_bank_saving_rate_s,
                "100_msci_saving_rate": print_100_capital_msci_saving_rate_s
            },

            "form_data": request.form
        }

        if print_wanted_necessary_pension != 0:
            results.update({
                "wanted_pension": {
                    "wanted_capital_inflation_bank_saving_rate": print_wanted_capital_inflation_msci_saving_rate_s,
                    "wanted_capital_inflation_bank_saving_rate": print_wanted_capital_inflation_bank_saving_rate_s,
                    "wanted_inflation_msci_saving_rate": print_wanted_inflation_msci_saving_rate_s,
                    "wanted_inflation_bank_saving_rate": print_wanted_inflation_bank_saving_rate_s,
                    "wanted_capital_msci_saving_rate": print_wanted_capital_msci_saving_rate_s,
                }
            })
        
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return render_template("partials/results_block.html", results = results)

    return render_template("altersvorsorge.html", results = results, form_data = request.form)


if __name__ == "__main__":
    app.run(debug=True)
