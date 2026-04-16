import numpy as np
from PIL import Image

img = np.array(Image.open('merged_3frames.png').convert('RGBA'))

# Copy to modify
out_img = img.copy()

h, w, c = out_img.shape

for y in range(h):
    for x in range(w):
        r, g, b, a = out_img[y, x]
        if a == 0: continue
        
        # calculate max and min using built in max/min
        mx = max(r, g, b)
        mn = min(r, g, b)
        
        # Shadow target: maxC - minC < 25 (desaturated), maxC > 55 (lighter than outline), maxC < 140 (darker than cushion)
        if (mx - mn) < 25 and 55 < mx < 130:
            out_img[y, x, 3] = 0 # set alpha to 0

Image.fromarray(out_img).save('merged_3frames_noshadow.png')
print("Saved merged_3frames_noshadow.png")
