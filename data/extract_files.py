from dotenv import load_dotenv
import os
from paramiko import Ed25519Key
import paramiko
import time

start = time.time()

load_dotenv()

key_path = os.getenv("FTP_KEY_PATH")
host = os.getenv("FTP_HOST")
user = os.getenv("FTP_USER")
remote_dir = "/uploads/"
local_dir = "./data/encoded_xml_files"

key = Ed25519Key.from_private_key_file(key_path)

transport = paramiko.Transport((host, 22))
transport.connect(username=user, pkey=key)
sftp = paramiko.SFTPClient.from_transport(transport)

sftp.chdir("/")
print("Connected. Current dir:", sftp.getcwd())

sftp.chdir("/uploads/000")
remote_dir += "000/"

head_files_000 = sftp.listdir()[0:100]
extract_amount = 30
count_extraction = 0

for file in head_files_000:
    if file[-7:] == "XML.xml":
        sftp.get(f"{remote_dir}/{file}", f"{local_dir}/{file}")
        print(f"Extracted {file} to {local_dir + file}")
        count_extraction += 1
        print(f"extraction num: {count_extraction}")

        if count_extraction >= extract_amount:
            break

sftp.close()
transport.close()

end = time.time()
print(f"Total Execution time: {end - start:.2f} seconds")