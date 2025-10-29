import base64
from xml.etree import ElementTree as ET
import os

xml_dir_path = "./data/xml_files/"
xml_files = os.listdir(xml_dir_path)
first_files = xml_files[1:9]

for file in first_files:
    tree = ET.parse(xml_dir_path + file)
    root = tree.getroot()
    ns = {"ns1": "ns://firmenbuch.justiz.gv.at/Abfrage/UrkundeResponse"}
    content_elem = root.find(".//ns1:CONTENT", ns)

    if content_elem is not None and content_elem.text:
        data = base64.b64decode(content_elem.text)
        with open(xml_dir_path + "decoded_" + file, "wb") as f:
            f.write(data)
        print(f"Decoded {file}, saved as decoded_{file}")
    else:
        print(f"Failed in decoding {file}")