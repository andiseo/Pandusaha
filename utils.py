import pickle
import sqlite3
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import string
import os

# Mengunduh resource NLTK
nltk.download('stopwords')
nltk.download('punkt')

# Fungsi untuk memuat model dari file pickle
def load_model(filename):
    # Menggunakan os.path.join untuk memastikan kompatibilitas jalur
    model_path = os.path.join(os.path.dirname(__file__), '..', filename)
    with open(model_path, 'rb') as file:
        model = pickle.load(file)
    return model

# Fungsi untuk melakukan preprocessing teks
def preprocess_text(text):
    stemmer = PorterStemmer()
    stop_words = set(stopwords.words('indonesian'))
    
    # Lowercasing teks
    text = text.lower()
    
    # Tokenisasi teks
    tokens = word_tokenize(text)
    
    # Pembersihan teks dari tanda baca dan stopwords
    tokens = [token for token in tokens if token not in string.punctuation]
    tokens = [token for token in tokens if token not in stop_words]
    
    # Stemming teks
    tokens = [stemmer.stem(token) for token in tokens]
    
    # Menggabungkan kembali token-token menjadi kalimat
    preprocessed_text = ' '.join(tokens)
    
    return preprocessed_text

# Fungsi untuk melakukan analisis sentimen
def analyze_sentiment(text, model, vectorizer):
    # Preprocessing teks
    preprocessed_text = preprocess_text(text)
    
    # Transformasi teks
    processed_text = vectorizer.transform([preprocessed_text])
    
    # Prediksi sentimen
    sentiment = model.predict(processed_text)[0]
    return sentiment

# Fungsi untuk menyimpan hasil analisis ke database SQLite
def save_to_database(text, sentiment):
    try:
        # Membuat atau terhubung ke database SQLite
        conn = sqlite3.connect('pandusaha.db')
        cursor = conn.cursor()
        
        # Membuat tabel jika belum ada
        cursor.execute('''CREATE TABLE IF NOT EXISTS sentiment_analysis
                        (id INTEGER PRIMARY KEY AUTOINCREMENT, text TEXT, sentiment TEXT)''')

        # Menyimpan data ke database
        cursor.execute("INSERT INTO sentiment_analysis (text, sentiment) VALUES (?, ?)", (text, sentiment))
        
        # Commit perubahan
        conn.commit()
        
        # Menutup koneksi
        cursor.close()
        conn.close()
        
        return True
    except Exception as ex:
        return False

# Fungsi untuk menghapus data dari database
def delete_data_from_database():
    try:
        conn = sqlite3.connect('pandusaha.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM sentiment_analysis")
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        return False

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
        return None

# Fungsi untuk mengambil data dari database
def get_data_from_database():
    try:
        conn = sqlite3.connect('pandusaha.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM sentiment_analysis")
        data = cursor.fetchall()
        conn.close()
        return data
    except Exception as e:
        return None

# Fungsi untuk menghapus data dari database berdasarkan ID
def delete_data_by_id(ids):
    try:
        conn = sqlite3.connect('pandusaha.db')
        cursor = conn.cursor()
        for id in ids:
            cursor.execute("DELETE FROM sentiment_analysis WHERE ID=?", (id,))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        return False
