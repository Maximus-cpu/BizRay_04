import os
import xmltodict
import dotenv
from pprint import pprint
import time

# start = time.time()

dec_xml_dir = "./app/utils/decoded_xml_files"
testing_dec_xml = os.path.join(dec_xml_dir, os.listdir(dec_xml_dir)[10])

def deserialize_financial_statement(xml_file_path: str) -> dict:
    print(f"Deserializing financial statement from:\n{xml_file_path}\n")

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

    with open(xml_file_path, "rb") as f:
        data = xmltodict.parse(f.read())
        file_info = data.get("UEBERMITTLUNG", {}).get("INFO_DATEN", {})
        file_info_version = file_info.get("VERS") 
        document = data["UEBERMITTLUNG"].get("BILANZ_GLIEDERUNG")
        
        if document:
            first_key = list(document.keys())[1]
        else:
            raise Exception("No BILANZ_GLIEDERUNG found in the document!")

        if first_key == "ALLG_JUSTIZ":

            justice_ministry_dict = document[first_key]
            doc_version = justice_ministry_dict["VERS"]

            company = justice_ministry_dict["FIRMA"]
            FNR = company["FNR"]
            company_name = company["F_NAME"]["Z"]

            if isinstance(company_name, list):
                company_name = ", ".join(company_name)
            
            filing_year = justice_ministry_dict["GJ"]
            filing_year_begin = filing_year["BEGINN"]
            filing_year_end = filing_year["ENDE"]
            legal_structure = filing_year["FORM"]
            legal_structure_full = company_legal_structure_map.get(legal_structure, legal_structure)

            financial_statement = document["HGB_Form_2"]
            assets_dict = financial_statement["HGB_224_2"]
            equity_dict = financial_statement["HGB_224_3"]

            balance_sheet_total = assets_dict["POSTENZEILE"]["BETRAG"]

            fixed_assets_items = assets_dict["HGB_224_2_A"]
            fixed_assets = fixed_assets_items["POSTENZEILE"]["BETRAG"]
            intangible_assets = fixed_assets_items.get("HGB_224_2_A_I", {}).get("POSTENZEILE", {}).get("BETRAG", 0.00)
            tangible_assets = fixed_assets_items.get("HGB_224_2_A_II", {}).get("POSTENZEILE", {}).get("BETRAG", 0.00)
            financial_assets = fixed_assets_items.get("HGB_224_2_A_III", {}).get("POSTENZEILE", {}).get("BETRAG", 0.00)
            
            
            current_assets_items = assets_dict["HGB_224_2_B"]
            current_assets = current_assets_items["POSTENZEILE"]["BETRAG"]
            stockpiles = current_assets_items.get("HGB_224_2_B_I", {}).get("POSTENZEILE", {}).get("BETRAG", 0.00)
            receivables = current_assets_items.get("HGB_224_2_B_II", {}).get("POSTENZEILE", {}).get("BETRAG", 0.00)
            securities_and_shares = current_assets_items.get("HGB_224_2_B_III", {}).get("POSTENZEILE", {}).get("BETRAG", 0.00)
            cash_and_bank_balances = current_assets_items.get("HGB_224_2_B_IV", {}).get("POSTENZEILE", {}).get("BETRAG", 0.00)

            prepaid_expenses = assets_dict["HGB_224_2_C"]["POSTENZEILE"]["BETRAG"]

            equity_items = equity_dict["HGB_224_3_A"]
            equity = equity_items["POSTENZEILE"]["BETRAG"]

            # Here it could be any of the following for required share capital:
            # HGB_224_3_A_I
            # HGB_229_1_A_I
            # XXX_224_3_A_I_X
            # XXX_224_3_A_I_Y
            # Due to edge cases I am setting it to 0.00 for now
            # required_share_capital = equity_items["HGB_229_1_A_I"]["POSTENZEILE"]["BETRAG"]
            required_share_capital = 0.00
            capital_reserves = equity_items.get("HGB_224_3_A_II", {}).get("POSTENZEILE", {}).get("BETRAG", 0.00)
            retained_earnings = equity_items.get("HGB_224_3_A_III", {}).get("POSTENZEILE", {}).get("BETRAG", 0.00)
            balance_sheet_profit = equity_items.get("HGB_224_3_A_IV", {}).get("POSTENZEILE", {}).get("BETRAG", 0.00)
            profit_carried_forward = equity_items.get("HGB_224_3_A_IV", {}).get("HGB_224_3_A_IV_x", {}).get("POSTENZEILE", {}).get("BETRAG", 0.00)
            
            accruals = equity_dict.get("HGB_224_3_C", {}).get("POSTENZEILE", {}).get("BETRAG", 0.00)
            liabilities = equity_dict.get("HGB_224_3_D", {}).get("POSTENZEILE", {}).get("BETRAG", 0.00)

            # Here we might have another edge case:
            # long_term_liabilities could be found in:

            # <HGB_224_3_D>
            # 			<POSTENZEILE>
            # 				<BETRAG>325473.20</BETRAG>
            # 				<BETRAG_VJ>280457.77</BETRAG_VJ>
            # 			</POSTENZEILE>
            # 			<HGB_224_3_D_HGB_225b>
            # 				<POSTENZEILE>
            # 					<BETRAG>77226.66</BETRAG>
            
            long_term_liabilities = equity_dict.get("HGB_224_3_D", {}).get("HGB_224_3_D_I", {}).get("POSTENZEILE", {}).get("BETRAG", 0.00)

            # Fields to calculate:

            # ongoing_result
            # equity_ratio
            # debt_ratio
            # coverage_fixed_assets
            # liquidity_ratio
            # working_capital

            return {
                "company_name": company_name,
                "FNR": FNR,
                "legal_structure_full": legal_structure_full,
                "legal_structure": legal_structure,
                "balance_sheet_total": float(balance_sheet_total),
                "fixed_assets": float(fixed_assets),
                "intangible_assets": float(intangible_assets),
                "tangible_assets": float(tangible_assets),
                "financial_assets": float(financial_assets),
                "current_assets": float(current_assets),
                "stockpiles": float(stockpiles),
                "receivables": float(receivables),
                "securities_and_shares": float(securities_and_shares),
                "cash_and_bank_balances": float(cash_and_bank_balances),
                "prepaid_expenses": float(prepaid_expenses),
                "equity": float(equity),
                "required_share_capital": float(required_share_capital),
                "capital_reserves": float(capital_reserves),
                "retained_earnings": float(retained_earnings),
                "balance_sheet_profit": float(balance_sheet_profit),
                "profit_carried_forward": float(profit_carried_forward),
                "accruals": float(accruals),
                "liabilities": float(liabilities),
                "long_term_liabilities": float(long_term_liabilities),
                "filing_year_begin": filing_year_begin,
                "filing_year_end": filing_year_end
            }
        
        else:
            raise Exception("Finanz Ministry document was found instead of Justice Ministry document!")

    # end = time.time()
    # print(f"Total Execution time: {end - start:.5f} seconds")
    
for key, value in deserialize_financial_statement(testing_dec_xml).items():
    print(key, value)