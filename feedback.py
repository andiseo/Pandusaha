import streamlit as st
from utils import analyze_sentiment, save_to_database
import os

def feedback_page(model, vectorizer):
    col1, col2 = st.columns(2)

    with col1:
        # Menggunakan os.path.join untuk memastikan kompatibilitas jalur
        image_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'Hero-Image.png')
        st.image(image_path)

    with col2:
        st.markdown("""
            <div style='margin-top: 100px;'>
                <h3>Terima kasih telah mengikuti pembelajaran bersama Pandusaha</h3>
            </div>
            """, unsafe_allow_html=True)

    text = st.text_area('Masukkan anda sangat berharga bagi Pandusaha untuk terus mengembangkan layanan edukasi : ')
    if st.button('Kirim Feedback'):
        if text:
            sentiment = analyze_sentiment(text, model, vectorizer)
            
            # Simpan hasil analisis ke database
            if save_to_database(text, sentiment):
                st.success('Terima kasih atas feedback yang Anda berikan. Feedback Anda sangat berharga untuk perbaikan layanan kami.')
            else:
                st.error('Feedback gagal terkirim, mohon coba lagi dalam beberapa saat')
        else:
            st.warning('Silakan masukkan feedback Anda sebelum mengirim.')
