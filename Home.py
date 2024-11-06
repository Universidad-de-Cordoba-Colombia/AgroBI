import streamlit as st
import urllib.request
import shutil
import os

if not os.path.exists('datos'):
    os.makedirs('datos')

urlinsumos = "https://agrounicor.s3.us-east-1.amazonaws.com/datos/vista_insumos.csv"
output_file_insumos = "datos/vista_insumos.csv"
with urllib.request.urlopen(urlinsumos) as response1, open(output_file_insumos, 'wb') as out_file1:
    shutil.copyfileobj(response1, out_file1)

urlBI = "https://agrounicor.s3.us-east-1.amazonaws.com/datos/VistaBI.csv"
output_file_BI = "datos/vista_BI.csv"
with urllib.request.urlopen(urlBI) as response2, open(output_file_BI, 'wb') as out_file2:
    shutil.copyfileobj(response2, out_file2)

st.set_page_config(
    page_title="Plataforma BI",
    page_icon="👋",
initial_sidebar_state="collapsed"
)

st.write("# Inteligencia de negocios! 👋")



