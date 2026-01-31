from flask import Flask, render_template, request, jsonify, send_file
import base64
import cv2
import numpy as np
from PIL import Image
import mediapipe as mp
from tensorflow.keras.models import load_model
import traceback
from transformers import T5Tokenizer, T5ForConditionalGeneration
import torch
import pyttsx3
import os
import uuid
import sys

# Add speech_to_sign module to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'speech_to_sign'))
from speech_to_sign import (
    SpeechRecognizer, 
    ISLMapper, 
    AvatarRenderer,
    NLPProcessor,
    AnimationGenerator,
    ISLDatabase
)

# Flask setup
app = Flask(__name__)

# Get the base directory of this file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

os.makedirs(os.path.join(BASE_DIR, 'tts_output'), exist_ok=True)
tts_engine = pyttsx3.init()
tts_engine.setProperty('rate', 150)

# Initialize Speech-to-Sign components following the architecture:
# NLP Processing → ISL Database → Animation Generation → Avatar Rendering
nlp_processor = NLPProcessor()
isl_database = ISLDatabase()
animation_generator = AnimationGenerator(isl_database)
isl_mapper = ISLMapper(nlp_processor, isl_database)
avatar_renderer = AvatarRenderer(isl_database, animation_generator)
speech_recognizer = SpeechRecognizer()


# Load gesture model (for sign-to-speech)
model = None
gesture_model_path = os.path.join(BASE_DIR, 'fullset.h5')
if os.path.exists(gesture_model_path):
    model = load_model(gesture_model_path)
    print("Gesture recognition model loaded successfully!")
else:
    print(f"WARNING: Gesture model not found at {gesture_model_path}")
    print("Sign-to-Speech will be disabled. Speech-to-Sign will still work.")

class_labels = [
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
    'A', 'Alright', 'Animal', 'B', 'Beautiful', 'Bed', 'Bedroom', 'Bird', 'Black', 'Blind',
    'C', 'Cat', 'Chair', 'Colour', 'Cow', 'D', 'Daughter', 'Deaf', 'Dog', 'Door', 'Dream',
    'E', 'F', 'Father', 'Fish', 'Friday', 'G', 'Good Morning', 'Good night', 'Grey',
    'H', 'Happy', 'He', 'Hello', 'Horse', 'How are you', 'I','I', 'It',
    'J', 'K', 'L', 'Loud', 'M', 'Monday', 'Mother', 'Mouse',
    'N', 'O', 'Orange', 'P', 'Parent', 'Pink', 'Pleased',
    'Q', 'Quiet', 'R', 'S', 'Sad', 'Saturday', 'She', 'Son', 'Sunday',
    'T', 'Table', 'Thank you', 'Thursday', 'Today', 'Tuesday',
    'U', 'Ugly', 'V', 'W', 'Wednesday', 'White', 'Window',
    'X', 'Y', 'You', 'Z']

# Initialize MediaPipe hands (for sign-to-speech gesture recognition)
mp_hands = None
hands = None
try:
    import mediapipe as mp
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2,
                           min_detection_confidence=0.7, min_tracking_confidence=0.7)
    print("MediaPipe hands initialized successfully!")
except Exception as e:
    print(f"WARNING: MediaPipe hands initialization failed: {e}")
    print("Sign-to-Speech gesture recognition will be limited.")

# Load T5 model for sentence generation (for sign-to-speech)
tokenizer = None
sentence_model = None
t5_model_path = os.path.join(BASE_DIR, 'flan-t5-customm')
if os.path.exists(t5_model_path):
    print("Loading T5 model and tokenizer...")
    tokenizer = T5Tokenizer.from_pretrained(t5_model_path)
    sentence_model = T5ForConditionalGeneration.from_pretrained(
        t5_model_path,
        device_map='auto',
        low_cpu_mem_usage=True,
        torch_dtype=torch.float16
    )
    print("T5 model loaded successfully!")
else:
    print(f"WARNING: T5 model not found at {t5_model_path}")
    print("Sentence generation will be disabled. Basic word concatenation will be used.")

def extract_keypoints(frame):
    if hands is None:
        return [0] * 126, None
    
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(image)
    keypoints = []

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks[:2]:
            for lm in hand_landmarks.landmark:
                keypoints.extend([lm.x, lm.y, lm.z])
        if len(results.multi_hand_landmarks) == 1:
            keypoints.extend([0] * 63)
    else:
        keypoints = [0] * 126
    return keypoints, results

def generate_speech(text):
    # Generate a unique filename
    filename = os.path.join(BASE_DIR, 'tts_output', f"{str(uuid.uuid4())}.wav")
    
    # Generate speech using pyttsx3
    tts_engine.save_to_file(text, filename)
    tts_engine.runAndWait()
    
    return filename

def generate_sentence_from_words(words):
    # If T5 model is not available, use simple concatenation
    if tokenizer is None or sentence_model is None:
        return " ".join(words).capitalize() + "."
    
    prompt = (
        "form a valid and grammatically correct sentence using the following words only once with proper structure and verb form: "
        + ", ".join(words)
    )
    input_ids = tokenizer.encode(prompt, return_tensors="pt")
    
    # Move input to the same device as the model's first parameter
    device = next(sentence_model.parameters()).device
    input_ids = input_ids.to(device)
    
    outputs = sentence_model.generate(
        input_ids=input_ids,
        max_length=30,
        num_beams=5,
        no_repeat_ngram_size=2,
        early_stopping=True
    )
    return tokenizer.decode(outputs[0], skip_special_tokens=True)


@app.route('/')
def index():
    cleanup_old_files()
    return render_template('integrated.html')

@app.route('/original')
def original():
    cleanup_old_files()
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    try:
        if model is None:
            return jsonify({"error": "Gesture model not loaded. Sign-to-Speech is disabled."}), 503
        
        data = request.json
        frames = data.get("frames", [])

        if len(frames) != 30:
            return jsonify({"error": "Expected 30 frames"}), 400

        sequence = []
        for frame_data in frames:
            frame_bytes = base64.b64decode(frame_data.split(',')[1])
            np_arr = np.frombuffer(frame_bytes, np.uint8)
            frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

            keypoints, _ = extract_keypoints(frame)
            sequence.append(keypoints)

        time_indices = np.linspace(0, 1, 30).reshape(30, 1)
        sequence_with_time = np.concatenate([sequence, time_indices], axis=1)
        input_seq = np.expand_dims(sequence_with_time, axis=0)

        prediction = model.predict(input_seq)[0]
        predicted_class = class_labels[np.argmax(prediction)]

        return jsonify({"prediction": predicted_class})
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@app.route('/generate_sentence', methods=['POST'])
def generate_sentence():
    try:
        data = request.json
        words = data.get("words", [])

        if not words or not isinstance(words, list):
            return jsonify({"error": "Invalid word list"}), 400

        # Generate sentence
        sentence = generate_sentence_from_words(words)
        
        # Generate speech from the sentence
        audio_file = generate_speech(sentence)
        
        return jsonify({
            "sentence": sentence,
            "audio_url": f"/get_audio/{os.path.basename(audio_file)}"
        })
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@app.route('/get_audio/<filename>')
def get_audio(filename):
    try:
        return send_file(
            f"tts_output/{filename}",
            mimetype="audio/wav",
            as_attachment=True,
            download_name=filename
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 404

def cleanup_old_files():
    import glob
    import time
    
    current_time = time.time()
    tts_dir = os.path.join(BASE_DIR, 'tts_output')
    for file in glob.glob(os.path.join(tts_dir, "*.wav")):
        if os.path.getmtime(file) < current_time - 3600:  # 3600 seconds = 1 hour
            try:
                os.remove(file)
            except:
                pass

@app.route('/translate_to_isl', methods=['POST'])
def translate_to_isl():
    """
    Speech-to-Sign Translation Endpoint
    Following Architecture in Figure 3.4:
    1. Input text (from speech recognition)
    2. NLP Processing (Text Preprocessing → Tokenization → Lemmatization → Stop-word Removal)
    3. ISL Database Lookup (Sign Repository with Keypoints)
    4. Animation Generation (Keyframes → Motion Interpolation → Facial Expression → Body Posture)
    5. Avatar Rendering (Animated ISL Avatar)
    """
    try:
        data = request.json
        text = data.get('text', '')
        
        if not text:
            return jsonify({"error": "No text provided"}), 400
        
        # Step 1 & 2: NLP Processing + ISL Mapping
        isl_signs = isl_mapper.map_to_isl(text)
        
        # Get detailed processing info for debugging
        processing_details = isl_mapper.get_processing_details(text)
        
        if not isl_signs:
            return jsonify({
                'isl_sequence': [],
                'animation_frames': [],
                'processing_details': processing_details,
                'message': 'No matching signs found'
            })
        
        # Step 3 & 4 & 5: Get animation sequence with keypoints and render
        # Use the full animation pipeline from avatar renderer
        animation_result = avatar_renderer.render_full_animation(isl_signs)
        
        return jsonify({
            'isl_sequence': isl_signs,
            'animation_frames': animation_result.get('frames', []),
            'schedule': animation_result.get('schedule', []),
            'total_duration': animation_result.get('total_duration', 0),
            'processing_details': processing_details,
            'input_text': text
        })
        
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@app.route('/recognize_speech', methods=['POST'])
def recognize_speech():
    try:
        # Handle audio file if sent
        if 'audio' in request.files:
            audio_file = request.files['audio']
            # Save temporarily
            temp_path = f"tts_output/temp_speech_{uuid.uuid4()}.wav"
            audio_file.save(temp_path)
            
            # Use speech recognizer
            text = speech_recognizer.recognize_from_file(temp_path)
            
            # Clean up
            try:
                os.remove(temp_path)
            except:
                pass
            
            if text.startswith("Error"):
                return jsonify({'error': text}), 400
                
            return jsonify({
                'text': text,
                'confidence': 0.9
            })
        
        # If no audio file, try to get text from JSON body
        data = request.json if request.is_json else {}
        text = data.get('text', '')
        
        if text:
            return jsonify({
                'text': text,
                'confidence': 1.0
            })
        
        return jsonify({
            'error': 'No audio or text provided'
        }), 400
        
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@app.route('/get_available_signs', methods=['GET'])
def get_available_signs():
    """Return the list of available signs (class_labels)"""
    try:
        return jsonify({
            'signs': class_labels,
            'count': len(class_labels)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    try:
        print("Starting Flask server...")
        app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
    except Exception as e:
        print(f"Error starting server: {str(e)}")
        
    finally:
        print("Cleaning up...")
        cleanup_old_files()
        tts_engine.stop()
