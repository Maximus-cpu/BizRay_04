import base64
from xml.etree import ElementTree as ET
import os

def decode_xml_file(xml_file: str, enc_xml_dir_path: str) -> None:
    tree = ET.parse(f"./{enc_xml_dir_path}/{xml_file}")
    root = tree.getroot()
    ns = {"ns1": "ns://firmenbuch.justiz.gv.at/Abfrage/UrkundeResponse"}
    content_elem = root.find(".//ns1:CONTENT", ns)

    if content_elem is not None and content_elem.text:
        data = base64.b64decode(content_elem.text)
        with open(f"./data/decoded_xml_files/dec_{xml_file}", "wb") as f:
            f.write(data)
        print(f"Decoded {xml_file}, saved as dec_{xml_file}")
    else:
        print(f"Failed in decoding {xml_file}")

enc_xml_dir_path = "./data/encoded_xml_files"

enc_xml_files = os.listdir(enc_xml_dir_path)

for file in enc_xml_files:
    decode_xml_file(file, enc_xml_dir_path)