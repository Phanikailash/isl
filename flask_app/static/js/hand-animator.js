/**
 * High-Quality ISL Hand Animation System
 * Uses smooth interpolation and realistic hand rendering
 */

class ISLHandAnimator {
    constructor(canvas) {
        this.canvas = canvas;
        this.ctx = canvas.getContext('2d');
        this.width = canvas.width;
        this.height = canvas.height;
        
        // Animation state
        this.currentFrame = 0;
        this.frames = [];
        this.isPlaying = false;
        this.animationId = null;
        this.fps = 30;
        
        // Hand configuration
        this.handConfig = {
            skinColor: '#F5CBA7',
            skinColorDark: '#D4A574',
            outlineColor: '#B8860B',
            nailColor: '#FFE4E1',
            jointColor: '#E8C4A0',
            shadowColor: 'rgba(0, 0, 0, 0.2)'
        };
        
        // Avatar body position
        this.body = {
            centerX: 250,
            centerY: 200,
            shoulderRightX: 310,
            shoulderLeftX: 190,
            shoulderY: 290
        };
    }
    
    // Smooth easing functions
    easeInOutCubic(t) {
        return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
    }
    
    easeOutBack(t) {
        const c1 = 1.70158;
        const c3 = c1 + 1;
        return 1 + c3 * Math.pow(t - 1, 3) + c1 * Math.pow(t - 1, 2);
    }
    
    // Interpolate between two hand poses
    interpolateHands(hand1, hand2, t) {
        if (!hand1 || !hand2) return hand1 || hand2;
        
        const eased = this.easeInOutCubic(t);
        const result = [];
        
        for (let i = 0; i < 21; i++) {
            result.push({
                x: hand1[i].x + (hand2[i].x - hand1[i].x) * eased,
                y: hand1[i].y + (hand2[i].y - hand1[i].y) * eased,
                z: (hand1[i].z || 0) + ((hand2[i].z || 0) - (hand1[i].z || 0)) * eased
            });
        }
        
        return result;
    }
    
    // Draw the complete avatar with animated hands
    drawFrame(frame) {
        const ctx = this.ctx;
        ctx.clearRect(0, 0, this.width, this.height);
        
        // Background gradient
        const bgGrad = ctx.createLinearGradient(0, 0, 0, this.height);
        bgGrad.addColorStop(0, '#E8F4FC');
        bgGrad.addColorStop(1, '#D4E9F7');
        ctx.fillStyle = bgGrad;
        ctx.fillRect(0, 0, this.width, this.height);
        
        // Draw body
        this.drawBody(ctx);
        
        // Draw facial expression
        if (frame.facial_expression) {
            this.drawFace(ctx, frame.facial_expression);
        }
        
        // Draw hands (on top of body)
        if (frame.right_hand && frame.right_hand.keypoints) {
            this.drawHand(ctx, frame.right_hand.keypoints, 'right');
        }
        
        if (frame.left_hand && frame.left_hand.keypoints) {
            this.drawHand(ctx, frame.left_hand.keypoints, 'left');
        }
        
        // Draw sign label
        this.drawSignLabel(ctx, frame.sign);
    }
    
    drawBody(ctx) {
        const cx = this.body.centerX;
        
        // Torso
        ctx.fillStyle = '#3498db';
        ctx.beginPath();
        ctx.moveTo(cx - 60, 280);
        ctx.lineTo(cx + 60, 280);
        ctx.lineTo(cx + 70, 450);
        ctx.lineTo(cx - 70, 450);
        ctx.closePath();
        ctx.fill();
        
        // Neck
        ctx.fillStyle = this.handConfig.skinColor;
        ctx.fillRect(cx - 15, 220, 30, 65);
        
        // Head
        ctx.beginPath();
        ctx.ellipse(cx, 160, 55, 70, 0, 0, 2 * Math.PI);
        ctx.fill();
        
        // Hair
        ctx.fillStyle = '#2c3e50';
        ctx.beginPath();
        ctx.ellipse(cx, 130, 58, 50, 0, Math.PI, 2 * Math.PI);
        ctx.fill();
        
        // Ears
        ctx.fillStyle = this.handConfig.skinColor;
        ctx.beginPath();
        ctx.ellipse(cx - 55, 160, 10, 15, 0, 0, 2 * Math.PI);
        ctx.fill();
        ctx.beginPath();
        ctx.ellipse(cx + 55, 160, 10, 15, 0, 0, 2 * Math.PI);
        ctx.fill();
        
        // Shoulders
        ctx.fillStyle = '#3498db';
        ctx.beginPath();
        ctx.ellipse(cx - 70, 290, 25, 15, 0, 0, 2 * Math.PI);
        ctx.fill();
        ctx.beginPath();
        ctx.ellipse(cx + 70, 290, 25, 15, 0, 0, 2 * Math.PI);
        ctx.fill();
    }
    
    drawFace(ctx, expr) {
        const cx = this.body.centerX;
        const eyeY = 155;
        
        // Eyes
        ctx.fillStyle = 'white';
        ctx.beginPath();
        ctx.ellipse(cx - 20, eyeY, 8, 10, 0, 0, 2 * Math.PI);
        ctx.fill();
        ctx.beginPath();
        ctx.ellipse(cx + 20, eyeY, 8, 10, 0, 0, 2 * Math.PI);
        ctx.fill();
        
        // Pupils
        ctx.fillStyle = '#2c3e50';
        ctx.beginPath();
        ctx.arc(cx - 20, eyeY, 4, 0, 2 * Math.PI);
        ctx.fill();
        ctx.beginPath();
        ctx.arc(cx + 20, eyeY, 4, 0, 2 * Math.PI);
        ctx.fill();
        
        // Eyebrows
        const browOffset = (expr.eyebrows || 0) * 5;
        ctx.strokeStyle = '#2c3e50';
        ctx.lineWidth = 3;
        ctx.beginPath();
        ctx.moveTo(cx - 28, 140 - browOffset);
        ctx.lineTo(cx - 12, 138 - browOffset);
        ctx.stroke();
        ctx.beginPath();
        ctx.moveTo(cx + 12, 138 - browOffset);
        ctx.lineTo(cx + 28, 140 - browOffset);
        ctx.stroke();
        
        // Nose
        ctx.strokeStyle = this.handConfig.skinColorDark;
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.moveTo(cx, 155);
        ctx.lineTo(cx - 5, 175);
        ctx.lineTo(cx + 5, 175);
        ctx.stroke();
        
        // Mouth
        const mouthCurve = expr.mouth_curve || 0;
        ctx.strokeStyle = '#C0392B';
        ctx.lineWidth = 3;
        ctx.beginPath();
        if (mouthCurve > 0.1) {
            ctx.arc(cx, 190, 15, 0.1 * Math.PI, 0.9 * Math.PI);
        } else if (mouthCurve < -0.1) {
            ctx.arc(cx, 200, 12, 1.1 * Math.PI, 1.9 * Math.PI);
        } else {
            ctx.moveTo(cx - 15, 195);
            ctx.lineTo(cx + 15, 195);
        }
        ctx.stroke();
    }
    
    drawHand(ctx, keypoints, side) {
        if (!keypoints || keypoints.length < 21) return;
        
        // Transform keypoints to canvas coordinates
        const scale = 2.0;
        const baseX = side === 'right' ? 350 : 150;
        const baseY = 320;
        
        // Calculate center
        let cx = 0, cy = 0;
        keypoints.forEach(kp => { cx += kp.x; cy += kp.y; });
        cx /= 21; cy /= 21;
        
        // Transform points
        const pts = keypoints.map(kp => {
            let x = (kp.x - cx) * scale * 120;
            let y = (kp.y - cy) * scale * 120;
            if (side === 'left') x = -x;
            return { x: baseX + x, y: baseY + y, z: kp.z || 0 };
        });
        
        // Draw arm
        this.drawArm(ctx, pts[0], side);
        
        // Draw palm (solid, no patches)
        this.drawPalm(ctx, pts);
        
        // Draw all 5 fingers clearly
        this.drawFinger(ctx, pts, [1, 2, 3, 4], 12);      // Thumb
        this.drawFinger(ctx, pts, [5, 6, 7, 8], 10);      // Index
        this.drawFinger(ctx, pts, [9, 10, 11, 12], 10);   // Middle
        this.drawFinger(ctx, pts, [13, 14, 15, 16], 9);   // Ring
        this.drawFinger(ctx, pts, [17, 18, 19, 20], 8);   // Pinky
        
        // Draw joints
        this.drawJoints(ctx, pts);
        
        // Draw fingernails
        this.drawNails(ctx, pts);
    }
    
    drawArm(ctx, wrist, side) {
        const shoulderX = side === 'right' ? this.body.shoulderRightX : this.body.shoulderLeftX;
        const shoulderY = this.body.shoulderY;
        
        // Calculate elbow
        const dx = wrist.x - shoulderX;
        const dy = wrist.y - shoulderY;
        const angle = Math.atan2(dy, dx);
        const elbowX = shoulderX + Math.cos(angle) * 50;
        const elbowY = shoulderY + Math.sin(angle) * 50 + 15;
        
        ctx.save();
        ctx.lineCap = 'round';
        
        // Upper arm (sleeve)
        ctx.strokeStyle = '#2980B9';
        ctx.lineWidth = 24;
        ctx.beginPath();
        ctx.moveTo(shoulderX, shoulderY);
        ctx.lineTo(elbowX, elbowY);
        ctx.stroke();
        
        // Forearm (skin)
        ctx.strokeStyle = this.handConfig.skinColor;
        ctx.lineWidth = 20;
        ctx.beginPath();
        ctx.moveTo(elbowX, elbowY);
        ctx.lineTo(wrist.x, wrist.y);
        ctx.stroke();
        
        // Outline
        ctx.strokeStyle = this.handConfig.skinColorDark;
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.moveTo(elbowX, elbowY);
        ctx.lineTo(wrist.x, wrist.y);
        ctx.stroke();
        
        ctx.restore();
    }
    
    drawPalm(ctx, pts) {
        ctx.save();
        
        // Palm shape
        ctx.fillStyle = this.handConfig.skinColor;
        ctx.strokeStyle = this.handConfig.skinColorDark;
        ctx.lineWidth = 2;
        
        ctx.beginPath();
        ctx.moveTo(pts[0].x, pts[0].y);
        ctx.lineTo(pts[5].x, pts[5].y);
        ctx.lineTo(pts[9].x, pts[9].y);
        ctx.lineTo(pts[13].x, pts[13].y);
        ctx.lineTo(pts[17].x, pts[17].y);
        ctx.closePath();
        ctx.fill();
        ctx.stroke();
        
        ctx.restore();
    }
    
    drawFinger(ctx, pts, indices, baseWidth) {
        ctx.save();
        ctx.fillStyle = this.handConfig.skinColor;
        ctx.strokeStyle = this.handConfig.skinColorDark;
        ctx.lineWidth = 1.5;
        ctx.lineCap = 'round';
        
        for (let i = 0; i < indices.length - 1; i++) {
            const p1 = pts[indices[i]];
            const p2 = pts[indices[i + 1]];
            const width = baseWidth * (1 - i * 0.2);
            
            // Calculate perpendicular for segment width
            const angle = Math.atan2(p2.y - p1.y, p2.x - p1.x);
            const perpX = Math.cos(angle + Math.PI/2);
            const perpY = Math.sin(angle + Math.PI/2);
            
            const w1 = width / 2;
            const w2 = width * 0.4;
            
            // Draw tapered finger segment
            ctx.beginPath();
            ctx.moveTo(p1.x - perpX * w1, p1.y - perpY * w1);
            ctx.lineTo(p2.x - perpX * w2, p2.y - perpY * w2);
            ctx.lineTo(p2.x + perpX * w2, p2.y + perpY * w2);
            ctx.lineTo(p1.x + perpX * w1, p1.y + perpY * w1);
            ctx.closePath();
            ctx.fill();
            ctx.stroke();
        }
        
        ctx.restore();
    }
    
    drawJoints(ctx, pts) {
        ctx.save();
        
        for (let i = 1; i < 21; i++) {
            const pt = pts[i];
            const isTip = [4, 8, 12, 16, 20].includes(i);
            const radius = isTip ? 5 : 4;
            
            ctx.fillStyle = this.handConfig.jointColor;
            ctx.strokeStyle = this.handConfig.skinColorDark;
            ctx.lineWidth = 1;
            
            ctx.beginPath();
            ctx.arc(pt.x, pt.y, radius, 0, 2 * Math.PI);
            ctx.fill();
            ctx.stroke();
        }
        
        ctx.restore();
    }
    
    drawNails(ctx, pts) {
        const tips = [4, 8, 12, 16, 20];
        
        ctx.save();
        ctx.fillStyle = this.handConfig.nailColor;
        ctx.strokeStyle = this.handConfig.skinColorDark;
        ctx.lineWidth = 1;
        
        tips.forEach(i => {
            const tip = pts[i];
            const prev = pts[i - 1];
            const angle = Math.atan2(tip.y - prev.y, tip.x - prev.x);
            
            ctx.save();
            ctx.translate(tip.x, tip.y);
            ctx.rotate(angle);
            
            ctx.beginPath();
            ctx.ellipse(4, 0, 5, 3.5, 0, 0, 2 * Math.PI);
            ctx.fill();
            ctx.stroke();
            
            ctx.restore();
        });
        
        ctx.restore();
    }
    
    drawSignLabel(ctx, sign) {
        if (!sign) return;
        
        ctx.save();
        
        // Label background
        ctx.fillStyle = 'rgba(44, 62, 80, 0.9)';
        ctx.beginPath();
        ctx.roundRect(175, 460, 150, 30, 8);
        ctx.fill();
        
        // Label text
        ctx.fillStyle = '#FFFFFF';
        ctx.font = 'bold 16px Poppins, sans-serif';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(sign, 250, 475);
        
        ctx.restore();
    }
    
    // Play animation
    play(frames) {
        this.frames = frames;
        this.currentFrame = 0;
        this.isPlaying = true;
        this.animate();
    }
    
    animate() {
        if (!this.isPlaying || this.currentFrame >= this.frames.length) {
            this.isPlaying = false;
            return;
        }
        
        this.drawFrame(this.frames[this.currentFrame]);
        this.currentFrame++;
        
        this.animationId = setTimeout(() => this.animate(), 1000 / this.fps);
    }
    
    stop() {
        this.isPlaying = false;
        if (this.animationId) {
            clearTimeout(this.animationId);
        }
    }
}

// Export for use
window.ISLHandAnimator = ISLHandAnimator;
