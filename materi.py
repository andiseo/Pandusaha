import streamlit as st
import sqlite3
import os

def upload_material():
    st.write('## Unggah Materi Baru')

    # Input dari pengguna
    title = st.text_input('Judul Materi')
    description = st.text_area('Deskripsi Materi')
    link = st.text_input('Tautan Materi')
    image = st.file_uploader('Unggah Gambar Materi', type=['jpg', 'png', 'jpeg'])

    if st.button('Unggah Materi'):
        if title and description and link and image:
            # Simpan gambar yang diunggah
            if not os.path.exists('images'):
                os.makedirs('images')
                
            image_path = f"images/{image.name}"
            with open(image_path, 'wb') as file:
                file.write(image.getbuffer())

            # Simpan data ke database
            conn = sqlite3.connect('pandusaha.db')
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS materials (
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    Title TEXT,
                    Description TEXT,
                    Link TEXT,
                    ImagePath TEXT
                )
            """)
            cursor.execute("INSERT INTO materials (Title, Description, Link, ImagePath) VALUES (?, ?, ?, ?)", 
                          (title, description, link, image_path))
            conn.commit()
            conn.close()

            st.success('Materi berhasil diunggah!')
        else:
            st.error('Mohon lengkapi semua field sebelum mengunggah.')

def display_material():
    conn = sqlite3.connect('pandusaha.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM materials")
    materials = cursor.fetchall()
    conn.close()

    if materials:
        for material in materials:
          col1, col2 = st.columns(2)

          with col1:
            {st.image(material[4], width=350)}  
          
          with col2:

            st.markdown(
            f"""
            <div style='margin: 10px;
            '>
                <h5>{material[1]}</h5>
                <p>{material[2]}</p>
                <a href='{material[3]}' target='_blank'>
                <button style='
                    background-color: blue;
                    color: white;
                    padding: 5px 10px;
                    width: 100%;
                    border: none;
                    cursor: pointer;
                    border-radius: 5px;
                    text-align: center;
                    text-decoration: none;
                    display: inline-block;
                    font-size: 16px;
                '>
                    Pelajari
                </button>
            </a>
            </div>
            """,
            unsafe_allow_html=True)



    else:
        st.write('Belum ada materi yang diunggah.')
        
def delete_material():
    st.write('## Manage Materi')

    # Ambil daftar materi dari database
    conn = sqlite3.connect('pandusaha.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM materials")
    materials = cursor.fetchall()
    conn.close()

    if materials:
        for material in materials:
          col1, col2 = st.columns(2)

          with col1:
            {st.image(material[4], width=350)}  
          
          with col2:

            st.markdown(
            f"""
            <div style='margin-left: 10px; margin-top: 50px;
            '>
                <h5>{material[1]}</h5>
                <p>{material[2]}</p>
                
            </div>
            """,
            unsafe_allow_html=True)
          st.info(material[3])
          if st.button(f"Hapus Materi {material[0]}"):
            delete_material_from_database(material[0])
            st.success('Materi berhasil dihapus.')
    else:
        st.write("Tidak ada materi yang tersedia.")

def delete_material_from_database(material_id):
    # Fungsi untuk menghapus materi dari database berdasarkan ID
    conn = sqlite3.connect('pandusaha.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM materials WHERE ID=?", (material_id,))
    conn.commit()
    conn.close()
