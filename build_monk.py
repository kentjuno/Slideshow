import base64
import os

def build_monk_butterfly():
    monk_img_path = r"f:\AntiGravity\Slideshow\merged_3frames_noshadow2.png"
    butterfly_img_path = r"C:\Users\Kent\.gemini\antigravity\brain\072a3b75-c43c-4b8d-9bef-f0396b7cafdf\butterfly_spritesheet_1776296992762.png"
    
    with open(monk_img_path, "rb") as f:
        monk_b64 = "data:image/png;base64," + base64.b64encode(f.read()).decode('utf-8')
        
    with open(butterfly_img_path, "rb") as f:
        butterfly_b64 = "data:image/png;base64," + base64.b64encode(f.read()).decode('utf-8')
        
    html = f"""<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OBS Monk and Butterfly</title>
    <style>
        body, html {{ margin: 0; padding: 0; width: 100vw; height: 100vh; overflow: hidden; background-color: transparent; }}
        
        #monk-container {{
            position: absolute;
            bottom: -5px; /* Giống con mèo ban đầu */
            left: 50%;
            transform: translateX(-50%);
            width: 250px; /* Kích thước tương đối */
            z-index: 9998;
        }}
        
        #butterfly-container {{
            position: absolute;
            width: 60px;
            z-index: 9999;
        }}
        
        canvas {{
            width: 100%;
            height: auto;
            image-rendering: -moz-crisp-edges;
            image-rendering: -webkit-optimize-contrast;
            image-rendering: pixelated; 
        }}
    </style>
</head>
<body>
    <div id="monk-container"><canvas id="monk-canvas"></canvas></div>
    <div id="butterfly-container"><canvas id="butterfly-canvas"></canvas></div>

    <script>
        // Utilities to process sprites
        function loadProcessedSprite(b64Data, totalFrames, useFloodFill, callback) {{
            const img = new Image();
            img.src = b64Data;
            img.onload = function() {{
                const frameWidth = img.width / totalFrames; 
                const frameHeight = img.height;
                const tempCanvas = document.createElement('canvas');
                tempCanvas.width = frameWidth;
                tempCanvas.height = frameHeight;
                const ctx = tempCanvas.getContext('2d', {{ willReadFrequently: true }});
                
                let framesLoaded = 0;
                const processedFrames = [];
                
                for(let i = 0; i < totalFrames; i++) {{
                    ctx.clearRect(0,0, frameWidth, frameHeight);
                    ctx.drawImage(img, i * frameWidth, 0, frameWidth, frameHeight, 0, 0, frameWidth, frameHeight);
                    
                    const imageData = ctx.getImageData(0, 0, frameWidth, frameHeight);
                    const data = imageData.data;
                    
                    if (useFloodFill) {{
                        const width = frameWidth;
                        const height = frameHeight;
                        const visited = new Uint8Array(width * height);
                        const stackX = [0];
                        const stackY = [0];
                        
                        while (stackX.length > 0) {{
                            const x = stackX.pop();
                            const y = stackY.pop();
                            const idx = y * width + x;
                            
                            if (visited[idx]) continue;
                            visited[idx] = 1;
                            
                            const p = idx * 4;
                            if (data[p] > 230 && data[p+1] > 230 && data[p+2] > 230) {{
                                data[p+3] = 0; 
                                if (x > 0 && !visited[idx - 1]) {{ stackX.push(x - 1); stackY.push(y); }}
                                if (x < width - 1 && !visited[idx + 1]) {{ stackX.push(x + 1); stackY.push(y); }}
                                if (y > 0 && !visited[idx - width]) {{ stackX.push(x); stackY.push(y - 1); }}
                                if (y < height - 1 && !visited[idx + width]) {{ stackX.push(x); stackY.push(y + 1); }}
                            }}
                        }}
                        
                        // Protect internal white pixels from OBS Color Key filter
                        for (let j = 0; j < data.length; j += 4) {{
                            if (data[j+3] !== 0) {{ // Nếu pixel này chưa bị xoá (tức là nằm bên trong nhân vật)
                                if (data[j] > 220 && data[j+1] > 220 && data[j+2] > 220) {{
                                    data[j] = 210;
                                    data[j+1] = 210;
                                    data[j+2] = 220; // Màu trắng ngà hơi xanh xám để OBS ko nhận diện là trắng xoá
                                }}
                            }}
                        }}
                    }} else {{
                        for (let j = 0; j < data.length; j += 4) {{
                            if (data[j] > 230 && data[j+1] > 230 && data[j+2] > 230) {{
                                data[j+3] = 0; 
                            }}
                        }}
                    }}
                    ctx.putImageData(imageData, 0, 0);
                    
                    const frameImg = new Image();
                    frameImg.onload = () => {{
                        framesLoaded++;
                        if (framesLoaded === totalFrames) {{
                            callback(processedFrames, frameWidth, frameHeight);
                        }}
                    }};
                    frameImg.src = tempCanvas.toDataURL("image/png");
                    processedFrames.push(frameImg);
                }}
            }};
        }}

        // Setup Monk
        const monkCanvas = document.getElementById('monk-canvas');
        const monkCtx = monkCanvas.getContext('2d');
        let monkFrames = [];
        let monkAttentive = false;

        let monkCurrentFrame = 0;
        let monkLastFrameTime = 0;

        loadProcessedSprite("{monk_b64}", 3, true, (frames, w, h) => {{
            monkFrames = frames;
            monkCanvas.width = w;
            monkCanvas.height = h;
            requestAnimationFrame(drawMonk);
        }});

        function drawMonk(now) {{
            if (monkFrames.length > 0) {{
                if (!monkLastFrameTime) monkLastFrameTime = now;
                let targetFrame = monkAttentive ? 2 : 0;
                
                if (now - monkLastFrameTime > 80) {{
                    if (monkCurrentFrame < targetFrame) monkCurrentFrame++;
                    else if (monkCurrentFrame > targetFrame) monkCurrentFrame--;
                    monkLastFrameTime = now;
                }}
                
                monkCtx.clearRect(0, 0, monkCanvas.width, monkCanvas.height);
                monkCtx.drawImage(monkFrames[monkCurrentFrame], 0, 0);
            }}
            requestAnimationFrame(drawMonk);
        }}

        // Setup Butterfly
        const butterflyContainer = document.getElementById('butterfly-container');
        const bfCanvas = document.getElementById('butterfly-canvas');
        const bfCtx = bfCanvas.getContext('2d');
        let bfFrames = [];
        let bfCurrentFrame = 0;
        let bfLastFrameTime = 0;

        let bPosX = Math.random() * window.innerWidth;
        let bPosY = Math.random() * window.innerHeight;
        let bTargetX = Math.random() * window.innerWidth;
        let bTargetY = Math.random() * window.innerHeight;
        let bSpeed = 1.5;

        // Butterfly states: 'wander' (random targets), 'visit' (flies around monk)
        let bfState = 'wander'; 
        let visitTargetCount = 0;

        function getWanderTarget() {{
            let maxW = window.innerWidth || 1920;
            let maxH = window.innerHeight || 1080;
            return {{ x: Math.random() * (maxW-100), y: Math.random() * (maxH-100) }};
        }}

        function getVisitTarget() {{
            // Monk is at bottom center: x = innerWidth/2, y = innerHeight - 150
            let maxW = window.innerWidth || 1920;
            let maxH = window.innerHeight || 1080;
            let monkCenter = {{ x: maxW / 2, y: maxH - 150 }};
            return {{ 
                x: monkCenter.x - 150 + Math.random() * 300, 
                y: monkCenter.y - 250 + Math.random() * 150 
            }};
        }}

        loadProcessedSprite("{butterfly_b64}", 3, false, (frames, w, h) => {{
            bfFrames = frames;
            bfCanvas.width = w;
            bfCanvas.height = h;
            requestAnimationFrame(updateButterfly);
        }});

        function updateButterfly(now) {{
            // Animation Frames
            if (!bfLastFrameTime) bfLastFrameTime = now;
            const elapsed = now - bfLastFrameTime;
            if (elapsed > 100) {{
                bfCurrentFrame = (bfCurrentFrame + 1) % bfFrames.length;
                bfLastFrameTime = now - (elapsed % 100);
            }}

            if (bfFrames.length > 0) {{
                bfCtx.clearRect(0, 0, bfCanvas.width, bfCanvas.height);
                bfCtx.drawImage(bfFrames[bfCurrentFrame], 0, 0);
            }}

            // Movement Logic
            let maxW = window.innerWidth || 1920;
            let maxH = window.innerHeight || 1080;
            
            let dx = bTargetX - bPosX;
            let dy = bTargetY - bPosY;
            let dist = Math.sqrt(dx*dx + dy*dy);

            // Monk interaction logic: where is the butterfly relative to the monk?
            let distToMonk = Math.sqrt(Math.pow(Math.abs(bPosX - maxW/2), 2) + Math.pow(Math.abs(bPosY - (maxH - 150)), 2));
            monkAttentive = distToMonk < 350; // Look up if butterfly is near

            if (dist < 50) {{
                if (bfState === 'wander') {{
                    if (Math.random() < 0.35) {{ // 35% chance to go visit monk after reaching a target
                        bfState = 'visit';
                        visitTargetCount = 3 + Math.floor(Math.random() * 5); // fly 3-7 targets around monk
                        let n = getVisitTarget();
                        bTargetX = n.x; bTargetY = n.y;
                    }} else {{
                        let n = getWanderTarget();
                        bTargetX = n.x; bTargetY = n.y;
                    }}
                }} else if (bfState === 'visit') {{
                    visitTargetCount--;
                    if (visitTargetCount <= 0) {{
                        bfState = 'wander';
                        let n = getWanderTarget();
                        bTargetX = n.x; bTargetY = n.y;
                    }} else {{
                        let n = getVisitTarget();
                        bTargetX = n.x; bTargetY = n.y;
                    }}
                }}
                bSpeed = 1.0 + Math.random() * 1.5; 
            }}
            
            if (dist > 0.001) {{
                bPosX += (dx / dist) * bSpeed;
                bPosY += (dy / dist) * bSpeed;
            }}

            if (isNaN(bPosX) || isNaN(bPosY)) {{
                bPosX = maxW / 2; bPosY = maxH / 2;
                bTargetX = bPosX; bTargetY = bPosY;
            }}
            bPosX = Math.max(-100, Math.min(bPosX, maxW + 100));
            bPosY = Math.max(-100, Math.min(bPosY, maxH + 100));
            
            let flip = dx < 0 ? -1 : 1; 
            let wiggleY = Math.sin(Date.now() / 150) * 8;
            
            butterflyContainer.style.left = bPosX + 'px';
            butterflyContainer.style.top = (bPosY + wiggleY) + 'px';
            butterflyContainer.style.transform = `scaleX(${{flip}})`;

            requestAnimationFrame(updateButterfly);
        }}
    </script>
</body>
</html>
"""
    output_path = r"f:\AntiGravity\Slideshow\monk_butterfly.html"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    print("Done generating", output_path)

if __name__ == "__main__":
    build_monk_butterfly()
