import flask
from flask import request, jsonify
import sqlite3

import psycopg2
import pandas as pd
from sshtunnel import SSHTunnelForwarder

try:

    with SSHTunnelForwarder(
         ('ml.cs.smu.ca', 22),
         #ssh_private_key="</path/to/private/ssh/key>",
         ### in my case, I used a password instead of a private key
         ssh_username="agyle",
         ssh_password="preparedAGYLE2020", 
         remote_bind_address=('localhost', 5432)) as server:
         
         server.start()
         print("server connected")

         params = {
             'database': 'agyle',
             'user': 'agyle',
             'password': 'preparedAGYLE2020',
             'host': 'localhost',
             'port': server.local_bind_port
             }

         conn = psycopg2.connect(**params)
         print("database connected")
         cursor = conn.cursor()
         cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND table_type='BASE TABLE';")
         res = cursor.fetchall()
         colnames = [desc[0] for desc in cursor.description]
         cursor.close()
         print(pd.DataFrame(res, columns=colnames))
         
except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
