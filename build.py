import base64
import os

image_path = r"C:\Users\Kent\.gemini\antigravity\brain\072a3b75-c43c-4b8d-9bef-f0396b7cafdf\cat_spritesheet_1776295699736.png"
output_html = r"f:\AntiGravity\Slideshow\cat.html"

with open(image_path, "rb") as img_file:
    b64_string = base64.b64encode(img_file.read()).decode('utf-8')
    b64_data_uri = f"data:image/png;base64,{b64_string}"

html_content = f"""<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OBS Cat Overlay 24/7</title>
    <style>
        body, html {{
            margin: 0; padding: 0; width: 100vw; height: 100vh; overflow: hidden; background-color: transparent;
        }}

        #cat-container {{
            position: absolute;
            bottom: -5px; /* Ép sát đáy màn hình + ăn gian 5px để chân đạp đất thật hơn */
            left: -350px;
            width: 300px;
            animation: walk-across 30s linear infinite;
            z-index: 9999;
        }}

        canvas {{
            width: 100%;
            height: auto;
            image-rendering: -moz-crisp-edges;
            image-rendering: -webkit-optimize-contrast;
            image-rendering: pixelated; 
        }}

        @keyframes walk-across {{
            0%   {{ left: -350px; transform: scaleX(1); }}
            45%  {{ left: 110vw; transform: scaleX(1); }}
            50%  {{ left: 110vw; transform: scaleX(-1); }}
            95%  {{ left: -350px; transform: scaleX(-1); }}
            100% {{ left: -350px; transform: scaleX(1); }}
        }}
    </style>
</head>
<body>
    <div id="cat-container">
        <!-- Sử dụng HTML5 Canvas để chiếu Sprite Sheet Animation -->
        <canvas id="cat-canvas"></canvas>
    </div>

    <script>
        const canvas = document.getElementById('cat-canvas');
        const ctx = canvas.getContext('2d', {{ willReadFrequently: true }});
        
        // Nhúng nguyên tệp ảnh vào mã để bỏ qua hoàn toàn lỗi CORS của Browser
        const b64Data = "{b64_data_uri}";
        
        const img = new Image();
        img.src = b64Data;
        
        // AI tạo ra 1 tấm ảnh chứa 4 bước đi của mèo (Sprite Sheet 4 frames)
        const totalFrames = 4;
        let currentFrame = 0;
        let lastFrameTime = 0;
        const frameInterval = 200; // Tốc độ bước chân (ms)

        img.onload = function() {{
            const frameWidth = img.width / totalFrames; // Cắt ảnh làm 4
            const frameHeight = img.height;
            
            canvas.width = frameWidth;
            canvas.height = frameHeight;
            
            // Xóa nền trắng và lưu từng khung hình (frame)
            const transparentFrames = [];
            let framesLoaded = 0;
            
            for(let i = 0; i < totalFrames; i++) {{
                ctx.clearRect(0,0, canvas.width, canvas.height);
                // Vẽ 1 khúc của tấm ảnh dài (1 khung hình)
                ctx.drawImage(img, i * frameWidth, 0, frameWidth, frameHeight, 0, 0, frameWidth, frameHeight);
                
                const imageData = ctx.getImageData(0, 0, frameWidth, frameHeight);
                const data = imageData.data;
                for (let j = 0; j < data.length; j += 4) {{
                    // Xóa hoàn toàn điểm mầu Trắng -> Alpha = 0
                    if (data[j] > 230 && data[j+1] > 230 && data[j+2] > 230) {{
                        data[j+3] = 0; 
                    }}
                }}
                ctx.putImageData(imageData, 0, 0);
                
                const frameImg = new Image();
                frameImg.onload = () => {{
                    framesLoaded++;
                    // Nếu đã xử lý nền xong 4 khung hình thì chạy Animation
                    if (framesLoaded === totalFrames) {{
                        requestAnimationFrame(animate);
                    }}
                }};
                frameImg.src = canvas.toDataURL("image/png");
                transparentFrames.push(frameImg);
            }}

            // Vòng lặp liên tục phát các khung hình như video
            function animate(now) {{
                if (!lastFrameTime) lastFrameTime = now;
                const elapsed = now - lastFrameTime;
                
                // Đổi Frame
                if (elapsed > frameInterval) {{
                    currentFrame = (currentFrame + 1) % totalFrames;
                    lastFrameTime = now - (elapsed % frameInterval);
                }}
                
                // Lau canvas và Vẽ khung hình hiện tại
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                ctx.drawImage(transparentFrames[currentFrame], 0, 0);
                
                requestAnimationFrame(animate);
            }}
        }};
    </script>
</body>
</html>"""

with open(output_html, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Bypass CORS success and rewrite {output_html} complete!")
