import os
import xmltodict
import dotenv
from pprint import pprint

dec_xml_dir = "./data/decoded_xml_files"
testing_dec_xml = os.path.join(dec_xml_dir, os.listdir(dec_xml_dir)[0])

def print_statement(
    company_name, FNR, legal_structure, total_balance_sheet, fixed_assets, current_assets,
    prepaid_expenses, equity_capital, provisions, liabilities) -> None:
    
    statement = f"""
    Company {company_name} has the following data:

    FNR: {FNR} | legal structure: {legal_structure}
    Their total balance sheet is {total_balance_sheet}
    current assets: {current_assets}
    prepaid expenses: {prepaid_expenses}
    equity capital: {equity_capital}"
    provisions: {provisions}
    liabilities: {liabilities}
    """

with open(testing_dec_xml, "rb") as f:
    data = xmltodict.parse(f.read())
    # pprint(data)
    file_info = data.get("UEBERMITTLUNG", {}).get("INFO_DATEN", {})
    file_info_version = file_info.get("VERS") 
    document = data["UEBERMITTLUNG"].get("BILANZ_GLIEDERUNG")
    first_key = list(document.keys())[1]

    if first_key == "ALLG_JUSTIZ":
        justice_doc = document[first_key]
        doc_version = justice_doc["VERS"]

        company = justice_doc["FIRMA"]
        FNR = company["FNR"]
        company_name = company["F_NAME"]
        
        filing_year = justice_doc["GJ"]
        filing_year_begin = filing_year["BEGINN"]
        filing_year_end = filing_year["ENDE"]
        legal_structure = filing_year["FORM"]

        financial_statement = document["HGB_Form_2"]
        assets = financial_statement["HGB_224_2"]
        total_balance_sheet = assets["POSTENZEILE"]["BETRAG"]
        fixed_assets = assets["HGB_224_2_A"]["POSTENZEILE"]["BETRAG"]
        current_assets = assets["HGB_224_2_B"]["POSTENZEILE"]["BETRAG"]
        prepaid_expenses = assets["HGB_224_2_C"]["POSTENZEILE"]["BETRAG"]

        equity_items = financial_statement["HGB_224_3"]
        equity_capital = equity_items["HGB_224_3_A"]["POSTENZEILE"]["BETRAG"]
        provisions = equity_items["HGB_224_3_C"]["POSTENZEILE"]["BETRAG"]
        liabilities = equity_items["HGB_224_3_D"]["POSTENZEILE"]["BETRAG"]

        print_statement(company_name, FNR, legal_structure, total_balance_sheet, fixed_assets, current_assets,
        prepaid_expenses, equity_capital, provisions, liabilities)
    
    else:
        raise Exception("Finanz Ministry document was found instead of Justice Ministry document!")

# Testing making changes with git push + authentication: