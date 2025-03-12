import os
from pydub import AudioSegment

# Set the path to ffmpeg explicitly
AudioSegment.converter = "C:\\ffmpeg\\bin\\ffmpeg.exe"
AudioSegment.ffprobe = "C:\\ffmpeg\\bin\\ffprobe.exe"

import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import json
import speech_recognition as sr
import io

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
            "headache": "Headache",
            "vomiting": "Vomiting",
            "diarrhea": "Diarrhea",
            "rash": "Rash",
            "difficulty_breathing": "Difficulty Breathing",
            "swollen_lymph_nodes": "Swollen Lymph Nodes",
            "loss_of_appetite": "Loss of Appetite",
            "abdominal_pain": "Abdominal Pain",
            "chills": "Chills",
            "convulsions": "Convulsions",
            "dehydration": "Dehydration",
            "pale_gums": "Pale Gums",
            "jaundice": "Jaundice",
            "joint_pain": "Joint Pain",
            "itching": "Itching",
            "malnutrition": "Malnutrition",
        }
    },
    "lg": {
        "title": "AI Okuyamba mu By'obulwadde 🇺🇬",
        "language": "Lulimi:",
        "input_method": "Enkola y'okwewandiisa",
        "voice": "Eddoboozi",
        "manual": "Amannyo",
        "check_button": "Kakasa Ebimubulamu",
        "result": "Obulwadde",
        "first_aid": "Ebyokukola mu By'obulwadde",
        "symptoms": {
            "fever": "Omusujja",
            "cough": "Enkuba",
            "fatigue": "Okukankana",
            "headache": "Okulumwa omutwe",
            "vomiting": "Okusebya",
            "diarrhea": "Okukyankalana",
            "rash": "Obubalya",
            "difficulty_breathing": "Obuzibu bw'okussa omukka",
            "swollen_lymph_nodes": "Amasiri agakulukutira",
            "loss_of_appetite": "Okugwa kw'amaanyi",
            "abdominal_pain": "Obulumi bw'endya",
            "chills": "Okubungubungu",
            "convulsions": "Okukankana",
            "dehydration": "Okukankana",
            "pale_gums": "Amalala agakulukutira",
            "jaundice": "Obulwadde bw'omujjofu",
            "joint_pain": "Obulumi bw'amalundi",
            "itching": "Okunyiga",
            "malnutrition": "Obulwadde bw'omukambwe",
        }
    },
    "sw": {
        "title": "Kianga cha Dalili za Watoto 🇺🇬",
        "language": "Lugha:",
        "input_method": "Njia ya Uingizaji",
        "voice": "Sauti",
        "manual": "Mkono",
        "check_button": "Angalia Dalili",
        "result": "Ugonjwa",
        "first_aid": "Mwongozo wa Kwanza",
        "symptoms": {
            "fever": "Homa",
            "cough": "Kikohozi",
            "fatigue": "Uchovu",
            "headache": "Maumivu ya kichwa",
            "vomiting": "Kutapika",
            "diarrhea": "Kuhara",
            "rash": "Upele",
            "difficulty_breathing": "Ugumu wa kupumua",
            "swollen_lymph_nodes": "Vimbe za tezi za limfu",
            "loss_of_appetite": "Kupoteza hamu ya kula",
            "abdominal_pain": "Maumivu ya tumbo",
            "chills": "Vimbe",
            "convulsions": "Kifafa",
            "dehydration": "Ukame",
            "pale_gums": "Ufinyu wa mdomo",
            "jaundice": "Yeloo",
            "joint_pain": "Maumivu ya viungo",
            "itching": "Kuwasha",
            "malnutrition": "Utabaka wa lishe",
        }
    },
    "ryn": {
        "title": "AI Kuriisa Oburwayi bw'Abana 🇺🇬",
        "language": "Oruhanga:",
        "input_method": "Enkyukakyuka y'okuteera",
        "voice": "Eijwi",
        "manual": "Eiboko",
        "check_button": "Kakasa Ebimubulamu",
        "result": "Obulwadde",
        "first_aid": "Ebyokukola mu By'obulwadde",
        "symptoms": {
            "fever": "Embura",
            "cough": "Enkohozi",
            "fatigue": "Okukankana",
            "headache": "Okulumwa omutwe",
            "vomiting": "Okusebya",
            "diarrhea": "Okukyankalana",
            "rash": "Obubalya",
            "difficulty_breathing": "Obuzibu bw'okussa omukka",
            "swollen_lymph_nodes": "Amasiri agakulukutira",
            "loss_of_appetite": "Okugwa kw'amaanyi",
            "abdominal_pain": "Obulumi bw'endya",
            "chills": "Okubungubungu",
            "convulsions": "Okukankana",
            "dehydration": "Okukankana",
            "pale_gums": "Amalala agakulukutira",
            "jaundice": "Obulwadde bw'omujjofu",
            "joint_pain": "Obulumi bw'amalundi",
            "itching": "Okunyiga",
            "malnutrition": "Obulwadde bw'omukambwe",
        }
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

def convert_audio(uploaded_file):
    """Convert various audio formats to WAV"""
    try:
        # Map file extensions to pydub formats
        format_map = {
            "mp3": "mp3",
            "opus": "ogg",  # OPUS is commonly in OGG container
            "wav": "wav",
            "ogg": "ogg"
        }
        
        file_format = uploaded_file.name.split(".")[-1].lower()
        audio = AudioSegment.from_file(
            io.BytesIO(uploaded_file.read()), 
            format=format_map.get(file_format, "wav")
        )
        
        # Convert to WAV format for speech recognition
        wav_io = io.BytesIO()
        audio.export(wav_io, format="wav")
        wav_io.seek(0)
        return wav_io
        
    except Exception as e:
        st.error(f"Audio conversion error: {str(e)}")
        return None
    
# Browser-based voice input
def get_voice_input():
    uploaded_file = st.file_uploader(
        translations[lang_code]["voice"],
        type=["wav", "mp3", "ogg", "opus"]
    )
    
    if uploaded_file is not None:
        try:
            # Convert to WAV
            wav_io = convert_audio(uploaded_file)
            if not wav_io:
                return None
                
            # Perform speech recognition
            r = sr.Recognizer()
            with sr.AudioFile(wav_io) as source:
                audio = r.record(source)
                return r.recognize_google(audio)
                
        except sr.UnknownValueError:
            st.error("Could not understand audio")
        except sr.RequestError as e:
            st.error(f"Google API error: {e}")
        except Exception as e:
            st.error(f"Error processing audio: {str(e)}")
    
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
            "fatigue": ["fatigue", "okukankana", "uchovu", "okukankana"],
            "headache": ["headache", "okulumwa omutwe", "maumivu ya kichwa", "okulumwa omutwe"],
            "vomiting": ["vomiting", "okusebya", "kutapika", "okusebya"],
            "diarrhea": ["diarrhea", "okukyankalana", "kuhara", "okukyankalana"],
            "rash": ["rash", "obubalya", "upele", "obubalya"],
            "difficulty_breathing": ["difficulty breathing", "obuzibu bw'okussa omukka", "ugumu wa kupumua", "obuzibu bw'okussa omukka"],
            "swollen_lymph_nodes": ["swollen lymph nodes", "amasiri agakulukutira", "vimbe za tezi za limfu", "amasiri agakulukutira"],
            "loss_of_appetite": ["loss of appetite", "okugwa kw'amaanyi", "kupoteza hamu ya kula", "okugwa kw'amaanyi"],
            "abdominal_pain": ["abdominal pain", "obulumi bw'endya", "maumivu ya tumbo", "obulumi bw'endya"],
            "chills": ["chills", "okubungubungu", "vimbe", "okubungubungu"],
            "convulsions": ["convulsions", "okukankana", "kifafa", "okukankana"],
            "dehydration": ["dehydration", "okukankana", "ukame", "okukankana"],
            "pale_gums": ["pale gums", "amalala agakulukutira", "ufinyu wa mdomo", "amalala agakulukutira"],
            "jaundice": ["jaundice", "obulwadde bw'omujjofu", "yeloo", "obulwadde bw'omujjofu"],
            "joint_pain": ["joint pain", "obulumi bw'amalundi", "maumivu ya viungo", "obulumi bw'amalundi"],
            "itching": ["itching", "okunyiga", "kuwasha", "okunyiga"],
            "malnutrition": ["malnutrition", "obulwadde bw'omukambwe", "utabaka wa lishe", "obulwadde bw'omukambwe"],
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
                translations[lang_code]["symptoms"].get(sym, sym),  # Use .get() to avoid KeyError
                min_value=0, max_value=1, value=0
            )
    with col2:
        for sym in ["diarrhea", "rash", "difficulty_breathing", "swollen_lymph_nodes", "loss_of_appetite"]:
            symptoms[sym] = st.number_input(
                translations[lang_code]["symptoms"].get(sym, sym),  # Use .get() to avoid KeyError
                min_value=0, max_value=1, value=0
            )
    with col3:
        for sym in ["abdominal_pain", "chills", "convulsions", "dehydration", "pale_gums"]:
            symptoms[sym] = st.number_input(
                translations[lang_code]["symptoms"].get(sym, sym),  # Use .get() to avoid KeyError
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
        advice = first_aid.get(disease, {})
        lang_keys = {"en": "english", "lg": "luganda", "sw": "swahili", "ryn": "runyankole"}
        st.write(advice.get(lang_keys[lang_code], "Information not available"))
        
    except Exception as e:
        st.error(f"Prediction error: {str(e)}")