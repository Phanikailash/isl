import re
from typing import List, Dict

class ISLMapper:
    def __init__(self):
        # Exact class_labels from app.py - ONLY these signs are available
        self.class_labels = [
            '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
            'A', 'Alright', 'Animal', 'B', 'Beautiful', 'Bed', 'Bedroom', 'Bird', 'Black', 'Blind',
            'C', 'Cat', 'Chair', 'Colour', 'Cow', 'D', 'Daughter', 'Deaf', 'Dog', 'Door', 'Dream',
            'E', 'F', 'Father', 'Fish', 'Friday', 'G', 'Good Morning', 'Good night', 'Grey',
            'H', 'Happy', 'He', 'Hello', 'Horse', 'How are you', 'I', 'It',
            'J', 'K', 'L', 'Loud', 'M', 'Monday', 'Mother', 'Mouse',
            'N', 'O', 'Orange', 'P', 'Parent', 'Pink', 'Pleased',
            'Q', 'Quiet', 'R', 'S', 'Sad', 'Saturday', 'She', 'Son', 'Sunday',
            'T', 'Table', 'Thank you', 'Thursday', 'Today', 'Tuesday',
            'U', 'Ugly', 'V', 'W', 'Wednesday', 'White', 'Window',
            'X', 'Y', 'You', 'Z'
        ]
        
        # Create lowercase lookup set for fast matching
        self.class_labels_lower = {label.lower(): label for label in self.class_labels}
        
        # Direct word-to-sign mappings (only for words in class_labels)
        self.direct_mappings = {
            # Numbers (spoken)
            'zero': '0', 'one': '1', 'two': '2', 'three': '3', 'four': '4',
            'five': '5', 'six': '6', 'seven': '7', 'eight': '8', 'nine': '9',
            
            # Numbers (digit)
            '0': '0', '1': '1', '2': '2', '3': '3', '4': '4', '5': '5',
            '6': '6', '7': '7', '8': '8', '9': '9',
            
            # Letters
            'a': 'A', 'b': 'B', 'c': 'C', 'd': 'D', 'e': 'E', 'f': 'F',
            'g': 'G', 'h': 'H', 'i': 'I', 'j': 'J', 'k': 'K', 'l': 'L',
            'm': 'M', 'n': 'N', 'o': 'O', 'p': 'P', 'q': 'Q', 'r': 'R',
            's': 'S', 't': 'T', 'u': 'U', 'v': 'V', 'w': 'W', 'x': 'X',
            'y': 'Y', 'z': 'Z',
            
            # Words with direct mapping to class labels
            'hello': 'Hello',
            'hi': 'Hello',
            'hey': 'Hello',
            'thanks': 'Thank you',
            'thank': 'Thank you',
            'thankyou': 'Thank you',
            'happy': 'Happy',
            'sad': 'Sad',
            'beautiful': 'Beautiful',
            'pretty': 'Beautiful',
            'lovely': 'Beautiful',
            'please': 'Pleased',
            'pleased': 'Pleased',
            'alright': 'Alright',
            'okay': 'Alright',
            'ok': 'Alright',
            'fine': 'Alright',
            
            # Animals
            'animal': 'Animal',
            'animals': 'Animal',
            'bird': 'Bird',
            'birds': 'Bird',
            'cat': 'Cat',
            'cats': 'Cat',
            'dog': 'Dog',
            'dogs': 'Dog',
            'cow': 'Cow',
            'cows': 'Cow',
            'horse': 'Horse',
            'horses': 'Horse',
            'mouse': 'Mouse',
            'mice': 'Mouse',
            'fish': 'Fish',
            'fishes': 'Fish',
            
            # Family
            'mother': 'Mother',
            'mom': 'Mother',
            'mum': 'Mother',
            'mommy': 'Mother',
            'father': 'Father',
            'dad': 'Father',
            'daddy': 'Father',
            'daughter': 'Daughter',
            'daughters': 'Daughter',
            'son': 'Son',
            'sons': 'Son',
            'parent': 'Parent',
            'parents': 'Parent',
            
            # Furniture/Objects
            'chair': 'Chair',
            'chairs': 'Chair',
            'table': 'Table',
            'tables': 'Table',
            'bed': 'Bed',
            'beds': 'Bed',
            'bedroom': 'Bedroom',
            'bedrooms': 'Bedroom',
            'door': 'Door',
            'doors': 'Door',
            'window': 'Window',
            'windows': 'Window',
            
            # Colors
            'black': 'Black',
            'white': 'White',
            'orange': 'Orange',
            'pink': 'Pink',
            'grey': 'Grey',
            'gray': 'Grey',
            'colour': 'Colour',
            'color': 'Colour',
            'colors': 'Colour',
            'colours': 'Colour',
            
            # Days
            'monday': 'Monday',
            'tuesday': 'Tuesday',
            'wednesday': 'Wednesday',
            'thursday': 'Thursday',
            'friday': 'Friday',
            'saturday': 'Saturday',
            'sunday': 'Sunday',
            'today': 'Today',
            
            # Pronouns
            'i': 'I',
            'me': 'I',
            'you': 'You',
            'your': 'You',
            'he': 'He',
            'him': 'He',
            'his': 'He',
            'she': 'She',
            'her': 'She',
            'it': 'It',
            'its': 'It',
            
            # Other words
            'blind': 'Blind',
            'deaf': 'Deaf',
            'dream': 'Dream',
            'dreams': 'Dream',
            'dreaming': 'Dream',
            'loud': 'Loud',
            'loudly': 'Loud',
            'quiet': 'Quiet',
            'quietly': 'Quiet',
            'silence': 'Quiet',
            'silent': 'Quiet',
            'ugly': 'Ugly',
            
            # Time-related
            'morning': 'Good Morning',
            'night': 'Good night',
            'goodnight': 'Good night',
        }
        
        # Time expressions that come first in ISL
        self.time_expressions = [
            'today', 'monday', 'tuesday', 'wednesday',
            'thursday', 'friday', 'saturday', 'sunday'
        ]
        
        # Common phrases that map to single signs
        self.phrase_mappings = {
            'how are you': 'How are you',
            'howareyou': 'How are you',
            'good morning': 'Good Morning',
            'goodmorning': 'Good Morning',
            'good night': 'Good night',
            'goodnight': 'Good night',
            'thank you': 'Thank you',
            'thankyou': 'Thank you'
        }
    
    def map_to_isl(self, text: str) -> List[str]:
        """Convert English text to ISL sequence using only available class_labels"""
        text = text.lower().strip()
        
        if not text:
            return []
        
        # Check for phrase mappings first
        for phrase, isl_sign in self.phrase_mappings.items():
            if phrase in text:
                # Remove the phrase from text and add the sign
                text = text.replace(phrase, ' ')
                return [isl_sign] + self.map_to_isl(text.strip())
        
        # Split into words
        words = re.findall(r'\b\w+\b', text)
        
        if not words:
            return []
        
        # Map words to ISL signs
        isl_signs = []
        time_signs = []
        other_signs = []
        
        skip_next = False
        for i, word in enumerate(words):
            if skip_next:
                skip_next = False
                continue
                
            # Check for two-word phrases
            if i < len(words) - 1:
                two_word = f"{word} {words[i+1]}"
                if two_word in self.phrase_mappings:
                    other_signs.append(self.phrase_mappings[two_word])
                    skip_next = True
                    continue
            
            # Check if word has direct mapping
            if word in self.direct_mappings:
                sign = self.direct_mappings[word]
                
                # Verify sign is in class_labels
                if sign in self.class_labels:
                    # Separate time expressions
                    if word in self.time_expressions:
                        time_signs.append(sign)
                    else:
                        other_signs.append(sign)
            else:
                # Word not in direct mappings - fingerspell using letters
                # Only spell words longer than 2 characters
                if len(word) > 2:
                    for char in word.upper():
                        if char in self.class_labels:
                            other_signs.append(char)
        
        # ISL structure: Time + Subject + Object + Verb
        # For simplicity, we'll use: Time signs first, then other signs
        isl_sequence = time_signs + other_signs
        
        # Remove duplicates while preserving order (for repeated words)
        # But keep intentional repetitions
        return isl_sequence if isl_sequence else []
    
    def get_available_signs(self) -> List[str]:
        """Return list of all available signs (class_labels)"""
        return self.class_labels.copy()
    
    def is_valid_sign(self, sign: str) -> bool:
        """Check if a sign exists in class_labels"""
        return sign in self.class_labels
    
    def get_animation_sequence(self, isl_signs: List[str]) -> List[Dict]:
        """Convert ISL signs to animation sequence"""
        animations = []
        
        for sign in isl_signs:
            if sign in self.class_labels:
                animations.append({
                    'sign': sign,
                    'duration': 1500,  # 1.5 seconds per sign
                    'type': self._get_sign_type(sign),
                    'hand_position': self._get_hand_position(sign),
                    'facial_expression': self._get_facial_expression(sign)
                })
        
        return animations
    
    def _get_sign_type(self, sign: str) -> str:
        """Determine the type of sign"""
        if len(sign) == 1 and sign.isalpha():
            return 'letter'
        elif sign.isdigit():
            return 'number'
        else:
            return 'word'
    
    def _get_hand_position(self, sign: str) -> str:
        """Get hand position type for a sign"""
        if len(sign) == 1 and sign.isalpha():
            return 'fingerspelling'
        elif sign.isdigit():
            return 'numbers'
        else:
            return 'gesture'
    
    def _get_facial_expression(self, sign: str) -> str:
        """Get facial expression for a sign"""
        if sign in ['Happy', 'Beautiful', 'Pleased', 'Hello', 'Good Morning', 'Alright']:
            return 'smile'
        elif sign in ['Sad', 'Ugly', 'Blind', 'Deaf']:
            return 'sad'
        elif sign in ['How are you']:
            return 'question'
        elif sign in ['Loud']:
            return 'intense'
        elif sign in ['Quiet', 'Good night', 'Dream']:
            return 'calm'
        else:
            return 'neutral'
