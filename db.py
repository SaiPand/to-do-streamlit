import mysql.connector
import streamlit as st

conn = mysql.connector.connect(
    host="localhost",
    user=st.secrets.connections.mysql.username,
    password=st.secrets.connections.mysql.password,
)

cursor = conn.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTES tarea_streamlit")
cursor.execute("USE tarea_streamlit")
cursor.execute(
    """  CREATE TABLE IF NOT EXISTES tarea(
    id INT AUTO_INCREMENT PRIMARY KEY, texto VARCHAR(255) NOT NULL, completada BOOLEAN DEFAULT FALSE )  """
)

conn.commit()
conn.close()
