import base64
from lxml import etree
import os

def decode_xml_file(xml_file: str, enc_xml_dir: str) -> None:
    file_path = os.path.join(enc_xml_dir, xml_file)

    try:
        tree = etree.parse(file_path)
        root = tree.getroot()

        ns = {"ns1": "ns://firmenbuch.justiz.gv.at/Abfrage/UrkundeResponse"}
        content_elem = root.find(".//ns1:CONTENT", namespaces=ns)

        if content_elem is not None and content_elem.text:
            data = base64.b64decode(content_elem.text)
            out_dir = "./data/decoded_xml_files"
            os.makedirs(out_dir, exist_ok=True)

            out_path = os.path.join(out_dir, f"dec_{xml_file}")
            with open(out_path, "wb") as f:
                f.write(data)

            print(f"Decoded {xml_file}, saved as {out_path}")
        else:
            print(f"Failed to find CONTENT in {xml_file}")

    except etree.XMLSyntaxError as e:
        print(f"XML parsing failed for {xml_file}: {e}")

enc_xml_dir = "./data/encoded_xml_files"
enc_xml_files = os.listdir(enc_xml_dir)

for file in enc_xml_files:
    decode_xml_file(file, enc_xml_dir)