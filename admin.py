import streamlit as st
from sentiment import data_page
from materi import upload_material, delete_material  # Mengimpor fungsi delete_material

pages = {
    "Data Feedback": data_page,
    "Upload Materi": upload_material,
    "Manage Materi": delete_material  # Menggunakan fungsi delete_material dalam daftar halaman
}

st.sidebar.title("Navigation")
selection = st.sidebar.selectbox("Choose a page", list(pages.keys()))

# Panggil fungsi terkait dengan pemilihan pengguna
pages[selection]()
