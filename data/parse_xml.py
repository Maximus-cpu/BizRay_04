import os
from lxml import etree

# * Here the xml schema files (.xsd) are used to validate and parse the decoded xml files
schema_dir = "./data/xml_schemas"
root_schema = os.path.join(schema_dir, "AllgemeineStruktur.xsd")
xsd_doc = etree.parse(root_schema)
schema = etree.XMLSchema(xsd_doc)

dec_xml_dir = "./data/decoded_xml_files"

# * When you try to only parse the first file you get an output of invalid due to the xml schema being from 2017 and the actual data being from 2023.
for file in os.listdir(dec_xml_dir)[0:1]:
    xml_path = os.path.join(dec_xml_dir, file)
    tree = etree.parse(xml_path)
    root = tree.getroot()

    # * This schema validation is not necessary for now.
    # if schema.validate(tree):
    #     print(f"{file} is valid")
    # else:
    #     print(f"{file} is invalid")
    #     for error in schema.error_log:
    #         print(f"Line {error.line}, column {error.column}: {error.message}")