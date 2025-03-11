import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import json
import av
import numpy as np
from streamlit_webrtc import webrtc_streamer, WebRtcMode

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

# Updated translations dictionary
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
            # ... (keep existing symptom translations)
        }
    },
    # ... (keep other language translations)
}

# Language setup (keep existing)

# Browser-based audio input using WebRTC
def audio_frame_callback(frame: av.AudioFrame) -> av.AudioFrame:
    # Convert audio to numpy array
    audio_data = frame.to_ndarray()
    
    # Simple voice activity detection
    if np.abs(audio_data).mean() > 0.01:  # Adjust threshold as needed
        st.session_state.last_audio = audio_data
        
    return frame

# Voice input handler using browser microphone
def get_voice_input():
    webrtc_ctx = webrtc_streamer(
        key="speech-input",
        mode=WebRtcMode.SENDONLY,
        audio_frame_callback=audio_frame_callback,
        rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
        media_stream_constraints={"audio": True},
    )
    
    if 'last_audio' in st.session_state and st.session_state.last_audio is not None:
        # Convert audio to text using SpeechRecognition
        try:
            import speech_recognition as sr
            r = sr.Recognizer()
            
            # Convert numpy array to audio data
            audio_data = sr.AudioData(
                st.session_state.last_audio.tobytes(),
                sample_rate=48000,
                sample_width=2
            )
            
            return r.recognize_google(audio_data)
        except Exception as e:
            st.error(f"Speech recognition error: {e}")
            return None

# UI Components (keep existing until input method selection)

# Input method selection
input_method = st.radio(
    translations[lang_code]["input_method"],
    [translations[lang_code]["voice"], translations[lang_code]["manual"]]
)

# Symptom collection
if input_method == translations[lang_code]["voice"]:
    st.write(translations[lang_code]["voice_instructions"])
    voice_input = get_voice_input()
    
    if voice_input:
        st.write(f"Recognized: {voice_input}")
        symptoms = {col: 0 for col in X.columns}
        
        # Expanded keyword mapping for all symptoms
        keyword_map = {
            "fever": ["fever", "omusujja", "homa", "emburara"],
            "cough": ["cough", "enkuba", "kikohozi", "enkohozi"],
            "diarrhea": ["diarrhea", "endwadde", "kuhara", "okusharara"],
            "rash": ["rash", "akabombo", "upele", "ebiheni"],
            "fatigue": ["fatigue", "okuwuka", "uchovu", "obunaku"],
            # Add mappings for all other symptoms...
        }
        
        for symptom, keywords in keyword_map.items():
            for keyword in keywords:
                if keyword.lower() in voice_input.lower():
                    symptoms[symptom] = 1
else:
    # Keep existing manual input columns
    col1, col2, col3 = st.columns(3)
    with col1:
        for sym in ["fever", "cough", "fatigue", "headache", "vomiting"]:
            symptoms[sym] = st.number_input(
                translations[lang_code]["symptoms"][sym],
                min_value=0, max_value=1, value=0
            )
    # ... (keep rest of manual input code)

# Keep existing prediction and results code