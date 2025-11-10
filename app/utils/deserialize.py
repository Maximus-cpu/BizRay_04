import os
import xmltodict
import dotenv
from pprint import pprint

dec_xml_dir = "./app/utils/decoded_xml_files"
testing_dec_xml = os.path.join(dec_xml_dir, os.listdir(dec_xml_dir)[0])

def print_statement(
    company_name, FNR, legal_structure, total_balance_sheet, fixed_assets, current_assets,
    prepaid_expenses, equity_capital, accruals, liabilities) -> None:
    
    statement = f"""
    Company {company_name} has the following data:

    FNR: {FNR}
    Legal structure: {legal_structure} => {company_legal_structure_map.get(legal_structure)}

    ------Financial Statement------

    total balance sheet: {total_balance_sheet}
    fixed assets: {fixed_assets}
    current assets: {current_assets}
    prepaid expenses: {prepaid_expenses}

    equity capital: {equity_capital}
    accruals: {accruals}
    liabilities: {liabilities}
    """

    print(statement)

company_legal_structure_map = {
    "GmbH": "Gesellschaft mit beschränkter Haftung",
    "AG": "Aktiengesellschaft",
    "OG": "Offene Gesellschaft",
    "KG": "Kommanditgesellschaft",
    "GmbH & Co KG": "Kommanditgesellschaft mit einer GmbH als Komplementärin",
    "e.U.": "Eingetragener Unternehmer",
    "Einzelunternehmen": "Einzelunternehmen",
    "GesbR": "Gesellschaft bürgerlichen Rechts",
    "Genossenschaft": "Genossenschaft",
    "Erwerbs- und Wirtschaftsgenossenschaft": "Erwerbs- und Wirtschaftsgenossenschaft",
    "Verein": "Verein (gemeinnützige Organisation)",
    "Stiftung": "Stiftung",
    "Privatstiftung": "Privatstiftung",
    "SE": "Europäische Gesellschaft (Societas Europaea)",
    "SCE": "Europäische Genossenschaft (Societas Cooperativa Europaea)",
    "OG mbH": "Offene Gesellschaft mit beschränkter Haftung",
    "PartG": "Partnerschaftsgesellschaft",
    "GmbH & Co OG": "Offene Gesellschaft mit einer GmbH als Gesellschafterin",
    "GmbH & Co OHG": "Offene Handelsgesellschaft mit einer GmbH als Komplementärin"
}

with open(testing_dec_xml, "rb") as f:
    data = xmltodict.parse(f.read())
    # pprint(data)
    file_info = data.get("UEBERMITTLUNG", {}).get("INFO_DATEN", {})
    file_info_version = file_info.get("VERS") 
    document = data["UEBERMITTLUNG"].get("BILANZ_GLIEDERUNG")
    
    if document:
        first_key = list(document.keys())[1]
    else:
        raise Exception("No BILANZ_GLIEDERUNG found in the document!")

    if first_key == "ALLG_JUSTIZ":
        justice_doc = document[first_key]
        doc_version = justice_doc["VERS"]

        company = justice_doc["FIRMA"]
        FNR = company["FNR"]
        company_name = company["F_NAME"]["Z"]
        
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
        accruals = equity_items["HGB_224_3_C"]["POSTENZEILE"]["BETRAG"]
        liabilities = equity_items["HGB_224_3_D"]["POSTENZEILE"]["BETRAG"]

        # Fields to add later:
        # balance_sheet_profit = equity_items["HGB_224_3_B"]["POSTENZEILE"]["BETRAG"]
        # retained_earnings = equity_items["HGB_224_3_E"]["POSTENZEILE"]["BETRAG"]
        # current_year_results = equity_items["HGB_224_3_F"]["POSTENZEILE"]["BETRAG"]

        print_statement(company_name, FNR, legal_structure, total_balance_sheet, fixed_assets, current_assets,
        prepaid_expenses, equity_capital, accruals, liabilities)
    
    else:
        raise Exception("Finanz Ministry document was found instead of Justice Ministry document!")