import streamlit as st
from utils import load_model

# Load model dan vectorizer
model = load_model('model/logistic_regression.pkl')
vectorizer = load_model('model/vectorizer.pkl')

from feedback import feedback_page
from review import review_page
from beranda import beranda_page

pages = {
    "Beranda": beranda_page,
    "Feedback": feedback_page,
    "Review": review_page
}

st.sidebar.title("Navigation")
selection = st.sidebar.selectbox("Choose a page", list(pages.keys()))

pages[selection](model, vectorizer)
