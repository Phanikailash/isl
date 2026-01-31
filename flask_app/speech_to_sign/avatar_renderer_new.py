"""
3D Avatar Renderer Module for Speech-to-Sign System
Following the architecture in Figure 3.4

Uses keypoint coordinates from ISL Database for realistic hand rendering.
Generates animation frames for frontend visualization.
"""

import math
from typing import List, Dict, Tuple
from .sign_database import ISLDatabase, isl_database
from .animation_generator import AnimationGenerator, animation_generator


class AvatarRenderer:
    """
    3D Avatar Rendering Module
    
    Converts ISL sign data to rendered animation frames for display.
    Uses keypoint coordinates for realistic hand positions.
    """
    
    def __init__(self, sign_db: ISLDatabase = None, anim_gen: AnimationGenerator = None):
        self.sign_db = sign_db or isl_database
        self.anim_gen = anim_gen or animation_generator
        
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
        
        # Avatar configuration
        self.config = {
            'canvas_width': 500,
            'canvas_height': 500,
            'skin_color': '#FFDAB9',
            'outline_color': '#2c3e50',
            'hand_color': '#FFDAB9',
            'joint_color': '#e8c4a0',
            'background_color': '#f0f0f0'
        }
        
        # Hand landmark names for reference
        self.landmark_names = [
            'WRIST',
            'THUMB_CMC', 'THUMB_MCP', 'THUMB_IP', 'THUMB_TIP',
            'INDEX_MCP', 'INDEX_PIP', 'INDEX_DIP', 'INDEX_TIP',
            'MIDDLE_MCP', 'MIDDLE_PIP', 'MIDDLE_DIP', 'MIDDLE_TIP',
            'RING_MCP', 'RING_PIP', 'RING_DIP', 'RING_TIP',
            'PINKY_MCP', 'PINKY_PIP', 'PINKY_DIP', 'PINKY_TIP'
        ]
        
        # Finger connections for drawing
        self.finger_connections = [
            # Thumb
            (0, 1), (1, 2), (2, 3), (3, 4),
            # Index
            (0, 5), (5, 6), (6, 7), (7, 8),
            # Middle
            (0, 9), (9, 10), (10, 11), (11, 12),
            # Ring
            (0, 13), (13, 14), (14, 15), (15, 16),
            # Pinky
            (0, 17), (17, 18), (18, 19), (19, 20),
            # Palm
            (5, 9), (9, 13), (13, 17)
        ]
    
    def render_animation_sequence(self, animations: List[Dict]) -> List[Dict]:
        """
        Main entry point: Render animation sequence for a list of signs
        
        Args:
            animations: List of animation data from ISLMapper.get_animation_sequence()
        
        Returns:
            List of rendered frames ready for frontend display
        """
        all_frames = []
        current_timestamp = 0
        
        for anim in animations:
            sign = anim.get('sign', '')
            duration = anim.get('duration', 1500)
            
            # Get sign data from database
            sign_data = self.sign_db.get_sign(sign)
            
            # Generate frames for this sign
            sign_frames = self._render_sign_frames(sign, sign_data, duration, current_timestamp)
            all_frames.extend(sign_frames)
            
            current_timestamp += duration
        
        return all_frames
    
    def _render_sign_frames(self, sign: str, sign_data: Dict, 
                            duration: int, start_time: int) -> List[Dict]:
        """Render all frames for a single sign"""
        frames = []
        fps = 30
        total_frames = max(int(duration / 1000 * fps), 5)
        
        # Get keyframes and motion info from sign data
        keyframes = sign_data.get('keyframes', [])
        motion_type = sign_data.get('motion_type', 'static')
        facial_expr = sign_data.get('facial_expression', 'neutral')
        body_region = sign_data.get('body_region', 'neutral')
        two_hands = sign_data.get('two_hands', False)
        
        for frame_num in range(total_frames):
            progress = frame_num / max(total_frames - 1, 1)
            eased_progress = self._ease_in_out(progress)
            
            # Interpolate keyframes
            right_hand_keypoints = self._get_interpolated_keypoints(
                keyframes, eased_progress, motion_type, sign_data
            )
            
            left_hand_keypoints = None
            if two_hands:
                left_hand_keypoints = self._mirror_hand(right_hand_keypoints)
            
            # Build frame data
            frame = {
                'frame': frame_num,
                'total_frames': total_frames,
                'sign': sign,
                'timestamp': start_time + (frame_num * 1000 / fps),
                'progress': eased_progress,
                
                # Hand keypoints (21 landmarks each)
                'right_hand': {
                    'keypoints': right_hand_keypoints,
                    'connections': self.finger_connections
                },
                'left_hand': {
                    'keypoints': left_hand_keypoints,
                    'connections': self.finger_connections
                } if two_hands else None,
                
                # Rendering info
                'facial_expression': self._get_facial_data(facial_expr, eased_progress),
                'body_pose': self._get_body_pose(body_region, eased_progress),
                'motion_type': motion_type,
                
                # Visual settings
                'hand_color': self.config['hand_color'],
                'outline_color': self.config['outline_color'],
                'canvas_size': {
                    'width': self.config['canvas_width'],
                    'height': self.config['canvas_height']
                }
            }
            
            frames.append(frame)
        
        return frames
    
    def _get_interpolated_keypoints(self, keyframes: List[Dict], progress: float,
                                    motion_type: str, sign_data: Dict) -> List[Dict]:
        """Get interpolated keypoints for current progress"""
        if not keyframes:
            return self._get_default_keypoints()
        
        # Get base keypoints
        if len(keyframes) >= 2:
            # Interpolate between first and last keyframe
            start = keyframes[0].get('right_hand', self._get_default_keypoints())
            end = keyframes[-1].get('right_hand', start)
            base_keypoints = self._interpolate_keypoints(start, end, progress)
        else:
            base_keypoints = keyframes[0].get('right_hand', self._get_default_keypoints())
        
        # Apply motion modifier
        if motion_type != 'static':
            base_keypoints = self._apply_motion(base_keypoints, motion_type, progress)
        
        return base_keypoints
    
    def _interpolate_keypoints(self, start: List[Dict], end: List[Dict], 
                               progress: float) -> List[Dict]:
        """Linear interpolation between two sets of keypoints"""
        if not start or not end:
            return start or end or self._get_default_keypoints()
        
        result = []
        for i in range(min(len(start), len(end))):
            result.append({
                'x': start[i]['x'] + (end[i]['x'] - start[i]['x']) * progress,
                'y': start[i]['y'] + (end[i]['y'] - start[i]['y']) * progress,
                'z': start[i]['z'] + (end[i]['z'] - start[i]['z']) * progress
            })
        
        return result
    
    def _apply_motion(self, keypoints: List[Dict], motion_type: str, 
                      progress: float) -> List[Dict]:
        """Apply motion modifications to keypoints"""
        modified = [kp.copy() for kp in keypoints]
        
        if motion_type == 'wave':
            wave = math.sin(progress * math.pi * 4) * 0.05
            for kp in modified:
                kp['x'] += wave
                
        elif motion_type == 'circular':
            angle = progress * math.pi * 2
            radius = 0.03
            for kp in modified:
                kp['x'] += math.cos(angle) * radius
                kp['y'] += math.sin(angle) * radius
                
        elif motion_type == 'wiggling':
            for i, kp in enumerate(modified):
                wiggle = math.sin(progress * math.pi * 6 + i * 0.5) * 0.02
                kp['x'] += wiggle
                
        elif motion_type == 'outward':
            for kp in modified:
                kp['y'] += progress * 0.1
                
        elif motion_type == 'downward':
            for kp in modified:
                kp['y'] += progress * 0.15
                
        elif motion_type == 'rising':
            for kp in modified:
                kp['y'] -= progress * 0.15
                
        elif motion_type == 'tapping':
            tap = abs(math.sin(progress * math.pi * 4)) * 0.03
            for kp in modified:
                kp['y'] += tap
                
        elif motion_type == 'rocking':
            rock = math.sin(progress * math.pi * 4) * 0.04
            for kp in modified:
                kp['y'] += rock
        
        return modified
    
    def _mirror_hand(self, keypoints: List[Dict]) -> List[Dict]:
        """Mirror hand keypoints for left hand"""
        if not keypoints:
            return None
        
        mirrored = []
        for kp in keypoints:
            mirrored.append({
                'x': 1.0 - kp['x'],  # Mirror horizontally
                'y': kp['y'],
                'z': kp['z']
            })
        
        return mirrored
    
    def _get_default_keypoints(self) -> List[Dict]:
        """Get default relaxed hand keypoints"""
        return self.sign_db._create_base_hand(0.5, 0.5)
    
    def _get_facial_data(self, expression: str, progress: float) -> Dict:
        """Get facial expression data for rendering"""
        expressions = {
            'neutral': {
                'eyebrows': 0,
                'eye_openness': 1.0,
                'mouth_curve': 0,
                'mouth_openness': 0
            },
            'smile': {
                'eyebrows': 0.1,
                'eye_openness': 0.9,
                'mouth_curve': 0.5,
                'mouth_openness': 0.1
            },
            'sad': {
                'eyebrows': -0.3,
                'eye_openness': 0.8,
                'mouth_curve': -0.4,
                'mouth_openness': 0
            },
            'question': {
                'eyebrows': 0.4,
                'eye_openness': 1.1,
                'mouth_curve': 0,
                'mouth_openness': 0.2
            },
            'calm': {
                'eyebrows': 0,
                'eye_openness': 0.7,
                'mouth_curve': 0.1,
                'mouth_openness': 0
            },
            'frown': {
                'eyebrows': -0.4,
                'eye_openness': 0.9,
                'mouth_curve': -0.3,
                'mouth_openness': 0
            },
            'intense': {
                'eyebrows': 0.3,
                'eye_openness': 1.2,
                'mouth_curve': 0,
                'mouth_openness': 0.3
            }
        }
        
        expr_data = expressions.get(expression, expressions['neutral'])
        
        # Add subtle animation
        blink = 1.0 if progress % 0.3 > 0.05 else 0.2
        expr_data = expr_data.copy()
        expr_data['eye_openness'] *= blink
        
        return expr_data
    
    def _get_body_pose(self, body_region: str, progress: float) -> Dict:
        """Get body pose data for rendering"""
        poses = {
            'neutral': {'head_tilt': 0, 'shoulder_offset': 0},
            'head': {'head_tilt': 5, 'shoulder_offset': 0},
            'face': {'head_tilt': 0, 'shoulder_offset': 0},
            'forehead': {'head_tilt': -5, 'shoulder_offset': 0},
            'chin': {'head_tilt': 10, 'shoulder_offset': 0},
            'chest': {'head_tilt': 0, 'shoulder_offset': 0},
            'ear': {'head_tilt': 0, 'shoulder_offset': 5},
            'ears': {'head_tilt': 0, 'shoulder_offset': 5},
            'temple': {'head_tilt': -3, 'shoulder_offset': 3},
            'eyes': {'head_tilt': -5, 'shoulder_offset': 0},
            'nose': {'head_tilt': 0, 'shoulder_offset': 0},
            'mouth': {'head_tilt': 5, 'shoulder_offset': 0},
            'lips': {'head_tilt': 5, 'shoulder_offset': 0},
            'cheek': {'head_tilt': 0, 'shoulder_offset': 3},
            'thigh': {'head_tilt': 15, 'shoulder_offset': 0}
        }
        
        pose = poses.get(body_region, poses['neutral'])
        
        # Add subtle breathing animation
        breathing = math.sin(progress * math.pi * 2) * 0.5
        pose = pose.copy()
        pose['shoulder_offset'] += breathing
        
        return pose
    
    def _ease_in_out(self, t: float) -> float:
        """Smooth easing function"""
        if t < 0.5:
            return 2 * t * t
        else:
            return 1 - pow(-2 * t + 2, 2) / 2
    
    def get_sign_render_data(self, sign: str) -> Dict:
        """Get complete render data for a single sign"""
        if sign not in self.class_labels:
            return {'error': f'Sign "{sign}" not found'}
        
        sign_data = self.sign_db.get_sign(sign)
        keypoints = self.sign_db.get_keypoints(sign)
        
        return {
            'sign': sign,
            'keypoints': keypoints,
            'sign_data': sign_data,
            'connections': self.finger_connections,
            'landmark_names': self.landmark_names,
            'config': self.config
        }
    
    def render_full_animation(self, isl_signs: List[str]) -> Dict:
        """
        Render complete animation data for a sequence of ISL signs
        Uses animation generator for full keyframe interpolation
        """
        # Generate animation sequence with full interpolation
        animation_data = self.anim_gen.generate_animation_sequence(isl_signs)
        
        # Convert to render frames
        render_frames = []
        for frame in animation_data.get('frames', []):
            render_frame = self._convert_to_render_frame(frame)
            render_frames.append(render_frame)
        
        return {
            'signs': isl_signs,
            'total_duration': animation_data.get('total_duration', 0),
            'frames': render_frames,
            'schedule': animation_data.get('schedule', []),
            'config': self.config
        }
    
    def _convert_to_render_frame(self, frame: Dict) -> Dict:
        """Convert animation frame to render frame format"""
        return {
            'frame': frame.get('frame_number', 0),
            'total_frames': frame.get('total_frames', 1),
            'sign': frame.get('sign', ''),
            'timestamp': frame.get('timestamp', 0),
            'progress': frame.get('progress', 0),
            
            'right_hand': {
                'keypoints': frame.get('right_hand', []),
                'connections': self.finger_connections
            },
            'left_hand': {
                'keypoints': frame.get('left_hand'),
                'connections': self.finger_connections
            } if frame.get('left_hand') else None,
            
            'facial_expression': frame.get('facial_expression', {}),
            'body_pose': frame.get('body_posture', {}),
            'motion_type': frame.get('motion_type', 'static'),
            'two_hands': frame.get('two_hands', False),
            
            'config': self.config
        }


# Module-level instance
avatar_renderer = AvatarRenderer()
