import streamlit as st
import sqlite3
import os
from materi import display_material
image_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'Hero-Image.png')


def beranda_page(model, vectorizer):
  col1, col2= st.columns(2)

  with col1:
    st.markdown("""
      <div style='margin-top: 100px;'>
        <h2>Selamat Datang di Pandusaha</h2>
      </div>
    """, unsafe_allow_html=True)
  with col2:
    st.image(image_path)

  st.markdown("""
      <div style='text-align: center;'>
        <h3 style='margin-bottom: 30px'>Jelajahi Materi Kami</h1>
      </div>
    """, unsafe_allow_html=True)
  
  display_material()

  