# admin.py

import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def data_page():
    # Fungsi untuk mengambil data dari database
    def get_data_from_database():
        conn = sqlite3.connect('pandusaha.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM sentiment_analysis")
        data = cursor.fetchall()
        conn.close()
        return data

    # Fungsi untuk menghapus data dari database berdasarkan ID
    def delete_data_from_database(ids):
        conn = sqlite3.connect('pandusaha.db')
        cursor = conn.cursor()
        for id in ids:
            cursor.execute("DELETE FROM sentiment_analysis WHERE ID=?", (id,))
        conn.commit()
        conn.close()
        st.success("Data berhasil dihapus")

    # Ambil data dari database
    data = get_data_from_database()

    # Tampilkan data jika ada
    if data:
        # Konversi data ke DataFrame
        df = pd.DataFrame(data, columns=['ID', 'Feedback', 'Sentiment'])

        # Menampilkan tabel interaktif dengan st.table()
        st.write('## Data Sentimen:')
        st.table(df[['Feedback', 'Sentiment']])
        
        # Menambahkan multiselect untuk memilih data yang ingin dihapus
        st.write('Pilih data yang ingin dihapus:')
        selected_feedback = st.multiselect(
            "Pilih Feedback yang akan dihapus:",
            df['Feedback'].tolist()
        )

        # Filter ID berdasarkan feedback yang dipilih
        selected_ids = df[df['Feedback'].isin(selected_feedback)]['ID'].tolist()

        # Tombol untuk menghapus data yang dipilih
        if st.button('Hapus Data Terpilih'):
            if selected_ids:
                delete_data_from_database(selected_ids)
                # Refresh data setelah penghapusan
                data = get_data_from_database()
                if data:
                    df = pd.DataFrame(data, columns=['ID', 'Feedback', 'Sentiment'])
                    st.table(df[['Feedback', 'Sentiment']])
                else:
                    st.write("Tidak ada data yang tersedia.")
            else:
                st.warning("Tidak ada data yang dipilih untuk dihapus.")
        
        # Menghitung jumlah dan persentase sentimen
        sentiment_counts = df['Sentiment'].value_counts()
        total = sum(sentiment_counts)
        percentages = [(count / total) * 100 for count in sentiment_counts.values]
        labels = [f"{sentiment} ({percent:.1f}%)" for sentiment, percent in zip(sentiment_counts.index, percentages)]
        
        # Menampilkan visualisasi jumlah sentimen
        st.write('## Visualisasi Jumlah Sentimen:')
        fig, ax = plt.subplots(figsize=(10, 7))
        colors = sns.color_palette('pastel')[0:len(sentiment_counts)]
        patches, texts, _ = ax.pie(sentiment_counts, startangle=140, colors=colors, wedgeprops={'edgecolor': 'none'}, autopct='', pctdistance=0.85)
        for text, color in zip(texts, colors):
            text.set_color(color)
        ax.legend(patches, labels, loc="best")
        centre_circle = plt.Circle((0,0),0.70,fc='white', alpha=0.0)  # Membuat lingkaran pusat transparan
        fig.gca().add_artist(centre_circle)
        fig.patch.set_alpha(0.0)
        ax.set_title('Persentase Sentimen', fontsize=16)
        st.pyplot(fig)

    else:
        st.write('Tidak ada data yang tersedia.')
