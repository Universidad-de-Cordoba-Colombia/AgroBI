import streamlit as st

def template1_page_style():  
    with open('template1_style.css') as f:
        css = f.read()
    st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

def template0_page_style():  
    with open('template0_style.css') as f:
        css = f.read()
    st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)