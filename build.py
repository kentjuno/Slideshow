import base64
import os

def build_html(image_path, output_html, total_frames, frame_interval, animation_css, container_css, canvas_css, title, custom_js=""):
    with open(image_path, "rb") as img_file:
        b64_string = base64.b64encode(img_file.read()).decode('utf-8')
        b64_data_uri = f"data:image/png;base64,{b64_string}"

    html_content = f"""<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body, html {{
            margin: 0; padding: 0; width: 100vw; height: 100vh; overflow: hidden; background-color: transparent;
        }}

        #animation-container {{
            {container_css}
        }}

        canvas {{
            {canvas_css}
        }}

        {animation_css}
    </style>
</head>
<body>
    <div id="animation-container">
        <!-- Sử dụng HTML5 Canvas để chiếu Sprite Sheet Animation -->
        <canvas id="animation-canvas"></canvas>
    </div>

    <script>
        const canvas = document.getElementById('animation-canvas');
        const ctx = canvas.getContext('2d', {{ willReadFrequently: true }});
        
        // Nhúng nguyên tệp ảnh vào mã để bỏ qua hoàn toàn lỗi CORS của Browser
        const b64Data = "{b64_data_uri}";
        
        const img = new Image();
        img.src = b64Data;
        
        const totalFrames = {total_frames};
        let currentFrame = 0;
        let lastFrameTime = 0;
        let frameInterval = {frame_interval}; // Tốc độ (ms)

        img.onload = function() {{
            const frameWidth = img.width / totalFrames; 
            const frameHeight = img.height;
            
            canvas.width = frameWidth;
            canvas.height = frameHeight;
            
            // Xóa nền trắng và lưu từng khung hình (frame)
            const transparentFrames = [];
            let framesLoaded = 0;
            
            for(let i = 0; i < totalFrames; i++) {{
                ctx.clearRect(0,0, canvas.width, canvas.height);
                ctx.drawImage(img, i * frameWidth, 0, frameWidth, frameHeight, 0, 0, frameWidth, frameHeight);
                
                const imageData = ctx.getImageData(0, 0, frameWidth, frameHeight);
                const data = imageData.data;
                for (let j = 0; j < data.length; j += 4) {{
                    // Xóa hoàn toàn điểm mầu Trắng -> Alpha = 0
                    // Cho phép sai số một chút ở vùng rìa chống răng cưa
                    if (data[j] > 230 && data[j+1] > 230 && data[j+2] > 230) {{
                        data[j+3] = 0; 
                    }}
                }}
                ctx.putImageData(imageData, 0, 0);
                
                const frameImg = new Image();
                frameImg.onload = () => {{
                    framesLoaded++;
                    if (framesLoaded === totalFrames) {{
                        requestAnimationFrame(animate);
                    }}
                }};
                frameImg.src = canvas.toDataURL("image/png");
                transparentFrames.push(frameImg);
            }}

            function animate(now) {{
                if (!lastFrameTime) lastFrameTime = now;
                const elapsed = now - lastFrameTime;
                
                if (elapsed > frameInterval) {{
                    currentFrame = (currentFrame + 1) % totalFrames;
                    lastFrameTime = now - (elapsed % frameInterval);
                }}
                
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                ctx.drawImage(transparentFrames[currentFrame], 0, 0);
                
                requestAnimationFrame(animate);
            }}
        }};
        
        {custom_js}
    </script>
</body>
</html>"""

    with open(output_html, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"Bypass CORS success and rewrite {output_html} complete!")


# ==============================================================
# 1. Build Cat
# ==============================================================
cat_image = r"C:\Users\Kent\.gemini\antigravity\brain\072a3b75-c43c-4b8d-9bef-f0396b7cafdf\cat_spritesheet_1776295699736.png"
cat_output = r"f:\AntiGravity\Slideshow\cat.html"
cat_container = """
            position: absolute;
            bottom: -5px; /* Ép sát đáy màn hình + ăn gian 5px để chân đạp đất thật hơn */
            left: -350px;
            width: 150px;
            animation: walk-across 30s linear infinite;
            z-index: 9999;
"""
cat_canvas = """
            width: 80%;
            height: auto;
            image-rendering: -moz-crisp-edges;
            image-rendering: -webkit-optimize-contrast;
            image-rendering: pixelated; 
"""
cat_anim = """
        @keyframes walk-across {
            0%   { left: -350px; transform: scaleX(1); }
            45%  { left: 110vw; transform: scaleX(1); }
            50%  { left: 110vw; transform: scaleX(-1); }
            95%  { left: -350px; transform: scaleX(-1); }
            100% { left: -350px; transform: scaleX(1); }
        }
"""
build_html(cat_image, cat_output, 4, 200, cat_anim, cat_container, cat_canvas, "OBS Cat Overlay 24/7")

# ==============================================================
# 2. Build Butterfly
# ==============================================================
butterfly_image = r"C:\Users\Kent\.gemini\antigravity\brain\072a3b75-c43c-4b8d-9bef-f0396b7cafdf\butterfly_spritesheet_1776296992762.png"
butterfly_output = r"f:\AntiGravity\Slideshow\butterfly.html"
butterfly_container = """
            position: absolute;
            width: 60px; /* Nhỏ hơn, dễ thương hơn */
            z-index: 9998;
"""
butterfly_canvas = """
            width: 100%;
            height: auto;
            image-rendering: -moz-crisp-edges;
            image-rendering: -webkit-optimize-contrast;
            image-rendering: pixelated; 
"""
butterfly_anim = ""
butterfly_js = """
        const butterflyContainer = document.getElementById('animation-container');
        let posX = Math.random() * window.innerWidth;
        let posY = Math.random() * window.innerHeight;
        let targetX = Math.random() * window.innerWidth;
        let targetY = Math.random() * window.innerHeight;
        let speed = 1.5;

        function updateFly() {
            let maxW = window.innerWidth || 1920;
            let maxH = window.innerHeight || 1080;
            
            let dx = targetX - posX;
            let dy = targetY - posY;
            let dist = Math.sqrt(dx*dx + dy*dy);
            
            if (dist < 50) {
                targetX = Math.random() * (maxW - 100);
                targetY = Math.random() * (maxH - 100);
                speed = 1.0 + Math.random(); // Vary speed slightly
            }
            
            if (dist > 0.001) {
                posX += (dx / dist) * speed;
                posY += (dy / dist) * speed;
            }

            // Boundary safeguard
            if (isNaN(posX) || isNaN(posY)) {
                posX = maxW / 2; posY = maxH / 2;
            }
            posX = Math.max(-100, Math.min(posX, maxW + 100));
            posY = Math.max(-100, Math.min(posY, maxH + 100));
            
            let flip = dx < 0 ? -1 : 1; 

            // Lắc lư nhẹ nhàng
            let wiggleY = Math.sin(Date.now() / 150) * 8;
            
            butterflyContainer.style.left = posX + 'px';
            butterflyContainer.style.top = (posY + wiggleY) + 'px';
            butterflyContainer.style.transform = `scaleX(${flip})`;

            requestAnimationFrame(updateFly);
        }
        requestAnimationFrame(updateFly);
"""
build_html(butterfly_image, butterfly_output, 3, 100, butterfly_anim, butterfly_container, butterfly_canvas, "OBS Butterfly Overlay 24/7", butterfly_js)


# ==============================================================
# 3. Build Cat Chasing
# ==============================================================
catchasing_image = r"C:\Users\Kent\.gemini\antigravity\brain\072a3b75-c43c-4b8d-9bef-f0396b7cafdf\cat_pouncing_spritesheet_1776297974601.png"
catchasing_output = r"f:\AntiGravity\Slideshow\catchasing.html"
catchasing_container = """
            position: absolute;
            width: 100px; /* Bằng 1/2 ban đầu */
            z-index: 9999;
"""
catchasing_canvas = """
            width: 100%;
            height: auto;
            image-rendering: -moz-crisp-edges;
            image-rendering: -webkit-optimize-contrast;
            image-rendering: pixelated; 
"""
catchasing_anim = ""
catchasing_js = """
        const catContainer = document.getElementById('animation-container');
        let posX = Math.random() * (window.innerWidth || 1920);
        let posY = Math.random() * (window.innerHeight || 1080);
        let targetX = posX;
        let targetY = posY;
        let state = 'run'; // 'run', 'prepare', 'pounce'
        let speed = 0.4; 

        function getNewTarget() {
            let maxW = (window.innerWidth || 1920) - 100;
            let maxH = (window.innerHeight || 1080) - 100;
            if (maxW < 0) maxW = 0;
            if (maxH < 0) maxH = 0;
            return {
                x: Math.random() * maxW,
                y: Math.random() * maxH
            };
        }

        let newT = getNewTarget();
        targetX = newT.x;
        targetY = newT.y;

        function updateChase() {
            let maxW = window.innerWidth || 1920;
            let maxH = window.innerHeight || 1080;

            let dx = targetX - posX;
            let dy = targetY - posY;
            let dist = Math.sqrt(dx*dx + dy*dy);
            
            // Fix overshoot bằng cách xem dist có bé hơn speed (khoảng cách vừa nhảy) không
            let reachedTarget = dist <= Math.max(speed, 5); 

            if (state === 'run') {
                frameInterval = 250; 
                if (reachedTarget) {
                    posX = targetX;
                    posY = targetY;
                    
                    let n = getNewTarget();
                    targetX = n.x;
                    targetY = n.y;
                    
                    if (Math.random() < 0.8) {
                        state = 'prepare';
                        speed = 0; 
                        frameInterval = 999999; 
                        setTimeout(() => {
                            state = 'pounce';
                            frameInterval = 50; 
                            speed = 15 + Math.random() * 15; 
                        }, 2000); 
                    } else {
                        // Reset lại tốc độ lén lút
                        speed = 0.2 + Math.random() * 0.4;
                    }
                } else if (dist > 0.001) {
                    posX += (dx / dist) * speed;
                    posY += (dy / dist) * speed;
                }
            } else if (state === 'pounce') {
                if (reachedTarget) {
                    posX = targetX;
                    posY = targetY;
                    state = 'run';
                    // QUAN TRỌNG: Trả lại tốc độ chậm đi bộ sau khi vồ tới nơi
                    speed = 0.2 + Math.random() * 0.4; 
                    
                    let n = getNewTarget();
                    targetX = n.x;
                    targetY = n.y;
                } else if (dist > 0.001) {
                    posX += (dx / dist) * speed;
                    posY += (dy / dist) * speed;
                }
            }
            
            // Safety bounds to prevent flying out of screen forever
            if (isNaN(posX) || isNaN(posY)) {
                posX = maxW / 2; posY = maxH / 2;
                let n = getNewTarget();
                targetX = n.x; targetY = n.y;
            }
            posX = Math.max(-100, Math.min(posX, maxW + 100));
            posY = Math.max(-100, Math.min(posY, maxH + 100));
            
            let flip = (dx >= 0) ? 1 : -1; 
            
            let angle = 0;
            if (state === 'pounce') {
                angle = Math.atan2(dy, Math.abs(dx)) * 180 / Math.PI;
            }
            
            catContainer.style.left = posX + 'px';
            catContainer.style.top = posY + 'px';
            catContainer.style.transform = `scaleX(${flip}) rotate(${angle}deg)`;

            requestAnimationFrame(updateChase);
        }
        requestAnimationFrame(updateChase);
"""

build_html(catchasing_image, catchasing_output, 4, 100, catchasing_anim, catchasing_container, catchasing_canvas, "OBS Cat Chasing 24/7", catchasing_js)
