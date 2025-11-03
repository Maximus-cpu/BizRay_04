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