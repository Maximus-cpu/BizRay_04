import os
import xmltodict
import dotenv
from pprint import pprint

dec_xml_dir = "./data/decoded_xml_files"
testing_dec_xml = os.path.join(dec_xml_dir, os.listdir(dec_xml_dir)[1])

with open(testing_dec_xml, "r", encoding="utf-8") as f:
    data = xmltodict.parse(f.read())
    # pprint(data)
    file_info = data["UEBERMITTLUNG"]["INFO_DATEN"]
    file_version = file_info["VERS"]

    if file_version == "03.32": 
        justiz_data = data["UEBERMITTLUNG"]["BILANZ_GLIEDERUNG"]
        company_data = justiz_data["FIRMA"]

        FNR = company_data["FNR"]
        company_name = company_data["F_NAME"]
        legal_structure = company_data["GJ"]["FORM"]
    else:
        raise Exception("Unexpected xml file. Version does not correspond to schema version.")