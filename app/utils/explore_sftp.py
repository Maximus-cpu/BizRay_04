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
root_dir = "/uploads"
# remote_dir = ""

key = Ed25519Key.from_private_key_file(key_path)

transport = paramiko.Transport((host, 22))
transport.connect(username=user, pkey=key)
sftp = paramiko.SFTPClient.from_transport(transport)

sftp.chdir(root_dir)
print("Connected. Current dir:", sftp.getcwd())

# * I would run this with only up to 5 directories until the script is made more efficient with concurrency.
directories = sftp.listdir()[0:5]

# * For testing round trip of listdir() to the sftp server and back
# ! My average is around 5 seconds 
# start = time.perf_counter()
# sftp.listdir(directories[0])
# print("One listdir took", time.perf_counter() - start, "seconds")

total_files = 0
total_xml_files = 0
total_pdf_files = 0
files_list = []

for dir in directories:
    print(f"\nExploring [{dir}] directory now:")

    dir_path = f"{root_dir}/{dir}"
    files_list = sftp.listdir(dir_path)
    num_files = len(files_list)
    print(f"directory [{dir}] has {num_files} files")
    
    num_xml_files = sum(1 for f in files_list if f.endswith("XML.xml"))
    num_pdf_files = num_files - num_xml_files

    # * I used generators with the sum function for efficiency but below is earlier implementation
    # for file in files_list:
    #     if file[-7:] == "XML.xml":
    #         num_xml_files += 1
    #     else:
    #         num_pdf_files += 1
    
    total_files += num_files
    total_xml_files += num_xml_files
    total_pdf_files += num_pdf_files

    print(f"directory [{dir}] has {num_xml_files} xml files") 
    print(f"directory [{dir}] has {num_pdf_files} pdf files")
    
print(f"\nThe total number of files is {total_files}")
print(f"The total number of XML files is {total_xml_files}")
print(f"The total number of PDF files is {total_pdf_files}")

sftp.close()
transport.close()

end = time.time()
print(f"Total Execution time: {end - start:.2f} seconds")
