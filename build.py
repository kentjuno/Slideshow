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
        const frameInterval = {frame_interval}; // Tốc độ (ms)

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
            width: 300px;
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
            let dx = targetX - posX;
            let dy = targetY - posY;
            let dist = Math.sqrt(dx*dx + dy*dy);
            
            if (dist < 50) {
                targetX = Math.random() * (window.innerWidth - 100);
                targetY = Math.random() * (window.innerHeight - 100);
                speed = 1.0 + Math.random(); // Vary speed slightly
            }
            
            posX += (dx / dist) * speed;
            posY += (dy / dist) * speed;
            
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
