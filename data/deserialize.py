import os
import xmltodict
import dotenv
from pprint import pprint

dec_xml_dir = "./data/decoded_xml_files"
testing_dec_xml = os.path.join(dec_xml_dir, os.listdir(dec_xml_dir)[1])

def print_statement(
    company_name, FNR, legal_structure, total_balance_sheet, fixed_assets, current_assets,
    prepaid_expenses, equity_capital, provisions, liabilities) -> None:

    print(f"Company {company_name} has the following data:")
    print(f"FNR: {FNR} | legal structure: {legal_structure}")
    print(f"Their total balance sheet is {total_balance_sheet}")
    print(f"fixed assets: {fixed_assets}")
    print(f"current assets: {current_assets}")
    print(f"prepaid expenses: {prepaid_expenses}\n")
    print(f"equity capital: {equity_capital}")
    print(f"provisions: {provisions}")
    print(f"liabilities: {liabilities}")

with open(testing_dec_xml, "r", encoding="utf-8") as f:
    data = xmltodict.parse(f.read())
    # pprint(data)
    file_info = data.get("UEBERMITTLUNG", {}).get("INFO_DATEN", {})
    file_info_version = file_info["VERS"] if file_info is not None else None
    document = data["UEBERMITTLUNG"].get(["BILANZ_GLIEDERUNG"]) 

    if document == "ALLG_JUSTIZ":
        justice_doc = document
        doc_version = justice_doc["VERS"]

        company = justice_doc["FIRMA"]
        FNR = company["FNR"]
        company_name = company["F_NAME"]
        
        filing_year = justice_doc["GJ"]
        filing_year_begin = filing_year["BEGINN"]
        filing_year_end = filing_year["ENDE"]
        legal_structure = filing_year["FORM"]

        financial_statement = justice_doc["HGB_Form_2"]
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
        Exception("Finanz Ministry document was found instead of Justice Ministry document!")
