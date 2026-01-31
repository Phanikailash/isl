"""
Animation Generation Module for Speech-to-Sign System
Following the architecture in Figure 3.4:
Keyframes → Motion Interpolation → Facial Expression Mapping → Body Posture Coordination → Setup & Animation Scheduling
"""

import math
from typing import List, Dict, Tuple, Optional
from .sign_database import isl_database, ISLDatabase


class AnimationGenerator:
    """
    Animation Generation Module following the architecture:
    - Keyframes: Get keyframe data from ISL Database
    - Motion Interpolation: Smooth transitions between keyframes
    - Facial Expression Mapping: Map signs to facial expressions
    - Body Posture Coordination: Coordinate body movements with signs
    - Setup & Animation Scheduling: Schedule animation timing
    """
    
    def __init__(self, sign_db: ISLDatabase = None):
        self.sign_db = sign_db or isl_database
        
        # Animation configuration
        self.config = {
            'fps': 30,
            'default_sign_duration': 1500,  # ms
            'transition_duration': 300,  # ms between signs
            'min_sign_duration': 800,
            'max_sign_duration': 2500
        }
        
        # Facial expression configurations
        self.facial_expressions = {
            'neutral': {'eyebrows': 0, 'mouth': 'closed', 'eyes': 'open'},
            'smile': {'eyebrows': 0.1, 'mouth': 'smile', 'eyes': 'open'},
            'sad': {'eyebrows': -0.2, 'mouth': 'frown', 'eyes': 'droopy'},
            'question': {'eyebrows': 0.3, 'mouth': 'open_slight', 'eyes': 'wide'},
            'calm': {'eyebrows': 0, 'mouth': 'closed', 'eyes': 'relaxed'},
            'frown': {'eyebrows': -0.3, 'mouth': 'frown', 'eyes': 'narrow'},
            'intense': {'eyebrows': 0.2, 'mouth': 'open', 'eyes': 'wide'}
        }
        
        # Body posture configurations
        self.body_postures = {
            'neutral': {'shoulder_rotation': 0, 'torso_tilt': 0, 'head_tilt': 0},
            'head': {'shoulder_rotation': 0, 'torso_tilt': 0, 'head_tilt': 0.1},
            'chest': {'shoulder_rotation': 0, 'torso_tilt': 0.05, 'head_tilt': 0},
            'face': {'shoulder_rotation': 0, 'torso_tilt': 0, 'head_tilt': 0.15},
            'forehead': {'shoulder_rotation': 0, 'torso_tilt': 0, 'head_tilt': 0.2},
            'chin': {'shoulder_rotation': 0, 'torso_tilt': 0, 'head_tilt': -0.1},
            'ears': {'shoulder_rotation': 0.1, 'torso_tilt': 0, 'head_tilt': 0},
            'temple': {'shoulder_rotation': 0.05, 'torso_tilt': 0, 'head_tilt': 0.1},
            'nose': {'shoulder_rotation': 0, 'torso_tilt': 0, 'head_tilt': 0.05},
            'mouth': {'shoulder_rotation': 0, 'torso_tilt': 0, 'head_tilt': 0},
            'lips': {'shoulder_rotation': 0, 'torso_tilt': 0, 'head_tilt': 0},
            'cheek': {'shoulder_rotation': 0.05, 'torso_tilt': 0, 'head_tilt': 0.05},
            'eyes': {'shoulder_rotation': 0, 'torso_tilt': 0, 'head_tilt': 0.1},
            'ear': {'shoulder_rotation': 0.1, 'torso_tilt': 0, 'head_tilt': 0.05},
            'thigh': {'shoulder_rotation': 0, 'torso_tilt': 0.1, 'head_tilt': -0.1}
        }
        
        # Motion types and their interpolation patterns
        self.motion_patterns = {
            'static': self._interpolate_static,
            'wave': self._interpolate_wave,
            'circular': self._interpolate_circular,
            'outward': self._interpolate_outward,
            'downward': self._interpolate_downward,
            'rising': self._interpolate_rising,
            'opening': self._interpolate_opening,
            'closing': self._interpolate_closing,
            'wiggling': self._interpolate_wiggling,
            'tapping': self._interpolate_tapping,
            'brushing': self._interpolate_brushing,
            'rocking': self._interpolate_rocking,
            'alternating': self._interpolate_alternating,
            'swimming': self._interpolate_swimming,
            'flapping': self._interpolate_flapping,
            'squeezing': self._interpolate_squeezing,
            'patting': self._interpolate_patting,
            'pointing_out': self._interpolate_pointing,
            'pointing_side': self._interpolate_pointing,
            'pointing_down': self._interpolate_pointing,
            'opening_closing': self._interpolate_open_close,
            'across': self._interpolate_across,
            'sliding': self._interpolate_sliding,
            'passing': self._interpolate_passing,
            'expanding': self._interpolate_expanding,
            'touching': self._interpolate_touching,
            'twisting': self._interpolate_twisting,
            'questioning': self._interpolate_questioning,
            'cradling': self._interpolate_cradling,
            'resting': self._interpolate_resting,
            'box_shape': self._interpolate_box
        }
    
    def generate_animation_sequence(self, isl_signs: List[str]) -> Dict:
        """
        Main entry point: Generate complete animation sequence for ISL signs
        Returns animation data with all keyframes, expressions, and body poses
        """
        animation_data = {
            'signs': isl_signs,
            'total_duration': 0,
            'frames': [],
            'schedule': []
        }
        
        current_time = 0
        
        for i, sign_name in enumerate(isl_signs):
            # Step 1: Get keyframes from ISL Database
            sign_data = self.sign_db.get_sign(sign_name)
            
            # Step 2: Calculate duration based on sign complexity
            duration = self._calculate_sign_duration(sign_data)
            
            # Step 3: Generate frames with motion interpolation
            sign_frames = self._generate_sign_frames(sign_name, sign_data, duration, current_time)
            
            # Step 4: Add to schedule
            animation_data['schedule'].append({
                'sign': sign_name,
                'start_time': current_time,
                'end_time': current_time + duration,
                'duration': duration,
                'frame_start': len(animation_data['frames']),
                'frame_count': len(sign_frames)
            })
            
            # Add frames to total
            animation_data['frames'].extend(sign_frames)
            
            # Update time
            current_time += duration
            
            # Add transition frames if not last sign
            if i < len(isl_signs) - 1:
                transition_frames = self._generate_transition_frames(
                    sign_data, 
                    self.sign_db.get_sign(isl_signs[i + 1]),
                    current_time
                )
                animation_data['frames'].extend(transition_frames)
                current_time += self.config['transition_duration']
        
        animation_data['total_duration'] = current_time
        
        return animation_data
    
    def _calculate_sign_duration(self, sign_data: Dict) -> int:
        """Calculate appropriate duration for a sign based on complexity"""
        base_duration = self.config['default_sign_duration']
        
        # Adjust based on sign type
        sign_type = sign_data.get('type', 'word')
        if sign_type == 'letter':
            base_duration = 800  # Letters are faster
        elif sign_type == 'number':
            base_duration = 1000
        elif sign_type == 'phrase':
            base_duration = 2000  # Phrases take longer
        elif sign_type == 'animated':
            base_duration = 1800  # Animated signs need more time
        
        # Adjust based on motion type
        motion = sign_data.get('motion_type', 'static')
        if motion in ['circular', 'wave', 'alternating']:
            base_duration += 300
        elif motion == 'static':
            base_duration -= 200
        
        # Clamp to min/max
        return max(self.config['min_sign_duration'], 
                   min(self.config['max_sign_duration'], base_duration))
    
    def _generate_sign_frames(self, sign_name: str, sign_data: Dict, 
                              duration: int, start_time: int) -> List[Dict]:
        """Generate all frames for a single sign with interpolation"""
        frames = []
        fps = self.config['fps']
        total_frames = max(int(duration / 1000 * fps), 5)
        
        # Get motion interpolation function
        motion_type = sign_data.get('motion_type', 'static')
        interpolate_fn = self.motion_patterns.get(motion_type, self._interpolate_static)
        
        # Get keyframes from sign data
        keyframes = sign_data.get('keyframes', [])
        if not keyframes:
            keyframes = [{'right_hand': self.sign_db._create_base_hand()}]
        
        # Get facial expression
        facial_expr = sign_data.get('facial_expression', 'neutral')
        facial_data = self.facial_expressions.get(facial_expr, self.facial_expressions['neutral'])
        
        # Get body posture
        body_region = sign_data.get('body_region', 'neutral')
        body_posture = self.body_postures.get(body_region, self.body_postures['neutral'])
        
        for frame_num in range(total_frames):
            progress = frame_num / max(total_frames - 1, 1)
            
            # Apply easing
            eased_progress = self._ease_in_out_cubic(progress)
            
            # Step 2: Motion Interpolation
            hand_positions = interpolate_fn(keyframes, eased_progress, sign_data)
            
            # Step 3: Facial Expression Mapping
            facial_frame = self._interpolate_facial(facial_data, eased_progress)
            
            # Step 4: Body Posture Coordination
            body_frame = self._interpolate_body_posture(body_posture, eased_progress)
            
            frame = {
                'frame_number': frame_num,
                'total_frames': total_frames,
                'timestamp': start_time + (frame_num * 1000 / fps),
                'progress': eased_progress,
                'sign': sign_name,
                'right_hand': hand_positions.get('right_hand', []),
                'left_hand': hand_positions.get('left_hand'),
                'facial_expression': facial_frame,
                'body_posture': body_frame,
                'motion_type': motion_type,
                'two_hands': sign_data.get('two_hands', False)
            }
            
            frames.append(frame)
        
        return frames
    
    def _generate_transition_frames(self, from_sign: Dict, to_sign: Dict, 
                                    start_time: int) -> List[Dict]:
        """Generate smooth transition frames between two signs"""
        frames = []
        fps = self.config['fps']
        duration = self.config['transition_duration']
        total_frames = max(int(duration / 1000 * fps), 3)
        
        # Get end position of from_sign and start position of to_sign
        from_keyframes = from_sign.get('keyframes', [])
        to_keyframes = to_sign.get('keyframes', [])
        
        from_hand = from_keyframes[-1]['right_hand'] if from_keyframes else self.sign_db._create_base_hand()
        to_hand = to_keyframes[0]['right_hand'] if to_keyframes else self.sign_db._create_base_hand()
        
        for frame_num in range(total_frames):
            progress = frame_num / max(total_frames - 1, 1)
            eased = self._ease_in_out_cubic(progress)
            
            # Interpolate hand positions
            interpolated_hand = self.sign_db._interpolate_landmarks(from_hand, to_hand, eased)
            
            frame = {
                'frame_number': frame_num,
                'total_frames': total_frames,
                'timestamp': start_time + (frame_num * 1000 / fps),
                'progress': eased,
                'sign': 'transition',
                'right_hand': interpolated_hand,
                'left_hand': None,
                'facial_expression': self.facial_expressions['neutral'],
                'body_posture': self.body_postures['neutral'],
                'motion_type': 'transition',
                'two_hands': False
            }
            
            frames.append(frame)
        
        return frames
    
    # ============ MOTION INTERPOLATION FUNCTIONS ============
    
    def _interpolate_static(self, keyframes: List[Dict], progress: float, 
                           sign_data: Dict) -> Dict:
        """Static sign - no motion, just show the pose"""
        hand = keyframes[0].get('right_hand', self.sign_db._create_base_hand())
        return {
            'right_hand': hand,
            'left_hand': keyframes[0].get('left_hand') if sign_data.get('two_hands') else None
        }
    
    def _interpolate_wave(self, keyframes: List[Dict], progress: float,
                         sign_data: Dict) -> Dict:
        """Wave motion - side to side"""
        base_hand = keyframes[0].get('right_hand', self.sign_db._create_base_hand())
        wave_offset = math.sin(progress * math.pi * 4) * 0.05
        
        modified = []
        for lm in base_hand:
            modified.append({
                'x': lm['x'] + wave_offset,
                'y': lm['y'],
                'z': lm['z']
            })
        
        return {'right_hand': modified, 'left_hand': None}
    
    def _interpolate_circular(self, keyframes: List[Dict], progress: float,
                             sign_data: Dict) -> Dict:
        """Circular motion"""
        base_hand = keyframes[0].get('right_hand', self.sign_db._create_base_hand())
        angle = progress * math.pi * 2
        radius = 0.03
        
        modified = []
        for lm in base_hand:
            modified.append({
                'x': lm['x'] + math.cos(angle) * radius,
                'y': lm['y'] + math.sin(angle) * radius,
                'z': lm['z']
            })
        
        return {'right_hand': modified, 'left_hand': None}
    
    def _interpolate_outward(self, keyframes: List[Dict], progress: float,
                            sign_data: Dict) -> Dict:
        """Outward motion - moving away from body"""
        if len(keyframes) >= 2:
            start = keyframes[0].get('right_hand', [])
            end = keyframes[1].get('right_hand', [])
            interpolated = self.sign_db._interpolate_landmarks(start, end, progress)
            return {'right_hand': interpolated, 'left_hand': None}
        
        base_hand = keyframes[0].get('right_hand', self.sign_db._create_base_hand())
        modified = []
        for lm in base_hand:
            modified.append({
                'x': lm['x'],
                'y': lm['y'] + progress * 0.1,
                'z': lm['z'] - progress * 0.05
            })
        return {'right_hand': modified, 'left_hand': None}
    
    def _interpolate_downward(self, keyframes: List[Dict], progress: float,
                             sign_data: Dict) -> Dict:
        """Downward motion"""
        base_hand = keyframes[0].get('right_hand', self.sign_db._create_base_hand())
        modified = []
        for lm in base_hand:
            modified.append({
                'x': lm['x'],
                'y': lm['y'] + progress * 0.15,
                'z': lm['z']
            })
        return {'right_hand': modified, 'left_hand': None}
    
    def _interpolate_rising(self, keyframes: List[Dict], progress: float,
                           sign_data: Dict) -> Dict:
        """Rising/upward motion"""
        if len(keyframes) >= 2:
            start = keyframes[0].get('right_hand', [])
            end = keyframes[1].get('right_hand', [])
            interpolated = self.sign_db._interpolate_landmarks(start, end, progress)
            return {'right_hand': interpolated, 'left_hand': None}
        
        base_hand = keyframes[0].get('right_hand', self.sign_db._create_base_hand())
        modified = []
        for lm in base_hand:
            modified.append({
                'x': lm['x'],
                'y': lm['y'] - progress * 0.15,
                'z': lm['z']
            })
        return {'right_hand': modified, 'left_hand': None}
    
    def _interpolate_opening(self, keyframes: List[Dict], progress: float,
                            sign_data: Dict) -> Dict:
        """Opening motion (like a door)"""
        base_hand = keyframes[0].get('right_hand', self.sign_db._create_base_hand())
        rotation = progress * 0.1
        
        modified = []
        for lm in base_hand:
            modified.append({
                'x': lm['x'] + rotation,
                'y': lm['y'],
                'z': lm['z'] - rotation * 0.5
            })
        return {'right_hand': modified, 'left_hand': None}
    
    def _interpolate_closing(self, keyframes: List[Dict], progress: float,
                            sign_data: Dict) -> Dict:
        """Closing motion"""
        base_hand = keyframes[0].get('right_hand', self.sign_db._create_base_hand())
        close_amount = progress * 0.05
        
        modified = []
        for i, lm in enumerate(base_hand):
            # Move fingers toward center
            center_x = 0.5
            modified.append({
                'x': lm['x'] + (center_x - lm['x']) * close_amount,
                'y': lm['y'],
                'z': lm['z'] + close_amount
            })
        return {'right_hand': modified, 'left_hand': None}
    
    def _interpolate_wiggling(self, keyframes: List[Dict], progress: float,
                             sign_data: Dict) -> Dict:
        """Wiggling fingers motion"""
        base_hand = keyframes[0].get('right_hand', self.sign_db._create_base_hand())
        
        modified = []
        for i, lm in enumerate(base_hand):
            # Wiggle each finger differently
            wiggle = math.sin(progress * math.pi * 6 + i * 0.5) * 0.02
            modified.append({
                'x': lm['x'] + wiggle,
                'y': lm['y'],
                'z': lm['z']
            })
        return {'right_hand': modified, 'left_hand': None}
    
    def _interpolate_tapping(self, keyframes: List[Dict], progress: float,
                            sign_data: Dict) -> Dict:
        """Tapping motion"""
        base_hand = keyframes[0].get('right_hand', self.sign_db._create_base_hand())
        tap = abs(math.sin(progress * math.pi * 4)) * 0.03
        
        modified = []
        for lm in base_hand:
            modified.append({
                'x': lm['x'],
                'y': lm['y'] + tap,
                'z': lm['z'] - tap
            })
        return {'right_hand': modified, 'left_hand': modified if sign_data.get('two_hands') else None}
    
    def _interpolate_brushing(self, keyframes: List[Dict], progress: float,
                             sign_data: Dict) -> Dict:
        """Brushing motion across a surface"""
        base_hand = keyframes[0].get('right_hand', self.sign_db._create_base_hand())
        brush = math.sin(progress * math.pi * 2) * 0.08
        
        modified = []
        for lm in base_hand:
            modified.append({
                'x': lm['x'] + brush,
                'y': lm['y'],
                'z': lm['z']
            })
        return {'right_hand': modified, 'left_hand': None}
    
    def _interpolate_rocking(self, keyframes: List[Dict], progress: float,
                            sign_data: Dict) -> Dict:
        """Rocking back and forth motion"""
        base_hand = keyframes[0].get('right_hand', self.sign_db._create_base_hand())
        rock = math.sin(progress * math.pi * 4) * 0.04
        
        modified = []
        for lm in base_hand:
            modified.append({
                'x': lm['x'],
                'y': lm['y'] + rock,
                'z': lm['z'] + rock * 0.5
            })
        return {'right_hand': modified, 'left_hand': modified if sign_data.get('two_hands') else None}
    
    def _interpolate_alternating(self, keyframes: List[Dict], progress: float,
                                sign_data: Dict) -> Dict:
        """Alternating motion between two hands"""
        base_hand = keyframes[0].get('right_hand', self.sign_db._create_base_hand())
        alt = math.sin(progress * math.pi * 4) * 0.05
        
        right_modified = []
        left_modified = []
        
        for lm in base_hand:
            right_modified.append({
                'x': lm['x'],
                'y': lm['y'] + alt,
                'z': lm['z']
            })
            left_modified.append({
                'x': 1 - lm['x'],  # Mirror x
                'y': lm['y'] - alt,  # Opposite direction
                'z': lm['z']
            })
        
        return {'right_hand': right_modified, 'left_hand': left_modified}
    
    def _interpolate_swimming(self, keyframes: List[Dict], progress: float,
                             sign_data: Dict) -> Dict:
        """Swimming fish-like motion"""
        base_hand = keyframes[0].get('right_hand', self.sign_db._create_base_hand())
        swim = math.sin(progress * math.pi * 6) * 0.05
        forward = progress * 0.1
        
        modified = []
        for lm in base_hand:
            modified.append({
                'x': lm['x'] + forward,
                'y': lm['y'] + swim,
                'z': lm['z']
            })
        return {'right_hand': modified, 'left_hand': None}
    
    def _interpolate_flapping(self, keyframes: List[Dict], progress: float,
                             sign_data: Dict) -> Dict:
        """Flapping motion (like wings or ears)"""
        base_hand = keyframes[0].get('right_hand', self.sign_db._create_base_hand())
        flap = abs(math.sin(progress * math.pi * 6)) * 0.04
        
        modified = []
        for i, lm in enumerate(base_hand):
            # Flap mainly affects fingertips
            if i >= 5:  # Finger landmarks
                modified.append({
                    'x': lm['x'],
                    'y': lm['y'] - flap,
                    'z': lm['z']
                })
            else:
                modified.append(lm.copy())
        
        return {'right_hand': modified, 'left_hand': None}
    
    def _interpolate_squeezing(self, keyframes: List[Dict], progress: float,
                              sign_data: Dict) -> Dict:
        """Squeezing motion"""
        base_hand = keyframes[0].get('right_hand', self.sign_db._create_base_hand())
        squeeze = math.sin(progress * math.pi * 4) * 0.02
        
        modified = []
        for lm in base_hand:
            modified.append({
                'x': lm['x'],
                'y': lm['y'],
                'z': lm['z'] + squeeze
            })
        return {'right_hand': modified, 'left_hand': None}
    
    def _interpolate_patting(self, keyframes: List[Dict], progress: float,
                            sign_data: Dict) -> Dict:
        """Patting/tapping downward motion"""
        base_hand = keyframes[0].get('right_hand', self.sign_db._create_base_hand())
        pat = abs(math.sin(progress * math.pi * 4)) * 0.05
        
        modified = []
        for lm in base_hand:
            modified.append({
                'x': lm['x'],
                'y': lm['y'] + pat,
                'z': lm['z']
            })
        return {'right_hand': modified, 'left_hand': modified if sign_data.get('two_hands') else None}
    
    def _interpolate_pointing(self, keyframes: List[Dict], progress: float,
                             sign_data: Dict) -> Dict:
        """Pointing gesture"""
        base_hand = keyframes[0].get('right_hand', self.sign_db._create_base_hand())
        # Slight forward thrust
        thrust = progress * 0.05
        
        modified = []
        for lm in base_hand:
            modified.append({
                'x': lm['x'],
                'y': lm['y'],
                'z': lm['z'] - thrust
            })
        return {'right_hand': modified, 'left_hand': None}
    
    def _interpolate_open_close(self, keyframes: List[Dict], progress: float,
                               sign_data: Dict) -> Dict:
        """Opening and closing motion (like a beak)"""
        base_hand = keyframes[0].get('right_hand', self.sign_db._create_base_hand())
        open_close = abs(math.sin(progress * math.pi * 4)) * 0.03
        
        modified = []
        for i, lm in enumerate(base_hand):
            if i == 4 or i == 8:  # Thumb tip and index tip
                modified.append({
                    'x': lm['x'],
                    'y': lm['y'] - open_close if i == 8 else lm['y'] + open_close,
                    'z': lm['z']
                })
            else:
                modified.append(lm.copy())
        
        return {'right_hand': modified, 'left_hand': None}
    
    def _interpolate_across(self, keyframes: List[Dict], progress: float,
                           sign_data: Dict) -> Dict:
        """Across/horizontal motion"""
        base_hand = keyframes[0].get('right_hand', self.sign_db._create_base_hand())
        across = progress * 0.15
        
        modified = []
        for lm in base_hand:
            modified.append({
                'x': lm['x'] + across,
                'y': lm['y'],
                'z': lm['z']
            })
        return {'right_hand': modified, 'left_hand': None}
    
    def _interpolate_sliding(self, keyframes: List[Dict], progress: float,
                            sign_data: Dict) -> Dict:
        """Sliding motion"""
        base_hand = keyframes[0].get('right_hand', self.sign_db._create_base_hand())
        slide = math.sin(progress * math.pi * 2) * 0.08
        
        modified = []
        for lm in base_hand:
            modified.append({
                'x': lm['x'],
                'y': lm['y'] + slide,
                'z': lm['z']
            })
        return {'right_hand': modified, 'left_hand': modified if sign_data.get('two_hands') else None}
    
    def _interpolate_passing(self, keyframes: List[Dict], progress: float,
                            sign_data: Dict) -> Dict:
        """Passing through motion (two hands)"""
        base_hand = keyframes[0].get('right_hand', self.sign_db._create_base_hand())
        pass_amt = progress * 0.15
        
        right_modified = []
        left_modified = []
        
        for lm in base_hand:
            right_modified.append({
                'x': lm['x'] + pass_amt,
                'y': lm['y'],
                'z': lm['z']
            })
            left_modified.append({
                'x': 1 - lm['x'] - pass_amt,
                'y': lm['y'],
                'z': lm['z']
            })
        
        return {'right_hand': right_modified, 'left_hand': left_modified}
    
    def _interpolate_expanding(self, keyframes: List[Dict], progress: float,
                              sign_data: Dict) -> Dict:
        """Expanding outward motion (two hands)"""
        base_hand = keyframes[0].get('right_hand', self.sign_db._create_base_hand())
        expand = progress * 0.12
        
        right_modified = []
        left_modified = []
        
        for lm in base_hand:
            right_modified.append({
                'x': lm['x'] + expand,
                'y': lm['y'],
                'z': lm['z']
            })
            left_modified.append({
                'x': 1 - lm['x'] - expand,
                'y': lm['y'],
                'z': lm['z']
            })
        
        return {'right_hand': right_modified, 'left_hand': left_modified}
    
    def _interpolate_touching(self, keyframes: List[Dict], progress: float,
                             sign_data: Dict) -> Dict:
        """Touching motion toward a point"""
        base_hand = keyframes[0].get('right_hand', self.sign_db._create_base_hand())
        touch = math.sin(progress * math.pi) * 0.05
        
        modified = []
        for lm in base_hand:
            modified.append({
                'x': lm['x'],
                'y': lm['y'],
                'z': lm['z'] + touch
            })
        return {'right_hand': modified, 'left_hand': None}
    
    def _interpolate_twisting(self, keyframes: List[Dict], progress: float,
                             sign_data: Dict) -> Dict:
        """Twisting/rotating motion"""
        base_hand = keyframes[0].get('right_hand', self.sign_db._create_base_hand())
        twist = math.sin(progress * math.pi * 2) * 0.04
        
        modified = []
        center_x = sum(lm['x'] for lm in base_hand) / len(base_hand)
        center_y = sum(lm['y'] for lm in base_hand) / len(base_hand)
        
        for lm in base_hand:
            # Rotate around center
            dx = lm['x'] - center_x
            dy = lm['y'] - center_y
            modified.append({
                'x': center_x + dx * math.cos(twist) - dy * math.sin(twist),
                'y': center_y + dx * math.sin(twist) + dy * math.cos(twist),
                'z': lm['z']
            })
        
        return {'right_hand': modified, 'left_hand': None}
    
    def _interpolate_questioning(self, keyframes: List[Dict], progress: float,
                                sign_data: Dict) -> Dict:
        """Questioning gesture with slight tilt"""
        base_hand = keyframes[0].get('right_hand', self.sign_db._create_base_hand())
        question = math.sin(progress * math.pi * 2) * 0.05
        
        modified = []
        for i, lm in enumerate(base_hand):
            modified.append({
                'x': lm['x'] + question,
                'y': lm['y'] - question * 0.5,
                'z': lm['z']
            })
        return {'right_hand': modified, 'left_hand': None}
    
    def _interpolate_cradling(self, keyframes: List[Dict], progress: float,
                             sign_data: Dict) -> Dict:
        """Cradling motion (like holding a baby)"""
        base_hand = keyframes[0].get('right_hand', self.sign_db._create_base_hand())
        cradle = math.sin(progress * math.pi * 2) * 0.04
        
        right_modified = []
        left_modified = []
        
        for lm in base_hand:
            right_modified.append({
                'x': lm['x'],
                'y': lm['y'] + cradle,
                'z': lm['z']
            })
            left_modified.append({
                'x': 1 - lm['x'],
                'y': lm['y'] - cradle,
                'z': lm['z']
            })
        
        return {'right_hand': right_modified, 'left_hand': left_modified}
    
    def _interpolate_resting(self, keyframes: List[Dict], progress: float,
                            sign_data: Dict) -> Dict:
        """Resting/sleeping position"""
        base_hand = keyframes[0].get('right_hand', self.sign_db._create_base_hand())
        # Minimal movement
        modified = [lm.copy() for lm in base_hand]
        return {'right_hand': modified, 'left_hand': modified if sign_data.get('two_hands') else None}
    
    def _interpolate_box(self, keyframes: List[Dict], progress: float,
                        sign_data: Dict) -> Dict:
        """Box shape motion (for room signs)"""
        base_hand = keyframes[0].get('right_hand', self.sign_db._create_base_hand())
        
        # Move in a box pattern
        segment = int(progress * 4) % 4
        seg_progress = (progress * 4) % 1
        
        offsets = [
            (0, 0.1),   # Right
            (0.1, 0),   # Down
            (0, -0.1),  # Left
            (-0.1, 0)   # Up
        ]
        
        ox, oy = offsets[segment]
        ox *= seg_progress
        oy *= seg_progress
        
        right_modified = []
        left_modified = []
        
        for lm in base_hand:
            right_modified.append({'x': lm['x'] + ox, 'y': lm['y'] + oy, 'z': lm['z']})
            left_modified.append({'x': 1 - lm['x'] - ox, 'y': lm['y'] + oy, 'z': lm['z']})
        
        return {'right_hand': right_modified, 'left_hand': left_modified}
    
    # ============ EXPRESSION & POSTURE INTERPOLATION ============
    
    def _interpolate_facial(self, expression: Dict, progress: float) -> Dict:
        """Interpolate facial expression over time"""
        # For now, return the expression directly
        # Could add subtle micro-expressions here
        return expression.copy()
    
    def _interpolate_body_posture(self, posture: Dict, progress: float) -> Dict:
        """Interpolate body posture over time"""
        # Return posture with slight natural movement
        variation = math.sin(progress * math.pi * 2) * 0.02
        return {
            'shoulder_rotation': posture['shoulder_rotation'] + variation,
            'torso_tilt': posture['torso_tilt'],
            'head_tilt': posture['head_tilt']
        }
    
    # ============ EASING FUNCTIONS ============
    
    def _ease_in_out_cubic(self, t: float) -> float:
        """Cubic ease in-out for smooth animations"""
        if t < 0.5:
            return 4 * t * t * t
        else:
            return 1 - pow(-2 * t + 2, 3) / 2
    
    def _ease_out_elastic(self, t: float) -> float:
        """Elastic ease out for bouncy finish"""
        if t == 0 or t == 1:
            return t
        return pow(2, -10 * t) * math.sin((t - 0.075) * (2 * math.pi) / 0.3) + 1


# Module-level instance
animation_generator = AnimationGenerator()
