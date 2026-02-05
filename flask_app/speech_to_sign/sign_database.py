"""
ISL Database Module - Sign Repository with Keypoints/Coordinates
Following the architecture in Figure 3.4

Contains 21 hand landmark keypoints (x, y, z) for each sign, matching MediaPipe format:
0: WRIST
1-4: THUMB (CMC, MCP, IP, TIP)
5-8: INDEX (MCP, PIP, DIP, TIP)
9-12: MIDDLE (MCP, PIP, DIP, TIP)
13-16: RING (MCP, PIP, DIP, TIP)
17-20: PINKY (MCP, PIP, DIP, TIP)

Coordinates are normalized (0.0 to 1.0) relative to image dimensions
"""

from typing import Dict, List, Tuple
import math


class ISLDatabase:
    """
    ISL Sign Repository containing keypoint coordinates for all signs
    """
    
    def __init__(self):
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
        
        # Landmark indices
        self.WRIST = 0
        self.THUMB = (1, 2, 3, 4)  # CMC, MCP, IP, TIP
        self.INDEX = (5, 6, 7, 8)  # MCP, PIP, DIP, TIP
        self.MIDDLE = (9, 10, 11, 12)
        self.RING = (13, 14, 15, 16)
        self.PINKY = (17, 18, 19, 20)
        
        # Initialize sign database
        self.signs = self._build_sign_database()
    
    def _create_base_hand(self, x_offset: float = 0.5, y_offset: float = 0.5) -> List[Dict]:
        """Create base hand position (relaxed/neutral)"""
        landmarks = []
        
        # WRIST (center point)
        landmarks.append({'x': x_offset, 'y': y_offset, 'z': 0.0})
        
        # THUMB (extending to the side)
        landmarks.append({'x': x_offset - 0.08, 'y': y_offset - 0.02, 'z': 0.0})  # CMC
        landmarks.append({'x': x_offset - 0.12, 'y': y_offset - 0.05, 'z': 0.0})  # MCP
        landmarks.append({'x': x_offset - 0.14, 'y': y_offset - 0.08, 'z': 0.0})  # IP
        landmarks.append({'x': x_offset - 0.16, 'y': y_offset - 0.10, 'z': 0.0})  # TIP
        
        # INDEX FINGER (pointing up)
        landmarks.append({'x': x_offset - 0.04, 'y': y_offset - 0.08, 'z': 0.0})  # MCP
        landmarks.append({'x': x_offset - 0.04, 'y': y_offset - 0.14, 'z': 0.0})  # PIP
        landmarks.append({'x': x_offset - 0.04, 'y': y_offset - 0.18, 'z': 0.0})  # DIP
        landmarks.append({'x': x_offset - 0.04, 'y': y_offset - 0.22, 'z': 0.0})  # TIP
        
        # MIDDLE FINGER
        landmarks.append({'x': x_offset, 'y': y_offset - 0.08, 'z': 0.0})  # MCP
        landmarks.append({'x': x_offset, 'y': y_offset - 0.15, 'z': 0.0})  # PIP
        landmarks.append({'x': x_offset, 'y': y_offset - 0.20, 'z': 0.0})  # DIP
        landmarks.append({'x': x_offset, 'y': y_offset - 0.24, 'z': 0.0})  # TIP
        
        # RING FINGER
        landmarks.append({'x': x_offset + 0.04, 'y': y_offset - 0.08, 'z': 0.0})  # MCP
        landmarks.append({'x': x_offset + 0.04, 'y': y_offset - 0.14, 'z': 0.0})  # PIP
        landmarks.append({'x': x_offset + 0.04, 'y': y_offset - 0.18, 'z': 0.0})  # DIP
        landmarks.append({'x': x_offset + 0.04, 'y': y_offset - 0.21, 'z': 0.0})  # TIP
        
        # PINKY FINGER
        landmarks.append({'x': x_offset + 0.08, 'y': y_offset - 0.08, 'z': 0.0})  # MCP
        landmarks.append({'x': x_offset + 0.08, 'y': y_offset - 0.12, 'z': 0.0})  # PIP
        landmarks.append({'x': x_offset + 0.08, 'y': y_offset - 0.15, 'z': 0.0})  # DIP
        landmarks.append({'x': x_offset + 0.08, 'y': y_offset - 0.18, 'z': 0.0})  # TIP
        
        return landmarks
    
    def _create_fist(self, x_offset: float = 0.5, y_offset: float = 0.5) -> List[Dict]:
        """Create closed fist position"""
        landmarks = []
        
        # WRIST
        landmarks.append({'x': x_offset, 'y': y_offset, 'z': 0.0})
        
        # THUMB (tucked in)
        landmarks.append({'x': x_offset - 0.06, 'y': y_offset - 0.02, 'z': 0.02})
        landmarks.append({'x': x_offset - 0.08, 'y': y_offset - 0.04, 'z': 0.03})
        landmarks.append({'x': x_offset - 0.06, 'y': y_offset - 0.06, 'z': 0.04})
        landmarks.append({'x': x_offset - 0.04, 'y': y_offset - 0.06, 'z': 0.05})
        
        # INDEX (curled)
        landmarks.append({'x': x_offset - 0.04, 'y': y_offset - 0.08, 'z': 0.0})
        landmarks.append({'x': x_offset - 0.04, 'y': y_offset - 0.10, 'z': 0.04})
        landmarks.append({'x': x_offset - 0.02, 'y': y_offset - 0.08, 'z': 0.06})
        landmarks.append({'x': x_offset - 0.02, 'y': y_offset - 0.04, 'z': 0.05})
        
        # MIDDLE (curled)
        landmarks.append({'x': x_offset, 'y': y_offset - 0.08, 'z': 0.0})
        landmarks.append({'x': x_offset, 'y': y_offset - 0.10, 'z': 0.04})
        landmarks.append({'x': x_offset + 0.02, 'y': y_offset - 0.08, 'z': 0.06})
        landmarks.append({'x': x_offset + 0.02, 'y': y_offset - 0.04, 'z': 0.05})
        
        # RING (curled)
        landmarks.append({'x': x_offset + 0.04, 'y': y_offset - 0.08, 'z': 0.0})
        landmarks.append({'x': x_offset + 0.04, 'y': y_offset - 0.10, 'z': 0.04})
        landmarks.append({'x': x_offset + 0.05, 'y': y_offset - 0.08, 'z': 0.06})
        landmarks.append({'x': x_offset + 0.05, 'y': y_offset - 0.04, 'z': 0.05})
        
        # PINKY (curled)
        landmarks.append({'x': x_offset + 0.08, 'y': y_offset - 0.08, 'z': 0.0})
        landmarks.append({'x': x_offset + 0.08, 'y': y_offset - 0.09, 'z': 0.03})
        landmarks.append({'x': x_offset + 0.08, 'y': y_offset - 0.07, 'z': 0.05})
        landmarks.append({'x': x_offset + 0.08, 'y': y_offset - 0.04, 'z': 0.04})
        
        return landmarks
    
    def _modify_finger(self, landmarks: List[Dict], finger_indices: Tuple, 
                       extended: bool = True, x_offset: float = 0.0, 
                       y_offset: float = 0.0, curl_amount: float = 0.0) -> List[Dict]:
        """Modify a specific finger's position"""
        modified = [lm.copy() for lm in landmarks]
        base_idx = finger_indices[0]
        
        if extended:
            # Extend finger straight
            for i, idx in enumerate(finger_indices):
                modified[idx]['x'] += x_offset
                modified[idx]['y'] -= 0.04 * (i + 1) + y_offset
                modified[idx]['z'] = 0.0
        else:
            # Curl finger
            for i, idx in enumerate(finger_indices):
                curl = curl_amount * (i / len(finger_indices))
                modified[idx]['z'] = curl * 0.08
                if i > 0:
                    modified[idx]['y'] = modified[finger_indices[0]]['y'] - 0.02 * i + curl * 0.04
        
        return modified
    
    def _build_sign_database(self) -> Dict:
        """Build the complete sign database with keypoints"""
        signs = {}
        
        # ============ NUMBERS 0-9 ============
        signs['0'] = self._create_sign_0()
        signs['1'] = self._create_sign_1()
        signs['2'] = self._create_sign_2()
        signs['3'] = self._create_sign_3()
        signs['4'] = self._create_sign_4()
        signs['5'] = self._create_sign_5()
        signs['6'] = self._create_sign_6()
        signs['7'] = self._create_sign_7()
        signs['8'] = self._create_sign_8()
        signs['9'] = self._create_sign_9()
        
        # ============ LETTERS A-Z ============
        for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            signs[letter] = self._create_letter_sign(letter)
        
        # ============ WORDS ============
        # Greetings
        signs['Hello'] = self._create_sign_hello()
        signs['Thank you'] = self._create_sign_thank_you()
        signs['Good Morning'] = self._create_sign_good_morning()
        signs['Good night'] = self._create_sign_good_night()
        signs['How are you'] = self._create_sign_how_are_you()
        
        # Emotions
        signs['Happy'] = self._create_sign_happy()
        signs['Sad'] = self._create_sign_sad()
        signs['Beautiful'] = self._create_sign_beautiful()
        signs['Ugly'] = self._create_sign_ugly()
        signs['Alright'] = self._create_sign_alright()
        signs['Pleased'] = self._create_sign_pleased()
        
        # Animals
        signs['Animal'] = self._create_sign_animal()
        signs['Bird'] = self._create_sign_bird()
        signs['Cat'] = self._create_sign_cat()
        signs['Dog'] = self._create_sign_dog()
        signs['Cow'] = self._create_sign_cow()
        signs['Horse'] = self._create_sign_horse()
        signs['Mouse'] = self._create_sign_mouse()
        signs['Fish'] = self._create_sign_fish()
        
        # Family
        signs['Mother'] = self._create_sign_mother()
        signs['Father'] = self._create_sign_father()
        signs['Daughter'] = self._create_sign_daughter()
        signs['Son'] = self._create_sign_son()
        signs['Parent'] = self._create_sign_parent()
        
        # Objects
        signs['Chair'] = self._create_sign_chair()
        signs['Table'] = self._create_sign_table()
        signs['Bed'] = self._create_sign_bed()
        signs['Bedroom'] = self._create_sign_bedroom()
        signs['Door'] = self._create_sign_door()
        signs['Window'] = self._create_sign_window()
        
        # Colors
        signs['Black'] = self._create_sign_black()
        signs['White'] = self._create_sign_white()
        signs['Orange'] = self._create_sign_orange()
        signs['Pink'] = self._create_sign_pink()
        signs['Grey'] = self._create_sign_grey()
        signs['Colour'] = self._create_sign_colour()
        
        # Days
        for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']:
            signs[day] = self._create_sign_day(day)
        signs['Today'] = self._create_sign_today()
        
        # Pronouns
        signs['I'] = self._create_sign_i()
        signs['You'] = self._create_sign_you()
        signs['He'] = self._create_sign_he()
        signs['She'] = self._create_sign_she()
        signs['It'] = self._create_sign_it()
        
        # Other
        signs['Blind'] = self._create_sign_blind()
        signs['Deaf'] = self._create_sign_deaf()
        signs['Dream'] = self._create_sign_dream()
        signs['Loud'] = self._create_sign_loud()
        signs['Quiet'] = self._create_sign_quiet()
        
        return signs
    
    # ============ NUMBER SIGNS ============
    
    def _create_sign_0(self) -> Dict:
        """Number 0 - Circle with fingers"""
        landmarks = self._create_fist()
        # Touch thumb to index forming a circle
        landmarks[4]['x'] = landmarks[8]['x'] + 0.02
        landmarks[4]['y'] = landmarks[8]['y']
        return self._create_sign_data('0', landmarks, 'number')
    
    def _create_sign_1(self) -> Dict:
        """Number 1 - Index finger extended"""
        landmarks = self._create_fist()
        # Extend index finger
        landmarks[5]['y'] -= 0.02
        landmarks[6]['y'] -= 0.06
        landmarks[7]['y'] -= 0.10
        landmarks[8]['y'] -= 0.14
        for i in range(5, 9):
            landmarks[i]['z'] = 0.0
        return self._create_sign_data('1', landmarks, 'number')
    
    def _create_sign_2(self) -> Dict:
        """Number 2 - Index and middle extended (V shape)"""
        landmarks = self._create_fist()
        # Extend index
        for i in range(5, 9):
            landmarks[i]['y'] -= 0.04 * (i - 4)
            landmarks[i]['z'] = 0.0
            landmarks[i]['x'] -= 0.02
        # Extend middle
        for i in range(9, 13):
            landmarks[i]['y'] -= 0.04 * (i - 8)
            landmarks[i]['z'] = 0.0
            landmarks[i]['x'] += 0.02
        return self._create_sign_data('2', landmarks, 'number')
    
    def _create_sign_3(self) -> Dict:
        """Number 3 - Thumb, index, middle extended"""
        landmarks = self._create_fist()
        # Extend thumb outward
        landmarks[4]['x'] -= 0.06
        landmarks[4]['y'] -= 0.08
        # Extend index and middle
        for i in range(5, 9):
            landmarks[i]['y'] -= 0.04 * (i - 4)
            landmarks[i]['z'] = 0.0
        for i in range(9, 13):
            landmarks[i]['y'] -= 0.04 * (i - 8)
            landmarks[i]['z'] = 0.0
        return self._create_sign_data('3', landmarks, 'number')
    
    def _create_sign_4(self) -> Dict:
        """Number 4 - Four fingers extended, thumb tucked"""
        landmarks = self._create_base_hand()
        # Tuck thumb
        landmarks[4]['x'] = landmarks[5]['x'] + 0.02
        landmarks[4]['y'] = landmarks[5]['y'] + 0.02
        landmarks[4]['z'] = 0.04
        return self._create_sign_data('4', landmarks, 'number')
    
    def _create_sign_5(self) -> Dict:
        """Number 5 - All fingers extended (open hand)"""
        return self._create_sign_data('5', self._create_base_hand(), 'number')
    
    def _create_sign_6(self) -> Dict:
        """Number 6 - Fist with thumb extended upward (thumbs up style)"""
        landmarks = []
        x, y = 0.5, 0.5
        landmarks.append({'x': x, 'y': y, 'z': 0.0})  # Wrist
        # Thumb pointing straight UP
        landmarks.append({'x': x - 0.06, 'y': y - 0.04, 'z': 0.0})
        landmarks.append({'x': x - 0.08, 'y': y - 0.10, 'z': 0.0})
        landmarks.append({'x': x - 0.09, 'y': y - 0.16, 'z': 0.0})
        landmarks.append({'x': x - 0.09, 'y': y - 0.22, 'z': 0.0})  # Thumb tip UP
        # All other fingers tightly curled into fist
        for i, offset in enumerate([-0.03, 0.01, 0.05, 0.09]):
            base_x = x + offset
            landmarks.append({'x': base_x, 'y': y - 0.06, 'z': 0.0})
            landmarks.append({'x': base_x, 'y': y - 0.04, 'z': 0.06})
            landmarks.append({'x': base_x + 0.02, 'y': y - 0.02, 'z': 0.08})
            landmarks.append({'x': base_x + 0.03, 'y': y + 0.02, 'z': 0.06})
        return self._create_sign_data('6', landmarks, 'number')
    
    def _create_sign_7(self) -> Dict:
        """Number 7 - Index and middle pointing sideways (gun shape)"""
        landmarks = []
        x, y = 0.5, 0.5
        landmarks.append({'x': x, 'y': y, 'z': 0.0})  # Wrist
        # Thumb pointing up
        landmarks.append({'x': x - 0.05, 'y': y - 0.03, 'z': 0.0})
        landmarks.append({'x': x - 0.07, 'y': y - 0.08, 'z': 0.0})
        landmarks.append({'x': x - 0.08, 'y': y - 0.13, 'z': 0.0})
        landmarks.append({'x': x - 0.08, 'y': y - 0.18, 'z': 0.0})
        # Index pointing LEFT (horizontal)
        landmarks.append({'x': x - 0.02, 'y': y - 0.06, 'z': 0.0})
        landmarks.append({'x': x - 0.10, 'y': y - 0.06, 'z': 0.0})
        landmarks.append({'x': x - 0.18, 'y': y - 0.06, 'z': 0.0})
        landmarks.append({'x': x - 0.26, 'y': y - 0.06, 'z': 0.0})  # Index tip
        # Middle also pointing LEFT (parallel to index)
        landmarks.append({'x': x + 0.01, 'y': y - 0.04, 'z': 0.0})
        landmarks.append({'x': x - 0.07, 'y': y - 0.02, 'z': 0.0})
        landmarks.append({'x': x - 0.15, 'y': y - 0.01, 'z': 0.0})
        landmarks.append({'x': x - 0.23, 'y': y, 'z': 0.0})  # Middle tip
        # Ring and pinky curled
        for i, offset in enumerate([0.05, 0.09]):
            base_x = x + offset
            landmarks.append({'x': base_x, 'y': y - 0.05, 'z': 0.0})
            landmarks.append({'x': base_x, 'y': y - 0.03, 'z': 0.05})
            landmarks.append({'x': base_x + 0.01, 'y': y, 'z': 0.07})
            landmarks.append({'x': base_x + 0.02, 'y': y + 0.03, 'z': 0.05})
        return self._create_sign_data('7', landmarks, 'number')
    
    def _create_sign_8(self) -> Dict:
        """Number 8 - Three fingers (index, middle, ring) extended, thumb and pinky touching"""
        landmarks = []
        x, y = 0.5, 0.5
        landmarks.append({'x': x, 'y': y, 'z': 0.0})  # Wrist
        # Thumb curving to touch pinky
        landmarks.append({'x': x - 0.04, 'y': y - 0.02, 'z': 0.02})
        landmarks.append({'x': x - 0.02, 'y': y - 0.04, 'z': 0.04})
        landmarks.append({'x': x + 0.02, 'y': y - 0.05, 'z': 0.05})
        landmarks.append({'x': x + 0.06, 'y': y - 0.06, 'z': 0.04})  # Thumb tip touching pinky
        # Index extended UP
        landmarks.append({'x': x - 0.04, 'y': y - 0.08, 'z': 0.0})
        landmarks.append({'x': x - 0.05, 'y': y - 0.14, 'z': 0.0})
        landmarks.append({'x': x - 0.06, 'y': y - 0.20, 'z': 0.0})
        landmarks.append({'x': x - 0.06, 'y': y - 0.26, 'z': 0.0})
        # Middle extended UP
        landmarks.append({'x': x, 'y': y - 0.08, 'z': 0.0})
        landmarks.append({'x': x, 'y': y - 0.15, 'z': 0.0})
        landmarks.append({'x': x, 'y': y - 0.22, 'z': 0.0})
        landmarks.append({'x': x, 'y': y - 0.28, 'z': 0.0})
        # Ring extended UP
        landmarks.append({'x': x + 0.04, 'y': y - 0.08, 'z': 0.0})
        landmarks.append({'x': x + 0.05, 'y': y - 0.14, 'z': 0.0})
        landmarks.append({'x': x + 0.06, 'y': y - 0.20, 'z': 0.0})
        landmarks.append({'x': x + 0.06, 'y': y - 0.25, 'z': 0.0})
        # Pinky bent to touch thumb
        landmarks.append({'x': x + 0.08, 'y': y - 0.06, 'z': 0.0})
        landmarks.append({'x': x + 0.09, 'y': y - 0.04, 'z': 0.03})
        landmarks.append({'x': x + 0.08, 'y': y - 0.05, 'z': 0.05})
        landmarks.append({'x': x + 0.06, 'y': y - 0.06, 'z': 0.04})  # Touching thumb
        return self._create_sign_data('8', landmarks, 'number')
    
    def _create_sign_9(self) -> Dict:
        """Number 9 - Closed fist with pinky extended (like 'I love you' without thumb)"""
        landmarks = []
        x, y = 0.5, 0.5
        landmarks.append({'x': x, 'y': y, 'z': 0.0})  # Wrist
        # Thumb curled into fist
        landmarks.append({'x': x - 0.05, 'y': y - 0.02, 'z': 0.03})
        landmarks.append({'x': x - 0.06, 'y': y - 0.04, 'z': 0.05})
        landmarks.append({'x': x - 0.04, 'y': y - 0.05, 'z': 0.06})
        landmarks.append({'x': x - 0.02, 'y': y - 0.04, 'z': 0.06})
        # Index, middle, ring all curled into tight fist
        for i, offset in enumerate([-0.03, 0.01, 0.05]):
            base_x = x + offset
            landmarks.append({'x': base_x, 'y': y - 0.06, 'z': 0.0})
            landmarks.append({'x': base_x, 'y': y - 0.04, 'z': 0.06})
            landmarks.append({'x': base_x + 0.02, 'y': y - 0.02, 'z': 0.08})
            landmarks.append({'x': base_x + 0.03, 'y': y + 0.02, 'z': 0.06})
        # Pinky extended straight UP
        landmarks.append({'x': x + 0.09, 'y': y - 0.06, 'z': 0.0})
        landmarks.append({'x': x + 0.10, 'y': y - 0.12, 'z': 0.0})
        landmarks.append({'x': x + 0.11, 'y': y - 0.17, 'z': 0.0})
        landmarks.append({'x': x + 0.12, 'y': y - 0.22, 'z': 0.0})  # Pinky tip UP
        return self._create_sign_data('9', landmarks, 'number')
    
    # ============ LETTER SIGNS ============
    
    def _create_letter_sign(self, letter: str) -> Dict:
        """Create fingerspelling sign for a letter"""
        # Base hand configurations for ASL/ISL fingerspelling
        letter_configs = {
            'A': self._letter_a(),
            'B': self._letter_b(),
            'C': self._letter_c(),
            'D': self._letter_d(),
            'E': self._letter_e(),
            'F': self._letter_f(),
            'G': self._letter_g(),
            'H': self._letter_h(),
            'I': self._letter_i(),
            'J': self._letter_j(),
            'K': self._letter_k(),
            'L': self._letter_l(),
            'M': self._letter_m(),
            'N': self._letter_n(),
            'O': self._letter_o(),
            'P': self._letter_p(),
            'Q': self._letter_q(),
            'R': self._letter_r(),
            'S': self._letter_s(),
            'T': self._letter_t(),
            'U': self._letter_u(),
            'V': self._letter_v(),
            'W': self._letter_w(),
            'X': self._letter_x(),
            'Y': self._letter_y(),
            'Z': self._letter_z()
        }
        
        landmarks = letter_configs.get(letter, self._create_fist())
        return self._create_sign_data(letter, landmarks, 'letter')
    
    def _letter_a(self) -> List[Dict]:
        """A - Fist with thumb to the side"""
        landmarks = self._create_fist()
        landmarks[4]['x'] -= 0.04
        landmarks[4]['y'] = landmarks[5]['y']
        return landmarks
    
    def _letter_b(self) -> List[Dict]:
        """B - Flat hand, fingers together, thumb across palm"""
        landmarks = self._create_base_hand()
        landmarks[4] = {'x': 0.52, 'y': 0.45, 'z': 0.04}
        return landmarks
    
    def _letter_c(self) -> List[Dict]:
        """C - Curved hand like holding a cup"""
        landmarks = self._create_base_hand()
        # Curve all fingers
        for i in range(5, 21):
            landmarks[i]['z'] = 0.03
            landmarks[i]['x'] -= 0.02
        landmarks[4]['x'] = 0.42
        landmarks[4]['y'] = 0.42
        return landmarks
    
    def _letter_d(self) -> List[Dict]:
        """D - Index up, others touch thumb"""
        landmarks = self._create_sign_1()['keyframes'][0]['right_hand']
        # Curl middle, ring, pinky to touch thumb
        landmarks[4]['y'] = landmarks[12]['y'] = landmarks[16]['y'] = landmarks[20]['y'] = 0.42
        landmarks[4]['z'] = landmarks[12]['z'] = landmarks[16]['z'] = landmarks[20]['z'] = 0.03
        return landmarks
    
    def _letter_e(self) -> List[Dict]:
        """E - All fingers curled, thumb across"""
        landmarks = self._create_fist()
        landmarks[4] = {'x': 0.46, 'y': 0.42, 'z': 0.04}
        return landmarks
    
    def _letter_f(self) -> List[Dict]:
        """F - Index and thumb touching in circle, others extended"""
        landmarks = self._create_base_hand()
        landmarks[4] = {'x': landmarks[8]['x'], 'y': landmarks[8]['y'], 'z': 0.02}
        return landmarks
    
    def _letter_g(self) -> List[Dict]:
        """G - Index pointing to side, thumb parallel"""
        landmarks = self._create_fist()
        landmarks[4] = {'x': 0.38, 'y': 0.42, 'z': 0.0}
        landmarks[5]['y'] = landmarks[6]['y'] = 0.42
        landmarks[7] = {'x': 0.38, 'y': 0.42, 'z': 0.0}
        landmarks[8] = {'x': 0.35, 'y': 0.42, 'z': 0.0}
        return landmarks
    
    def _letter_h(self) -> List[Dict]:
        """H - Index and middle pointing to side"""
        landmarks = self._letter_g()
        landmarks[9]['y'] = landmarks[10]['y'] = 0.42
        landmarks[11] = {'x': 0.38, 'y': 0.44, 'z': 0.0}
        landmarks[12] = {'x': 0.35, 'y': 0.44, 'z': 0.0}
        return landmarks
    
    def _letter_i(self) -> List[Dict]:
        """I - Pinky extended, others closed"""
        landmarks = self._create_fist()
        for i in range(17, 21):
            landmarks[i]['y'] -= 0.04 * (i - 16)
            landmarks[i]['z'] = 0.0
        return landmarks
    
    def _letter_j(self) -> List[Dict]:
        """J - Like I but with motion (represented statically here)"""
        return self._letter_i()
    
    def _letter_k(self) -> List[Dict]:
        """K - Index and middle up in V, thumb between them"""
        landmarks = self._create_sign_2()['keyframes'][0]['right_hand']
        landmarks[4] = {'x': 0.48, 'y': 0.38, 'z': 0.02}
        return landmarks
    
    def _letter_l(self) -> List[Dict]:
        """L - Index up, thumb out (L shape)"""
        landmarks = self._create_fist()
        # Index up
        for i in range(5, 9):
            landmarks[i]['y'] -= 0.04 * (i - 4)
            landmarks[i]['z'] = 0.0
        # Thumb out
        landmarks[4] = {'x': 0.36, 'y': 0.50, 'z': 0.0}
        return landmarks
    
    def _letter_m(self) -> List[Dict]:
        """M - Three fingers over thumb"""
        landmarks = self._create_fist()
        landmarks[4] = {'x': 0.54, 'y': 0.44, 'z': 0.06}
        for i in [8, 12, 16]:
            landmarks[i]['z'] = 0.05
            landmarks[i]['y'] = 0.44
        return landmarks
    
    def _letter_n(self) -> List[Dict]:
        """N - Two fingers over thumb"""
        landmarks = self._create_fist()
        landmarks[4] = {'x': 0.52, 'y': 0.44, 'z': 0.06}
        for i in [8, 12]:
            landmarks[i]['z'] = 0.05
            landmarks[i]['y'] = 0.44
        return landmarks
    
    def _letter_o(self) -> List[Dict]:
        """O - All fingers touch thumb in circle"""
        return self._create_sign_0()['keyframes'][0]['right_hand']
    
    def _letter_p(self) -> List[Dict]:
        """P - Like K but pointing down"""
        landmarks = self._letter_k()
        # Rotate hand downward
        for lm in landmarks:
            lm['y'] += 0.15
        return landmarks
    
    def _letter_q(self) -> List[Dict]:
        """Q - Like G but pointing down"""
        landmarks = self._letter_g()
        for lm in landmarks:
            lm['y'] += 0.15
        return landmarks
    
    def _letter_r(self) -> List[Dict]:
        """R - Index and middle crossed"""
        landmarks = self._create_sign_2()['keyframes'][0]['right_hand']
        # Cross index over middle
        landmarks[8]['x'] = landmarks[12]['x']
        return landmarks
    
    def _letter_s(self) -> List[Dict]:
        """S - Fist with thumb across fingers"""
        landmarks = self._create_fist()
        landmarks[4] = {'x': 0.46, 'y': 0.44, 'z': 0.04}
        return landmarks
    
    def _letter_t(self) -> List[Dict]:
        """T - Thumb between index and middle"""
        landmarks = self._create_fist()
        landmarks[4] = {'x': 0.48, 'y': 0.42, 'z': 0.05}
        return landmarks
    
    def _letter_u(self) -> List[Dict]:
        """U - Index and middle together, pointing up"""
        landmarks = self._create_fist()
        for i in range(5, 13):
            landmarks[i]['y'] -= 0.04 * ((i - 5) % 4 + 1)
            landmarks[i]['z'] = 0.0
        # Keep them together
        for i in range(9, 13):
            landmarks[i]['x'] = landmarks[i-4]['x'] + 0.02
        return landmarks
    
    def _letter_v(self) -> List[Dict]:
        """V - Index and middle spread (V shape)"""
        return self._create_sign_2()['keyframes'][0]['right_hand']
    
    def _letter_w(self) -> List[Dict]:
        """W - Three fingers spread"""
        landmarks = self._create_fist()
        # Extend index, middle, ring spread apart
        for i in range(5, 9):
            landmarks[i]['y'] -= 0.04 * (i - 4)
            landmarks[i]['x'] -= 0.03
            landmarks[i]['z'] = 0.0
        for i in range(9, 13):
            landmarks[i]['y'] -= 0.04 * (i - 8)
            landmarks[i]['z'] = 0.0
        for i in range(13, 17):
            landmarks[i]['y'] -= 0.04 * (i - 12)
            landmarks[i]['x'] += 0.03
            landmarks[i]['z'] = 0.0
        return landmarks
    
    def _letter_x(self) -> List[Dict]:
        """X - Index finger hooked"""
        landmarks = self._create_fist()
        landmarks[5]['y'] -= 0.02
        landmarks[6]['y'] -= 0.04
        landmarks[7] = {'x': 0.48, 'y': 0.40, 'z': 0.03}
        landmarks[8] = {'x': 0.50, 'y': 0.42, 'z': 0.04}
        return landmarks
    
    def _letter_y(self) -> List[Dict]:
        """Y - Thumb and pinky extended"""
        landmarks = self._create_fist()
        # Extend thumb
        landmarks[4] = {'x': 0.36, 'y': 0.46, 'z': 0.0}
        # Extend pinky
        for i in range(17, 21):
            landmarks[i]['y'] -= 0.04 * (i - 16)
            landmarks[i]['z'] = 0.0
        return landmarks
    
    def _letter_z(self) -> List[Dict]:
        """Z - Index finger traces Z (static representation)"""
        return self._create_sign_1()['keyframes'][0]['right_hand']
    
    # ============ WORD SIGNS ============
    
    def _create_sign_hello(self) -> Dict:
        """Hello - Open hand wave near forehead with spread fingers"""
        landmarks = []
        x, y = 0.6, 0.28
        landmarks.append({'x': x, 'y': y, 'z': 0.0})  # Wrist
        # Thumb pointing outward
        landmarks.append({'x': x - 0.10, 'y': y - 0.02, 'z': 0.0})
        landmarks.append({'x': x - 0.14, 'y': y - 0.06, 'z': 0.0})
        landmarks.append({'x': x - 0.17, 'y': y - 0.10, 'z': 0.0})
        landmarks.append({'x': x - 0.19, 'y': y - 0.14, 'z': 0.0})
        # Fingers spread wide (wave position)
        for i, offset in enumerate([-0.05, 0.0, 0.05, 0.10]):
            base_x = x + offset
            for j in range(4):
                landmarks.append({'x': base_x + (j * 0.01), 'y': y - 0.08 - (j * 0.05), 'z': 0.0})
        start_hand = landmarks
        end_hand = [{'x': lm['x'] + 0.08, 'y': lm['y'], 'z': lm['z']} for lm in landmarks]
        return self._create_animated_sign('Hello', start_hand, end_hand, 
                                          motion='wave', facial='smile', 
                                          body_region='head')
    
    def _create_sign_thank_you(self) -> Dict:
        """Thank you - Flat hand touching chin then moving outward"""
        landmarks = []
        x, y = 0.5, 0.32
        landmarks.append({'x': x, 'y': y, 'z': 0.0})  # Wrist
        # Thumb tucked slightly
        landmarks.append({'x': x - 0.06, 'y': y - 0.01, 'z': 0.02})
        landmarks.append({'x': x - 0.08, 'y': y - 0.03, 'z': 0.03})
        landmarks.append({'x': x - 0.09, 'y': y - 0.05, 'z': 0.03})
        landmarks.append({'x': x - 0.10, 'y': y - 0.07, 'z': 0.03})
        # Fingers together flat
        for i, offset in enumerate([-0.03, 0.0, 0.03, 0.06]):
            base_x = x + offset
            for j in range(4):
                landmarks.append({'x': base_x, 'y': y - 0.08 - (j * 0.04), 'z': 0.01})
        start_hand = landmarks
        end_hand = [{'x': lm['x'], 'y': lm['y'] + 0.18, 'z': lm['z'] - 0.02} for lm in landmarks]
        return self._create_animated_sign('Thank you', start_hand, end_hand,
                                          motion='outward', facial='smile',
                                          body_region='chin')
    
    def _create_sign_good_morning(self) -> Dict:
        """Good Morning - Sun rising motion with open hand"""
        landmarks = []
        x, y = 0.35, 0.55
        landmarks.append({'x': x, 'y': y, 'z': 0.0})  # Wrist
        # Thumb up and out
        landmarks.append({'x': x - 0.08, 'y': y - 0.04, 'z': 0.0})
        landmarks.append({'x': x - 0.12, 'y': y - 0.10, 'z': 0.0})
        landmarks.append({'x': x - 0.14, 'y': y - 0.15, 'z': 0.0})
        landmarks.append({'x': x - 0.15, 'y': y - 0.20, 'z': 0.0})
        # Fingers spread upward like sun rays
        for i, offset in enumerate([-0.04, 0.0, 0.04, 0.08]):
            base_x = x + offset
            for j in range(4):
                angle = (i - 1.5) * 0.08
                landmarks.append({'x': base_x + (j * angle * 0.3), 'y': y - 0.10 - (j * 0.05), 'z': 0.0})
        start_hand = landmarks
        end_hand = [{'x': lm['x'] + 0.15, 'y': lm['y'] - 0.25, 'z': lm['z']} for lm in landmarks]
        return self._create_animated_sign('Good Morning', start_hand, end_hand,
                                          motion='rising', facial='smile',
                                          body_region='chest')
    
    def _create_sign_good_night(self) -> Dict:
        """Good night - Palms together near tilted head"""
        landmarks = []
        x, y = 0.55, 0.30
        landmarks.append({'x': x, 'y': y, 'z': 0.0})  # Wrist
        # Thumb folded in (prayer position)
        landmarks.append({'x': x - 0.04, 'y': y - 0.02, 'z': 0.04})
        landmarks.append({'x': x - 0.05, 'y': y - 0.04, 'z': 0.05})
        landmarks.append({'x': x - 0.05, 'y': y - 0.06, 'z': 0.05})
        landmarks.append({'x': x - 0.04, 'y': y - 0.08, 'z': 0.04})
        # Fingers together vertically
        for i, offset in enumerate([-0.02, 0.0, 0.02, 0.04]):
            base_x = x + offset
            for j in range(4):
                landmarks.append({'x': base_x, 'y': y - 0.08 - (j * 0.045), 'z': 0.02})
        return self._create_sign_data('Good night', landmarks, 'phrase',
                                      facial='calm', motion='closing',
                                      two_hands=True)
    
    def _create_sign_how_are_you(self) -> Dict:
        """How are you - Curved questioning hands"""
        landmarks = []
        x, y = 0.45, 0.42
        landmarks.append({'x': x, 'y': y, 'z': 0.0})  # Wrist
        # Thumb curved inward
        landmarks.append({'x': x - 0.06, 'y': y - 0.02, 'z': 0.02})
        landmarks.append({'x': x - 0.09, 'y': y - 0.05, 'z': 0.03})
        landmarks.append({'x': x - 0.10, 'y': y - 0.08, 'z': 0.04})
        landmarks.append({'x': x - 0.09, 'y': y - 0.10, 'z': 0.05})
        # Fingers curved like asking question
        for i, offset in enumerate([-0.03, 0.0, 0.03, 0.06]):
            base_x = x + offset
            for j in range(4):
                curve = 0.02 * j if j > 1 else 0
                landmarks.append({'x': base_x + curve, 'y': y - 0.08 - (j * 0.04), 'z': 0.02 + curve})
        start_hand = landmarks
        end_hand = [{'x': lm['x'] + 0.12, 'y': lm['y'], 'z': lm['z']} for lm in landmarks]
        return self._create_animated_sign('How are you', start_hand, end_hand,
                                          motion='questioning', facial='question',
                                          body_region='chest')
    
    def _create_sign_happy(self) -> Dict:
        """Happy - Open palm patting chest upward"""
        landmarks = []
        x, y = 0.48, 0.48
        landmarks.append({'x': x, 'y': y, 'z': 0.0})  # Wrist
        # Thumb extended sideways
        landmarks.append({'x': x - 0.09, 'y': y - 0.01, 'z': 0.0})
        landmarks.append({'x': x - 0.13, 'y': y - 0.03, 'z': 0.0})
        landmarks.append({'x': x - 0.16, 'y': y - 0.05, 'z': 0.0})
        landmarks.append({'x': x - 0.18, 'y': y - 0.06, 'z': 0.0})
        # All fingers extended and slightly spread (brushing upward)
        for i, offset in enumerate([-0.03, 0.01, 0.05, 0.09]):
            base_x = x + offset
            for j in range(4):
                landmarks.append({'x': base_x, 'y': y - 0.09 - (j * 0.045), 'z': 0.01})
        return self._create_sign_data('Happy', landmarks, 'emotion',
                                      facial='smile', motion='circular',
                                      body_region='chest')
    
    def _create_sign_sad(self) -> Dict:
        """Sad - Both hands with fingers down, drooping from face"""
        landmarks = []
        x, y = 0.5, 0.35
        landmarks.append({'x': x, 'y': y, 'z': 0.0})  # Wrist
        # Thumb relaxed
        landmarks.append({'x': x - 0.07, 'y': y + 0.01, 'z': 0.01})
        landmarks.append({'x': x - 0.10, 'y': y + 0.03, 'z': 0.02})
        landmarks.append({'x': x - 0.12, 'y': y + 0.06, 'z': 0.02})
        landmarks.append({'x': x - 0.13, 'y': y + 0.09, 'z': 0.02})
        # Fingers drooping downward (sad expression)
        for i, offset in enumerate([-0.04, 0.0, 0.04, 0.08]):
            base_x = x + offset
            for j in range(4):
                landmarks.append({'x': base_x, 'y': y + 0.02 + (j * 0.05), 'z': 0.02})
        start_hand = landmarks
        end_hand = [{'x': lm['x'], 'y': lm['y'] + 0.15, 'z': lm['z']} for lm in landmarks]
        return self._create_animated_sign('Sad', start_hand, end_hand,
                                          motion='downward', facial='sad',
                                          body_region='face')
    
    def _create_sign_beautiful(self) -> Dict:
        """Beautiful - Open hand circling the face"""
        landmarks = []
        x, y = 0.55, 0.28
        landmarks.append({'x': x, 'y': y, 'z': 0.0})  # Wrist
        # Thumb extended
        landmarks.append({'x': x - 0.08, 'y': y - 0.03, 'z': 0.0})
        landmarks.append({'x': x - 0.11, 'y': y - 0.07, 'z': 0.0})
        landmarks.append({'x': x - 0.13, 'y': y - 0.11, 'z': 0.0})
        landmarks.append({'x': x - 0.14, 'y': y - 0.14, 'z': 0.0})
        # Fingers together elegantly
        for i, offset in enumerate([-0.02, 0.01, 0.04, 0.07]):
            base_x = x + offset
            for j in range(4):
                landmarks.append({'x': base_x, 'y': y - 0.08 - (j * 0.048), 'z': 0.0})
        return self._create_sign_data('Beautiful', landmarks, 'adjective',
                                      facial='smile', motion='circular',
                                      body_region='face')
    
    def _create_sign_ugly(self) -> Dict:
        """Ugly - Bent claw-like fingers crossing face"""
        landmarks = []
        x, y = 0.48, 0.32
        landmarks.append({'x': x, 'y': y, 'z': 0.0})  # Wrist
        # Thumb bent
        landmarks.append({'x': x - 0.06, 'y': y - 0.02, 'z': 0.03})
        landmarks.append({'x': x - 0.08, 'y': y - 0.05, 'z': 0.05})
        landmarks.append({'x': x - 0.07, 'y': y - 0.07, 'z': 0.06})
        landmarks.append({'x': x - 0.05, 'y': y - 0.08, 'z': 0.06})
        # Fingers bent like claws
        for i, offset in enumerate([-0.04, 0.0, 0.04, 0.08]):
            base_x = x + offset
            landmarks.append({'x': base_x, 'y': y - 0.08, 'z': 0.0})
            landmarks.append({'x': base_x, 'y': y - 0.12, 'z': 0.04})
            landmarks.append({'x': base_x + 0.02, 'y': y - 0.10, 'z': 0.07})
            landmarks.append({'x': base_x + 0.03, 'y': y - 0.06, 'z': 0.06})
        return self._create_sign_data('Ugly', landmarks, 'adjective',
                                      facial='frown', motion='across',
                                      body_region='face')
    
    def _create_sign_alright(self) -> Dict:
        """Alright - OK gesture with thumb and index circle, other fingers up"""
        landmarks = []
        x, y = 0.5, 0.45
        landmarks.append({'x': x, 'y': y, 'z': 0.0})  # Wrist
        # Thumb touching index tip to form OK circle
        landmarks.append({'x': x - 0.05, 'y': y - 0.03, 'z': 0.02})
        landmarks.append({'x': x - 0.07, 'y': y - 0.06, 'z': 0.03})
        landmarks.append({'x': x - 0.06, 'y': y - 0.09, 'z': 0.03})
        landmarks.append({'x': x - 0.04, 'y': y - 0.11, 'z': 0.02})  # Thumb tip
        # Index finger curling to meet thumb
        landmarks.append({'x': x - 0.03, 'y': y - 0.08, 'z': 0.0})
        landmarks.append({'x': x - 0.04, 'y': y - 0.11, 'z': 0.02})
        landmarks.append({'x': x - 0.05, 'y': y - 0.12, 'z': 0.03})
        landmarks.append({'x': x - 0.04, 'y': y - 0.11, 'z': 0.02})  # Meeting thumb
        # Middle, ring, pinky extended upward
        for i, offset in enumerate([0.01, 0.05, 0.09]):
            base_x = x + offset
            for j in range(4):
                landmarks.append({'x': base_x, 'y': y - 0.08 - (j * 0.05), 'z': 0.0})
        return self._create_sign_data('Alright', landmarks, 'expression',
                                      facial='neutral', motion='static')
    
    def _create_sign_pleased(self) -> Dict:
        """Pleased - Both hands flat on chest moving outward"""
        landmarks = []
        x, y = 0.52, 0.50
        landmarks.append({'x': x, 'y': y, 'z': 0.0})  # Wrist
        # Thumb tucked under
        landmarks.append({'x': x - 0.05, 'y': y + 0.01, 'z': 0.03})
        landmarks.append({'x': x - 0.06, 'y': y + 0.02, 'z': 0.04})
        landmarks.append({'x': x - 0.05, 'y': y + 0.03, 'z': 0.04})
        landmarks.append({'x': x - 0.03, 'y': y + 0.03, 'z': 0.03})
        # Fingers flat together pointing forward
        for i, offset in enumerate([-0.02, 0.02, 0.06, 0.10]):
            base_x = x + offset
            for j in range(4):
                landmarks.append({'x': base_x, 'y': y - 0.06 - (j * 0.04), 'z': 0.04})
        return self._create_sign_data('Pleased', landmarks, 'emotion',
                                      facial='smile', motion='outward',
                                      body_region='chest')
    
    # ============ ANIMAL SIGNS ============
    
    def _create_sign_animal(self) -> Dict:
        """Animal - Fingertips on chest with rocking claw motion"""
        landmarks = []
        x, y = 0.5, 0.52
        landmarks.append({'x': x, 'y': y, 'z': 0.0})  # Wrist
        # Thumb curled
        landmarks.append({'x': x - 0.05, 'y': y - 0.03, 'z': 0.03})
        landmarks.append({'x': x - 0.06, 'y': y - 0.06, 'z': 0.05})
        landmarks.append({'x': x - 0.05, 'y': y - 0.08, 'z': 0.06})
        landmarks.append({'x': x - 0.03, 'y': y - 0.09, 'z': 0.05})
        # All fingers curved like claws touching chest
        for i, offset in enumerate([-0.04, 0.0, 0.04, 0.08]):
            base_x = x + offset
            landmarks.append({'x': base_x, 'y': y - 0.07, 'z': 0.0})
            landmarks.append({'x': base_x, 'y': y - 0.10, 'z': 0.06})
            landmarks.append({'x': base_x, 'y': y - 0.08, 'z': 0.10})
            landmarks.append({'x': base_x, 'y': y - 0.05, 'z': 0.08})
        return self._create_sign_data('Animal', landmarks, 'noun',
                                      motion='rocking', body_region='chest')
    
    def _create_sign_bird(self) -> Dict:
        """Bird - Index and thumb forming beak opening/closing near mouth"""
        landmarks = []
        x, y = 0.48, 0.33
        landmarks.append({'x': x, 'y': y, 'z': 0.0})  # Wrist
        # Thumb forming beak - upper part
        landmarks.append({'x': x - 0.06, 'y': y - 0.04, 'z': 0.0})
        landmarks.append({'x': x - 0.10, 'y': y - 0.08, 'z': 0.0})
        landmarks.append({'x': x - 0.13, 'y': y - 0.11, 'z': 0.0})
        landmarks.append({'x': x - 0.15, 'y': y - 0.13, 'z': 0.0})  # Beak tip
        # Index forming beak - lower part
        landmarks.append({'x': x - 0.04, 'y': y - 0.06, 'z': 0.0})
        landmarks.append({'x': x - 0.08, 'y': y - 0.10, 'z': 0.0})
        landmarks.append({'x': x - 0.12, 'y': y - 0.13, 'z': 0.0})
        landmarks.append({'x': x - 0.15, 'y': y - 0.14, 'z': 0.01})  # Meeting thumb
        # Other fingers curled in
        for i, offset in enumerate([0.0, 0.04, 0.08]):
            base_x = x + offset
            landmarks.append({'x': base_x, 'y': y - 0.06, 'z': 0.0})
            landmarks.append({'x': base_x, 'y': y - 0.08, 'z': 0.04})
            landmarks.append({'x': base_x + 0.01, 'y': y - 0.06, 'z': 0.06})
            landmarks.append({'x': base_x + 0.01, 'y': y - 0.03, 'z': 0.05})
        return self._create_sign_data('Bird', landmarks, 'noun',
                                      motion='opening_closing', body_region='mouth')
    
    def _create_sign_cat(self) -> Dict:
        """Cat - Pinching whiskers at cheeks, pulling outward"""
        landmarks = []
        x, y = 0.52, 0.34
        landmarks.append({'x': x, 'y': y, 'z': 0.0})  # Wrist
        # Thumb and index pinched for whisker
        landmarks.append({'x': x - 0.05, 'y': y - 0.03, 'z': 0.01})
        landmarks.append({'x': x - 0.07, 'y': y - 0.06, 'z': 0.02})
        landmarks.append({'x': x - 0.08, 'y': y - 0.08, 'z': 0.02})
        landmarks.append({'x': x - 0.08, 'y': y - 0.10, 'z': 0.01})  # Whisker pinch
        # Index near thumb
        landmarks.append({'x': x - 0.03, 'y': y - 0.06, 'z': 0.0})
        landmarks.append({'x': x - 0.05, 'y': y - 0.09, 'z': 0.01})
        landmarks.append({'x': x - 0.07, 'y': y - 0.11, 'z': 0.01})
        landmarks.append({'x': x - 0.08, 'y': y - 0.11, 'z': 0.01})
        # Middle, ring, pinky loosely curled
        for i, offset in enumerate([0.0, 0.04, 0.08]):
            base_x = x + offset
            landmarks.append({'x': base_x, 'y': y - 0.06, 'z': 0.0})
            landmarks.append({'x': base_x, 'y': y - 0.09, 'z': 0.03})
            landmarks.append({'x': base_x + 0.01, 'y': y - 0.08, 'z': 0.05})
            landmarks.append({'x': base_x + 0.02, 'y': y - 0.05, 'z': 0.04})
        return self._create_sign_data('Cat', landmarks, 'noun',
                                      motion='outward', body_region='cheek',
                                      two_hands=True)
    
    def _create_sign_dog(self) -> Dict:
        """Dog - Snapping fingers with patting thigh motion"""
        landmarks = []
        x, y = 0.5, 0.58
        landmarks.append({'x': x, 'y': y, 'z': 0.0})  # Wrist
        # Thumb ready to snap
        landmarks.append({'x': x - 0.06, 'y': y - 0.02, 'z': 0.02})
        landmarks.append({'x': x - 0.08, 'y': y - 0.05, 'z': 0.03})
        landmarks.append({'x': x - 0.07, 'y': y - 0.08, 'z': 0.04})
        landmarks.append({'x': x - 0.05, 'y': y - 0.09, 'z': 0.04})
        # Index and middle extended for snapping
        landmarks.append({'x': x - 0.03, 'y': y - 0.08, 'z': 0.0})
        landmarks.append({'x': x - 0.03, 'y': y - 0.12, 'z': 0.0})
        landmarks.append({'x': x - 0.03, 'y': y - 0.16, 'z': 0.0})
        landmarks.append({'x': x - 0.03, 'y': y - 0.19, 'z': 0.0})
        landmarks.append({'x': x + 0.01, 'y': y - 0.08, 'z': 0.0})
        landmarks.append({'x': x + 0.01, 'y': y - 0.12, 'z': 0.0})
        landmarks.append({'x': x + 0.01, 'y': y - 0.16, 'z': 0.0})
        landmarks.append({'x': x + 0.01, 'y': y - 0.19, 'z': 0.0})
        # Ring and pinky curled
        for i, offset in enumerate([0.05, 0.09]):
            base_x = x + offset
            landmarks.append({'x': base_x, 'y': y - 0.07, 'z': 0.0})
            landmarks.append({'x': base_x, 'y': y - 0.09, 'z': 0.04})
            landmarks.append({'x': base_x + 0.01, 'y': y - 0.07, 'z': 0.06})
            landmarks.append({'x': base_x + 0.01, 'y': y - 0.04, 'z': 0.05})
        return self._create_sign_data('Dog', landmarks, 'noun',
                                      motion='patting', body_region='thigh')
    
    def _create_sign_cow(self) -> Dict:
        """Cow - Y handshape at temples representing horns"""
        landmarks = []
        x, y = 0.55, 0.25
        landmarks.append({'x': x, 'y': y, 'z': 0.0})  # Wrist
        # Thumb extended out for horn
        landmarks.append({'x': x - 0.08, 'y': y - 0.02, 'z': 0.0})
        landmarks.append({'x': x - 0.13, 'y': y - 0.05, 'z': 0.0})
        landmarks.append({'x': x - 0.17, 'y': y - 0.09, 'z': 0.0})
        landmarks.append({'x': x - 0.20, 'y': y - 0.12, 'z': 0.0})
        # Index, middle, ring curled in fist
        for i, offset in enumerate([-0.04, 0.0, 0.04]):
            base_x = x + offset
            landmarks.append({'x': base_x, 'y': y - 0.06, 'z': 0.0})
            landmarks.append({'x': base_x, 'y': y - 0.08, 'z': 0.04})
            landmarks.append({'x': base_x + 0.01, 'y': y - 0.06, 'z': 0.06})
            landmarks.append({'x': base_x + 0.01, 'y': y - 0.03, 'z': 0.05})
        # Pinky extended for other horn
        landmarks.append({'x': x + 0.08, 'y': y - 0.06, 'z': 0.0})
        landmarks.append({'x': x + 0.10, 'y': y - 0.10, 'z': 0.0})
        landmarks.append({'x': x + 0.12, 'y': y - 0.14, 'z': 0.0})
        landmarks.append({'x': x + 0.14, 'y': y - 0.17, 'z': 0.0})
        return self._create_sign_data('Cow', landmarks, 'noun',
                                      motion='twisting', body_region='temple')
    
    def _create_sign_horse(self) -> Dict:
        """Horse - Thumb at temple with fingers flapping like ears"""
        landmarks = []
        x, y = 0.58, 0.26
        landmarks.append({'x': x, 'y': y, 'z': 0.0})  # Wrist
        # Thumb touching temple
        landmarks.append({'x': x - 0.06, 'y': y - 0.02, 'z': 0.03})
        landmarks.append({'x': x - 0.08, 'y': y - 0.04, 'z': 0.05})
        landmarks.append({'x': x - 0.09, 'y': y - 0.06, 'z': 0.06})
        landmarks.append({'x': x - 0.09, 'y': y - 0.08, 'z': 0.06})
        # Index and middle extended upward as ears
        landmarks.append({'x': x - 0.03, 'y': y - 0.08, 'z': 0.0})
        landmarks.append({'x': x - 0.04, 'y': y - 0.14, 'z': 0.0})
        landmarks.append({'x': x - 0.05, 'y': y - 0.19, 'z': 0.0})
        landmarks.append({'x': x - 0.06, 'y': y - 0.23, 'z': 0.0})
        landmarks.append({'x': x + 0.01, 'y': y - 0.08, 'z': 0.0})
        landmarks.append({'x': x + 0.01, 'y': y - 0.14, 'z': 0.0})
        landmarks.append({'x': x + 0.01, 'y': y - 0.19, 'z': 0.0})
        landmarks.append({'x': x + 0.01, 'y': y - 0.23, 'z': 0.0})
        # Ring and pinky curled
        for i, offset in enumerate([0.05, 0.09]):
            base_x = x + offset
            landmarks.append({'x': base_x, 'y': y - 0.06, 'z': 0.0})
            landmarks.append({'x': base_x, 'y': y - 0.08, 'z': 0.04})
            landmarks.append({'x': base_x + 0.01, 'y': y - 0.06, 'z': 0.06})
            landmarks.append({'x': base_x + 0.01, 'y': y - 0.03, 'z': 0.05})
        return self._create_sign_data('Horse', landmarks, 'noun',
                                      motion='flapping', body_region='temple')
    
    def _create_sign_mouse(self) -> Dict:
        """Mouse - Index finger brushing nose repeatedly"""
        landmarks = []
        x, y = 0.5, 0.32
        landmarks.append({'x': x, 'y': y, 'z': 0.0})  # Wrist
        # Thumb relaxed
        landmarks.append({'x': x - 0.05, 'y': y - 0.02, 'z': 0.02})
        landmarks.append({'x': x - 0.07, 'y': y - 0.04, 'z': 0.03})
        landmarks.append({'x': x - 0.08, 'y': y - 0.06, 'z': 0.03})
        landmarks.append({'x': x - 0.08, 'y': y - 0.08, 'z': 0.03})
        # Index extended pointing at nose
        landmarks.append({'x': x - 0.02, 'y': y - 0.06, 'z': 0.0})
        landmarks.append({'x': x - 0.02, 'y': y - 0.12, 'z': 0.0})
        landmarks.append({'x': x - 0.02, 'y': y - 0.17, 'z': 0.0})
        landmarks.append({'x': x - 0.02, 'y': y - 0.21, 'z': 0.0})
        # Other fingers curled
        for i, offset in enumerate([0.02, 0.06, 0.10]):
            base_x = x + offset
            landmarks.append({'x': base_x, 'y': y - 0.06, 'z': 0.0})
            landmarks.append({'x': base_x, 'y': y - 0.08, 'z': 0.04})
            landmarks.append({'x': base_x + 0.01, 'y': y - 0.06, 'z': 0.06})
            landmarks.append({'x': base_x + 0.01, 'y': y - 0.03, 'z': 0.05})
        return self._create_sign_data('Mouse', landmarks, 'noun',
                                      motion='brushing', body_region='nose')
    
    def _create_sign_fish(self) -> Dict:
        """Fish - Flat hand making swimming wave motion"""
        landmarks = []
        x, y = 0.5, 0.52
        landmarks.append({'x': x, 'y': y, 'z': 0.0})  # Wrist
        # Thumb alongside hand
        landmarks.append({'x': x - 0.05, 'y': y - 0.02, 'z': 0.02})
        landmarks.append({'x': x - 0.06, 'y': y - 0.05, 'z': 0.02})
        landmarks.append({'x': x - 0.06, 'y': y - 0.08, 'z': 0.02})
        landmarks.append({'x': x - 0.05, 'y': y - 0.10, 'z': 0.02})
        # Fingers together flat like fish body, slight wave
        for i, offset in enumerate([-0.02, 0.02, 0.06, 0.10]):
            base_x = x + offset
            wave = 0.01 if i % 2 == 0 else -0.01
            for j in range(4):
                landmarks.append({'x': base_x, 'y': y - 0.08 - (j * 0.04), 'z': wave})
        return self._create_sign_data('Fish', landmarks, 'noun',
                                      motion='swimming', body_region='neutral')
    
    # ============ FAMILY SIGNS ============
    
    def _create_sign_mother(self) -> Dict:
        """Mother - Open hand with thumb touching chin"""
        landmarks = []
        x, y = 0.5, 0.36
        landmarks.append({'x': x, 'y': y, 'z': 0.0})  # Wrist
        # Thumb touching chin
        landmarks.append({'x': x - 0.06, 'y': y - 0.04, 'z': 0.04})
        landmarks.append({'x': x - 0.08, 'y': y - 0.08, 'z': 0.06})
        landmarks.append({'x': x - 0.09, 'y': y - 0.11, 'z': 0.07})
        landmarks.append({'x': x - 0.09, 'y': y - 0.13, 'z': 0.07})  # On chin
        # Fingers spread open
        for i, offset in enumerate([-0.03, 0.01, 0.05, 0.09]):
            base_x = x + offset
            for j in range(4):
                landmarks.append({'x': base_x, 'y': y - 0.08 - (j * 0.045), 'z': 0.0})
        return self._create_sign_data('Mother', landmarks, 'noun',
                                      facial='smile', body_region='chin')
    
    def _create_sign_father(self) -> Dict:
        """Father - Open hand with thumb touching forehead"""
        landmarks = []
        x, y = 0.5, 0.26
        landmarks.append({'x': x, 'y': y, 'z': 0.0})  # Wrist
        # Thumb touching forehead
        landmarks.append({'x': x - 0.06, 'y': y - 0.03, 'z': 0.04})
        landmarks.append({'x': x - 0.08, 'y': y - 0.06, 'z': 0.06})
        landmarks.append({'x': x - 0.09, 'y': y - 0.09, 'z': 0.07})
        landmarks.append({'x': x - 0.09, 'y': y - 0.11, 'z': 0.07})  # On forehead
        # Fingers spread open
        for i, offset in enumerate([-0.03, 0.01, 0.05, 0.09]):
            base_x = x + offset
            for j in range(4):
                landmarks.append({'x': base_x, 'y': y - 0.08 - (j * 0.045), 'z': 0.0})
        return self._create_sign_data('Father', landmarks, 'noun',
                                      facial='neutral', body_region='forehead')
    
    def _create_sign_daughter(self) -> Dict:
        """Daughter - Girl sign (chin) + cradling baby motion"""
        landmarks = []
        x, y = 0.52, 0.42
        landmarks.append({'x': x, 'y': y, 'z': 0.0})  # Wrist
        # Thumb along side
        landmarks.append({'x': x - 0.05, 'y': y - 0.02, 'z': 0.01})
        landmarks.append({'x': x - 0.07, 'y': y - 0.04, 'z': 0.02})
        landmarks.append({'x': x - 0.08, 'y': y - 0.06, 'z': 0.02})
        landmarks.append({'x': x - 0.08, 'y': y - 0.08, 'z': 0.02})
        # Fingers curved as if cradling
        for i, offset in enumerate([-0.03, 0.01, 0.05, 0.09]):
            base_x = x + offset
            landmarks.append({'x': base_x, 'y': y - 0.06, 'z': 0.0})
            landmarks.append({'x': base_x - 0.01, 'y': y - 0.10, 'z': 0.03})
            landmarks.append({'x': base_x - 0.02, 'y': y - 0.12, 'z': 0.05})
            landmarks.append({'x': base_x - 0.02, 'y': y - 0.13, 'z': 0.06})
        return self._create_sign_data('Daughter', landmarks, 'noun',
                                      motion='cradling', body_region='chin')
    
    def _create_sign_son(self) -> Dict:
        """Son - Boy sign (forehead) + cradling motion"""
        landmarks = []
        x, y = 0.52, 0.32
        landmarks.append({'x': x, 'y': y, 'z': 0.0})  # Wrist
        # Thumb along side
        landmarks.append({'x': x - 0.05, 'y': y - 0.02, 'z': 0.01})
        landmarks.append({'x': x - 0.07, 'y': y - 0.04, 'z': 0.02})
        landmarks.append({'x': x - 0.08, 'y': y - 0.06, 'z': 0.02})
        landmarks.append({'x': x - 0.08, 'y': y - 0.08, 'z': 0.02})
        # Fingers in salute position at forehead
        for i, offset in enumerate([-0.02, 0.02, 0.06, 0.10]):
            base_x = x + offset
            landmarks.append({'x': base_x, 'y': y - 0.07, 'z': 0.0})
            landmarks.append({'x': base_x, 'y': y - 0.12, 'z': 0.0})
            landmarks.append({'x': base_x, 'y': y - 0.16, 'z': 0.0})
            landmarks.append({'x': base_x, 'y': y - 0.19, 'z': 0.0})
        return self._create_sign_data('Son', landmarks, 'noun',
                                      motion='cradling', body_region='forehead')
    
    def _create_sign_parent(self) -> Dict:
        """Parent - Alternating between forehead and chin touch"""
        landmarks = []
        x, y = 0.5, 0.34
        landmarks.append({'x': x, 'y': y, 'z': 0.0})  # Wrist
        # Thumb extended
        landmarks.append({'x': x - 0.07, 'y': y - 0.03, 'z': 0.03})
        landmarks.append({'x': x - 0.10, 'y': y - 0.07, 'z': 0.04})
        landmarks.append({'x': x - 0.12, 'y': y - 0.10, 'z': 0.05})
        landmarks.append({'x': x - 0.13, 'y': y - 0.12, 'z': 0.05})
        # Fingers together
        for i, offset in enumerate([-0.02, 0.02, 0.06, 0.10]):
            base_x = x + offset
            for j in range(4):
                landmarks.append({'x': base_x, 'y': y - 0.08 - (j * 0.042), 'z': 0.02})
        return self._create_sign_data('Parent', landmarks, 'noun',
                                      motion='alternating', body_region='face',
                                      two_hands=True)
    
    # ============ OBJECT SIGNS ============
    
    def _create_sign_chair(self) -> Dict:
        """Chair - Two bent fingers (legs) sitting on horizontal thumb"""
        landmarks = []
        x, y = 0.5, 0.52
        landmarks.append({'x': x, 'y': y, 'z': 0.0})  # Wrist
        # Thumb horizontal as seat
        landmarks.append({'x': x - 0.06, 'y': y - 0.04, 'z': 0.0})
        landmarks.append({'x': x - 0.10, 'y': y - 0.04, 'z': 0.0})
        landmarks.append({'x': x - 0.14, 'y': y - 0.04, 'z': 0.0})
        landmarks.append({'x': x - 0.17, 'y': y - 0.04, 'z': 0.0})
        # Index and middle bent down (legs)
        landmarks.append({'x': x - 0.03, 'y': y - 0.08, 'z': 0.0})
        landmarks.append({'x': x - 0.03, 'y': y - 0.12, 'z': 0.03})
        landmarks.append({'x': x - 0.03, 'y': y - 0.10, 'z': 0.06})
        landmarks.append({'x': x - 0.03, 'y': y - 0.06, 'z': 0.06})
        landmarks.append({'x': x + 0.01, 'y': y - 0.08, 'z': 0.0})
        landmarks.append({'x': x + 0.01, 'y': y - 0.12, 'z': 0.03})
        landmarks.append({'x': x + 0.01, 'y': y - 0.10, 'z': 0.06})
        landmarks.append({'x': x + 0.01, 'y': y - 0.06, 'z': 0.06})
        # Ring and pinky curled
        for i, offset in enumerate([0.05, 0.09]):
            base_x = x + offset
            landmarks.append({'x': base_x, 'y': y - 0.06, 'z': 0.0})
            landmarks.append({'x': base_x, 'y': y - 0.08, 'z': 0.04})
            landmarks.append({'x': base_x + 0.01, 'y': y - 0.06, 'z': 0.06})
            landmarks.append({'x': base_x + 0.01, 'y': y - 0.03, 'z': 0.05})
        return self._create_sign_data('Chair', landmarks, 'noun',
                                      motion='tapping', two_hands=True)
    
    def _create_sign_table(self) -> Dict:
        """Table - Both flat hands forming horizontal surface"""
        landmarks = []
        x, y = 0.5, 0.55
        landmarks.append({'x': x, 'y': y, 'z': 0.0})  # Wrist
        # Thumb tucked under
        landmarks.append({'x': x - 0.04, 'y': y + 0.01, 'z': 0.03})
        landmarks.append({'x': x - 0.05, 'y': y + 0.02, 'z': 0.04})
        landmarks.append({'x': x - 0.04, 'y': y + 0.03, 'z': 0.04})
        landmarks.append({'x': x - 0.02, 'y': y + 0.03, 'z': 0.03})
        # All fingers flat, horizontal (palm down)
        for i, offset in enumerate([-0.02, 0.02, 0.06, 0.10]):
            base_x = x + offset
            for j in range(4):
                landmarks.append({'x': base_x, 'y': y - 0.04 - (j * 0.03), 'z': 0.08})
        return self._create_sign_data('Table', landmarks, 'noun',
                                      motion='patting', two_hands=True)
    
    def _create_sign_bed(self) -> Dict:
        """Bed - Tilted head on hands (sleeping gesture)"""
        landmarks = []
        x, y = 0.58, 0.32
        landmarks.append({'x': x, 'y': y, 'z': 0.0})  # Wrist
        # Thumb along palm
        landmarks.append({'x': x - 0.04, 'y': y - 0.02, 'z': 0.02})
        landmarks.append({'x': x - 0.05, 'y': y - 0.04, 'z': 0.03})
        landmarks.append({'x': x - 0.05, 'y': y - 0.06, 'z': 0.03})
        landmarks.append({'x': x - 0.04, 'y': y - 0.07, 'z': 0.03})
        # Fingers together, tilted as pillow
        for i, offset in enumerate([-0.02, 0.01, 0.04, 0.07]):
            base_x = x + offset
            for j in range(4):
                landmarks.append({'x': base_x + (j * 0.02), 'y': y - 0.06 - (j * 0.03), 'z': 0.02})
        return self._create_sign_data('Bed', landmarks, 'noun',
                                      facial='calm', motion='resting',
                                      body_region='head')
    
    def _create_sign_bedroom(self) -> Dict:
        """Bedroom - Bed sign + box/room outline"""
        landmarks = []
        x, y = 0.5, 0.48
        landmarks.append({'x': x, 'y': y, 'z': 0.0})  # Wrist
        # Thumb extended
        landmarks.append({'x': x - 0.07, 'y': y - 0.02, 'z': 0.0})
        landmarks.append({'x': x - 0.11, 'y': y - 0.04, 'z': 0.0})
        landmarks.append({'x': x - 0.14, 'y': y - 0.06, 'z': 0.0})
        landmarks.append({'x': x - 0.16, 'y': y - 0.08, 'z': 0.0})
        # Fingers making L shape for room corner
        landmarks.append({'x': x - 0.03, 'y': y - 0.08, 'z': 0.0})
        landmarks.append({'x': x - 0.03, 'y': y - 0.13, 'z': 0.0})
        landmarks.append({'x': x - 0.03, 'y': y - 0.17, 'z': 0.0})
        landmarks.append({'x': x - 0.03, 'y': y - 0.20, 'z': 0.0})
        # Other fingers curved inward
        for i, offset in enumerate([0.01, 0.05, 0.09]):
            base_x = x + offset
            landmarks.append({'x': base_x, 'y': y - 0.07, 'z': 0.0})
            landmarks.append({'x': base_x, 'y': y - 0.10, 'z': 0.03})
            landmarks.append({'x': base_x + 0.01, 'y': y - 0.08, 'z': 0.05})
            landmarks.append({'x': base_x + 0.02, 'y': y - 0.05, 'z': 0.04})
        return self._create_sign_data('Bedroom', landmarks, 'noun',
                                      motion='box_shape', two_hands=True)
    
    def _create_sign_door(self) -> Dict:
        """Door - Flat hand swinging open like door"""
        landmarks_start = []
        landmarks_end = []
        x, y = 0.42, 0.48
        # Start position - closed door
        landmarks_start.append({'x': x, 'y': y, 'z': 0.0})
        landmarks_start.append({'x': x - 0.05, 'y': y - 0.02, 'z': 0.02})
        landmarks_start.append({'x': x - 0.06, 'y': y - 0.04, 'z': 0.03})
        landmarks_start.append({'x': x - 0.06, 'y': y - 0.06, 'z': 0.03})
        landmarks_start.append({'x': x - 0.05, 'y': y - 0.07, 'z': 0.02})
        for i, offset in enumerate([-0.02, 0.02, 0.06, 0.10]):
            base_x = x + offset
            for j in range(4):
                landmarks_start.append({'x': base_x, 'y': y - 0.08 - (j * 0.04), 'z': 0.0})
        # End position - open door (rotated)
        landmarks_end.append({'x': x + 0.18, 'y': y, 'z': 0.0})
        landmarks_end.append({'x': x + 0.13, 'y': y - 0.02, 'z': 0.02})
        landmarks_end.append({'x': x + 0.12, 'y': y - 0.04, 'z': 0.03})
        landmarks_end.append({'x': x + 0.12, 'y': y - 0.06, 'z': 0.03})
        landmarks_end.append({'x': x + 0.13, 'y': y - 0.07, 'z': 0.02})
        for i, offset in enumerate([0.16, 0.20, 0.24, 0.28]):
            base_x = x + offset
            for j in range(4):
                landmarks_end.append({'x': base_x, 'y': y - 0.08 - (j * 0.04), 'z': 0.04})
        return self._create_animated_sign('Door', landmarks_start, landmarks_end,
                                          motion='opening')
    
    def _create_sign_window(self) -> Dict:
        """Window - Flat hands sliding up and down"""
        landmarks = []
        x, y = 0.5, 0.42
        landmarks.append({'x': x, 'y': y, 'z': 0.0})  # Wrist
        # Thumb at side
        landmarks.append({'x': x - 0.06, 'y': y - 0.02, 'z': 0.01})
        landmarks.append({'x': x - 0.08, 'y': y - 0.04, 'z': 0.01})
        landmarks.append({'x': x - 0.09, 'y': y - 0.06, 'z': 0.01})
        landmarks.append({'x': x - 0.10, 'y': y - 0.07, 'z': 0.01})
        # Fingers spread forming window frame
        for i, offset in enumerate([-0.03, 0.01, 0.05, 0.09]):
            base_x = x + offset
            for j in range(4):
                landmarks.append({'x': base_x, 'y': y - 0.07 - (j * 0.05), 'z': 0.0})
        return self._create_sign_data('Window', landmarks, 'noun',
                                      motion='sliding', two_hands=True)
    
    # ============ COLOR SIGNS ============
    
    def _create_sign_black(self) -> Dict:
        """Black - Index finger drawing line across forehead"""
        landmarks = []
        x, y = 0.45, 0.24
        landmarks.append({'x': x, 'y': y, 'z': 0.0})  # Wrist
        # Thumb tucked
        landmarks.append({'x': x - 0.04, 'y': y - 0.02, 'z': 0.03})
        landmarks.append({'x': x - 0.05, 'y': y - 0.04, 'z': 0.04})
        landmarks.append({'x': x - 0.04, 'y': y - 0.05, 'z': 0.04})
        landmarks.append({'x': x - 0.02, 'y': y - 0.05, 'z': 0.03})
        # Index extended horizontally across forehead
        landmarks.append({'x': x - 0.02, 'y': y - 0.06, 'z': 0.0})
        landmarks.append({'x': x - 0.06, 'y': y - 0.06, 'z': 0.0})
        landmarks.append({'x': x - 0.10, 'y': y - 0.06, 'z': 0.0})
        landmarks.append({'x': x - 0.14, 'y': y - 0.06, 'z': 0.0})
        # Other fingers curled
        for i, offset in enumerate([0.02, 0.06, 0.10]):
            base_x = x + offset
            landmarks.append({'x': base_x, 'y': y - 0.05, 'z': 0.0})
            landmarks.append({'x': base_x, 'y': y - 0.07, 'z': 0.04})
            landmarks.append({'x': base_x + 0.01, 'y': y - 0.05, 'z': 0.06})
            landmarks.append({'x': base_x + 0.01, 'y': y - 0.02, 'z': 0.05})
        return self._create_sign_data('Black', landmarks, 'adjective',
                                      motion='across', body_region='forehead')
    
    def _create_sign_white(self) -> Dict:
        """White - Open hand pulling away from chest"""
        landmarks_start = []
        landmarks_end = []
        x, y = 0.5, 0.48
        # Start - hand on chest
        landmarks_start.append({'x': x, 'y': y, 'z': 0.0})
        landmarks_start.append({'x': x - 0.07, 'y': y - 0.02, 'z': 0.05})
        landmarks_start.append({'x': x - 0.10, 'y': y - 0.04, 'z': 0.08})
        landmarks_start.append({'x': x - 0.12, 'y': y - 0.06, 'z': 0.10})
        landmarks_start.append({'x': x - 0.13, 'y': y - 0.08, 'z': 0.10})
        for i, offset in enumerate([-0.03, 0.01, 0.05, 0.09]):
            base_x = x + offset
            for j in range(4):
                landmarks_start.append({'x': base_x, 'y': y - 0.07 - (j * 0.04), 'z': 0.08})
        # End - hand pulled away
        landmarks_end.append({'x': x, 'y': y + 0.05, 'z': 0.0})
        landmarks_end.append({'x': x - 0.07, 'y': y + 0.03, 'z': 0.0})
        landmarks_end.append({'x': x - 0.10, 'y': y + 0.01, 'z': 0.0})
        landmarks_end.append({'x': x - 0.12, 'y': y - 0.01, 'z': 0.0})
        landmarks_end.append({'x': x - 0.13, 'y': y - 0.03, 'z': 0.0})
        for i, offset in enumerate([-0.03, 0.01, 0.05, 0.09]):
            base_x = x + offset
            for j in range(4):
                landmarks_end.append({'x': base_x, 'y': y + 0.02 - (j * 0.04), 'z': 0.0})
        return self._create_animated_sign('White', landmarks_start, landmarks_end,
                                          motion='outward', body_region='chest')
    
    def _create_sign_orange(self) -> Dict:
        """Orange - Squeezing motion near chin (like squeezing orange)"""
        landmarks = []
        x, y = 0.5, 0.36
        landmarks.append({'x': x, 'y': y, 'z': 0.0})  # Wrist
        # Thumb in squeezing position
        landmarks.append({'x': x - 0.05, 'y': y - 0.03, 'z': 0.02})
        landmarks.append({'x': x - 0.07, 'y': y - 0.06, 'z': 0.04})
        landmarks.append({'x': x - 0.06, 'y': y - 0.09, 'z': 0.05})
        landmarks.append({'x': x - 0.04, 'y': y - 0.11, 'z': 0.04})
        # All fingers curved to meet thumb (squeezing)
        for i, offset in enumerate([-0.02, 0.02, 0.06, 0.10]):
            base_x = x + offset
            landmarks.append({'x': base_x, 'y': y - 0.06, 'z': 0.0})
            landmarks.append({'x': base_x - 0.02, 'y': y - 0.09, 'z': 0.03})
            landmarks.append({'x': base_x - 0.03, 'y': y - 0.11, 'z': 0.05})
            landmarks.append({'x': base_x - 0.03, 'y': y - 0.12, 'z': 0.04})
        return self._create_sign_data('Orange', landmarks, 'adjective',
                                      motion='squeezing', body_region='chin')
    
    def _create_sign_pink(self) -> Dict:
        """Pink - P handshape brushing lips downward"""
        landmarks = []
        x, y = 0.48, 0.34
        landmarks.append({'x': x, 'y': y, 'z': 0.0})  # Wrist
        # Thumb out to side
        landmarks.append({'x': x - 0.06, 'y': y - 0.03, 'z': 0.0})
        landmarks.append({'x': x - 0.10, 'y': y - 0.05, 'z': 0.0})
        landmarks.append({'x': x - 0.13, 'y': y - 0.06, 'z': 0.0})
        landmarks.append({'x': x - 0.15, 'y': y - 0.06, 'z': 0.0})
        # Index pointing down (P shape)
        landmarks.append({'x': x - 0.02, 'y': y - 0.06, 'z': 0.0})
        landmarks.append({'x': x - 0.02, 'y': y - 0.02, 'z': 0.0})
        landmarks.append({'x': x - 0.02, 'y': y + 0.03, 'z': 0.0})
        landmarks.append({'x': x - 0.02, 'y': y + 0.08, 'z': 0.0})
        # Middle also pointing down
        landmarks.append({'x': x + 0.02, 'y': y - 0.06, 'z': 0.0})
        landmarks.append({'x': x + 0.02, 'y': y - 0.02, 'z': 0.0})
        landmarks.append({'x': x + 0.02, 'y': y + 0.03, 'z': 0.0})
        landmarks.append({'x': x + 0.02, 'y': y + 0.08, 'z': 0.0})
        # Ring and pinky curled
        for i, offset in enumerate([0.06, 0.10]):
            base_x = x + offset
            landmarks.append({'x': base_x, 'y': y - 0.05, 'z': 0.0})
            landmarks.append({'x': base_x, 'y': y - 0.07, 'z': 0.04})
            landmarks.append({'x': base_x + 0.01, 'y': y - 0.05, 'z': 0.06})
            landmarks.append({'x': base_x + 0.01, 'y': y - 0.02, 'z': 0.05})
        return self._create_sign_data('Pink', landmarks, 'adjective',
                                      motion='brushing', body_region='lips')
    
    def _create_sign_grey(self) -> Dict:
        """Grey - Open hands weaving through each other"""
        landmarks = []
        x, y = 0.5, 0.50
        landmarks.append({'x': x, 'y': y, 'z': 0.0})  # Wrist
        # Thumb spread wide
        landmarks.append({'x': x - 0.09, 'y': y - 0.02, 'z': 0.0})
        landmarks.append({'x': x - 0.14, 'y': y - 0.04, 'z': 0.0})
        landmarks.append({'x': x - 0.18, 'y': y - 0.06, 'z': 0.0})
        landmarks.append({'x': x - 0.21, 'y': y - 0.08, 'z': 0.0})
        # Fingers spread wide for weaving
        for i, offset in enumerate([-0.05, 0.0, 0.05, 0.10]):
            base_x = x + offset
            for j in range(4):
                landmarks.append({'x': base_x, 'y': y - 0.08 - (j * 0.05), 'z': 0.02 if j % 2 == 0 else -0.02})
        return self._create_sign_data('Grey', landmarks, 'adjective',
                                      motion='passing', two_hands=True)
    
    def _create_sign_colour(self) -> Dict:
        """Colour - Wiggling fingers at chin level"""
        landmarks = []
        x, y = 0.5, 0.38
        landmarks.append({'x': x, 'y': y, 'z': 0.0})  # Wrist
        # Thumb extended
        landmarks.append({'x': x - 0.08, 'y': y - 0.02, 'z': 0.0})
        landmarks.append({'x': x - 0.12, 'y': y - 0.04, 'z': 0.0})
        landmarks.append({'x': x - 0.15, 'y': y - 0.06, 'z': 0.0})
        landmarks.append({'x': x - 0.17, 'y': y - 0.08, 'z': 0.0})
        # Fingers spread and wiggling (staggered z positions)
        for i, offset in enumerate([-0.04, 0.0, 0.04, 0.08]):
            base_x = x + offset
            z_offset = 0.02 if i % 2 == 0 else -0.02
            for j in range(4):
                landmarks.append({'x': base_x, 'y': y - 0.07 - (j * 0.045), 'z': z_offset * (j + 1) / 4})
        return self._create_sign_data('Colour', landmarks, 'noun',
                                      motion='wiggling', body_region='chin')
    
    # ============ DAY SIGNS ============
    
    def _create_sign_day(self, day: str) -> Dict:
        """Day of week signs - Each has unique hand configuration"""
        landmarks = []
        x, y = 0.5, 0.45
        
        # Different configurations for each day
        day_configs = {
            'Monday': {'thumb_angle': 0.0, 'finger_spread': 0.03, 'curl': 0.0},
            'Tuesday': {'thumb_angle': 0.02, 'finger_spread': 0.035, 'curl': 0.01},
            'Wednesday': {'thumb_angle': 0.04, 'finger_spread': 0.04, 'curl': 0.02},
            'Thursday': {'thumb_angle': 0.06, 'finger_spread': 0.032, 'curl': 0.03},
            'Friday': {'thumb_angle': 0.08, 'finger_spread': 0.038, 'curl': 0.0},
            'Saturday': {'thumb_angle': 0.10, 'finger_spread': 0.042, 'curl': 0.01},
            'Sunday': {'thumb_angle': 0.12, 'finger_spread': 0.045, 'curl': 0.02}
        }
        config = day_configs.get(day, day_configs['Monday'])
        
        landmarks.append({'x': x, 'y': y, 'z': 0.0})  # Wrist
        # Thumb with varying angle
        landmarks.append({'x': x - 0.06 - config['thumb_angle'], 'y': y - 0.02, 'z': 0.0})
        landmarks.append({'x': x - 0.10 - config['thumb_angle'], 'y': y - 0.05, 'z': 0.0})
        landmarks.append({'x': x - 0.13 - config['thumb_angle'], 'y': y - 0.08, 'z': 0.0})
        landmarks.append({'x': x - 0.15 - config['thumb_angle'], 'y': y - 0.10, 'z': 0.0})
        # Fingers with varying spread
        spread = config['finger_spread']
        curl = config['curl']
        for i, offset in enumerate([-spread, 0.0, spread, spread * 2]):
            base_x = x + offset
            for j in range(4):
                landmarks.append({
                    'x': base_x + (j * 0.005),
                    'y': y - 0.08 - (j * 0.045),
                    'z': curl * (j / 3)
                })
        return self._create_sign_data(day, landmarks, 'time',
                                      motion='circular')
    
    def _create_sign_today(self) -> Dict:
        """Today - Both hands pointing down emphatically"""
        landmarks = []
        x, y = 0.5, 0.50
        landmarks.append({'x': x, 'y': y, 'z': 0.0})  # Wrist
        # Thumb alongside
        landmarks.append({'x': x - 0.06, 'y': y + 0.02, 'z': 0.01})
        landmarks.append({'x': x - 0.08, 'y': y + 0.05, 'z': 0.01})
        landmarks.append({'x': x - 0.09, 'y': y + 0.08, 'z': 0.01})
        landmarks.append({'x': x - 0.09, 'y': y + 0.10, 'z': 0.01})
        # All fingers pointing downward
        for i, offset in enumerate([-0.03, 0.01, 0.05, 0.09]):
            base_x = x + offset
            for j in range(4):
                landmarks.append({'x': base_x, 'y': y + 0.02 + (j * 0.05), 'z': 0.0})
        return self._create_sign_data('Today', landmarks, 'time',
                                      motion='downward', two_hands=True)
    
    # ============ PRONOUN SIGNS ============
    
    def _create_sign_i(self) -> Dict:
        """I - Index pointing to self/chest"""
        landmarks = []
        x, y = 0.52, 0.48
        landmarks.append({'x': x, 'y': y, 'z': 0.0})  # Wrist
        # Thumb tucked
        landmarks.append({'x': x - 0.04, 'y': y - 0.02, 'z': 0.03})
        landmarks.append({'x': x - 0.05, 'y': y - 0.04, 'z': 0.05})
        landmarks.append({'x': x - 0.04, 'y': y - 0.06, 'z': 0.05})
        landmarks.append({'x': x - 0.02, 'y': y - 0.07, 'z': 0.04})
        # Index pointing toward self (toward center/chest)
        landmarks.append({'x': x - 0.02, 'y': y - 0.08, 'z': 0.0})
        landmarks.append({'x': x - 0.04, 'y': y - 0.12, 'z': 0.06})
        landmarks.append({'x': x - 0.06, 'y': y - 0.15, 'z': 0.10})
        landmarks.append({'x': x - 0.08, 'y': y - 0.17, 'z': 0.12})
        # Other fingers curled
        for i, offset in enumerate([0.02, 0.06, 0.10]):
            base_x = x + offset
            landmarks.append({'x': base_x, 'y': y - 0.06, 'z': 0.0})
            landmarks.append({'x': base_x, 'y': y - 0.08, 'z': 0.04})
            landmarks.append({'x': base_x + 0.01, 'y': y - 0.06, 'z': 0.06})
            landmarks.append({'x': base_x + 0.01, 'y': y - 0.03, 'z': 0.05})
        return self._create_sign_data('I', landmarks, 'pronoun',
                                      body_region='chest')
    
    def _create_sign_you(self) -> Dict:
        """You - Index pointing outward/forward"""
        landmarks = []
        x, y = 0.5, 0.45
        landmarks.append({'x': x, 'y': y, 'z': 0.0})  # Wrist
        # Thumb tucked
        landmarks.append({'x': x - 0.04, 'y': y - 0.02, 'z': 0.03})
        landmarks.append({'x': x - 0.05, 'y': y - 0.04, 'z': 0.05})
        landmarks.append({'x': x - 0.04, 'y': y - 0.06, 'z': 0.05})
        landmarks.append({'x': x - 0.02, 'y': y - 0.07, 'z': 0.04})
        # Index pointing forward (negative z)
        landmarks.append({'x': x - 0.02, 'y': y - 0.08, 'z': 0.0})
        landmarks.append({'x': x - 0.02, 'y': y - 0.12, 'z': -0.04})
        landmarks.append({'x': x - 0.02, 'y': y - 0.16, 'z': -0.08})
        landmarks.append({'x': x - 0.02, 'y': y - 0.20, 'z': -0.12})
        # Other fingers curled
        for i, offset in enumerate([0.02, 0.06, 0.10]):
            base_x = x + offset
            landmarks.append({'x': base_x, 'y': y - 0.06, 'z': 0.0})
            landmarks.append({'x': base_x, 'y': y - 0.08, 'z': 0.04})
            landmarks.append({'x': base_x + 0.01, 'y': y - 0.06, 'z': 0.06})
            landmarks.append({'x': base_x + 0.01, 'y': y - 0.03, 'z': 0.05})
        return self._create_sign_data('You', landmarks, 'pronoun',
                                      motion='pointing_out')
    
    def _create_sign_he(self) -> Dict:
        """He - Index pointing to the right side"""
        landmarks = []
        x, y = 0.55, 0.42
        landmarks.append({'x': x, 'y': y, 'z': 0.0})  # Wrist
        # Thumb tucked
        landmarks.append({'x': x - 0.04, 'y': y - 0.02, 'z': 0.03})
        landmarks.append({'x': x - 0.05, 'y': y - 0.04, 'z': 0.05})
        landmarks.append({'x': x - 0.04, 'y': y - 0.06, 'z': 0.05})
        landmarks.append({'x': x - 0.02, 'y': y - 0.07, 'z': 0.04})
        # Index pointing to the right
        landmarks.append({'x': x - 0.02, 'y': y - 0.08, 'z': 0.0})
        landmarks.append({'x': x + 0.04, 'y': y - 0.09, 'z': 0.0})
        landmarks.append({'x': x + 0.10, 'y': y - 0.09, 'z': 0.0})
        landmarks.append({'x': x + 0.16, 'y': y - 0.09, 'z': 0.0})
        # Other fingers curled
        for i, offset in enumerate([0.02, 0.06, 0.10]):
            base_x = x + offset
            landmarks.append({'x': base_x, 'y': y - 0.06, 'z': 0.0})
            landmarks.append({'x': base_x, 'y': y - 0.08, 'z': 0.04})
            landmarks.append({'x': base_x + 0.01, 'y': y - 0.06, 'z': 0.06})
            landmarks.append({'x': base_x + 0.01, 'y': y - 0.03, 'z': 0.05})
        return self._create_sign_data('He', landmarks, 'pronoun',
                                      motion='pointing_side')
    
    def _create_sign_she(self) -> Dict:
        """She - Index pointing to the left side"""
        landmarks = []
        x, y = 0.45, 0.42
        landmarks.append({'x': x, 'y': y, 'z': 0.0})  # Wrist
        # Thumb tucked
        landmarks.append({'x': x - 0.04, 'y': y - 0.02, 'z': 0.03})
        landmarks.append({'x': x - 0.05, 'y': y - 0.04, 'z': 0.05})
        landmarks.append({'x': x - 0.04, 'y': y - 0.06, 'z': 0.05})
        landmarks.append({'x': x - 0.02, 'y': y - 0.07, 'z': 0.04})
        # Index pointing to the left
        landmarks.append({'x': x - 0.02, 'y': y - 0.08, 'z': 0.0})
        landmarks.append({'x': x - 0.08, 'y': y - 0.09, 'z': 0.0})
        landmarks.append({'x': x - 0.14, 'y': y - 0.09, 'z': 0.0})
        landmarks.append({'x': x - 0.20, 'y': y - 0.09, 'z': 0.0})
        # Other fingers curled
        for i, offset in enumerate([0.02, 0.06, 0.10]):
            base_x = x + offset
            landmarks.append({'x': base_x, 'y': y - 0.06, 'z': 0.0})
            landmarks.append({'x': base_x, 'y': y - 0.08, 'z': 0.04})
            landmarks.append({'x': base_x + 0.01, 'y': y - 0.06, 'z': 0.06})
            landmarks.append({'x': base_x + 0.01, 'y': y - 0.03, 'z': 0.05})
        return self._create_sign_data('She', landmarks, 'pronoun',
                                      motion='pointing_side')
    
    def _create_sign_it(self) -> Dict:
        """It - Index pointing downward"""
        landmarks = []
        x, y = 0.5, 0.48
        landmarks.append({'x': x, 'y': y, 'z': 0.0})  # Wrist
        # Thumb tucked
        landmarks.append({'x': x - 0.04, 'y': y - 0.02, 'z': 0.03})
        landmarks.append({'x': x - 0.05, 'y': y - 0.04, 'z': 0.05})
        landmarks.append({'x': x - 0.04, 'y': y - 0.06, 'z': 0.05})
        landmarks.append({'x': x - 0.02, 'y': y - 0.07, 'z': 0.04})
        # Index pointing downward
        landmarks.append({'x': x - 0.02, 'y': y - 0.06, 'z': 0.0})
        landmarks.append({'x': x - 0.02, 'y': y + 0.0, 'z': 0.0})
        landmarks.append({'x': x - 0.02, 'y': y + 0.06, 'z': 0.0})
        landmarks.append({'x': x - 0.02, 'y': y + 0.12, 'z': 0.0})
        # Other fingers curled
        for i, offset in enumerate([0.02, 0.06, 0.10]):
            base_x = x + offset
            landmarks.append({'x': base_x, 'y': y - 0.06, 'z': 0.0})
            landmarks.append({'x': base_x, 'y': y - 0.08, 'z': 0.04})
            landmarks.append({'x': base_x + 0.01, 'y': y - 0.06, 'z': 0.06})
            landmarks.append({'x': base_x + 0.01, 'y': y - 0.03, 'z': 0.05})
        return self._create_sign_data('It', landmarks, 'pronoun',
                                      motion='pointing_down')
    
    # ============ OTHER SIGNS ============
    
    def _create_sign_blind(self) -> Dict:
        """Blind - V fingers (index and middle) covering eyes"""
        landmarks = []
        x, y = 0.5, 0.26
        landmarks.append({'x': x, 'y': y, 'z': 0.0})  # Wrist
        # Thumb curled
        landmarks.append({'x': x - 0.04, 'y': y - 0.02, 'z': 0.03})
        landmarks.append({'x': x - 0.05, 'y': y - 0.04, 'z': 0.05})
        landmarks.append({'x': x - 0.04, 'y': y - 0.06, 'z': 0.05})
        landmarks.append({'x': x - 0.02, 'y': y - 0.07, 'z': 0.04})
        # Index and middle forming V over eyes
        landmarks.append({'x': x - 0.04, 'y': y - 0.08, 'z': 0.0})
        landmarks.append({'x': x - 0.06, 'y': y - 0.14, 'z': 0.02})
        landmarks.append({'x': x - 0.08, 'y': y - 0.18, 'z': 0.03})
        landmarks.append({'x': x - 0.10, 'y': y - 0.21, 'z': 0.03})
        landmarks.append({'x': x + 0.0, 'y': y - 0.08, 'z': 0.0})
        landmarks.append({'x': x + 0.02, 'y': y - 0.14, 'z': 0.02})
        landmarks.append({'x': x + 0.04, 'y': y - 0.18, 'z': 0.03})
        landmarks.append({'x': x + 0.06, 'y': y - 0.21, 'z': 0.03})
        # Ring and pinky curled
        for i, offset in enumerate([0.04, 0.08]):
            base_x = x + offset
            landmarks.append({'x': base_x, 'y': y - 0.06, 'z': 0.0})
            landmarks.append({'x': base_x, 'y': y - 0.08, 'z': 0.04})
            landmarks.append({'x': base_x + 0.01, 'y': y - 0.06, 'z': 0.06})
            landmarks.append({'x': base_x + 0.01, 'y': y - 0.03, 'z': 0.05})
        return self._create_sign_data('Blind', landmarks, 'adjective',
                                      facial='neutral', body_region='eyes')
    
    def _create_sign_deaf(self) -> Dict:
        """Deaf - Index touching ear then closing to fist"""
        landmarks = []
        x, y = 0.62, 0.28
        landmarks.append({'x': x, 'y': y, 'z': 0.0})  # Wrist
        # Thumb along side
        landmarks.append({'x': x - 0.04, 'y': y - 0.02, 'z': 0.02})
        landmarks.append({'x': x - 0.06, 'y': y - 0.04, 'z': 0.03})
        landmarks.append({'x': x - 0.07, 'y': y - 0.06, 'z': 0.03})
        landmarks.append({'x': x - 0.07, 'y': y - 0.08, 'z': 0.03})
        # Index pointing at ear
        landmarks.append({'x': x - 0.02, 'y': y - 0.08, 'z': 0.0})
        landmarks.append({'x': x - 0.02, 'y': y - 0.13, 'z': 0.0})
        landmarks.append({'x': x - 0.02, 'y': y - 0.17, 'z': 0.0})
        landmarks.append({'x': x - 0.02, 'y': y - 0.20, 'z': 0.0})
        # Other fingers slightly curled
        for i, offset in enumerate([0.02, 0.06, 0.10]):
            base_x = x + offset
            landmarks.append({'x': base_x, 'y': y - 0.07, 'z': 0.0})
            landmarks.append({'x': base_x, 'y': y - 0.10, 'z': 0.02})
            landmarks.append({'x': base_x + 0.01, 'y': y - 0.09, 'z': 0.04})
            landmarks.append({'x': base_x + 0.01, 'y': y - 0.06, 'z': 0.03})
        return self._create_sign_data('Deaf', landmarks, 'adjective',
                                      motion='touching', body_region='ear')
    
    def _create_sign_dream(self) -> Dict:
        """Dream - Index finger spiraling away from forehead"""
        landmarks_start = []
        landmarks_end = []
        x, y = 0.52, 0.25
        # Start position - finger at forehead
        landmarks_start.append({'x': x, 'y': y, 'z': 0.0})
        landmarks_start.append({'x': x - 0.04, 'y': y - 0.02, 'z': 0.03})
        landmarks_start.append({'x': x - 0.05, 'y': y - 0.04, 'z': 0.05})
        landmarks_start.append({'x': x - 0.04, 'y': y - 0.06, 'z': 0.05})
        landmarks_start.append({'x': x - 0.02, 'y': y - 0.07, 'z': 0.04})
        # Index extended
        landmarks_start.append({'x': x - 0.02, 'y': y - 0.08, 'z': 0.0})
        landmarks_start.append({'x': x - 0.02, 'y': y - 0.13, 'z': 0.0})
        landmarks_start.append({'x': x - 0.02, 'y': y - 0.17, 'z': 0.0})
        landmarks_start.append({'x': x - 0.02, 'y': y - 0.20, 'z': 0.0})
        for i, offset in enumerate([0.02, 0.06, 0.10]):
            base_x = x + offset
            landmarks_start.append({'x': base_x, 'y': y - 0.06, 'z': 0.0})
            landmarks_start.append({'x': base_x, 'y': y - 0.08, 'z': 0.04})
            landmarks_start.append({'x': base_x + 0.01, 'y': y - 0.06, 'z': 0.06})
            landmarks_start.append({'x': base_x + 0.01, 'y': y - 0.03, 'z': 0.05})
        
        # End position - finger moved away and up (dream floating away)
        x2, y2 = x + 0.12, y - 0.08
        landmarks_end.append({'x': x2, 'y': y2, 'z': 0.0})
        landmarks_end.append({'x': x2 - 0.04, 'y': y2 - 0.02, 'z': 0.03})
        landmarks_end.append({'x': x2 - 0.05, 'y': y2 - 0.04, 'z': 0.05})
        landmarks_end.append({'x': x2 - 0.04, 'y': y2 - 0.06, 'z': 0.05})
        landmarks_end.append({'x': x2 - 0.02, 'y': y2 - 0.07, 'z': 0.04})
        landmarks_end.append({'x': x2 - 0.02, 'y': y2 - 0.08, 'z': 0.0})
        landmarks_end.append({'x': x2 - 0.02, 'y': y2 - 0.13, 'z': 0.0})
        landmarks_end.append({'x': x2 - 0.02, 'y': y2 - 0.17, 'z': 0.0})
        landmarks_end.append({'x': x2 - 0.02, 'y': y2 - 0.20, 'z': 0.0})
        for i, offset in enumerate([0.02, 0.06, 0.10]):
            base_x = x2 + offset
            landmarks_end.append({'x': base_x, 'y': y2 - 0.06, 'z': 0.0})
            landmarks_end.append({'x': base_x, 'y': y2 - 0.08, 'z': 0.04})
            landmarks_end.append({'x': base_x + 0.01, 'y': y2 - 0.06, 'z': 0.06})
            landmarks_end.append({'x': base_x + 0.01, 'y': y2 - 0.03, 'z': 0.05})
        return self._create_animated_sign('Dream', landmarks_start, landmarks_end,
                                          motion='rising', facial='calm',
                                          body_region='forehead')
    
    def _create_sign_loud(self) -> Dict:
        """Loud - Hands at ears expanding outward"""
        landmarks = []
        x, y = 0.58, 0.28
        landmarks.append({'x': x, 'y': y, 'z': 0.0})  # Wrist
        # Thumb extended
        landmarks.append({'x': x - 0.08, 'y': y - 0.02, 'z': 0.0})
        landmarks.append({'x': x - 0.12, 'y': y - 0.04, 'z': 0.0})
        landmarks.append({'x': x - 0.15, 'y': y - 0.06, 'z': 0.0})
        landmarks.append({'x': x - 0.17, 'y': y - 0.08, 'z': 0.0})
        # Fingers spread wide (explosion/loud effect)
        for i, offset in enumerate([-0.05, 0.0, 0.05, 0.10]):
            base_x = x + offset
            angle = (i - 1.5) * 0.05
            for j in range(4):
                landmarks.append({
                    'x': base_x + (j * angle),
                    'y': y - 0.08 - (j * 0.05),
                    'z': 0.0
                })
        return self._create_sign_data('Loud', landmarks, 'adjective',
                                      motion='expanding', body_region='ears',
                                      two_hands=True)
    
    def _create_sign_quiet(self) -> Dict:
        """Quiet - Index finger on lips (shushing gesture)"""
        landmarks = []
        x, y = 0.5, 0.32
        landmarks.append({'x': x, 'y': y, 'z': 0.0})  # Wrist
        # Thumb alongside
        landmarks.append({'x': x - 0.05, 'y': y - 0.02, 'z': 0.03})
        landmarks.append({'x': x - 0.07, 'y': y - 0.04, 'z': 0.05})
        landmarks.append({'x': x - 0.08, 'y': y - 0.06, 'z': 0.06})
        landmarks.append({'x': x - 0.08, 'y': y - 0.08, 'z': 0.06})
        # Index extended vertically (at lips)
        landmarks.append({'x': x - 0.02, 'y': y - 0.06, 'z': 0.0})
        landmarks.append({'x': x - 0.02, 'y': y - 0.11, 'z': 0.0})
        landmarks.append({'x': x - 0.02, 'y': y - 0.15, 'z': 0.0})
        landmarks.append({'x': x - 0.02, 'y': y - 0.18, 'z': 0.0})
        # Other fingers tightly curled
        for i, offset in enumerate([0.02, 0.06, 0.10]):
            base_x = x + offset
            landmarks.append({'x': base_x, 'y': y - 0.05, 'z': 0.0})
            landmarks.append({'x': base_x, 'y': y - 0.07, 'z': 0.05})
            landmarks.append({'x': base_x + 0.02, 'y': y - 0.05, 'z': 0.07})
            landmarks.append({'x': base_x + 0.02, 'y': y - 0.02, 'z': 0.06})
        return self._create_sign_data('Quiet', landmarks, 'adjective',
                                      facial='calm', motion='downward',
                                      body_region='lips')
    
    # ============ HELPER METHODS ============
    
    def _create_sign_data(self, name: str, landmarks: List[Dict], 
                          sign_type: str = 'word', facial: str = 'neutral',
                          motion: str = 'static', body_region: str = 'neutral',
                          two_hands: bool = False) -> Dict:
        """Create sign data structure with single keyframe"""
        return {
            'name': name,
            'type': sign_type,
            'facial_expression': facial,
            'motion_type': motion,
            'body_region': body_region,
            'two_hands': two_hands,
            'keyframes': [
                {
                    'frame': 0,
                    'right_hand': landmarks,
                    'left_hand': landmarks if two_hands else None
                }
            ]
        }
    
    def _create_animated_sign(self, name: str, start_hand: List[Dict], 
                              end_hand: List[Dict], motion: str = 'dynamic',
                              facial: str = 'neutral', body_region: str = 'neutral',
                              two_hands: bool = False) -> Dict:
        """Create sign with animation between two keyframes"""
        return {
            'name': name,
            'type': 'animated',
            'facial_expression': facial,
            'motion_type': motion,
            'body_region': body_region,
            'two_hands': two_hands,
            'keyframes': [
                {
                    'frame': 0,
                    'right_hand': start_hand,
                    'left_hand': start_hand if two_hands else None
                },
                {
                    'frame': 1,
                    'right_hand': end_hand,
                    'left_hand': end_hand if two_hands else None
                }
            ]
        }
    
    def get_sign(self, sign_name: str) -> Dict:
        """Get sign data by name"""
        return self.signs.get(sign_name, self._get_default_sign())
    
    def _get_default_sign(self) -> Dict:
        """Return default sign for unknown words"""
        return self._create_sign_data('Unknown', self._create_base_hand(), 
                                      'default', facial='question')
    
    def get_keypoints(self, sign_name: str) -> List[Dict]:
        """Get keypoint coordinates for a sign"""
        sign = self.get_sign(sign_name)
        if sign and sign['keyframes']:
            return sign['keyframes'][0]['right_hand']
        return self._create_base_hand()
    
    def get_all_signs(self) -> List[str]:
        """Return all available sign names"""
        return list(self.signs.keys())
    
    def interpolate_keyframes(self, sign_name: str, progress: float) -> Dict:
        """Interpolate between keyframes for animation"""
        sign = self.get_sign(sign_name)
        keyframes = sign.get('keyframes', [])
        
        if len(keyframes) < 2:
            # Static sign, return first keyframe
            return keyframes[0] if keyframes else {'right_hand': self._create_base_hand()}
        
        # Interpolate between start and end
        start = keyframes[0]
        end = keyframes[1]
        
        interpolated = {
            'frame': progress,
            'right_hand': self._interpolate_landmarks(
                start['right_hand'], end['right_hand'], progress
            )
        }
        
        if start.get('left_hand') and end.get('left_hand'):
            interpolated['left_hand'] = self._interpolate_landmarks(
                start['left_hand'], end['left_hand'], progress
            )
        
        return interpolated
    
    def _interpolate_landmarks(self, start: List[Dict], end: List[Dict], 
                               progress: float) -> List[Dict]:
        """Interpolate between two sets of landmarks"""
        result = []
        for i in range(min(len(start), len(end))):
            result.append({
                'x': start[i]['x'] + (end[i]['x'] - start[i]['x']) * progress,
                'y': start[i]['y'] + (end[i]['y'] - start[i]['y']) * progress,
                'z': start[i]['z'] + (end[i]['z'] - start[i]['z']) * progress
            })
        return result


# Module-level instance
isl_database = ISLDatabase()
