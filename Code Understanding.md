# AI Symptom Checker for Rural Uganda 🇺🇬  
**A Simple Tool to Help Diagnose Common Childhood Illnesses**  

---

## Table of Contents  
1. [What This Project Does](#what-this-project-does)  
2. [Files Explained](#files-explained)  
   - [iSymptomChecker.py](#isymptomcheckerpy)  
   - [symptom2disease_ug_children.csv](#symptom2disease_ug_childrencsv)  
   - [first_aid.json](#first_aidjson)  
3. [How to Use the App](#how-to-use-the-app)  
4. [How It Works](#how-it-works)  
5. [Setup Guide](#setup-guide)  

---

## What This Project Does  
This app acts like a **digital nurse** for rural communities. It:  
1. Asks about a child’s symptoms (e.g., fever, cough).  
2. Predicts possible illnesses (like malaria or typhoid).  
3. Gives first-aid tips in **4 languages**: English, Luganda, Swahili, Runyankole.  

---

## Files Explained  

### `iSymptomChecker.py` (Main Code)  
This file contains the "brain" of the app. Here’s what each part does:  

```python  
# --- PART 1: Import Tools ---  
import streamlit as st          # Builds buttons and screens  
import pandas as pd             # Reads the symptom dataset  
import speech_recognition as sr # Lets you speak symptoms  
from sklearn.ensemble import RandomForestClassifier  # AI model  
from sklearn.preprocessing import LabelEncoder       # Organizes diseases  
import json                     # Reads first-aid tips  
import os                       # Checks files  

# --- PART 2: Load Data ---  
@st.cache_data  
def load_data():  
    data = pd.read_csv("symptom2disease_ug_children.csv")  # Open dataset  
    le = LabelEncoder()  
    data["disease_encoded"] = le.fit_transform(data["disease"])  # Convert diseases to numbers  
    return data, le  

# --- PART 3: Train the AI ---  
try:  
    data, le = load_data()  
    X = data.drop(["disease", "disease_encoded"], axis=1)  # Symptoms (inputs)  
    y = data["disease_encoded"]                           # Diseases (outputs)  
    model = RandomForestClassifier().fit(X, y)            # Teach AI  
    symptoms = {col: 0 for col in X.columns}              # Store user inputs  
except Exception as e:  
    st.error(f"Error: {e}")                               # Show errors  

# --- PART 4: Load First-Aid Tips ---  
try:  
    with open("first_aid.json", "r") as f:  
        first_aid = json.load(f)  
except:  
    st.error("First-aid file missing!")  

# --- PART 5: Language Setup ---  
translations = {  
    "en": {"title": "AI Symptom Checker...", "fever": "Fever", ...},  
    "lg": {"title": "AI Okuyamba...", "fever": "Omusujja", ...},  
    # ... Swahili & Runyankole  
}  

# --- PART 6: Voice Input ---  
def get_voice_input():  
    r = sr.Recognizer()  
    with sr.Microphone() as source:  
        st.write("Speak now..." if lang_code == "en" else "...")  
        audio = r.listen(source)  
    return r.recognize_google(audio)  # Convert speech to text  

# --- PART 7: User Interface ---  
language = st.radio("Language:", ["English", "Luganda", "Swahili", "Runyankole"])  
lang_code = "en" if language == "English" else "lg" if language == "Luganda" else ...  
st.title(translations[lang_code]["title"])  

# --- PART 8: Collect Symptoms ---  
if input_method == "Voice":  
    voice_input = get_voice_input()  
    # Map words like "omusujja" to fever  
else:  
    # Show sliders for manual input  
    symptoms["fever"] = st.number_input(translations[lang_code]["fever"], 0, 1)  

# --- PART 9: Predict & Show Results ---  
if st.button("Check Symptoms"):  
    prediction = model.predict([symptoms])  
    disease = le.inverse_transform(prediction)[0]  # Convert number to name  
    st.write(f"Diagnosis: {disease}")  
    st.write(first_aid[disease][lang_code])        # Show tips  

---

## Dataset 

### 'symptom2disease_ug_children.csv' (Dataset) 
This is the app’s "textbook" – it teaches the AI which symptoms match which diseases.

# --- Example Format:q --- 
```csv  
fever,cough,headache,...,disease  
1,1,0,...,Malaria  
0,1,1,...,Common Cold  

---

### How to Use This Documentation:  
1. Save it as `DOCUMENTATION.md`.  
2. Share with classmates/teachers.  
3. Modify it to add your own improvements!  

This guide uses **simple language**, **real-life examples**, and **step-by-step explanations** to help S3 students understand and present the project confidently! 🌟