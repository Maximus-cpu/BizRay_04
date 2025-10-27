from dotenv import load_dotenv
import os
from paramiko import Ed25519Key
import paramiko

load_dotenv()

key_path = os.getenv("FTP_KEY_PATH")
host = os.getenv("FTP_HOST")
user = os.getenv("FTP_USER")
remote_dir = "/uploads/"
local_dir = "./data/xml_files/"

key = Ed25519Key.from_private_key_file(key_path)

transport = paramiko.Transport((host, 22))
transport.connect(username=user, pkey=key)
sftp = paramiko.SFTPClient.from_transport(transport)

sftp.chdir("/")
print("Connected. Current dir:", sftp.getcwd())

sftp.chdir("/uploads/000")
remote_dir += "000/"

head_files_000 = sftp.listdir()[0:20]

for file in head_files_000:
    if file[-7:] == "XML.xml":
        sftp.get(remote_dir + file, local_dir + file)
        print(f"Extracted {file} to {local_dir + file}")

# sftp.get(remote_dir + "/000" + "/000002_6380471306070_000___000_30_7686006_XML.xml", local_dir + "/000002_6380471306070_000___000_30_7686006_XML.xml")

sftp.close()
transport.close()