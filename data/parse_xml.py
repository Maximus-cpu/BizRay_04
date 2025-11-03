import os
from lxml import etree

# * Here the xml schema files (.xsd) are used to validate and parse the decoded xml files
schema_dir = "./data/xml_schemas"
root_schema = os.path.join(schema_dir, "AllgemeineStruktur.xsd")
xsd_doc = etree.parse(root_schema)
schema = etree.XMLSchema(xsd_doc)

dec_xml_dir = "./data/decoded_xml_files"
# os.makedirs(out_dir, exist_ok=True)
for file in os.listdir(dec_xml_dir)[0:1]:
    xml_path = os.path.join(dec_xml_dir, file)
    parsed_xml = etree.parse(xml_path)
    if schema.validate(parsed_xml):
        print(f"{file} is valid")
    else:
        print(f"{file} is invalid")