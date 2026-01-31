# Integrated ISL Communication System

This project provides a bidirectional communication system for Indian Sign Language (ISL) with both **Sign-to-Speech** and **Speech-to-Sign** capabilities.

## Features

### 🤟 Sign-to-Speech Module
- Real-time hand gesture recognition using MediaPipe
- Video capture and processing
- Feature extraction from hand landmarks
- Gesture classification using trained neural network
- Text-to-speech conversion for recognized signs
- Sentence formation from multiple signs

### 🗣️ Speech-to-Sign Module  
- Speech recognition from microphone input
- Text input alternative
- ISL grammar mapping (Subject-Object-Verb structure)
- 3D avatar animation rendering
- Real-time sign visualization

## Project Structure

```
flask_app/
├── app.py                    # Main Flask application
├── requirements.txt          # Python dependencies
├── templates/
│   ├── integrated.html       # Main integrated UI
│   └── index.html           # Original Sign-to-Speech UI
├── speech_to_sign/          # Speech-to-Sign module
│   ├── __init__.py
│   ├── speech_recognition.py
│   ├── isl_mapper.py
│   └── avatar_renderer.py
└── tts_output/              # Generated audio files
```

## Installation

1. **Install Python dependencies:**
```bash
pip install flask opencv-python mediapipe tensorflow transformers torch pyttsx3 SpeechRecognition Pillow
```

2. **Download required models:**
   - `fullset.h5` - Trained gesture recognition model
   - `flan-t5-customm` - Text generation model

3. **Run the application:**
```bash
cd flask_app
python app.py
```

4. **Open in browser:**
   - Main integrated system: `http://localhost:5000`
   - Original Sign-to-Speech: `http://localhost:5000/original`

## Usage

### Sign-to-Speech
1. Click "Start Recognition"
2. Show hand gestures to the camera
3. System recognizes signs and builds sentences
4. Audio output generated for final sentence

### Speech-to-Sign
1. Switch to "Speech-to-Sign" mode
2. Choose text input or voice input
3. Enter text or record speech
4. Click "Translate to ISL"
5. View ISL sequence and play avatar animation

## Supported Signs

The system recognizes signs from the following categories:
- **Numbers:** 0-9
- **Alphabet:** A-Z
- **Common Words:** Hello, Thank you, Good morning, Happy, Sad, etc.
- **Family:** Mother, Father, Daughter, Son, Parent
- **Animals:** Cat, Dog, Cow, Horse, Mouse, Fish, Bird
- **Objects:** Chair, Table, Bed, Door, Window
- **Colors:** Black, White, Orange, Pink, Grey
- **Days:** Monday-Sunday, Today
- **Other:** Beautiful, Blind, Deaf, Dream, Loud, Quiet, Ugly

## Architecture

### Sign-to-Speech Flow:
1. **User Input** → Video capture from webcam
2. **Video Capture** → 30 frames processed per prediction
3. **Hand Landmark Detection** → MediaPipe extracts 21 landmarks per hand
4. **Feature Extraction** → 126 features (2 hands × 21 landmarks × 3 coordinates)
5. **Gesture Recognition** → LSTM neural network classification
6. **Spoken Audio** → Text-to-speech conversion

### Speech-to-Sign Flow:
1. **Speech/Text Input** → Microphone or text field
2. **NLP Processing** → Speech recognition and text processing
3. **ISL Grammar Mapping** → Convert to ISL structure (SOV)
4. **Animation Rendering** → Generate 3D avatar movements
5. **3D Avatar Output** → Visual sign representation

## Technical Details

### Hand Landmark Detection
- Uses MediaPipe Hands for real-time hand tracking
- Extracts 21 landmarks per hand (x, y, z coordinates)
- Supports both single and double hand gestures

### Neural Network Model
- LSTM-based architecture for sequence processing
- Input: 30 frames × 126 features + time index
- Output: Probability distribution over 75 sign classes
- Training data: Pre-recorded sign sequences

### ISL Grammar Mapping
- Converts English to ISL grammar structure
- Time expressions placed first
- Subject-Object-Verb word order
- Fingerspelling for unsupported words

### Avatar Animation
- Simplified 3D hand and body representation
- Keyframe interpolation for smooth animations
- Facial expressions for emotional context
- 30 FPS animation rendering

## Dependencies

- **Flask**: Web framework
- **OpenCV**: Computer vision and image processing
- **MediaPipe**: Hand landmark detection
- **TensorFlow**: Neural network inference
- **Transformers**: Text generation (T5 model)
- **PyTorch**: Alternative ML framework
- **pyttsx3**: Text-to-speech conversion
- **SpeechRecognition**: Voice input processing
- **Pillow**: Image processing

## Browser Compatibility

- **Chrome**: Full support (recommended)
- **Edge**: Full support
- **Firefox**: Partial support (MediaPipe may have issues)
- **Safari**: Limited support

## Troubleshooting

### Common Issues:

1. **Camera not working**
   - Check browser permissions
   - Ensure no other app is using the camera
   - Try refreshing the page

2. **Speech recognition not working**
   - Use Chrome or Edge browser
   - Check microphone permissions
   - Ensure quiet environment

3. **Model loading errors**
   - Verify `fullset.h5` is in the correct directory
   - Check TensorFlow version compatibility
   - Ensure sufficient RAM available

4. **Animation not playing**
   - Check browser console for errors
   - Ensure WebGL is enabled
   - Try refreshing the page

## Future Enhancements

- [ ] Support for more complex sentences
- [ ] Additional sign vocabulary
- [ ] More realistic 3D avatars
- [ ] Mobile app version
- [ ] Offline mode support
- [ ] Multi-language support
- [ ] Sign-to-sign dictionary
- [ ] Learning mode with tutorials

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is part of academic research and development for assistive technology.
