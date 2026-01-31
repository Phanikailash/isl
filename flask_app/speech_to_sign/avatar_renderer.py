import json
import math
from typing import List, Dict, Tuple

class AvatarRenderer:
    def __init__(self):
        # All class_labels from app.py
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
        
        # Avatar configuration
        self.avatar_config = {
            'width': 500,
            'height': 500,
            'background_color': '#f0f0f0',
            'skin_color': '#FFDAB9',
            'hand_color': '#FFDAB9',
            'outline_color': '#2c3e50'
        }
        
        # Initialize all gestures
        self.gestures = self._initialize_all_gestures()
    
    def _initialize_all_gestures(self) -> Dict:
        """Initialize gesture data for all class_labels"""
        gestures = {}
        
        # Numbers 0-9
        gestures['0'] = self._create_number_gesture(0)
        gestures['1'] = self._create_number_gesture(1)
        gestures['2'] = self._create_number_gesture(2)
        gestures['3'] = self._create_number_gesture(3)
        gestures['4'] = self._create_number_gesture(4)
        gestures['5'] = self._create_number_gesture(5)
        gestures['6'] = self._create_number_gesture(6)
        gestures['7'] = self._create_number_gesture(7)
        gestures['8'] = self._create_number_gesture(8)
        gestures['9'] = self._create_number_gesture(9)
        
        # Letters A-Z
        for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            gestures[letter] = self._create_letter_gesture(letter)
        
        # Words and phrases
        gestures['Hello'] = self._create_gesture_hello()
        gestures['Thank you'] = self._create_gesture_thank_you()
        gestures['Good Morning'] = self._create_gesture_good_morning()
        gestures['Good night'] = self._create_gesture_good_night()
        gestures['How are you'] = self._create_gesture_how_are_you()
        gestures['Happy'] = self._create_gesture_happy()
        gestures['Sad'] = self._create_gesture_sad()
        gestures['Beautiful'] = self._create_gesture_beautiful()
        gestures['Ugly'] = self._create_gesture_ugly()
        gestures['Alright'] = self._create_gesture_alright()
        gestures['Pleased'] = self._create_gesture_pleased()
        
        # Animals
        gestures['Animal'] = self._create_gesture_animal()
        gestures['Bird'] = self._create_gesture_bird()
        gestures['Cat'] = self._create_gesture_cat()
        gestures['Dog'] = self._create_gesture_dog()
        gestures['Cow'] = self._create_gesture_cow()
        gestures['Horse'] = self._create_gesture_horse()
        gestures['Mouse'] = self._create_gesture_mouse()
        gestures['Fish'] = self._create_gesture_fish()
        
        # Family
        gestures['Mother'] = self._create_gesture_mother()
        gestures['Father'] = self._create_gesture_father()
        gestures['Daughter'] = self._create_gesture_daughter()
        gestures['Son'] = self._create_gesture_son()
        gestures['Parent'] = self._create_gesture_parent()
        
        # Furniture/Objects
        gestures['Chair'] = self._create_gesture_chair()
        gestures['Table'] = self._create_gesture_table()
        gestures['Bed'] = self._create_gesture_bed()
        gestures['Bedroom'] = self._create_gesture_bedroom()
        gestures['Door'] = self._create_gesture_door()
        gestures['Window'] = self._create_gesture_window()
        
        # Colors
        gestures['Black'] = self._create_gesture_black()
        gestures['White'] = self._create_gesture_white()
        gestures['Orange'] = self._create_gesture_orange()
        gestures['Pink'] = self._create_gesture_pink()
        gestures['Grey'] = self._create_gesture_grey()
        gestures['Colour'] = self._create_gesture_colour()
        
        # Days
        gestures['Monday'] = self._create_gesture_day('M')
        gestures['Tuesday'] = self._create_gesture_day('T')
        gestures['Wednesday'] = self._create_gesture_day('W')
        gestures['Thursday'] = self._create_gesture_day('Th')
        gestures['Friday'] = self._create_gesture_day('F')
        gestures['Saturday'] = self._create_gesture_day('S')
        gestures['Sunday'] = self._create_gesture_day('Su')
        gestures['Today'] = self._create_gesture_today()
        
        # Pronouns
        gestures['I'] = self._create_gesture_i()
        gestures['You'] = self._create_gesture_you()
        gestures['He'] = self._create_gesture_he()
        gestures['She'] = self._create_gesture_she()
        gestures['It'] = self._create_gesture_it()
        
        # Other words
        gestures['Blind'] = self._create_gesture_blind()
        gestures['Deaf'] = self._create_gesture_deaf()
        gestures['Dream'] = self._create_gesture_dream()
        gestures['Loud'] = self._create_gesture_loud()
        gestures['Quiet'] = self._create_gesture_quiet()
        
        # Default gesture
        gestures['default'] = self._create_gesture_default()
        
        return gestures
    
    def render_animation_sequence(self, animations: List[Dict]) -> List[Dict]:
        """Render animation sequence for avatar"""
        rendered_frames = []
        
        for animation in animations:
            sign = animation['sign']
            duration = animation.get('duration', 1500)
            
            # Get gesture for this sign
            gesture = self.gestures.get(sign, self.gestures['default'])
            
            # Generate frames for this animation
            frames = self._generate_animation_frames(sign, gesture, duration)
            rendered_frames.extend(frames)
        
        return rendered_frames
    
    def _generate_animation_frames(self, sign: str, gesture: Dict, duration: int) -> List[Dict]:
        """Generate animation frames for a gesture"""
        frames = []
        fps = 30
        total_frames = max(int(duration / 1000 * fps), 10)
        
        for frame_num in range(total_frames):
            progress = frame_num / total_frames
            
            # Use easing function for smooth animation
            eased_progress = self._ease_in_out(progress)
            
            # Interpolate between start and end positions
            frame_data = {
                'frame': frame_num,
                'total_frames': total_frames,
                'sign': sign,
                'timestamp': frame_num * 1000 / fps,
                'progress': eased_progress,
                'left_hand': self._interpolate_hand(
                    gesture['left_hand_start'], 
                    gesture['left_hand_end'], 
                    eased_progress
                ),
                'right_hand': self._interpolate_hand(
                    gesture['right_hand_start'], 
                    gesture['right_hand_end'], 
                    eased_progress
                ),
                'facial_expression': gesture['facial_expression'],
                'body_pose': gesture.get('body_pose', 'standing'),
                'motion_type': gesture.get('motion_type', 'static'),
                'hand_movement': gesture.get('hand_movement', 'none')
            }
            frames.append(frame_data)
        
        return frames
    
    def _ease_in_out(self, t: float) -> float:
        """Smooth easing function"""
        if t < 0.5:
            return 2 * t * t
        else:
            return 1 - pow(-2 * t + 2, 2) / 2
    
    def _interpolate_hand(self, start: Dict, end: Dict, progress: float) -> Dict:
        """Interpolate hand position between start and end"""
        interpolated = {}
        
        for key in start:
            if isinstance(start[key], list):
                interpolated[key] = [
                    start[key][i] + (end[key][i] - start[key][i]) * progress
                    for i in range(len(start[key]))
                ]
            elif isinstance(start[key], dict):
                interpolated[key] = self._interpolate_hand(start[key], end[key], progress)
            elif isinstance(start[key], (int, float)):
                interpolated[key] = start[key] + (end[key] - start[key]) * progress
            else:
                interpolated[key] = end[key] if progress > 0.5 else start[key]
        
        return interpolated
    
    # ==================== NUMBER GESTURES ====================
    def _create_number_gesture(self, num: int) -> Dict:
        """Create gesture for numbers 0-9"""
        # Finger configurations for each number
        finger_configs = {
            0: {'thumb': 0, 'index': 0, 'middle': 0, 'ring': 0, 'pinky': 0},
            1: {'thumb': 0, 'index': 1, 'middle': 0, 'ring': 0, 'pinky': 0},
            2: {'thumb': 0, 'index': 1, 'middle': 1, 'ring': 0, 'pinky': 0},
            3: {'thumb': 1, 'index': 1, 'middle': 1, 'ring': 0, 'pinky': 0},
            4: {'thumb': 0, 'index': 1, 'middle': 1, 'ring': 1, 'pinky': 1},
            5: {'thumb': 1, 'index': 1, 'middle': 1, 'ring': 1, 'pinky': 1},
            6: {'thumb': 1, 'index': 0, 'middle': 0, 'ring': 0, 'pinky': 1},
            7: {'thumb': 1, 'index': 1, 'middle': 0, 'ring': 0, 'pinky': 0},
            8: {'thumb': 1, 'index': 1, 'middle': 1, 'ring': 0, 'pinky': 0},
            9: {'thumb': 0, 'index': 1, 'middle': 0, 'ring': 0, 'pinky': 0},
        }
        
        config = finger_configs.get(num, finger_configs[0])
        
        return {
            'left_hand_start': self._create_hand_at_rest(),
            'left_hand_end': self._create_hand_at_rest(),
            'right_hand_start': self._create_hand_at_rest(),
            'right_hand_end': self._create_hand_position(
                x=250, y=200,
                rotation=0,
                fingers=config
            ),
            'facial_expression': 'neutral',
            'body_pose': 'standing',
            'motion_type': 'static'
        }
    
    # ==================== LETTER GESTURES ====================
    def _create_letter_gesture(self, letter: str) -> Dict:
        """Create gesture for letters A-Z"""
        letter_configs = {
            'A': {'thumb': 0.5, 'index': 0, 'middle': 0, 'ring': 0, 'pinky': 0, 'rotation': 0},
            'B': {'thumb': 0, 'index': 1, 'middle': 1, 'ring': 1, 'pinky': 1, 'rotation': 0},
            'C': {'thumb': 0.5, 'index': 0.7, 'middle': 0.7, 'ring': 0.7, 'pinky': 0.7, 'rotation': 90},
            'D': {'thumb': 0.5, 'index': 1, 'middle': 0.3, 'ring': 0.3, 'pinky': 0.3, 'rotation': 0},
            'E': {'thumb': 0.3, 'index': 0.3, 'middle': 0.3, 'ring': 0.3, 'pinky': 0.3, 'rotation': 0},
            'F': {'thumb': 0.5, 'index': 0.5, 'middle': 1, 'ring': 1, 'pinky': 1, 'rotation': 0},
            'G': {'thumb': 0.5, 'index': 0.8, 'middle': 0, 'ring': 0, 'pinky': 0, 'rotation': 90},
            'H': {'thumb': 0, 'index': 0.8, 'middle': 0.8, 'ring': 0, 'pinky': 0, 'rotation': 90},
            'I': {'thumb': 0, 'index': 0, 'middle': 0, 'ring': 0, 'pinky': 1, 'rotation': 0},
            'J': {'thumb': 0, 'index': 0, 'middle': 0, 'ring': 0, 'pinky': 1, 'rotation': 45},
            'K': {'thumb': 0.5, 'index': 1, 'middle': 1, 'ring': 0, 'pinky': 0, 'rotation': 0},
            'L': {'thumb': 1, 'index': 1, 'middle': 0, 'ring': 0, 'pinky': 0, 'rotation': 0},
            'M': {'thumb': 0, 'index': 0.3, 'middle': 0.3, 'ring': 0.3, 'pinky': 0, 'rotation': 0},
            'N': {'thumb': 0, 'index': 0.3, 'middle': 0.3, 'ring': 0, 'pinky': 0, 'rotation': 0},
            'O': {'thumb': 0.5, 'index': 0.5, 'middle': 0.5, 'ring': 0.5, 'pinky': 0.5, 'rotation': 0},
            'P': {'thumb': 0.5, 'index': 1, 'middle': 0.8, 'ring': 0, 'pinky': 0, 'rotation': -45},
            'Q': {'thumb': 0.8, 'index': 0.8, 'middle': 0, 'ring': 0, 'pinky': 0, 'rotation': -90},
            'R': {'thumb': 0, 'index': 1, 'middle': 1, 'ring': 0, 'pinky': 0, 'rotation': 0},
            'S': {'thumb': 0.5, 'index': 0, 'middle': 0, 'ring': 0, 'pinky': 0, 'rotation': 0},
            'T': {'thumb': 0.5, 'index': 0.3, 'middle': 0, 'ring': 0, 'pinky': 0, 'rotation': 0},
            'U': {'thumb': 0, 'index': 1, 'middle': 1, 'ring': 0, 'pinky': 0, 'rotation': 0},
            'V': {'thumb': 0, 'index': 1, 'middle': 1, 'ring': 0, 'pinky': 0, 'rotation': 0},
            'W': {'thumb': 0, 'index': 1, 'middle': 1, 'ring': 1, 'pinky': 0, 'rotation': 0},
            'X': {'thumb': 0, 'index': 0.7, 'middle': 0, 'ring': 0, 'pinky': 0, 'rotation': 0},
            'Y': {'thumb': 1, 'index': 0, 'middle': 0, 'ring': 0, 'pinky': 1, 'rotation': 0},
            'Z': {'thumb': 0, 'index': 1, 'middle': 0, 'ring': 0, 'pinky': 0, 'rotation': 0},
        }
        
        config = letter_configs.get(letter, letter_configs['A'])
        
        return {
            'left_hand_start': self._create_hand_at_rest(),
            'left_hand_end': self._create_hand_at_rest(),
            'right_hand_start': self._create_hand_at_rest(),
            'right_hand_end': self._create_hand_position(
                x=250, y=180,
                rotation=config.get('rotation', 0),
                fingers={
                    'thumb': config['thumb'],
                    'index': config['index'],
                    'middle': config['middle'],
                    'ring': config['ring'],
                    'pinky': config['pinky']
                }
            ),
            'facial_expression': 'neutral',
            'body_pose': 'standing',
            'motion_type': 'static'
        }
    
    # ==================== WORD GESTURES ====================
    def _create_gesture_hello(self) -> Dict:
        """Wave gesture for Hello"""
        return {
            'left_hand_start': self._create_hand_at_rest(),
            'left_hand_end': self._create_hand_at_rest(),
            'right_hand_start': self._create_hand_position(x=280, y=150, rotation=-20,
                fingers={'thumb': 1, 'index': 1, 'middle': 1, 'ring': 1, 'pinky': 1}),
            'right_hand_end': self._create_hand_position(x=320, y=130, rotation=20,
                fingers={'thumb': 1, 'index': 1, 'middle': 1, 'ring': 1, 'pinky': 1}),
            'facial_expression': 'smile',
            'body_pose': 'standing',
            'motion_type': 'wave',
            'hand_movement': 'wave'
        }
    
    def _create_gesture_thank_you(self) -> Dict:
        """Hand from chin moving forward for Thank you"""
        return {
            'left_hand_start': self._create_hand_at_rest(),
            'left_hand_end': self._create_hand_at_rest(),
            'right_hand_start': self._create_hand_position(x=250, y=170, rotation=0,
                fingers={'thumb': 1, 'index': 1, 'middle': 1, 'ring': 1, 'pinky': 1}),
            'right_hand_end': self._create_hand_position(x=280, y=220, rotation=-30,
                fingers={'thumb': 1, 'index': 1, 'middle': 1, 'ring': 1, 'pinky': 1}),
            'facial_expression': 'smile',
            'body_pose': 'slight_bow',
            'motion_type': 'forward_arc'
        }
    
    def _create_gesture_good_morning(self) -> Dict:
        """Rising sun motion for Good Morning"""
        return {
            'left_hand_start': self._create_hand_position(x=180, y=300, rotation=0,
                fingers={'thumb': 1, 'index': 1, 'middle': 1, 'ring': 1, 'pinky': 1}),
            'left_hand_end': self._create_hand_position(x=180, y=180, rotation=0,
                fingers={'thumb': 1, 'index': 1, 'middle': 1, 'ring': 1, 'pinky': 1}),
            'right_hand_start': self._create_hand_position(x=320, y=300, rotation=0,
                fingers={'thumb': 1, 'index': 1, 'middle': 1, 'ring': 1, 'pinky': 1}),
            'right_hand_end': self._create_hand_position(x=320, y=180, rotation=0,
                fingers={'thumb': 1, 'index': 1, 'middle': 1, 'ring': 1, 'pinky': 1}),
            'facial_expression': 'smile',
            'body_pose': 'standing',
            'motion_type': 'rise'
        }
    
    def _create_gesture_good_night(self) -> Dict:
        """Hands together resting on cheek for Good Night"""
        return {
            'left_hand_start': self._create_hand_position(x=200, y=200, rotation=45,
                fingers={'thumb': 1, 'index': 1, 'middle': 1, 'ring': 1, 'pinky': 1}),
            'left_hand_end': self._create_hand_position(x=220, y=160, rotation=30,
                fingers={'thumb': 1, 'index': 1, 'middle': 1, 'ring': 1, 'pinky': 1}),
            'right_hand_start': self._create_hand_position(x=300, y=200, rotation=-45,
                fingers={'thumb': 1, 'index': 1, 'middle': 1, 'ring': 1, 'pinky': 1}),
            'right_hand_end': self._create_hand_position(x=260, y=160, rotation=-30,
                fingers={'thumb': 1, 'index': 1, 'middle': 1, 'ring': 1, 'pinky': 1}),
            'facial_expression': 'calm',
            'body_pose': 'head_tilt',
            'motion_type': 'together'
        }
    
    def _create_gesture_how_are_you(self) -> Dict:
        """Pointing gesture with question expression"""
        return {
            'left_hand_start': self._create_hand_at_rest(),
            'left_hand_end': self._create_hand_at_rest(),
            'right_hand_start': self._create_hand_position(x=250, y=220, rotation=0,
                fingers={'thumb': 0, 'index': 1, 'middle': 0, 'ring': 0, 'pinky': 0}),
            'right_hand_end': self._create_hand_position(x=300, y=200, rotation=-15,
                fingers={'thumb': 0, 'index': 1, 'middle': 0, 'ring': 0, 'pinky': 0}),
            'facial_expression': 'question',
            'body_pose': 'standing',
            'motion_type': 'point'
        }
    
    def _create_gesture_happy(self) -> Dict:
        """Both hands moving up near chest for Happy"""
        return {
            'left_hand_start': self._create_hand_position(x=180, y=280, rotation=0,
                fingers={'thumb': 1, 'index': 1, 'middle': 1, 'ring': 1, 'pinky': 1}),
            'left_hand_end': self._create_hand_position(x=180, y=200, rotation=0,
                fingers={'thumb': 1, 'index': 1, 'middle': 1, 'ring': 1, 'pinky': 1}),
            'right_hand_start': self._create_hand_position(x=320, y=280, rotation=0,
                fingers={'thumb': 1, 'index': 1, 'middle': 1, 'ring': 1, 'pinky': 1}),
            'right_hand_end': self._create_hand_position(x=320, y=200, rotation=0,
                fingers={'thumb': 1, 'index': 1, 'middle': 1, 'ring': 1, 'pinky': 1}),
            'facial_expression': 'big_smile',
            'body_pose': 'standing',
            'motion_type': 'upward_brush'
        }
    
    def _create_gesture_sad(self) -> Dict:
        """Hands moving down from face for Sad"""
        return {
            'left_hand_start': self._create_hand_position(x=190, y=170, rotation=0,
                fingers={'thumb': 1, 'index': 1, 'middle': 1, 'ring': 1, 'pinky': 1}),
            'left_hand_end': self._create_hand_position(x=190, y=250, rotation=0,
                fingers={'thumb': 1, 'index': 1, 'middle': 1, 'ring': 1, 'pinky': 1}),
            'right_hand_start': self._create_hand_position(x=310, y=170, rotation=0,
                fingers={'thumb': 1, 'index': 1, 'middle': 1, 'ring': 1, 'pinky': 1}),
            'right_hand_end': self._create_hand_position(x=310, y=250, rotation=0,
                fingers={'thumb': 1, 'index': 1, 'middle': 1, 'ring': 1, 'pinky': 1}),
            'facial_expression': 'sad',
            'body_pose': 'slouch',
            'motion_type': 'downward'
        }
    
    def _create_gesture_beautiful(self) -> Dict:
        """Circular motion near face for Beautiful"""
        return {
            'left_hand_start': self._create_hand_at_rest(),
            'left_hand_end': self._create_hand_at_rest(),
            'right_hand_start': self._create_hand_position(x=250, y=160, rotation=0,
                fingers={'thumb': 1, 'index': 1, 'middle': 1, 'ring': 1, 'pinky': 1}),
            'right_hand_end': self._create_hand_position(x=280, y=180, rotation=45,
                fingers={'thumb': 1, 'index': 1, 'middle': 1, 'ring': 1, 'pinky': 1}),
            'facial_expression': 'smile',
            'body_pose': 'standing',
            'motion_type': 'circle'
        }
    
    def _create_gesture_ugly(self) -> Dict:
        """Negative expression gesture for Ugly"""
        return {
            'left_hand_start': self._create_hand_at_rest(),
            'left_hand_end': self._create_hand_at_rest(),
            'right_hand_start': self._create_hand_position(x=250, y=180, rotation=0,
                fingers={'thumb': 0, 'index': 1, 'middle': 0, 'ring': 0, 'pinky': 0}),
            'right_hand_end': self._create_hand_position(x=280, y=200, rotation=-30,
                fingers={'thumb': 0, 'index': 0.5, 'middle': 0, 'ring': 0, 'pinky': 0}),
            'facial_expression': 'disgust',
            'body_pose': 'standing',
            'motion_type': 'twist'
        }
    
    def _create_gesture_alright(self) -> Dict:
        """OK sign for Alright"""
        return {
            'left_hand_start': self._create_hand_at_rest(),
            'left_hand_end': self._create_hand_at_rest(),
            'right_hand_start': self._create_hand_position(x=250, y=200, rotation=0,
                fingers={'thumb': 0.7, 'index': 0.7, 'middle': 1, 'ring': 1, 'pinky': 1}),
            'right_hand_end': self._create_hand_position(x=270, y=180, rotation=0,
                fingers={'thumb': 0.7, 'index': 0.7, 'middle': 1, 'ring': 1, 'pinky': 1}),
            'facial_expression': 'smile',
            'body_pose': 'standing',
            'motion_type': 'static'
        }
    
    def _create_gesture_pleased(self) -> Dict:
        """Similar to happy gesture for Pleased"""
        return {
            'left_hand_start': self._create_hand_at_rest(),
            'left_hand_end': self._create_hand_at_rest(),
            'right_hand_start': self._create_hand_position(x=250, y=250, rotation=0,
                fingers={'thumb': 1, 'index': 1, 'middle': 1, 'ring': 1, 'pinky': 1}),
            'right_hand_end': self._create_hand_position(x=250, y=200, rotation=0,
                fingers={'thumb': 1, 'index': 1, 'middle': 1, 'ring': 1, 'pinky': 1}),
            'facial_expression': 'smile',
            'body_pose': 'standing',
            'motion_type': 'chest_brush'
        }
    
    # ==================== ANIMAL GESTURES ====================
    def _create_gesture_animal(self) -> Dict:
        """Generic animal gesture with claw hands"""
        return {
            'left_hand_start': self._create_hand_position(x=180, y=200, rotation=0,
                fingers={'thumb': 0.7, 'index': 0.7, 'middle': 0.7, 'ring': 0.7, 'pinky': 0.7}),
            'left_hand_end': self._create_hand_position(x=180, y=220, rotation=10,
                fingers={'thumb': 0.7, 'index': 0.7, 'middle': 0.7, 'ring': 0.7, 'pinky': 0.7}),
            'right_hand_start': self._create_hand_position(x=320, y=200, rotation=0,
                fingers={'thumb': 0.7, 'index': 0.7, 'middle': 0.7, 'ring': 0.7, 'pinky': 0.7}),
            'right_hand_end': self._create_hand_position(x=320, y=220, rotation=-10,
                fingers={'thumb': 0.7, 'index': 0.7, 'middle': 0.7, 'ring': 0.7, 'pinky': 0.7}),
            'facial_expression': 'neutral',
            'body_pose': 'standing',
            'motion_type': 'claw'
        }
    
    def _create_gesture_bird(self) -> Dict:
        """Beak motion for Bird"""
        return {
            'left_hand_start': self._create_hand_at_rest(),
            'left_hand_end': self._create_hand_at_rest(),
            'right_hand_start': self._create_hand_position(x=270, y=170, rotation=0,
                fingers={'thumb': 0.8, 'index': 0.8, 'middle': 0, 'ring': 0, 'pinky': 0}),
            'right_hand_end': self._create_hand_position(x=270, y=170, rotation=0,
                fingers={'thumb': 0.5, 'index': 0.5, 'middle': 0, 'ring': 0, 'pinky': 0}),
            'facial_expression': 'neutral',
            'body_pose': 'standing',
            'motion_type': 'pinch'
        }
    
    def _create_gesture_cat(self) -> Dict:
        """Whiskers motion for Cat"""
        return {
            'left_hand_start': self._create_hand_position(x=200, y=170, rotation=0,
                fingers={'thumb': 0, 'index': 1, 'middle': 1, 'ring': 0, 'pinky': 0}),
            'left_hand_end': self._create_hand_position(x=180, y=170, rotation=0,
                fingers={'thumb': 0, 'index': 1, 'middle': 1, 'ring': 0, 'pinky': 0}),
            'right_hand_start': self._create_hand_position(x=300, y=170, rotation=0,
                fingers={'thumb': 0, 'index': 1, 'middle': 1, 'ring': 0, 'pinky': 0}),
            'right_hand_end': self._create_hand_position(x=320, y=170, rotation=0,
                fingers={'thumb': 0, 'index': 1, 'middle': 1, 'ring': 0, 'pinky': 0}),
            'facial_expression': 'neutral',
            'body_pose': 'standing',
            'motion_type': 'whiskers'
        }
    
    def _create_gesture_dog(self) -> Dict:
        """Patting motion for Dog"""
        return {
            'left_hand_start': self._create_hand_at_rest(),
            'left_hand_end': self._create_hand_at_rest(),
            'right_hand_start': self._create_hand_position(x=300, y=280, rotation=0,
                fingers={'thumb': 1, 'index': 1, 'middle': 1, 'ring': 1, 'pinky': 1}),
            'right_hand_end': self._create_hand_position(x=300, y=300, rotation=0,
                fingers={'thumb': 1, 'index': 1, 'middle': 1, 'ring': 1, 'pinky': 1}),
            'facial_expression': 'smile',
            'body_pose': 'standing',
            'motion_type': 'pat'
        }
    
    def _create_gesture_cow(self) -> Dict:
        """Horns gesture for Cow"""
        return {
            'left_hand_start': self._create_hand_position(x=180, y=130, rotation=45,
                fingers={'thumb': 1, 'index': 0, 'middle': 0, 'ring': 0, 'pinky': 1}),
            'left_hand_end': self._create_hand_position(x=170, y=120, rotation=50,
                fingers={'thumb': 1, 'index': 0, 'middle': 0, 'ring': 0, 'pinky': 1}),
            'right_hand_start': self._create_hand_position(x=320, y=130, rotation=-45,
                fingers={'thumb': 1, 'index': 0, 'middle': 0, 'ring': 0, 'pinky': 1}),
            'right_hand_end': self._create_hand_position(x=330, y=120, rotation=-50,
                fingers={'thumb': 1, 'index': 0, 'middle': 0, 'ring': 0, 'pinky': 1}),
            'facial_expression': 'neutral',
            'body_pose': 'standing',
            'motion_type': 'horns'
        }
    
    def _create_gesture_horse(self) -> Dict:
        """Galloping motion for Horse"""
        return {
            'left_hand_start': self._create_hand_position(x=200, y=200, rotation=0,
                fingers={'thumb': 0, 'index': 1, 'middle': 1, 'ring': 0, 'pinky': 0}),
            'left_hand_end': self._create_hand_position(x=200, y=180, rotation=-20,
                fingers={'thumb': 0, 'index': 1, 'middle': 1, 'ring': 0, 'pinky': 0}),
            'right_hand_start': self._create_hand_position(x=300, y=180, rotation=0,
                fingers={'thumb': 0, 'index': 1, 'middle': 1, 'ring': 0, 'pinky': 0}),
            'right_hand_end': self._create_hand_position(x=300, y=200, rotation=20,
                fingers={'thumb': 0, 'index': 1, 'middle': 1, 'ring': 0, 'pinky': 0}),
            'facial_expression': 'neutral',
            'body_pose': 'standing',
            'motion_type': 'gallop'
        }
    
    def _create_gesture_mouse(self) -> Dict:
        """Small pinching motion for Mouse"""
        return {
            'left_hand_start': self._create_hand_at_rest(),
            'left_hand_end': self._create_hand_at_rest(),
            'right_hand_start': self._create_hand_position(x=280, y=180, rotation=0,
                fingers={'thumb': 0.5, 'index': 0.5, 'middle': 0, 'ring': 0, 'pinky': 0}),
            'right_hand_end': self._create_hand_position(x=280, y=175, rotation=0,
                fingers={'thumb': 0.3, 'index': 0.3, 'middle': 0, 'ring': 0, 'pinky': 0}),
            'facial_expression': 'neutral',
            'body_pose': 'standing',
            'motion_type': 'small_pinch'
        }
    
    def _create_gesture_fish(self) -> Dict:
        """Swimming motion for Fish"""
        return {
            'left_hand_start': self._create_hand_at_rest(),
            'left_hand_end': self._create_hand_at_rest(),
            'right_hand_start': self._create_hand_position(x=250, y=220, rotation=-20,
                fingers={'thumb': 1, 'index': 1, 'middle': 1, 'ring': 1, 'pinky': 1}),
            'right_hand_end': self._create_hand_position(x=300, y=220, rotation=20,
                fingers={'thumb': 1, 'index': 1, 'middle': 1, 'ring': 1, 'pinky': 1}),
            'facial_expression': 'neutral',
            'body_pose': 'standing',
            'motion_type': 'swim'
        }
    
    # ==================== FAMILY GESTURES ====================
    def _create_gesture_mother(self) -> Dict:
        """Thumb on chin for Mother"""
        return {
            'left_hand_start': self._create_hand_at_rest(),
            'left_hand_end': self._create_hand_at_rest(),
            'right_hand_start': self._create_hand_position(x=250, y=200, rotation=0,
                fingers={'thumb': 1, 'index': 1, 'middle': 1, 'ring': 1, 'pinky': 1}),
            'right_hand_end': self._create_hand_position(x=250, y=180, rotation=0,
                fingers={'thumb': 1, 'index': 1, 'middle': 1, 'ring': 1, 'pinky': 1}),
            'facial_expression': 'gentle_smile',
            'body_pose': 'standing',
            'motion_type': 'chin_tap'
        }
    
    def _create_gesture_father(self) -> Dict:
        """Thumb on forehead for Father"""
        return {
            'left_hand_start': self._create_hand_at_rest(),
            'left_hand_end': self._create_hand_at_rest(),
            'right_hand_start': self._create_hand_position(x=250, y=180, rotation=0,
                fingers={'thumb': 1, 'index': 1, 'middle': 1, 'ring': 1, 'pinky': 1}),
            'right_hand_end': self._create_hand_position(x=250, y=150, rotation=0,
                fingers={'thumb': 1, 'index': 1, 'middle': 1, 'ring': 1, 'pinky': 1}),
            'facial_expression': 'neutral',
            'body_pose': 'standing',
            'motion_type': 'forehead_tap'
        }
    
    def _create_gesture_daughter(self) -> Dict:
        """Combination of female + child gesture"""
        return {
            'left_hand_start': self._create_hand_at_rest(),
            'left_hand_end': self._create_hand_at_rest(),
            'right_hand_start': self._create_hand_position(x=250, y=180, rotation=0,
                fingers={'thumb': 1, 'index': 1, 'middle': 1, 'ring': 1, 'pinky': 1}),
            'right_hand_end': self._create_hand_position(x=270, y=250, rotation=0,
                fingers={'thumb': 1, 'index': 1, 'middle': 1, 'ring': 1, 'pinky': 1}),
            'facial_expression': 'gentle_smile',
            'body_pose': 'standing',
            'motion_type': 'downward_arc'
        }
    
    def _create_gesture_son(self) -> Dict:
        """Combination of male + child gesture"""
        return {
            'left_hand_start': self._create_hand_at_rest(),
            'left_hand_end': self._create_hand_at_rest(),
            'right_hand_start': self._create_hand_position(x=250, y=150, rotation=0,
                fingers={'thumb': 1, 'index': 1, 'middle': 1, 'ring': 1, 'pinky': 1}),
            'right_hand_end': self._create_hand_position(x=270, y=250, rotation=0,
                fingers={'thumb': 1, 'index': 1, 'middle': 1, 'ring': 1, 'pinky': 1}),
            'facial_expression': 'neutral',
            'body_pose': 'standing',
            'motion_type': 'downward_arc'
        }
    
    def _create_gesture_parent(self) -> Dict:
        """Both mother and father combined"""
        return {
            'left_hand_start': self._create_hand_position(x=200, y=180, rotation=0,
                fingers={'thumb': 1, 'index': 1, 'middle': 1, 'ring': 1, 'pinky': 1}),
            'left_hand_end': self._create_hand_position(x=200, y=150, rotation=0,
                fingers={'thumb': 1, 'index': 1, 'middle': 1, 'ring': 1, 'pinky': 1}),
            'right_hand_start': self._create_hand_position(x=300, y=180, rotation=0,
                fingers={'thumb': 1, 'index': 1, 'middle': 1, 'ring': 1, 'pinky': 1}),
            'right_hand_end': self._create_hand_position(x=300, y=150, rotation=0,
                fingers={'thumb': 1, 'index': 1, 'middle': 1, 'ring': 1, 'pinky': 1}),
            'facial_expression': 'neutral',
            'body_pose': 'standing',
            'motion_type': 'double_tap'
        }
    
    # ==================== FURNITURE/OBJECT GESTURES ====================
    def _create_gesture_chair(self) -> Dict:
        """Sitting motion for Chair"""
        return {
            'left_hand_start': self._create_hand_position(x=200, y=200, rotation=0,
                fingers={'thumb': 0, 'index': 0.7, 'middle': 0.7, 'ring': 0, 'pinky': 0}),
            'left_hand_end': self._create_hand_position(x=200, y=220, rotation=0,
                fingers={'thumb': 0, 'index': 0.7, 'middle': 0.7, 'ring': 0, 'pinky': 0}),
            'right_hand_start': self._create_hand_position(x=300, y=200, rotation=0,
                fingers={'thumb': 0, 'index': 0.7, 'middle': 0.7, 'ring': 0, 'pinky': 0}),
            'right_hand_end': self._create_hand_position(x=300, y=220, rotation=0,
                fingers={'thumb': 0, 'index': 0.7, 'middle': 0.7, 'ring': 0, 'pinky': 0}),
            'facial_expression': 'neutral',
            'body_pose': 'standing',
            'motion_type': 'sit'
        }
    
    def _create_gesture_table(self) -> Dict:
        """Flat surface motion for Table"""
        return {
            'left_hand_start': self._create_hand_position(x=180, y=230, rotation=90,
                fingers={'thumb': 1, 'index': 1, 'middle': 1, 'ring': 1, 'pinky': 1}),
            'left_hand_end': self._create_hand_position(x=180, y=230, rotation=90,
                fingers={'thumb': 1, 'index': 1, 'middle': 1, 'ring': 1, 'pinky': 1}),
            'right_hand_start': self._create_hand_position(x=320, y=230, rotation=-90,
                fingers={'thumb': 1, 'index': 1, 'middle': 1, 'ring': 1, 'pinky': 1}),
            'right_hand_end': self._create_hand_position(x=320, y=230, rotation=-90,
                fingers={'thumb': 1, 'index': 1, 'middle': 1, 'ring': 1, 'pinky': 1}),
            'facial_expression': 'neutral',
            'body_pose': 'standing',
            'motion_type': 'flat'
        }
    
    def _create_gesture_bed(self) -> Dict:
        """Sleeping gesture for Bed"""
        return {
            'left_hand_start': self._create_hand_position(x=220, y=160, rotation=45,
                fingers={'thumb': 1, 'index': 1, 'middle': 1, 'ring': 1, 'pinky': 1}),
            'left_hand_end': self._create_hand_position(x=220, y=160, rotation=45,
                fingers={'thumb': 1, 'index': 1, 'middle': 1, 'ring': 1, 'pinky': 1}),
            'right_hand_start': self._create_hand_position(x=280, y=160, rotation=-45,
                fingers={'thumb': 1, 'index': 1, 'middle': 1, 'ring': 1, 'pinky': 1}),
            'right_hand_end': self._create_hand_position(x=280, y=160, rotation=-45,
                fingers={'thumb': 1, 'index': 1, 'middle': 1, 'ring': 1, 'pinky': 1}),
            'facial_expression': 'calm',
            'body_pose': 'head_tilt',
            'motion_type': 'sleep'
        }
    
    def _create_gesture_bedroom(self) -> Dict:
        """Bed + room gesture"""
        return self._create_gesture_bed()
    
    def _create_gesture_door(self) -> Dict:
        """Opening door motion"""
        return {
            'left_hand_start': self._create_hand_at_rest(),
            'left_hand_end': self._create_hand_at_rest(),
            'right_hand_start': self._create_hand_position(x=280, y=200, rotation=0,
                fingers={'thumb': 0, 'index': 0, 'middle': 0, 'ring': 0, 'pinky': 0}),
            'right_hand_end': self._create_hand_position(x=320, y=200, rotation=-45,
                fingers={'thumb': 0, 'index': 0, 'middle': 0, 'ring': 0, 'pinky': 0}),
            'facial_expression': 'neutral',
            'body_pose': 'standing',
            'motion_type': 'open'
        }
    
    def _create_gesture_window(self) -> Dict:
        """Square shape for Window"""
        return {
            'left_hand_start': self._create_hand_position(x=180, y=180, rotation=0,
                fingers={'thumb': 1, 'index': 1, 'middle': 1, 'ring': 1, 'pinky': 1}),
            'left_hand_end': self._create_hand_position(x=180, y=250, rotation=0,
                fingers={'thumb': 1, 'index': 1, 'middle': 1, 'ring': 1, 'pinky': 1}),
            'right_hand_start': self._create_hand_position(x=320, y=180, rotation=0,
                fingers={'thumb': 1, 'index': 1, 'middle': 1, 'ring': 1, 'pinky': 1}),
            'right_hand_end': self._create_hand_position(x=320, y=250, rotation=0,
                fingers={'thumb': 1, 'index': 1, 'middle': 1, 'ring': 1, 'pinky': 1}),
            'facial_expression': 'neutral',
            'body_pose': 'standing',
            'motion_type': 'square'
        }
    
    # ==================== COLOR GESTURES ====================
    def _create_gesture_black(self) -> Dict:
        """Eyebrow touch for Black"""
        return {
            'left_hand_start': self._create_hand_at_rest(),
            'left_hand_end': self._create_hand_at_rest(),
            'right_hand_start': self._create_hand_position(x=250, y=180, rotation=0,
                fingers={'thumb': 0, 'index': 1, 'middle': 0, 'ring': 0, 'pinky': 0}),
            'right_hand_end': self._create_hand_position(x=280, y=140, rotation=0,
                fingers={'thumb': 0, 'index': 1, 'middle': 0, 'ring': 0, 'pinky': 0}),
            'facial_expression': 'neutral',
            'body_pose': 'standing',
            'motion_type': 'eyebrow_touch'
        }
    
    def _create_gesture_white(self) -> Dict:
        """Chest touch expanding for White"""
        return {
            'left_hand_start': self._create_hand_at_rest(),
            'left_hand_end': self._create_hand_at_rest(),
            'right_hand_start': self._create_hand_position(x=250, y=240, rotation=0,
                fingers={'thumb': 1, 'index': 1, 'middle': 1, 'ring': 1, 'pinky': 1}),
            'right_hand_end': self._create_hand_position(x=300, y=220, rotation=0,
                fingers={'thumb': 1, 'index': 1, 'middle': 1, 'ring': 1, 'pinky': 1}),
            'facial_expression': 'neutral',
            'body_pose': 'standing',
            'motion_type': 'expand'
        }
    
    def _create_gesture_orange(self) -> Dict:
        """Squeezing motion for Orange"""
        return {
            'left_hand_start': self._create_hand_at_rest(),
            'left_hand_end': self._create_hand_at_rest(),
            'right_hand_start': self._create_hand_position(x=270, y=180, rotation=0,
                fingers={'thumb': 0.5, 'index': 0.5, 'middle': 0.5, 'ring': 0.5, 'pinky': 0.5}),
            'right_hand_end': self._create_hand_position(x=270, y=180, rotation=0,
                fingers={'thumb': 0, 'index': 0, 'middle': 0, 'ring': 0, 'pinky': 0}),
            'facial_expression': 'neutral',
            'body_pose': 'standing',
            'motion_type': 'squeeze'
        }
    
    def _create_gesture_pink(self) -> Dict:
        """Lip touch for Pink"""
        return {
            'left_hand_start': self._create_hand_at_rest(),
            'left_hand_end': self._create_hand_at_rest(),
            'right_hand_start': self._create_hand_position(x=250, y=190, rotation=0,
                fingers={'thumb': 0, 'index': 1, 'middle': 1, 'ring': 0, 'pinky': 0}),
            'right_hand_end': self._create_hand_position(x=250, y=180, rotation=0,
                fingers={'thumb': 0, 'index': 1, 'middle': 1, 'ring': 0, 'pinky': 0}),
            'facial_expression': 'smile',
            'body_pose': 'standing',
            'motion_type': 'lip_touch'
        }
    
    def _create_gesture_grey(self) -> Dict:
        """Mixing motion for Grey"""
        return {
            'left_hand_start': self._create_hand_position(x=200, y=220, rotation=0,
                fingers={'thumb': 1, 'index': 1, 'middle': 1, 'ring': 1, 'pinky': 1}),
            'left_hand_end': self._create_hand_position(x=220, y=220, rotation=0,
                fingers={'thumb': 1, 'index': 1, 'middle': 1, 'ring': 1, 'pinky': 1}),
            'right_hand_start': self._create_hand_position(x=300, y=220, rotation=0,
                fingers={'thumb': 1, 'index': 1, 'middle': 1, 'ring': 1, 'pinky': 1}),
            'right_hand_end': self._create_hand_position(x=280, y=220, rotation=0,
                fingers={'thumb': 1, 'index': 1, 'middle': 1, 'ring': 1, 'pinky': 1}),
            'facial_expression': 'neutral',
            'body_pose': 'standing',
            'motion_type': 'mix'
        }
    
    def _create_gesture_colour(self) -> Dict:
        """Wiggling fingers near chin for Colour"""
        return {
            'left_hand_start': self._create_hand_at_rest(),
            'left_hand_end': self._create_hand_at_rest(),
            'right_hand_start': self._create_hand_position(x=260, y=185, rotation=0,
                fingers={'thumb': 1, 'index': 1, 'middle': 1, 'ring': 1, 'pinky': 1}),
            'right_hand_end': self._create_hand_position(x=260, y=185, rotation=15,
                fingers={'thumb': 0.8, 'index': 0.8, 'middle': 0.8, 'ring': 0.8, 'pinky': 0.8}),
            'facial_expression': 'neutral',
            'body_pose': 'standing',
            'motion_type': 'wiggle'
        }
    
    # ==================== DAY GESTURES ====================
    def _create_gesture_day(self, initial: str) -> Dict:
        """Create gesture for days (showing letter)"""
        return self._create_letter_gesture(initial[0])
    
    def _create_gesture_today(self) -> Dict:
        """Pointing down for Today"""
        return {
            'left_hand_start': self._create_hand_at_rest(),
            'left_hand_end': self._create_hand_at_rest(),
            'right_hand_start': self._create_hand_position(x=250, y=200, rotation=0,
                fingers={'thumb': 0, 'index': 1, 'middle': 0, 'ring': 0, 'pinky': 0}),
            'right_hand_end': self._create_hand_position(x=250, y=280, rotation=0,
                fingers={'thumb': 0, 'index': 1, 'middle': 0, 'ring': 0, 'pinky': 0}),
            'facial_expression': 'neutral',
            'body_pose': 'standing',
            'motion_type': 'point_down'
        }
    
    # ==================== PRONOUN GESTURES ====================
    def _create_gesture_i(self) -> Dict:
        """Pointing to self for I/me"""
        return {
            'left_hand_start': self._create_hand_at_rest(),
            'left_hand_end': self._create_hand_at_rest(),
            'right_hand_start': self._create_hand_position(x=280, y=220, rotation=0,
                fingers={'thumb': 0, 'index': 1, 'middle': 0, 'ring': 0, 'pinky': 0}),
            'right_hand_end': self._create_hand_position(x=250, y=250, rotation=0,
                fingers={'thumb': 0, 'index': 1, 'middle': 0, 'ring': 0, 'pinky': 0}),
            'facial_expression': 'neutral',
            'body_pose': 'standing',
            'motion_type': 'point_self'
        }
    
    def _create_gesture_you(self) -> Dict:
        """Pointing forward for You"""
        return {
            'left_hand_start': self._create_hand_at_rest(),
            'left_hand_end': self._create_hand_at_rest(),
            'right_hand_start': self._create_hand_position(x=250, y=220, rotation=0,
                fingers={'thumb': 0, 'index': 1, 'middle': 0, 'ring': 0, 'pinky': 0}),
            'right_hand_end': self._create_hand_position(x=300, y=200, rotation=-20,
                fingers={'thumb': 0, 'index': 1, 'middle': 0, 'ring': 0, 'pinky': 0}),
            'facial_expression': 'neutral',
            'body_pose': 'standing',
            'motion_type': 'point_forward'
        }
    
    def _create_gesture_he(self) -> Dict:
        """Pointing to side for He"""
        return {
            'left_hand_start': self._create_hand_at_rest(),
            'left_hand_end': self._create_hand_at_rest(),
            'right_hand_start': self._create_hand_position(x=280, y=200, rotation=0,
                fingers={'thumb': 0, 'index': 1, 'middle': 0, 'ring': 0, 'pinky': 0}),
            'right_hand_end': self._create_hand_position(x=350, y=200, rotation=-30,
                fingers={'thumb': 0, 'index': 1, 'middle': 0, 'ring': 0, 'pinky': 0}),
            'facial_expression': 'neutral',
            'body_pose': 'standing',
            'motion_type': 'point_right'
        }
    
    def _create_gesture_she(self) -> Dict:
        """Pointing to other side for She"""
        return {
            'left_hand_start': self._create_hand_position(x=220, y=200, rotation=0,
                fingers={'thumb': 0, 'index': 1, 'middle': 0, 'ring': 0, 'pinky': 0}),
            'left_hand_end': self._create_hand_position(x=150, y=200, rotation=30,
                fingers={'thumb': 0, 'index': 1, 'middle': 0, 'ring': 0, 'pinky': 0}),
            'right_hand_start': self._create_hand_at_rest(),
            'right_hand_end': self._create_hand_at_rest(),
            'facial_expression': 'neutral',
            'body_pose': 'standing',
            'motion_type': 'point_left'
        }
    
    def _create_gesture_it(self) -> Dict:
        """Pointing down for It"""
        return {
            'left_hand_start': self._create_hand_at_rest(),
            'left_hand_end': self._create_hand_at_rest(),
            'right_hand_start': self._create_hand_position(x=250, y=220, rotation=0,
                fingers={'thumb': 0, 'index': 1, 'middle': 0, 'ring': 0, 'pinky': 0}),
            'right_hand_end': self._create_hand_position(x=250, y=280, rotation=0,
                fingers={'thumb': 0, 'index': 1, 'middle': 0, 'ring': 0, 'pinky': 0}),
            'facial_expression': 'neutral',
            'body_pose': 'standing',
            'motion_type': 'point_down'
        }
    
    # ==================== OTHER GESTURES ====================
    def _create_gesture_blind(self) -> Dict:
        """Covering eyes for Blind"""
        return {
            'left_hand_start': self._create_hand_position(x=180, y=170, rotation=0,
                fingers={'thumb': 0, 'index': 1, 'middle': 1, 'ring': 0, 'pinky': 0}),
            'left_hand_end': self._create_hand_position(x=200, y=155, rotation=0,
                fingers={'thumb': 0, 'index': 1, 'middle': 1, 'ring': 0, 'pinky': 0}),
            'right_hand_start': self._create_hand_position(x=320, y=170, rotation=0,
                fingers={'thumb': 0, 'index': 1, 'middle': 1, 'ring': 0, 'pinky': 0}),
            'right_hand_end': self._create_hand_position(x=300, y=155, rotation=0,
                fingers={'thumb': 0, 'index': 1, 'middle': 1, 'ring': 0, 'pinky': 0}),
            'facial_expression': 'closed_eyes',
            'body_pose': 'standing',
            'motion_type': 'cover_eyes'
        }
    
    def _create_gesture_deaf(self) -> Dict:
        """Pointing to ear for Deaf"""
        return {
            'left_hand_start': self._create_hand_at_rest(),
            'left_hand_end': self._create_hand_at_rest(),
            'right_hand_start': self._create_hand_position(x=280, y=160, rotation=0,
                fingers={'thumb': 0, 'index': 1, 'middle': 0, 'ring': 0, 'pinky': 0}),
            'right_hand_end': self._create_hand_position(x=310, y=155, rotation=0,
                fingers={'thumb': 0, 'index': 1, 'middle': 0, 'ring': 0, 'pinky': 0}),
            'facial_expression': 'neutral',
            'body_pose': 'standing',
            'motion_type': 'ear_touch'
        }
    
    def _create_gesture_dream(self) -> Dict:
        """Wavy motion from head for Dream"""
        return {
            'left_hand_start': self._create_hand_at_rest(),
            'left_hand_end': self._create_hand_at_rest(),
            'right_hand_start': self._create_hand_position(x=280, y=140, rotation=0,
                fingers={'thumb': 0, 'index': 1, 'middle': 0, 'ring': 0, 'pinky': 0}),
            'right_hand_end': self._create_hand_position(x=320, y=100, rotation=30,
                fingers={'thumb': 0, 'index': 1, 'middle': 0, 'ring': 0, 'pinky': 0}),
            'facial_expression': 'dreamy',
            'body_pose': 'standing',
            'motion_type': 'wavy'
        }
    
    def _create_gesture_loud(self) -> Dict:
        """Hands expanding from ears for Loud"""
        return {
            'left_hand_start': self._create_hand_position(x=180, y=155, rotation=0,
                fingers={'thumb': 1, 'index': 1, 'middle': 1, 'ring': 1, 'pinky': 1}),
            'left_hand_end': self._create_hand_position(x=140, y=155, rotation=0,
                fingers={'thumb': 1, 'index': 1, 'middle': 1, 'ring': 1, 'pinky': 1}),
            'right_hand_start': self._create_hand_position(x=320, y=155, rotation=0,
                fingers={'thumb': 1, 'index': 1, 'middle': 1, 'ring': 1, 'pinky': 1}),
            'right_hand_end': self._create_hand_position(x=360, y=155, rotation=0,
                fingers={'thumb': 1, 'index': 1, 'middle': 1, 'ring': 1, 'pinky': 1}),
            'facial_expression': 'intense',
            'body_pose': 'standing',
            'motion_type': 'expand'
        }
    
    def _create_gesture_quiet(self) -> Dict:
        """Finger on lips for Quiet"""
        return {
            'left_hand_start': self._create_hand_at_rest(),
            'left_hand_end': self._create_hand_at_rest(),
            'right_hand_start': self._create_hand_position(x=260, y=200, rotation=0,
                fingers={'thumb': 0, 'index': 1, 'middle': 0, 'ring': 0, 'pinky': 0}),
            'right_hand_end': self._create_hand_position(x=250, y=180, rotation=0,
                fingers={'thumb': 0, 'index': 1, 'middle': 0, 'ring': 0, 'pinky': 0}),
            'facial_expression': 'shh',
            'body_pose': 'standing',
            'motion_type': 'shh'
        }
    
    # ==================== UTILITY METHODS ====================
    def _create_gesture_default(self) -> Dict:
        """Create default resting gesture"""
        return {
            'left_hand_start': self._create_hand_at_rest(),
            'left_hand_end': self._create_hand_at_rest(),
            'right_hand_start': self._create_hand_at_rest(),
            'right_hand_end': self._create_hand_position(x=250, y=220, rotation=0,
                fingers={'thumb': 1, 'index': 1, 'middle': 1, 'ring': 1, 'pinky': 1}),
            'facial_expression': 'neutral',
            'body_pose': 'standing',
            'motion_type': 'static'
        }
    
    def _create_hand_at_rest(self) -> Dict:
        """Create hand at rest position (by the side)"""
        return {
            'x': 0,
            'y': 350,
            'rotation': 0,
            'visible': False,
            'fingers': {
                'thumb': 0.5,
                'index': 0.5,
                'middle': 0.5,
                'ring': 0.5,
                'pinky': 0.5
            }
        }
    
    def _create_hand_position(self, x: int, y: int, rotation: float, fingers: Dict) -> Dict:
        """Create a hand position with specified parameters"""
        return {
            'x': x,
            'y': y,
            'rotation': rotation,
            'visible': True,
            'fingers': fingers
        }
    
    def export_animation_data(self, frames: List[Dict]) -> str:
        """Export animation data as JSON"""
        return json.dumps(frames, indent=2)
