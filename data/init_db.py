import sqlite3
import random

conn = sqlite3.connect("./data/BizRay.db")

conn.commit()
conn.close()