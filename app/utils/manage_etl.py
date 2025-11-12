import os
from app import create_app
from app.utils.deserialize import deserialize_financial_statement
from app.utils.load_files import load_companies

app = create_app()

with app.app_context():
    dec_xml_dir = "./app/utils/decoded_xml_files"
    file = os.listdir(dec_xml_dir)[0]
    # print(files_list)

    # for files in files_list:
    testing_dec_xml = os.path.join(dec_xml_dir, file)
    company_data = deserialize_financial_statement(testing_dec_xml)
    load_companies(company_data)