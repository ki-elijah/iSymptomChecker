import streamlit as st
import pandas as pd
import speech_recognition as sr
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import json
import os

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

# Translations
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
            "headache": "Headache",
            "vomiting": "Vomiting",
            "diarrhea": "Diarrhea",
            "rash": "Rash",
            "difficulty_breathing": "Breathing Difficulty",
            "swollen_lymph_nodes": "Swollen Lymph Nodes",
            "loss_of_appetite": "Loss of Appetite",
            "abdominal_pain": "Abdominal Pain",
            "chills": "Chills",
            "convulsions": "Convulsions",
            "dehydration": "Dehydration",
            "malnutrition": "Malnutrition"
        }
    },
    "lg": {
        "title": "AI Okuyamba mu By'obulwadde 🇺🇬",
        "language": "Lulimi:",
        "input_method": "Enkola y'okwewandiisa",
        "voice": "Eddoboozi",
        "manual": "Amannyo",
        "check_button": "Pima Ebimubonero",
        "result": "Ebisobola okuba:",
        "first_aid": "Eby'okukola olw'okubanga:",
        "symptoms": {
            "fever": "Omusujja",
            "cough": "Enkuba",
            "fatigue": "Okuwuka",
            "headache": "Olubuto olw'omutwe",
            "vomiting": "Okusanza",
            "diarrhea": "Endwadde z'omunda",
            "rash": "Akabombo",
            "difficulty_breathing": "Okubeera n'ebizibu by'okussa omukka",
            "swollen_lymph_nodes": "Amasiri agukuba",
            "loss_of_appetite": "Okutamagwa n'emmere",
            "abdominal_pain": "Okulumwa omunda",
            "chills": "Okububbula",
            "convulsions": "Okukankana",
            "dehydration": "Ensonga y'okukaluubirira",
            "malnutrition": "Obwavu"
        }
    },
    "sw": {
        "title": "Kianga cha Dalili za Watoto 🇺🇬",
        "language": "Lugha:",
        "input_method": "Njia ya Uingizaji",
        "voice": "Sauti",
        "manual": "Mkono",
        "check_button": "Angalia Dalili",
        "result": "Uchunguzi",
        "first_aid": "Msaada wa Kwanza",
        "symptoms": {
            "fever": "Homa",
            "cough": "Kikohozi",
            "fatigue": "Uchovu",
            "headache": "Maumivu ya kichwa",
            "vomiting": "Kutapika",
            "diarrhea": "Kuhara",
            "rash": "Upele",
            "difficulty_breathing": "Ugumu wa kupumua",
            "swollen_lymph_nodes": "Vimbe limu",
            "loss_of_appetite": "Kupoteza hamu ya kula",
            "abdominal_pain": "Maumivu ya tumbo",
            "chills": "Vibaridi",
            "convulsions": "Kifafa",
            "dehydration": "Ukosefu wa maji",
            "malnutrition": "Utabibu mbaya"
        }
    },
    "ryn": {
        "title": "AI Kuriisa Oburwayi bw'Abana 🇺🇬",
        "language": "Oruhanga:",
        "input_method": "Enkyukakyuka y'okuteera",
        "voice": "Eijwi",
        "manual": "Eiboko",
        "check_button": "Shakisha Ebimubonero",
        "result": "Okushangwa",
        "first_aid": "Obuyambi obw'okw'okukora",
        "symptoms": {
            "fever": "Emburara",
            "cough": "Enkohozi",
            "fatigue": "Obunaku",
            "headache": "Obushuma bw'omutwe",
            "vomiting": "Okushatama",
            "diarrhea": "Okusharara",
            "rash": "Ebiheni",
            "difficulty_breathing": "Obuzibu bwo kwegyesa",
            "swollen_lymph_nodes": "Ebyondo eby'omubiri",
            "loss_of_appetite": "Okubura omushana gw'okurya",
            "abdominal_pain": "Obushuma bw'endya",
            "chills": "Obubabu",
            "convulsions": "Okukankana",
            "dehydration": "Obwenyana bw'amazi",
            "malnutrition": "Obubone bw'emmere"
        }
    }
}

# Language setup
language = st.radio(
    label=translations["en"]["language"],
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

# Voice input handler
def get_voice_input():
    lang_codes = {
        "en": "en-US",
        "sw": "sw-TZ",
        "lg": "en-US",
        "ryn": "en-US"
    }
    r = sr.Recognizer()
    with sr.Microphone() as source:
        prompt_text = {
            "en": "Speak now...",
            "lg": "Yogera kaakano...",
            "sw": "Sema sasa...",
            "ryn": "Hura omurambo..."
        }
        st.write(prompt_text[lang_code])
        audio = r.listen(source, timeout=5)
    try:
        return r.recognize_google(audio, language=lang_codes[lang_code])
    except Exception:
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
            "rash": ["rash", "akabombo", "upele", "ebiheni"],
            # Add more mappings for other symptoms
        }
        for symptom, keywords in keyword_map.items():
            for keyword in keywords:
                if keyword in voice_input.lower():
                    symptoms[symptom] = 1
else:
    col1, col2, col3 = st.columns(3)
    with col1:
        for sym in ["fever", "cough", "fatigue", "headache", "vomiting"]:
            symptoms[sym] = st.number_input(
                translations[lang_code]["symptoms"][sym],
                min_value=0, max_value=1, value=0
            )
    with col2:
        for sym in ["diarrhea", "rash", "difficulty_breathing", "swollen_lymph_nodes", "loss_of_appetite"]:
            symptoms[sym] = st.number_input(
                translations[lang_code]["symptoms"][sym],
                min_value=0, max_value=1, value=0
            )
    with col3:
        for sym in ["abdominal_pain", "chills", "convulsions", "dehydration", "malnutrition"]:
            symptoms[sym] = st.number_input(
                translations[lang_code]["symptoms"][sym],
                min_value=0, max_value=1, value=0
            )

# Prediction and results
if st.button(translations[lang_code]["check_button"]):
    input_data = pd.DataFrame([symptoms])[X.columns]
    try:
        prediction_encoded = model.predict(input_data)
        disease = le.inverse_transform(prediction_encoded)[0]
        
        st.subheader(translations[lang_code]["result"])
        st.write(f"**{disease}**")
        
        st.subheader(translations[lang_code]["first_aid"])
        try:
            advice = first_aid.get(disease, {})
            lang_keys = {
                "en": "english",
                "lg": "luganda",
                "sw": "swahili",
                "ryn": "runyankole"
            }
            st.write(advice.get(lang_keys[lang_code], "Information not available"))
        except Exception as e:
            st.error(f"Error: {str(e)}")
            
    except Exception as e:
        st.error(f"Prediction error: {str(e)}")