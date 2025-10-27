ETL stands for extract, transform, and load. This pipeline is used to take files from the sftp server and upload them to an external database.
### Extraction
- Is done with a python script `extract_files.py`
- There are PDF and XML files on sftp server, with both being 64-bit encoded and wrapped by another XML file.

### Transformation
This step requires decoding and parsing the data in the original xml file.

- Decoding and transformation done with the script inside of `transform.py`

### Loading
python script to upload data to a database will be created

### ETL Pipeline Management
- python file to manage or streamline this pipeline will be created.