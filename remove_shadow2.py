import numpy as np
from PIL import Image

img = np.array(Image.open('merged_3frames.png').convert('RGBA'))
h, w, c = img.shape
out_img = img.copy()

# Background is exactly white or very close
for y in range(h):
    for x in range(w):
        r, g, b, a = img[y, x]
        if max(r,g,b) - min(r,g,b) < 10 and max(r,g,b) > 230:
            out_img[y, x, 3] = 0

# The outline has maxC < 55 at the bottom.
# To safely remove the shadow, we can just erase any pixel that is below the bottom-most outline pixel!
for x in range(w):
    # Find the lowest black outline pixel in this column
    lowest_outline = -1
    for y in range(h-1, -1, -1):
        if out_img[y, x, 3] != 0:
            r, g, b, a = out_img[y, x]
            if max(r, g, b) < 55: # It's a dark outline pixel!
                lowest_outline = y
                break
    
    # Now erase anything BELOW the lowest outline pixel!
    if lowest_outline != -1:
        for y in range(lowest_outline + 1, h):
            out_img[y, x, 3] = 0

Image.fromarray(out_img).save('merged_3frames_noshadow2.png')
print("Saved merged_3frames_noshadow2.png")
