from flask import Flask, request, render_template

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
from Back_end.Altersvorsorge_tool.Pension_Calculator import ahv_contrib
from Back_end.Altersvorsorge_tool.Pension_Calculator import bvg_contrib
from Back_end.Altersvorsorge_tool.Pension_Calculator import koordinationsabzug
from Back_end.Altersvorsorge_tool.Pension_Calculator import max_bvg_income
from Back_end.Altersvorsorge_tool.Pension_Calculator import basic_year
from Back_end.Altersvorsorge_tool.Pension_Calculator import min_bvg_income
from Back_end.Altersvorsorge_tool.Pension_Calculator import pension_age

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
from Back_end.Altersvorsorge_tool.Pension_Calculator import time_for_saving_rate
from Back_end.Altersvorsorge_tool.Pension_Calculator import required_savings_rate
from Back_end.Altersvorsorge_tool.Pension_Calculator import final_portfolio_annual
from Back_end.Altersvorsorge_tool.Pension_Calculator import calculate_saving_rates


app = Flask(__name__, 
            template_folder="Front_end", static_folder="Front_end")

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/data.html", methods=["GET"])
def data_page():
    return render_template("data.html")


@app.route("/pension_calculator", methods=["POST"])
def results_pension_calculator():
    #Vintage 
    web_vintage = int(request.form["return-vintage"])

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
    web_contrib_gap_years = int(request.form["return-contrib-gap-years"])
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

    #Erziehungsgutschriften
    web_childcare_credits_has_children = request.form["return-has-children"]
    web_chilcare_credits_amount_children = int(request.form["return-amount-children-childcare-credits"])
    web_childcare_credits_vintage = [int(i) if i.strip() else 0 for i in request.form.getlist("return-vintage-children[]")]
    web_childcare_credits_erziehungsberechtigt = [int(i) if i.strip() else 0 for i in request.form.getlist("return-is-erziehungsberechtigt[]")]
    web_chilcare_credits_erziehungsberechtigt_status = [(i) if i.strip() else 0 for i in request.form.getlist("return-status-erziehungsberechtigt[]")]
    web_childcare_credits_erziehungsberechtigt_start_age = [int(i) if i.strip() else 0 for i in request.form.getlist("return-erziehungsberechtigt-start-age[]")]
    web_childcare_credits_erziehungsberechtigt_end_age = [int(i) if i.strip() else 0 for i in request.form.getlist("return-erziehungsberechtigt-end-age[]")]
    web_childcare_credits_erziehungsberechtigt_status_year = [i if i.strip() else 0 for i in request.form.getlist("return-erziehunsberechtigt-status[]")]

    #Betreuungsgutschriften
    web_betreuungsgutschriften_has = request.form["return-has-betreuungsgutschriften"]  
    web_betreuungsgutschriften_duration = int(request.form["return-duration-betreuungsgutschriften"])
    web_betreuungsgutschriften_start_year = int(request.form["return-start-year-betreuungsgutschriften"])

    #Plafonierte Rente
    web_plafonierte_rente = request.form["return-is-married"]

    #BVG-Contributions
    web_bvg_contrib_angestellt_spez = request.form["return-select-bvg-contrib-angestellt"] 
    web_bvg_contrib_angestellt_start_age = [int(i) if i.strip() else 0 for i in request.form.getlist("return-bvg-contrib-angestellt-start-age[]")]
    web_bvg_contrib_angestellt_end_age = [int(i) if i.strip() else 0 for i in request.form.getlist("return-bvg-contrib-angestellt-end-age[]")]
    web_bvg_contrib_angestellt_min_income = [int(i) if i.strip() else 0 for i in request.form.getlist("return-bvg-contrib-angestellt-min-vers-income[]")]
    web_bvg_contrib_angestellt_max_income = [int(i) if i.strip() else 0 for i in request.form.getlist("return-select-bvg-contrib-angestellt-max-vers-income[]")]
    web_bvg_contrib_angestellt_koordinationsabzug = [int(i) if i.strip() else 0 for i in request.form.getlist("return-bvg-contrib-angestellt-koordinationsabzug[]")]

    web_bvg_contrib_selbständig_spez = request.form("return-select-bvg-contrib-selbständig")
    web_bvg_contrib_selbständig_start_age = [int(i) if i.strip() else 0 for i in request.form.getlist("return-bvg-contrib-selbständig-start-age[]")]
    web_bvg_contrib_selbständig_end_age = [int(i) if i.strip() else 0 for i in request.form.getlist("return-bvg-contrib-selbständig-end-age[]")]
    web_bvg_contrib_selbständig_min_income = [int(i) if i.strip() else 0 for i in request.form.getlist("return-bvg-contrib-selbständig-min-vers-income[]")]
    web_bvg_contrib_selbständig_max_income = [int(i) if i.strip() else 0 for i in request.form.getlist("return-bvg-contrib-selbständig-max-vers-income[]")]
    web_bvg_contrib_selbständig_koordinationsabzug = [int(i) if i.strip() else 0 for i in request.form.getlist("return-bvg-contrib-selbständig-koordinationsabzug[]")]

    #BVG-Yield
    web_bvg_yield_start_age = [int(i) if i.strip() else 0 for i in request.form.getlist("return-bvg-yield-start-age[]")]
    web_bvg_yield_end_age = [int(i) if i.strip() else 0 for i in request.form.getlist("return-bvg-yield-end-age[]")]
    web_bvg_yield_yield = [int(i) if i.strip() else 0 for i in request.form.getlist("return-bvg-yield-yield[]")]

    #BVG-Deckungsgrad
    web_bvg_deckungsgrad_start_age = [int(i) if i.strip() else 0 for i in request.form.getlist("return-bvg-contrib-share-start-age[]")] 
    web_bvg_deckungsgrad_end_age = [int(i) if i.strip() else 0 for i in request.form.getlist("return-bvg-contrib-share-end-age[]")] 
    web_bvg_deckungsgrad_percentage = [int(i) if i.strip() else 0 for i in request.form.getlist("return-bvg-contrib-share-percentage[")] 

    #Nötiges Portfolio
    web_necessary_portfolio_amount = int(request.form["return-portfolio-necessary-input"])

    #Saving-Rate
    web_saving_rate_input = request.form["return-saving-rate-input"]
    web_saving_rate_start_age = int(request.form["return-saving-rate-start-age"])
    web_saving_rate_end_age = int(request.form["return-saving-rate-end_age"])

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

    #AB HIER FEHLT NOCH ERGÄNZUNGEN IN PENSION_CALCULATOR UND IM SKRIPT 
    print_yearly_status_data = calculate_yearly_status(print_contrib_data) 
    print_average_ahv_income = calculate_ahv_income(print_contrib_data, 21, 65 +1)
    print_combined_income = calculate_combined_income(print_contrib_data, print_yearly_status_data, print_contrib_years) 
    print_adjusted_ahv_income = calculate_aufwertungsfaktor(print_combined_income, print_vintage) 
    print_childcare_data = calculate_childcare_credits(print_yearly_status_data, print_contrib_years)
    print_childcare_credit_income = print_childcare_data.get("childcare_credits_yearly", 0)
    print_betreuungsgutschriften_income = calculate_betreuungsgutschriften(print_childcare_data, print_contrib_years)
    print_ahv_income = calculate_total_ahv_income(print_adjusted_ahv_income, print_childcare_credit_income, print_betreuungsgutschriften_income)
    print_pre_ahv_pension = calculate_pension(print_ahv_income, print_contrib_years)
    print_ahv_pension = calculate_plafonierte_pension(print_pre_ahv_pension, print_contrib_data)
    print_ahv_contrib = calculate_ahv_contrib(print_contrib_data, data_min_yearly_contrib, self_employed_contrib, employee_contrib, employer_contrib, print_contrib_years)
    print_deckungsgrad = calculate_deckungsgrad(print_ahv_pension, ahv_contrib)

    print_bvg_income = calculate_bvg_income(print_income_data, 25, 65 +1)
    print_bvg_contributions = calculate_bvg_contrib(print_income_data, bvg_contrib, koordinationsabzug, max_bvg_income, min_bvg_income)
    print_yearly_yield_list = calculate_bvg_yield()
    print_bvg_asset = calculate_bvg_capital(print_bvg_contributions, print_yearly_yield_list)
    print_bvg_pension = calculate_bvg_pension(print_bvg_asset)
    print_deckungsgrad_bvg = calculate_deckungsgrad_bvg(print_bvg_contributions, print_bvg_pension, print_income_data)
    print_bvg_pension_monthly = print_bvg_pension["pension_monthly"]
    print_bvg_pension_capital = print_bvg_pension["kapitalbezug"]
    print_bvg_total_pension = print_bvg_pension["total_pension"] 
    print_bvg_capital_monthly = print_bvg_pension["capital_pension_monthly"]

    print_last_income = calculate_last_income(print_income_data) 
    print_pension_1_2 = calculate_pension_1_2(print_bvg_pension, print_ahv_pension) 
    print_percentage_income = calculate_percentage_income(print_pension_1_2, print_last_income)
    print_necessary_pension = calculate_necessary_pension(print_pension_1_2, print_last_income)
    print_years_s = time_for_saving_rate(print_vintage, basic_year, pension_age)
    print_capital_inflation_msci_saving_rate_s = required_savings_rate(print_necessary_pension["necessary_portfolio_capital"], avg_yearly_yield_incl_infl, print_years_s, tol=1e-3, max_iter=100) 
    print_capital_inflation_msci_saving_rate_p = final_portfolio_annual(print_capital_inflation_msci_saving_rate_s, print_years_s, avg_yearly_yield_incl_infl, print_last_income)
    print_capital_inflation_bank_saving_rate_s = required_savings_rate(print_necessary_pension["necessary_portfolio_capital"], avg_saving_yield_incl_infl, print_years_s, tol=1e-3, max_iter=100) 
    print_capital_inflation_bank_saving_rate_p = final_portfolio_annual(print_capital_inflation_bank_saving_rate_s, print_years_s, avg_saving_yield_incl_infl, print_last_income) 
    print_inflation_msci_saving_rate_s = required_savings_rate(print_necessary_pension["necessary_portfolio"], avg_yearly_yield_incl_infl, print_years_s, tol=1e-3, max_iter=100) 
    print_inflation_msci_saving_rate_p = final_portfolio_annual(print_inflation_msci_saving_rate_s, print_years_s, avg_yearly_yield_incl_infl, print_last_income)
    print_inflation_bank_saving_rate_s = required_savings_rate(print_necessary_pension["necessary_portfolio"], avg_saving_yield_incl_infl, print_years_s, tol=1e-3, max_iter=100) 
    print_inflation_bank_saving_rate_p = final_portfolio_annual(print_inflation_bank_saving_rate_s, print_years_s, avg_saving_yield_incl_infl, print_last_income) 

    print_saving_rate_data = calculate_saving_rates(print_capital_inflation_msci_saving_rate_s, print_capital_inflation_bank_saving_rate_s, print_inflation_msci_saving_rate_s, print_inflation_bank_saving_rate_s)

    print_capital_inflation_msci_saving_rate_s = print_saving_rate_data["capital_inflation_msci_saving_rate"]
    print_capital_inflation_bank_saving_rate_s = print_saving_rate_data["capital_inflation_bank_saving_rate_s"]
    print_inflation_msci_saving_rate_s = print_saving_rate_data["inflation_msci_saving_rate_s"]
    print_inflation_bank_saving_rate_s = print_saving_rate_data ["inflation_bank_saving_rate_s"]

    print_pension_1_2_pension = print_pension_1_2["pension_total"]
    print_pension_1_2_capital = print_pension_1_2["pension_bvg_capital_total"]


    #Resultate speichern
    results = {
        "Jahrgang": print_vintage,
        "Income": print_income_data,
        "Average Income": print_average_income,
        "form_data": request.form
    }

    return render_template("data.html", results = results, form_data = request.form)


if __name__ == "__main__":
    app.run(debug=True)
