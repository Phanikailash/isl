# SpeakMySigns – Real-Time Gesture-to-Speech for Indian Sign Language Users

> _"From signs to sentences, from gestures to voices — SpeakMySigns speaks for you."_

## 📌 Overview
**SpeakMySigns** is a **real-time Gesture-to-Speech** system designed to bridge communication gaps for the deaf and hard-of-hearing community.  
Tailored for **Indian Sign Language (ISL)**, it captures sign gestures through a webcam, predicts their meaning, forms complete sentences, and speaks them aloud — enabling smooth conversation between signers and non-signers.

### How It Works
1. **Capture** – Detects both **static** and **dynamic** gestures in real time using a webcam.
2. **Predict** – Classifies gestures with a trained deep learning model.
3. **Compose** – Converts recognized sign sequences into grammatically correct sentences with a fine-tuned **FLAN-T5** model.
4. **Speak** – Uses Text-to-Speech (TTS) to vocalize the generated sentences.

---

## ✨ Features
- 🎥 **Real-Time Gesture Detection** – Works with both static and dynamic signs.
- 🧠 **Sentence Formation** – Turns multiple recognized gestures into structured sentences.
- 🔊 **Voice Output** – Built-in TTS for spoken communication.
- 🖥 **Dual Workflow** – Includes **training pipeline**, **Jupyter notebook experiments**, and **Flask web app**.
- 🌐 **Accessible & Inclusive** – Designed for **Indian Sign Language (ISL)** users.

---

## 📂 Additional Resources (Google Drive)
Due to large file sizes, the trained models and demo video are stored on Google Drive.

- 🎥 **Demo Video** – [View Demo](https://drive.google.com/file/d/1Ut89WZtQEOigP5h-83wkT-Ib3wxe_U_j/view?usp=drive_link)  
- 🧠 **FLAN-T5 Sentence Generator Model** – [Download FLAN-T5 Model](https://drive.google.com/file/d/1RauJbqOa3eZm1BHxuXOnWc_8dIyYJ-UI/view?usp=drive_link)  
- ✋ **Fullset Gesture Recognition Model** – [Download Fullset Model](https://drive.google.com/file/d/1GXxjMKo82cGE2DVJIO27_7fjIrbUWX23/view?usp=drive_link)

### 📌 Placement Instructions
After downloading:
1. Place the **FLAN-T5** folder inside:
   - `flask_app/flan-t5-custom/`
   - `notebook/flan-t5-custom/`

2. Place the **fullset.h5** model file inside:
   - `flask_app/fullset.h5`
   - `notebook/fullset.h5`


## ⚙️ Setup & Installation

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/DABD-RG/Anusree-SpeakMySigns-July-25.git
cd Anusree-SpeakMySigns-July-25
````

### 2️⃣ Install Dependencies

#### For Flask App

```bash
cd flask_app
pip install -r requirements.txt
```

#### For Notebook

```bash
cd notebook
pip install -r requirements.txt
```

#### For Training

```bash
cd training
pip install -r requirements.txt
```



## 🚀 Usage

### ▶️ Run the Flask App
```bash
cd flask_app
python app.py
````

Open the app in your browser at **[http://127.0.0.1:5000/](http://127.0.0.1:5000/)**
Use the webcam to show signs — the system will detect, predict, form a sentence, and speak it aloud.

---

### 📒 Run Notebook Experiments

```bash
cd notebook
jupyter notebook main_notebook.ipynb
```

---

### 🤖 Train the Model

```bash
cd training
jupyter notebook model_training.ipynb
```







👩‍💻 Author

Anusree – Developer of SpeakMySigns, as part of an academic internship project.

📜 License

This project is for educational and research purposes.


