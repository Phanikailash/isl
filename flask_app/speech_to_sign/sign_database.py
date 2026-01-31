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
        """Number 6 - Thumb touches pinky"""
        landmarks = self._create_base_hand()
        landmarks[4] = {'x': landmarks[20]['x'], 'y': landmarks[20]['y'], 'z': 0.02}
        return self._create_sign_data('6', landmarks, 'number')
    
    def _create_sign_7(self) -> Dict:
        """Number 7 - Thumb touches ring finger"""
        landmarks = self._create_base_hand()
        landmarks[4] = {'x': landmarks[16]['x'], 'y': landmarks[16]['y'], 'z': 0.02}
        return self._create_sign_data('7', landmarks, 'number')
    
    def _create_sign_8(self) -> Dict:
        """Number 8 - Thumb touches middle finger"""
        landmarks = self._create_base_hand()
        landmarks[4] = {'x': landmarks[12]['x'], 'y': landmarks[12]['y'], 'z': 0.02}
        return self._create_sign_data('8', landmarks, 'number')
    
    def _create_sign_9(self) -> Dict:
        """Number 9 - Thumb touches index finger"""
        landmarks = self._create_base_hand()
        landmarks[4] = {'x': landmarks[8]['x'], 'y': landmarks[8]['y'], 'z': 0.02}
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
        """Hello - Open hand wave near forehead"""
        start_hand = self._create_base_hand(0.6, 0.3)
        end_hand = self._create_base_hand(0.7, 0.3)
        return self._create_animated_sign('Hello', start_hand, end_hand, 
                                          motion='wave', facial='smile', 
                                          body_region='head')
    
    def _create_sign_thank_you(self) -> Dict:
        """Thank you - Flat hand from chin outward"""
        start_hand = self._create_base_hand(0.5, 0.35)
        end_hand = self._create_base_hand(0.5, 0.5)
        return self._create_animated_sign('Thank you', start_hand, end_hand,
                                          motion='outward', facial='smile',
                                          body_region='chin')
    
    def _create_sign_good_morning(self) -> Dict:
        """Good Morning - Rising sun motion"""
        start_hand = self._create_base_hand(0.4, 0.6)
        end_hand = self._create_base_hand(0.5, 0.3)
        return self._create_animated_sign('Good Morning', start_hand, end_hand,
                                          motion='rising', facial='smile',
                                          body_region='chest')
    
    def _create_sign_good_night(self) -> Dict:
        """Good night - Hands together, head tilt"""
        landmarks = self._create_base_hand(0.5, 0.35)
        return self._create_sign_data('Good night', landmarks, 'phrase',
                                      facial='calm', motion='closing',
                                      two_hands=True)
    
    def _create_sign_how_are_you(self) -> Dict:
        """How are you - Question gesture"""
        start_hand = self._create_base_hand(0.45, 0.4)
        end_hand = self._create_base_hand(0.55, 0.4)
        return self._create_animated_sign('How are you', start_hand, end_hand,
                                          motion='questioning', facial='question',
                                          body_region='chest')
    
    def _create_sign_happy(self) -> Dict:
        """Happy - Circular motion on chest"""
        landmarks = self._create_base_hand(0.5, 0.45)
        return self._create_sign_data('Happy', landmarks, 'emotion',
                                      facial='smile', motion='circular',
                                      body_region='chest')
    
    def _create_sign_sad(self) -> Dict:
        """Sad - Hands moving down from face"""
        start_hand = self._create_base_hand(0.5, 0.3)
        end_hand = self._create_base_hand(0.5, 0.5)
        return self._create_animated_sign('Sad', start_hand, end_hand,
                                          motion='downward', facial='sad',
                                          body_region='face')
    
    def _create_sign_beautiful(self) -> Dict:
        """Beautiful - Circle around face"""
        landmarks = self._create_base_hand(0.5, 0.3)
        return self._create_sign_data('Beautiful', landmarks, 'adjective',
                                      facial='smile', motion='circular',
                                      body_region='face')
    
    def _create_sign_ugly(self) -> Dict:
        """Ugly - Bent fingers across face"""
        landmarks = self._create_fist(0.5, 0.35)
        return self._create_sign_data('Ugly', landmarks, 'adjective',
                                      facial='frown', motion='across',
                                      body_region='face')
    
    def _create_sign_alright(self) -> Dict:
        """Alright - OK gesture"""
        landmarks = self._create_sign_0()['keyframes'][0]['right_hand']
        return self._create_sign_data('Alright', landmarks, 'expression',
                                      facial='neutral', motion='static')
    
    def _create_sign_pleased(self) -> Dict:
        """Pleased - Flat hand on chest, circular motion"""
        landmarks = self._create_base_hand(0.5, 0.45)
        return self._create_sign_data('Pleased', landmarks, 'emotion',
                                      facial='smile', motion='circular',
                                      body_region='chest')
    
    # ============ ANIMAL SIGNS ============
    
    def _create_sign_animal(self) -> Dict:
        """Animal - Fingertips on chest, rocking motion"""
        landmarks = self._create_fist(0.5, 0.45)
        landmarks[8] = landmarks[12] = landmarks[16] = landmarks[20] = {'x': 0.5, 'y': 0.45, 'z': 0.02}
        return self._create_sign_data('Animal', landmarks, 'noun',
                                      motion='rocking', body_region='chest')
    
    def _create_sign_bird(self) -> Dict:
        """Bird - Beak motion near mouth"""
        landmarks = self._create_fist(0.5, 0.35)
        # Index and thumb form beak
        landmarks[4] = {'x': 0.48, 'y': 0.32, 'z': 0.0}
        landmarks[8] = {'x': 0.48, 'y': 0.30, 'z': 0.0}
        return self._create_sign_data('Bird', landmarks, 'noun',
                                      motion='opening_closing', body_region='mouth')
    
    def _create_sign_cat(self) -> Dict:
        """Cat - Whiskers motion at cheeks"""
        landmarks = self._create_fist(0.5, 0.35)
        # Pinch for whiskers
        landmarks[4] = {'x': 0.46, 'y': 0.34, 'z': 0.0}
        landmarks[8] = {'x': 0.46, 'y': 0.32, 'z': 0.0}
        return self._create_sign_data('Cat', landmarks, 'noun',
                                      motion='outward', body_region='cheek',
                                      two_hands=True)
    
    def _create_sign_dog(self) -> Dict:
        """Dog - Snap fingers, patting motion"""
        landmarks = self._create_base_hand(0.5, 0.5)
        return self._create_sign_data('Dog', landmarks, 'noun',
                                      motion='patting', body_region='thigh')
    
    def _create_sign_cow(self) -> Dict:
        """Cow - Y hand at temple for horns"""
        landmarks = self._letter_y()
        # Move to temple
        for lm in landmarks:
            lm['y'] -= 0.15
        return self._create_sign_data('Cow', landmarks, 'noun',
                                      motion='twisting', body_region='temple')
    
    def _create_sign_horse(self) -> Dict:
        """Horse - Thumb at temple, fingers flapping"""
        landmarks = self._create_base_hand(0.55, 0.3)
        landmarks[4] = {'x': 0.55, 'y': 0.28, 'z': 0.02}
        return self._create_sign_data('Horse', landmarks, 'noun',
                                      motion='flapping', body_region='temple')
    
    def _create_sign_mouse(self) -> Dict:
        """Mouse - Finger brushing nose"""
        landmarks = self._create_sign_1()['keyframes'][0]['right_hand']
        # Position at nose
        for lm in landmarks:
            lm['y'] -= 0.1
        return self._create_sign_data('Mouse', landmarks, 'noun',
                                      motion='brushing', body_region='nose')
    
    def _create_sign_fish(self) -> Dict:
        """Fish - Flat hand swimming motion"""
        landmarks = self._create_base_hand(0.5, 0.5)
        return self._create_sign_data('Fish', landmarks, 'noun',
                                      motion='swimming', body_region='neutral')
    
    # ============ FAMILY SIGNS ============
    
    def _create_sign_mother(self) -> Dict:
        """Mother - Thumb on chin with open hand"""
        landmarks = self._create_base_hand(0.5, 0.38)
        landmarks[4] = {'x': 0.5, 'y': 0.36, 'z': 0.02}
        return self._create_sign_data('Mother', landmarks, 'noun',
                                      facial='smile', body_region='chin')
    
    def _create_sign_father(self) -> Dict:
        """Father - Thumb on forehead with open hand"""
        landmarks = self._create_base_hand(0.5, 0.28)
        landmarks[4] = {'x': 0.5, 'y': 0.26, 'z': 0.02}
        return self._create_sign_data('Father', landmarks, 'noun',
                                      facial='neutral', body_region='forehead')
    
    def _create_sign_daughter(self) -> Dict:
        """Daughter - Girl + baby motion"""
        landmarks = self._create_base_hand(0.5, 0.4)
        return self._create_sign_data('Daughter', landmarks, 'noun',
                                      motion='cradling', body_region='chin')
    
    def _create_sign_son(self) -> Dict:
        """Son - Boy + baby motion"""
        landmarks = self._create_base_hand(0.5, 0.3)
        return self._create_sign_data('Son', landmarks, 'noun',
                                      motion='cradling', body_region='forehead')
    
    def _create_sign_parent(self) -> Dict:
        """Parent - Combined mother/father"""
        landmarks = self._create_base_hand(0.5, 0.32)
        return self._create_sign_data('Parent', landmarks, 'noun',
                                      motion='alternating', body_region='face',
                                      two_hands=True)
    
    # ============ OBJECT SIGNS ============
    
    def _create_sign_chair(self) -> Dict:
        """Chair - Two fingers sitting on thumb"""
        landmarks = self._create_fist(0.5, 0.5)
        landmarks[8] = {'x': 0.46, 'y': 0.44, 'z': 0.0}
        landmarks[12] = {'x': 0.50, 'y': 0.44, 'z': 0.0}
        landmarks[4] = {'x': 0.48, 'y': 0.50, 'z': 0.0}
        return self._create_sign_data('Chair', landmarks, 'noun',
                                      motion='tapping', two_hands=True)
    
    def _create_sign_table(self) -> Dict:
        """Table - Flat hands forming surface"""
        landmarks = self._create_base_hand(0.5, 0.5)
        return self._create_sign_data('Table', landmarks, 'noun',
                                      motion='patting', two_hands=True)
    
    def _create_sign_bed(self) -> Dict:
        """Bed - Hands together by tilted head"""
        landmarks = self._create_base_hand(0.55, 0.35)
        return self._create_sign_data('Bed', landmarks, 'noun',
                                      facial='calm', motion='resting',
                                      body_region='head')
    
    def _create_sign_bedroom(self) -> Dict:
        """Bedroom - Bed + Room"""
        landmarks = self._create_base_hand(0.5, 0.45)
        return self._create_sign_data('Bedroom', landmarks, 'noun',
                                      motion='box_shape', two_hands=True)
    
    def _create_sign_door(self) -> Dict:
        """Door - Flat hand opening motion"""
        start_hand = self._create_base_hand(0.4, 0.5)
        end_hand = self._create_base_hand(0.6, 0.5)
        return self._create_animated_sign('Door', start_hand, end_hand,
                                          motion='opening')
    
    def _create_sign_window(self) -> Dict:
        """Window - Outline rectangle, then open"""
        landmarks = self._create_base_hand(0.5, 0.4)
        return self._create_sign_data('Window', landmarks, 'noun',
                                      motion='sliding', two_hands=True)
    
    # ============ COLOR SIGNS ============
    
    def _create_sign_black(self) -> Dict:
        """Black - Index across forehead"""
        landmarks = self._create_sign_1()['keyframes'][0]['right_hand']
        for lm in landmarks:
            lm['y'] -= 0.2
        return self._create_sign_data('Black', landmarks, 'adjective',
                                      motion='across', body_region='forehead')
    
    def _create_sign_white(self) -> Dict:
        """White - Open hand from chest outward"""
        start_hand = self._create_base_hand(0.5, 0.45)
        end_hand = self._create_base_hand(0.5, 0.5)
        for lm in end_hand:
            lm['z'] = 0.0
        return self._create_animated_sign('White', start_hand, end_hand,
                                          motion='outward', body_region='chest')
    
    def _create_sign_orange(self) -> Dict:
        """Orange - Squeezing motion near chin"""
        landmarks = self._create_fist(0.5, 0.38)
        return self._create_sign_data('Orange', landmarks, 'adjective',
                                      motion='squeezing', body_region='chin')
    
    def _create_sign_pink(self) -> Dict:
        """Pink - P handshape on lips"""
        landmarks = self._letter_p()
        for lm in landmarks:
            lm['y'] -= 0.1
        return self._create_sign_data('Pink', landmarks, 'adjective',
                                      motion='brushing', body_region='lips')
    
    def _create_sign_grey(self) -> Dict:
        """Grey - Open hands passing through each other"""
        landmarks = self._create_base_hand(0.5, 0.5)
        return self._create_sign_data('Grey', landmarks, 'adjective',
                                      motion='passing', two_hands=True)
    
    def _create_sign_colour(self) -> Dict:
        """Colour - Wiggling fingers at chin"""
        landmarks = self._create_base_hand(0.5, 0.38)
        return self._create_sign_data('Colour', landmarks, 'noun',
                                      motion='wiggling', body_region='chin')
    
    # ============ DAY SIGNS ============
    
    def _create_sign_day(self, day: str) -> Dict:
        """Day of week signs - Letter initialization"""
        letter_map = {
            'Monday': 'M', 'Tuesday': 'T', 'Wednesday': 'W',
            'Thursday': 'H', 'Friday': 'F', 'Saturday': 'S', 'Sunday': 'S'
        }
        letter = letter_map.get(day, 'D')
        landmarks = self._create_letter_sign(letter)['keyframes'][0]['right_hand']
        return self._create_sign_data(day, landmarks, 'time',
                                      motion='circular')
    
    def _create_sign_today(self) -> Dict:
        """Today - Both hands down motion"""
        landmarks = self._create_base_hand(0.5, 0.5)
        return self._create_sign_data('Today', landmarks, 'time',
                                      motion='downward', two_hands=True)
    
    # ============ PRONOUN SIGNS ============
    
    def _create_sign_i(self) -> Dict:
        """I - Point to self (chest)"""
        landmarks = self._create_sign_1()['keyframes'][0]['right_hand']
        # Point toward chest
        landmarks[8]['z'] = 0.05
        return self._create_sign_data('I', landmarks, 'pronoun',
                                      body_region='chest')
    
    def _create_sign_you(self) -> Dict:
        """You - Point outward"""
        landmarks = self._create_sign_1()['keyframes'][0]['right_hand']
        return self._create_sign_data('You', landmarks, 'pronoun',
                                      motion='pointing_out')
    
    def _create_sign_he(self) -> Dict:
        """He - Point to side"""
        landmarks = self._create_sign_1()['keyframes'][0]['right_hand']
        for lm in landmarks:
            lm['x'] += 0.1
        return self._create_sign_data('He', landmarks, 'pronoun',
                                      motion='pointing_side')
    
    def _create_sign_she(self) -> Dict:
        """She - Point to other side"""
        landmarks = self._create_sign_1()['keyframes'][0]['right_hand']
        for lm in landmarks:
            lm['x'] -= 0.1
        return self._create_sign_data('She', landmarks, 'pronoun',
                                      motion='pointing_side')
    
    def _create_sign_it(self) -> Dict:
        """It - Point forward/down"""
        landmarks = self._create_sign_1()['keyframes'][0]['right_hand']
        for lm in landmarks:
            lm['y'] += 0.05
        return self._create_sign_data('It', landmarks, 'pronoun',
                                      motion='pointing_down')
    
    # ============ OTHER SIGNS ============
    
    def _create_sign_blind(self) -> Dict:
        """Blind - V fingers over eyes"""
        landmarks = self._create_sign_2()['keyframes'][0]['right_hand']
        for lm in landmarks:
            lm['y'] -= 0.2
        return self._create_sign_data('Blind', landmarks, 'adjective',
                                      facial='neutral', body_region='eyes')
    
    def _create_sign_deaf(self) -> Dict:
        """Deaf - Point to ear, then close"""
        landmarks = self._create_sign_1()['keyframes'][0]['right_hand']
        for lm in landmarks:
            lm['x'] += 0.1
            lm['y'] -= 0.15
        return self._create_sign_data('Deaf', landmarks, 'adjective',
                                      motion='touching', body_region='ear')
    
    def _create_sign_dream(self) -> Dict:
        """Dream - Finger from forehead moving away"""
        start_hand = self._create_sign_1()['keyframes'][0]['right_hand']
        end_hand = [lm.copy() for lm in start_hand]
        for lm in start_hand:
            lm['y'] -= 0.2
        for lm in end_hand:
            lm['y'] -= 0.1
            lm['x'] += 0.1
        return self._create_animated_sign('Dream', start_hand, end_hand,
                                          motion='rising', facial='calm',
                                          body_region='forehead')
    
    def _create_sign_loud(self) -> Dict:
        """Loud - Hands at ears, moving outward"""
        landmarks = self._create_base_hand(0.55, 0.3)
        return self._create_sign_data('Loud', landmarks, 'adjective',
                                      motion='expanding', body_region='ears',
                                      two_hands=True)
    
    def _create_sign_quiet(self) -> Dict:
        """Quiet - Index on lips, then hands down"""
        landmarks = self._create_sign_1()['keyframes'][0]['right_hand']
        for lm in landmarks:
            lm['y'] -= 0.12
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
