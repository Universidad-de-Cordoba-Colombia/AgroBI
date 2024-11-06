import streamlit as st
from styling import template1_page_style
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

def main():  
    st.title('Welcome to Streamlit_UI_Template')  
    st.write('-'*50)
    st.markdown("<p style='text-align: center; color: black;'>This is a demo page created with Streamlit. \
                It uses a custom CSS file to modify the UI.</p>", unsafe_allow_html=True)  
    st.write('-'*50)
  
    user_name = st.text_input('Please enter your name')  
  
    # Add a selectbox to the sidebar.  
    option = st.selectbox(  
        'Which greeting do you prefer?',  
        ['Hello', 'Hi', 'Hey'])  
  
    if st.button('Greet Me'):  
        if user_name:  
            st.success(f'{option}, {user_name}! Nice to meet you.')  
        else:  
            st.success(f'{option} there! Nice to meet you.')  
  


if __name__ == "__main__":  
    template1_page_style()
    main()  






