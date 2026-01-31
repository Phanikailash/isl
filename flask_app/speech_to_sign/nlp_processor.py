"""
NLP Processing Module for Speech-to-Sign System
Implements: Text Preprocessing → Word Tokenization → Lemmatization → Stop-word Removal
Following the architecture in Figure 3.4
"""

import re
import string
from typing import List, Tuple

# Try to import NLTK, fallback to simple processing if not available
try:
    import nltk
    from nltk.tokenize import word_tokenize
    from nltk.stem import WordNetLemmatizer
    from nltk.corpus import stopwords
    
    # Download required NLTK data
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt', quiet=True)
    
    try:
        nltk.data.find('corpora/wordnet')
    except LookupError:
        nltk.download('wordnet', quiet=True)
        
    try:
        nltk.data.find('corpora/stopwords')
    except LookupError:
        nltk.download('stopwords', quiet=True)
    
    try:
        nltk.data.find('taggers/averaged_perceptron_tagger')
    except LookupError:
        nltk.download('averaged_perceptron_tagger', quiet=True)
    
    NLTK_AVAILABLE = True
except ImportError:
    NLTK_AVAILABLE = False


class NLPProcessor:
    """
    NLP Processing Module following the architecture:
    Text Preprocessing → Word Tokenization → Lemmatization → Stop-word Removal
    """
    
    def __init__(self):
        # Class labels from app.py - signs we can produce
        self.class_labels = [
            '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
            'A', 'Alright', 'Animal', 'B', 'Beautiful', 'Bed', 'Bedroom', 'Bird', 'Black', 'Blind',
            'C', 'Cat', 'Chair', 'Colour', 'Cow', 'D', 'Daughter', 'Deaf', 'Dog', 'Door', 'Dream',
            'E', 'F', 'Father', 'Fish', 'Friday', 'G', 'Good Morning', 'Good night', 'Grey',
            'H', 'Happy', 'He', 'Hello', 'Horse', 'How are you', 'I', 'It',
            'J', 'K', 'L', 'Loud', 'M', 'Monday', 'Mother', 'Mouse',
            'N', 'O', 'Orange', 'P', 'Parent', 'Pink', 'Pleased',
            'Q', 'Quiet', 'R', 'S', 'Sad', 'Saturday', 'Sunday', 'She', 'Son',
            'T', 'Table', 'Thank you', 'Thursday', 'Today', 'Tuesday',
            'U', 'Ugly', 'V', 'W', 'Wednesday', 'White', 'Window',
            'X', 'Y', 'You', 'Z'
        ]
        
        # Initialize NLTK components if available
        if NLTK_AVAILABLE:
            self.lemmatizer = WordNetLemmatizer()
            self.stop_words = set(stopwords.words('english'))
        else:
            self.lemmatizer = None
            self.stop_words = self._get_basic_stopwords()
        
        # Words to keep even if they are stopwords (because we have signs for them)
        self.keep_words = {
            'i', 'you', 'he', 'she', 'it', 'how', 'are',
            'good', 'morning', 'night', 'today'
        }
        
        # Remove these from stop_words since we have signs
        self.stop_words = self.stop_words - self.keep_words
        
        # Multi-word phrases to detect (check these before tokenization)
        self.phrases = {
            'how are you': 'How are you',
            'good morning': 'Good Morning', 
            'good night': 'Good night',
            'thank you': 'Thank you'
        }
        
        # Word to sign mappings (including lemmatized forms)
        self.word_to_sign = self._build_word_mappings()
    
    def _get_basic_stopwords(self) -> set:
        """Basic stopwords list if NLTK not available"""
        return {
            'a', 'an', 'the', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
            'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
            'should', 'may', 'might', 'must', 'shall', 'can', 'need', 'dare',
            'ought', 'used', 'to', 'of', 'in', 'for', 'on', 'with', 'at', 'by',
            'from', 'as', 'into', 'through', 'during', 'before', 'after',
            'above', 'below', 'between', 'under', 'again', 'further', 'then',
            'once', 'here', 'there', 'when', 'where', 'why', 'what', 'which',
            'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'and', 'but',
            'if', 'or', 'because', 'until', 'while', 'very', 'just', 'only',
            'own', 'same', 'so', 'than', 'too', 'also', 'such', 'no', 'not',
            'both', 'each', 'few', 'more', 'most', 'other', 'some', 'any', 'all'
        }
    
    def _build_word_mappings(self) -> dict:
        """Build comprehensive word to sign mappings including lemmatized forms"""
        mappings = {
            # Numbers
            'zero': '0', 'one': '1', 'two': '2', 'three': '3', 'four': '4',
            'five': '5', 'six': '6', 'seven': '7', 'eight': '8', 'nine': '9',
            '0': '0', '1': '1', '2': '2', '3': '3', '4': '4',
            '5': '5', '6': '6', '7': '7', '8': '8', '9': '9',
            
            # Letters (lowercase to class label)
            'a': 'A', 'b': 'B', 'c': 'C', 'd': 'D', 'e': 'E', 'f': 'F',
            'g': 'G', 'h': 'H', 'i': 'I', 'j': 'J', 'k': 'K', 'l': 'L',
            'm': 'M', 'n': 'N', 'o': 'O', 'p': 'P', 'q': 'Q', 'r': 'R',
            's': 'S', 't': 'T', 'u': 'U', 'v': 'V', 'w': 'W', 'x': 'X',
            'y': 'Y', 'z': 'Z',
            
            # Greetings/Expressions
            'hello': 'Hello', 'hi': 'Hello', 'hey': 'Hello',
            'thank': 'Thank you', 'thanks': 'Thank you',
            'happy': 'Happy', 'happiness': 'Happy', 'happily': 'Happy',
            'sad': 'Sad', 'sadness': 'Sad', 'sadly': 'Sad',
            'beautiful': 'Beautiful', 'beauty': 'Beautiful', 'pretty': 'Beautiful',
            'ugly': 'Ugly', 'ugliness': 'Ugly',
            'alright': 'Alright', 'okay': 'Alright', 'ok': 'Alright', 'fine': 'Alright',
            'please': 'Pleased', 'pleased': 'Pleased', 'pleasure': 'Pleased',
            
            # Animals - including singular/plural/lemmatized forms
            'animal': 'Animal', 'animals': 'Animal',
            'bird': 'Bird', 'birds': 'Bird',
            'cat': 'Cat', 'cats': 'Cat', 'kitten': 'Cat', 'kitty': 'Cat',
            'dog': 'Dog', 'dogs': 'Dog', 'puppy': 'Dog', 'puppies': 'Dog',
            'cow': 'Cow', 'cows': 'Cow', 'cattle': 'Cow',
            'horse': 'Horse', 'horses': 'Horse', 'pony': 'Horse',
            'mouse': 'Mouse', 'mice': 'Mouse', 'rat': 'Mouse',
            'fish': 'Fish', 'fishes': 'Fish', 'fishing': 'Fish',
            
            # Family - including variations
            'mother': 'Mother', 'mom': 'Mother', 'mum': 'Mother', 'mommy': 'Mother', 'mama': 'Mother',
            'father': 'Father', 'dad': 'Father', 'daddy': 'Father', 'papa': 'Father',
            'daughter': 'Daughter', 'daughters': 'Daughter',
            'son': 'Son', 'sons': 'Son',
            'parent': 'Parent', 'parents': 'Parent',
            
            # Furniture/Objects
            'chair': 'Chair', 'chairs': 'Chair', 'seat': 'Chair',
            'table': 'Table', 'tables': 'Table', 'desk': 'Table',
            'bed': 'Bed', 'beds': 'Bed', 'sleeping': 'Bed',
            'bedroom': 'Bedroom', 'bedrooms': 'Bedroom', 'room': 'Bedroom',
            'door': 'Door', 'doors': 'Door', 'doorway': 'Door',
            'window': 'Window', 'windows': 'Window',
            
            # Colors
            'black': 'Black', 'dark': 'Black',
            'white': 'White', 'light': 'White',
            'orange': 'Orange',
            'pink': 'Pink',
            'grey': 'Grey', 'gray': 'Grey',
            'colour': 'Colour', 'color': 'Colour', 'colors': 'Colour', 'colours': 'Colour',
            
            # Days
            'monday': 'Monday', 'mon': 'Monday',
            'tuesday': 'Tuesday', 'tue': 'Tuesday', 'tues': 'Tuesday',
            'wednesday': 'Wednesday', 'wed': 'Wednesday',
            'thursday': 'Thursday', 'thu': 'Thursday', 'thurs': 'Thursday',
            'friday': 'Friday', 'fri': 'Friday',
            'saturday': 'Saturday', 'sat': 'Saturday',
            'sunday': 'Sunday', 'sun': 'Sunday',
            'today': 'Today',
            
            # Pronouns
            'i': 'I', 'me': 'I', 'my': 'I', 'myself': 'I',
            'you': 'You', 'your': 'You', 'yours': 'You', 'yourself': 'You',
            'he': 'He', 'him': 'He', 'his': 'He', 'himself': 'He',
            'she': 'She', 'her': 'She', 'hers': 'She', 'herself': 'She',
            'it': 'It', 'its': 'It', 'itself': 'It',
            
            # Other words
            'blind': 'Blind', 'blindness': 'Blind',
            'deaf': 'Deaf', 'deafness': 'Deaf',
            'dream': 'Dream', 'dreams': 'Dream', 'dreaming': 'Dream', 'dreamt': 'Dream',
            'loud': 'Loud', 'loudly': 'Loud', 'loudness': 'Loud', 'noisy': 'Loud',
            'quiet': 'Quiet', 'quietly': 'Quiet', 'silence': 'Quiet', 'silent': 'Quiet',
            
            # Time greetings
            'morning': 'Good Morning',
            'night': 'Good night', 'goodnight': 'Good night',
        }
        
        return mappings
    
    def preprocess_text(self, text: str) -> str:
        """
        Step 1: Text Preprocessing
        - Convert to lowercase
        - Remove extra whitespace
        - Handle punctuation
        """
        # Convert to lowercase
        text = text.lower().strip()
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        # Keep letters, numbers, and spaces
        text = re.sub(r'[^\w\s]', ' ', text)
        text = ' '.join(text.split())
        
        return text
    
    def detect_phrases(self, text: str) -> Tuple[List[str], str]:
        """
        Detect multi-word phrases before tokenization
        Returns: (detected_phrases, remaining_text)
        """
        detected = []
        remaining = text.lower()
        
        # Sort phrases by length (longest first) to match longest phrases first
        sorted_phrases = sorted(self.phrases.keys(), key=len, reverse=True)
        
        for phrase in sorted_phrases:
            if phrase in remaining:
                detected.append(self.phrases[phrase])
                remaining = remaining.replace(phrase, ' ')
        
        # Clean up remaining text
        remaining = ' '.join(remaining.split())
        
        return detected, remaining
    
    def tokenize(self, text: str) -> List[str]:
        """
        Step 2: Word Tokenization
        Split text into individual word tokens
        """
        if NLTK_AVAILABLE:
            try:
                tokens = word_tokenize(text)
            except:
                tokens = text.split()
        else:
            tokens = text.split()
        
        return tokens
    
    def lemmatize(self, tokens: List[str]) -> List[str]:
        """
        Step 3: Lemmatization
        Reduce words to their base/root form
        E.g., 'running' -> 'run', 'cats' -> 'cat'
        """
        if not NLTK_AVAILABLE or self.lemmatizer is None:
            return tokens
        
        lemmatized = []
        for token in tokens:
            try:
                # Lemmatize as noun first
                lemma = self.lemmatizer.lemmatize(token, pos='n')
                # If unchanged, try as verb
                if lemma == token:
                    lemma = self.lemmatizer.lemmatize(token, pos='v')
                # If still unchanged, try as adjective
                if lemma == token:
                    lemma = self.lemmatizer.lemmatize(token, pos='a')
                lemmatized.append(lemma)
            except:
                lemmatized.append(token)
        
        return lemmatized
    
    def remove_stopwords(self, tokens: List[str]) -> List[str]:
        """
        Step 4: Stop-word Removal
        Remove common words that don't carry meaning
        But keep words we have signs for
        """
        filtered = []
        for token in tokens:
            # Keep if not a stopword OR if we have a sign for it
            if token not in self.stop_words or token in self.word_to_sign:
                filtered.append(token)
        
        return filtered
    
    def map_to_signs(self, tokens: List[str]) -> List[str]:
        """
        Map processed tokens to ISL signs
        Uses word_to_sign mappings and handles fingerspelling
        """
        signs = []
        
        for token in tokens:
            if token in self.word_to_sign:
                sign = self.word_to_sign[token]
                if sign not in signs or self._should_repeat(sign):
                    signs.append(sign)
            else:
                # Fingerspell unknown words (length > 2)
                if len(token) > 2:
                    for char in token.upper():
                        if char in self.class_labels:
                            signs.append(char)
        
        return signs
    
    def _should_repeat(self, sign: str) -> bool:
        """Determine if a sign should be repeated in sequence"""
        # Pronouns and short words can repeat
        return sign in ['I', 'You', 'He', 'She', 'It']
    
    def process(self, text: str) -> dict:
        """
        Main processing pipeline:
        Text Preprocessing → Word Tokenization → Lemmatization → Stop-word Removal
        Returns detailed processing results
        """
        result = {
            'original_text': text,
            'preprocessed': '',
            'phrases_detected': [],
            'tokens': [],
            'lemmatized': [],
            'filtered': [],
            'isl_signs': []
        }
        
        # Step 1: Preprocess
        preprocessed = self.preprocess_text(text)
        result['preprocessed'] = preprocessed
        
        # Detect phrases first
        phrases, remaining_text = self.detect_phrases(preprocessed)
        result['phrases_detected'] = phrases
        
        # Step 2: Tokenize remaining text
        tokens = self.tokenize(remaining_text)
        result['tokens'] = tokens
        
        # Step 3: Lemmatize
        lemmatized = self.lemmatize(tokens)
        result['lemmatized'] = lemmatized
        
        # Step 4: Remove stopwords
        filtered = self.remove_stopwords(lemmatized)
        result['filtered'] = filtered
        
        # Map to ISL signs
        word_signs = self.map_to_signs(filtered)
        
        # Combine phrase signs with word signs
        # ISL typically places time expressions first
        time_signs = []
        other_signs = []
        
        for sign in phrases + word_signs:
            if sign in ['Today', 'Monday', 'Tuesday', 'Wednesday', 
                       'Thursday', 'Friday', 'Saturday', 'Sunday']:
                time_signs.append(sign)
            else:
                other_signs.append(sign)
        
        result['isl_signs'] = time_signs + other_signs
        
        return result
    
    def get_processed_signs(self, text: str) -> List[str]:
        """Convenience method to get just the ISL signs"""
        result = self.process(text)
        return result['isl_signs']


# Module-level instance for easy import
nlp_processor = NLPProcessor()
