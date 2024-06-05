import streamlit as st
import os
import sqlite3

def review_page(model, vectorizer):
    # Menggunakan os.path.join untuk memastikan kompatibilitas jalur
    image_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'Hero-Image.png')

    # Antarmuka Streamlit
    col1, col2 = st.columns(2)

    with col1:
        st.image(image_path)

    with col2:
        st.markdown("""
            <div style='margin-top: 150px;'>
                <h3>Review Pengguna</h3>
            </div>
            """, unsafe_allow_html=True)


    # Fungsi untuk mengambil data testimoni dari database
    def get_testimonials_from_database():
        try:
            conn = sqlite3.connect('pandusaha.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM sentiment_analysis")
            data = cursor.fetchall()
            conn.close()
            return data
        except Exception as e:
            st.error(f"An error occurred: {e}")
            return None

    # Ambil data testimoni dari database
    testimonials = get_testimonials_from_database()

    # Tampilkan testimoni jika ada
    if testimonials:
        for testimonial in testimonials:
            # Jika sentimen adalah positif, gunakan st.success
            if testimonial[2] == 'Positif':
                st.success(testimonial[1])
            # Jika sentimen adalah negatif, gunakan st.warning
            elif testimonial[2] == 'Negatif':
                st.warning(testimonial[1])
        
    else:
        st.write("Tidak ada testimoni yang tersedia.")
