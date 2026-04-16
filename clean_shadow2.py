import numpy as np
from PIL import Image

img = np.array(Image.open('merged_3frames.png').convert('RGBA'))
h, w, c = img.shape

# Background is white
diff = np.abs(img[:, :, :3] - [255, 255, 255])
bg_mask = np.max(diff, axis=2) < 10

fg_mask = ~bg_mask

frames = w // 258

for i in range(frames):
    x_start = i * 258
    x_end = (i + 1) * 258
    
    frame_fg = fg_mask[:, x_start:x_end]
    fh, fw = frame_fg.shape
    
    visited = np.zeros_like(frame_fg, dtype=bool)
    components = []
    
    # BFS to find connected components
    for y in range(fh):
        for x in range(fw):
            if frame_fg[y, x] and not visited[y, x]:
                comp_pixels = []
                q = [(y, x)]
                visited[y, x] = True
                
                head = 0
                while head < len(q):
                    cy, cx = q[head]
                    head += 1
                    comp_pixels.append((cy, cx + x_start))
                    
                    for dy, dx in [(-1,0), (1,0), (0,-1), (0,1)]:
                        ny, nx = cy + dy, cx + dx
                        if 0 <= ny < fh and 0 <= nx < fw:
                            if frame_fg[ny, nx] and not visited[ny, nx]:
                                visited[ny, nx] = True
                                q.append((ny, nx))
                
                components.append(comp_pixels)
    
    if len(components) == 0: continue
    
    # Keep the largest component, zero out the rest
    components.sort(key=len, reverse=True)
    main_comp = set(components[0])
    
    for comp in components[1:]:
        for cy, cx in comp:
            img[cy, cx] = [0, 0, 0, 0]

Image.fromarray(img).save('merged_3frames_clean.png')
print("Successfully cleaned.")
