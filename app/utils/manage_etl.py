import os
from app.utils.deserialize import deserialize_financial_statement
from app.utils.load_files import load_companies

dec_xml_dir = "./app/utils/decoded_xml_files"
testing_dec_xml = os.path.join(dec_xml_dir, os.listdir(dec_xml_dir)[0])

company_data = deserialize_financial_statement(testing_dec_xml)
load_companies(company_data)