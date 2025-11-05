import os
import json
from lxml import etree
import xmlschema

# * Purpose of this script:
# First the normalization of the data in the xml files will be attempted to be automated with the xsd schema and the xmlschema package. 
# If an exception happen it will instead be attempted manually with the lxml package
schema_dir = "./data/xml_schemas"
root_schema = os.path.join(schema_dir, "AllgemeineStruktur.xsd")
dec_xml_dir = "./data/decoded_xml_files"
output_dir = "./data/normalized_json_files"

os.makedirs(output_dir, exist_ok=True)

# xsd_doc = etree.parse(root_schema)
# schema = etree.XMLSchema(xsd_doc)

schema = xmlschema.XMLSchema(root_schema)
normalized = []

# * When you try to only parse the first file you get an output of invalid due to the xml schema being from 2017 and the actual data being from 2023.
for file in os.listdir(dec_xml_dir)[0:10]:
    file_path = os.path.join(dec_xml_dir, file)
    json_path = os.path.join(output_dir, f"{os.path.splitext(file)[0]}.json")
    try:
        data_dict = schema.to_dict(file_path, validation='lax')
        normalized.append(data_dict)

        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(data_dict, f, ensure_ascii=False, indent=2, default=str)

        print(f"Parsed and saved: {file}")
    except xmlschema.XMLSchemaException as e:
        print(f"Skipped invalid file: {filename}")
        print(f"Reason: {e}")
    
    # xml_path = os.path.join(dec_xml_dir, file)
    # tree = etree.parse(xml_path)
    # root = tree.getroot()

    # * Schema validation with lxml instead of xmlschema:
    # if schema.validate(tree):
    #     print(f"{file} is valid")
    # else:
    #     print(f"{file} is invalid")
    #     for error in schema.error_log:
    #         print(f"Line {error.line}, column {error.column}: {error.message}")

# * Data exploration suggested:
# import json, glob

# for path in glob.glob("./data/normalized_json_files/*.json"):
#     with open(path, encoding="utf-8") as f:
#         data = json.load(f)
#         fastnr = data["UEBERMITTLUNG"]["INFO_DATEN"]["IDENTIFIKATIONSBEGRIFF"]
#         print(f"{os.path.basename(path)} → {fastnr}")
