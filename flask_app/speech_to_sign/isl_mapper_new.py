"""
ISL Mapper Module - English to ISL Sign Conversion
Integrates with NLP Processor for proper text processing
Following the architecture in Figure 3.4
"""

from typing import List, Dict
from .nlp_processor import NLPProcessor, nlp_processor
from .sign_database import ISLDatabase, isl_database


class ISLMapper:
    """
    Maps English text to ISL signs using NLP processing pipeline
    
    Pipeline:
    1. NLP Processing (Text Preprocessing → Tokenization → Lemmatization → Stop-word Removal)
    2. Word to Sign Mapping
    3. ISL Grammar Reordering (Time + Subject + Object structure)
    """
    
    def __init__(self, nlp: NLPProcessor = None, sign_db: ISLDatabase = None):
        self.nlp = nlp or nlp_processor
        self.sign_db = sign_db or isl_database
        
        # Class labels from app.py
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
        
        # Create lookup set for validation
        self.class_labels_set = set(self.class_labels)
    
    def map_to_isl(self, text: str) -> List[str]:
        """
        Convert English text to ISL sign sequence
        Uses NLP processing pipeline for proper text analysis
        """
        if not text or not text.strip():
            return []
        
        # Use NLP processor for full pipeline
        result = self.nlp.process(text)
        isl_signs = result.get('isl_signs', [])
        
        # Validate all signs are in class_labels
        valid_signs = [sign for sign in isl_signs if sign in self.class_labels_set]
        
        return valid_signs
    
    def get_processing_details(self, text: str) -> Dict:
        """
        Get detailed processing information for debugging/display
        Returns all intermediate steps of NLP processing
        """
        result = self.nlp.process(text)
        
        # Add validation info
        result['valid_signs'] = [s for s in result['isl_signs'] if s in self.class_labels_set]
        result['invalid_signs'] = [s for s in result['isl_signs'] if s not in self.class_labels_set]
        
        return result
    
    def get_animation_sequence(self, isl_signs: List[str]) -> List[Dict]:
        """
        Convert ISL signs to animation sequence data
        """
        animations = []
        
        for sign in isl_signs:
            if sign in self.class_labels_set:
                sign_data = self.sign_db.get_sign(sign)
                
                animations.append({
                    'sign': sign,
                    'duration': self._get_sign_duration(sign, sign_data),
                    'type': self._get_sign_type(sign),
                    'hand_position': self._get_hand_position(sign),
                    'facial_expression': sign_data.get('facial_expression', 'neutral'),
                    'motion_type': sign_data.get('motion_type', 'static'),
                    'body_region': sign_data.get('body_region', 'neutral'),
                    'two_hands': sign_data.get('two_hands', False),
                    'keyframes': sign_data.get('keyframes', [])
                })
        
        return animations
    
    def _get_sign_duration(self, sign: str, sign_data: Dict) -> int:
        """Calculate appropriate duration for a sign"""
        base_duration = 1500  # 1.5 seconds default
        
        sign_type = self._get_sign_type(sign)
        if sign_type == 'letter':
            return 800
        elif sign_type == 'number':
            return 1000
        elif sign_type == 'phrase':
            return 2000
        
        motion = sign_data.get('motion_type', 'static')
        if motion in ['circular', 'wave', 'alternating']:
            return 1800
        
        return base_duration
    
    def _get_sign_type(self, sign: str) -> str:
        """Determine the type of sign"""
        if len(sign) == 1 and sign.isalpha():
            return 'letter'
        elif sign.isdigit() or (len(sign) == 1 and sign in '0123456789'):
            return 'number'
        elif ' ' in sign:  # Multi-word phrases
            return 'phrase'
        else:
            return 'word'
    
    def _get_hand_position(self, sign: str) -> str:
        """Get hand position type for a sign"""
        sign_type = self._get_sign_type(sign)
        
        if sign_type == 'letter':
            return 'fingerspelling'
        elif sign_type == 'number':
            return 'numbers'
        else:
            return 'gesture'
    
    def _get_facial_expression(self, sign: str) -> str:
        """Get facial expression for a sign"""
        # Map certain signs to expressions
        expression_map = {
            'Happy': 'smile',
            'Beautiful': 'smile',
            'Pleased': 'smile',
            'Hello': 'smile',
            'Good Morning': 'smile',
            'Alright': 'smile',
            'Thank you': 'smile',
            'Sad': 'sad',
            'Ugly': 'frown',
            'Blind': 'neutral',
            'Deaf': 'neutral',
            'How are you': 'question',
            'Loud': 'intense',
            'Quiet': 'calm',
            'Good night': 'calm',
            'Dream': 'calm'
        }
        
        return expression_map.get(sign, 'neutral')
    
    def get_available_signs(self) -> List[str]:
        """Return list of all available signs (class_labels)"""
        return self.class_labels.copy()
    
    def is_valid_sign(self, sign: str) -> bool:
        """Check if a sign exists in class_labels"""
        return sign in self.class_labels_set
    
    def get_sign_info(self, sign: str) -> Dict:
        """Get complete information about a sign"""
        if sign not in self.class_labels_set:
            return {'error': f'Sign "{sign}" not found'}
        
        sign_data = self.sign_db.get_sign(sign)
        
        return {
            'name': sign,
            'type': self._get_sign_type(sign),
            'hand_position': self._get_hand_position(sign),
            'facial_expression': sign_data.get('facial_expression', 'neutral'),
            'motion_type': sign_data.get('motion_type', 'static'),
            'body_region': sign_data.get('body_region', 'neutral'),
            'two_hands': sign_data.get('two_hands', False),
            'keyframes': sign_data.get('keyframes', [])
        }


# Module-level instance for backward compatibility
isl_mapper = ISLMapper()
