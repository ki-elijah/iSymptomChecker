# AI-Powered Symptom Checker for Rural Uganda 🇺🇬
**From Code to Creativity – Exploring the AI Revolution**  
*Empowering Communities with Accessible Healthcare Tools*

---

## Table of Contents
1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Technical Specifications](#technical-specifications)
4. [Installation & Setup](#installation--setup)
5. [How to Use](#how-to-use)
6. [Advantages](#advantages)
7. [Limitations](#limitations)
8. [Future Improvements](#future-improvements)
9. [Acknowledgments](#acknowledgments)
10. [License](#license)

---

## Project Overview
### Problem Statement
Many rural Ugandan communities lack immediate access to doctors and medical facilities. This leads to delayed diagnoses and poor health outcomes, especially for children.

### Solution
An **AI-powered symptom checker** that:
- Diagnoses common childhood illnesses.
- Provides first-aid advice in **4 languages** (English, Luganda, Swahili, Runyankole).
- Works offline and with voice input.

### Target Audience
- Rural families, community health workers, and schools in Uganda.
- Students learning AI/tech skills.

---

## Features
| Feature | Description |  
|---------|-------------|  
| **Multi-Language Support** | Switch between English, Luganda, Swahili, and Runyankole. |  
| **Voice Input** | Speak symptoms instead of typing (supports English/Swahili). |  
| **First-Aid Tips** | Culturally relevant advice for 20+ diseases. |  
| **Offline Use** | No internet required after setup. |  
| **Simple Interface** | Designed for users with limited tech experience. |  

---

## Technical Specifications
### Dataset (`symptom2disease_ug_children.csv`)
- **Format**: CSV file with binary symptoms (`1` = present, `0` = absent).
- **Diseases Covered**: Malaria, Typhoid, Pneumonia, HIV/AIDS, etc.  
- **Example Row**:  
  ```csv
  fever,cough,fatigue,headache,...,disease
  1,1,0,1,...,Malaria

Tools & Libraries
    Python: Core programming language.

    Streamlit: For building the app interface.

    Scikit-learn: Trains the AI model (RandomForestClassifier).

    SpeechRecognition: For voice input support.

File Structure
📁 Project Folder/
├── 📄 iSymptomChecker.py               # Main app code
├── 📄 symptom2disease_ug_children.csv  # Dataset
├── 📄 first_aid.json                   # First-aid tips in 4 languages
└── 📁 images/                          # Screenshots (optional)


Installation & Setup
Requirements
Python 3.7+

Microphone (for voice input)

Steps
Install Dependencies:
pip install pandas streamlit scikit-learn SpeechRecognition pyaudio

How to Use
Choose Language
Select your preferred language (English, Luganda, Swahili, or Runyankole).

Input Symptoms

Voice: Click the microphone icon and speak (e.g., “Ndi musujja” = “I have a fever”).

Manual: Toggle sliders for symptoms (0 = No, 1 = Yes).

Get Diagnosis
Click Check Symptoms to see the predicted illness and first-aid tips.

App Screenshot Example: Diagnosing Malaria

Advantages
    Saves Time: Reduces unnecessary clinic visits.

    Educational: Teaches symptoms and prevention.

    Localized: Works in 4 Ugandan languages.

    Low-Cost: Free to use and modify.

Limitations
    Accuracy: May misdiagnose rare diseases.

    Tech Access: Requires a smartphone/computer.

    No Physical Exam: Can’t replace a doctor’s checkup.

Future Improvements
    Add SMS support for basic phones.

    Include pictures for symptom identification.

    Partner with clinics for real-world testing.

    Expand to more languages (e.g., Acholi, Ateso).

Acknowledgments
    Dataset Inspiration: Kaggle’s Symptom2Disease dataset.

    Translations: Collaborations with local language experts.

    Mentors: Teachers and open-source developers.


---

### 


echo "# iSymptomChecker" >> README.md
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/ki-elijah/iSymptomChecker.git
git push -u origin main