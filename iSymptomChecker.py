import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import json
import speech_recognition as sr
import numpy as np

# Load dataset
@st.cache_data
def load_data():
    data = pd.read_csv("symptom2disease_ug_children.csv")
    le = LabelEncoder()
    data["disease_encoded"] = le.fit_transform(data["disease"])
    return data, le

try:
    data, le = load_data()
    X = data.drop(["disease", "disease_encoded"], axis=1)
    y = data["disease_encoded"]
    model = RandomForestClassifier().fit(X, y)
    symptoms = {col: 0 for col in X.columns}
except Exception as e:
    st.error(f"Dataset error: {e}")
    st.stop()

# Load first-aid tips
try:
    with open("first_aid.json", "r") as f:
        first_aid = json.load(f)
except Exception as e:
    st.error(f"First-aid error: {e}")
    st.stop()

# Translations (fixed key consistency)
translations = {
    "en": {
        "title": "AI Pediatric Symptom Checker 🇺🇬",
        "language": "Language:",
        "input_method": "Input Method",
        "voice": "Voice",
        "manual": "Manual",
        "check_button": "Check Symptoms",
        "result": "Diagnosis",
        "first_aid": "First-Aid Tips",
        "symptoms": {
            "fever": "Fever",
            "cough": "Cough",
            "fatigue": "Fatigue",
            # ... include all other symptoms
        }
    },
    "lg": {
        "title": "AI Okuyamba mu By'obulwadde 🇺🇬",
        "language": "Lulimi:",
        "input_method": "Enkola y'okwewandiisa",
        "voice": "Eddoboozi",
        "manual": "Amannyo",
        # ... rest of Luganda translations
    },
    "sw": {
        "title": "Kianga cha Dalili za Watoto 🇺🇬",
        "language": "Lugha:",
        "input_method": "Njia ya Uingizaji",
        "voice": "Sauti",
        "manual": "Mkono",
        # ... rest of Swahili translations
    },
    "ryn": {
        "title": "AI Kuriisa Oburwayi bw'Abana 🇺🇬",
        "language": "Oruhanga:",
        "input_method": "Enkyukakyuka y'okuteera",
        "voice": "Eijwi",
        "manual": "Eiboko",
        # ... rest of Runyankole translations
    }
}

# Language setup at the TOP
language = st.radio(
    label="Select Language:",
    options=["English", "Luganda", "Swahili", "Runyankole"],
    index=0
)

lang_map = {
    "English": "en",
    "Luganda": "lg",
    "Swahili": "sw",
    "Runyankole": "ryn"
}
lang_code = lang_map[language]

# Browser-based voice input
def get_voice_input():
    audio_bytes = st.file_uploader(
        translations[lang_code]["voice"],
        type="wav"
    )
    
    if audio_bytes is not None:
        try:
            r = sr.Recognizer()
            with sr.AudioFile(audio_bytes) as source:
                audio = r.record(source)
                return r.recognize_google(audio)
        except Exception as e:
            st.error(f"Voice recognition error: {str(e)}")
    return None

# UI Components
st.title(translations[lang_code]["title"])

# Input method selection
input_method = st.radio(
    translations[lang_code]["input_method"],
    [translations[lang_code]["voice"], translations[lang_code]["manual"]]
)

# Symptom collection
if input_method == translations[lang_code]["voice"]:
    voice_input = get_voice_input()
    if voice_input:
        st.write(f"Recognized: {voice_input}")
        symptoms = {col: 0 for col in X.columns}
        keyword_map = {
            "fever": ["fever", "omusujja", "homa", "emburara"],
            "cough": ["cough", "enkuba", "kikohozi", "enkohozi"],
            # Add mappings for all symptoms...
        }
        for symptom, keywords in keyword_map.items():
            for keyword in keywords:
                if keyword.lower() in voice_input.lower():
                    symptoms[symptom] = 1
else:
    col1, col2, col3 = st.columns(3)
    with col1:
        for sym in ["fever", "cough", "fatigue", "headache", "vomiting"]:
            symptoms[sym] = st.number_input(
                translations[lang_code]["symptoms"][sym],
                min_value=0, max_value=1, value=0
            )
    # Add other columns similarly...

# Prediction and results
if st.button(translations[lang_code]["check_button"]):
    input_data = pd.DataFrame([symptoms])[X.columns]
    try:
        prediction_encoded = model.predict(input_data)
        disease = le.inverse_transform(prediction_encoded)[0]
        
        st.subheader(translations[lang_code]["result"])
        st.write(f"**{disease}**")
        
        st.subheader(translations[lang_code]["first_aid"])
        advice = first_aid.get(disease, {})
        lang_keys = {"en": "english", "lg": "luganda", "sw": "swahili", "ryn": "runyankole"}
        st.write(advice.get(lang_keys[lang_code], "Information not available"))
        
    except Exception as e:
        st.error(f"Prediction error: {str(e)}")