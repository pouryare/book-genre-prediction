import joblib
import nltk
import streamlit as st
import os
import re
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.corpus import stopwords

# Download NLTK data
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)

# Set up paths
current_dir = os.getcwd()
model_path = os.path.join(current_dir, 'genre_prediction_model.joblib')
vectorizer_path = os.path.join(current_dir, 'tfidf_vectorizer.joblib')
label_encoder_path = os.path.join(current_dir, 'label_encoder.joblib')

# Load the model and vectorizer
@st.cache_resource
def load_model():
    model = joblib.load(model_path)
    vectorizer = joblib.load(vectorizer_path)
    label_encoder = joblib.load(label_encoder_path)
    return model, vectorizer, label_encoder

model, vectorizer, label_encoder = load_model()

def clean_text(text):
    text = re.sub("'", "", text)
    text = re.sub("[^a-zA-Z]", " ", text)
    text = ' '.join(text.split())
    return text.lower()

def remove_stopwords(text):
    stop_words = set(stopwords.words('english'))
    return ' '.join([word for word in text.split() if word not in stop_words])

def lemmatize_text(text):
    lemmatizer = WordNetLemmatizer()
    return ' '.join([lemmatizer.lemmatize(word) for word in text.split()])

def stem_text(text):
    stemmer = PorterStemmer()
    return ' '.join([stemmer.stem(word) for word in text.split()])

@st.cache_data
def preprocess_text(text):
    text = clean_text(text)
    text = remove_stopwords(text)
    text = lemmatize_text(text)
    text = stem_text(text)
    return text

def predict_genre(text):
    preprocessed_text = preprocess_text(text)
    text_vector = vectorizer.transform([preprocessed_text])
    predicted_genre_encoded = model.predict(text_vector)[0]
    predicted_genre = label_encoder.inverse_transform([predicted_genre_encoded])[0]
    return predicted_genre

# Streamlit UI
st.title('Book Genre Prediction')

summary = st.text_area('Enter the Summary of the Book')

if st.button('Predict'):
    if summary:
        genre = predict_genre(summary)
        st.success(f"Predicted Genre: {genre}")
        st.write(f"Summary (first 100 characters): {summary[:100]}...")
    else:
        st.warning('Please enter a summary.')