import os
from PIL import Image
import numpy as np

img1_path = r"C:\Users\Kent\.gemini\antigravity\brain\072a3b75-c43c-4b8d-9bef-f0396b7cafdf\pixel_monk_closed_1776309589763.png"
img2_path = r"C:\Users\Kent\.gemini\antigravity\brain\072a3b75-c43c-4b8d-9bef-f0396b7cafdf\pixel_monk_open_1776309602931.png"

def get_content_bbox(img):
    arr = np.array(img.convert("RGBA"))
    is_bg = np.all(arr[:, :, :3] > 230, axis=2)
    non_bg_rows = np.any(~is_bg, axis=1)
    non_bg_cols = np.any(~is_bg, axis=0)
    
    if not np.any(non_bg_rows):
        return (0, 0, img.width, img.height)
        
    row_indices = np.where(non_bg_rows)[0]
    col_indices = np.where(non_bg_cols)[0]
    
    ymin, ymax = row_indices[0], row_indices[-1]
    xmin, xmax = col_indices[0], col_indices[-1]
    return (xmin, ymin, xmax + 1, ymax + 1)

img1 = Image.open(img1_path)
img2 = Image.open(img2_path)

bbox1 = get_content_bbox(img1)
bbox2 = get_content_bbox(img2)

cropped1 = img1.crop(bbox1)
cropped2 = img2.crop(bbox2)

w1, h1 = cropped1.size
w2, h2 = cropped2.size

tgt_w = max(w1, w2)
tgt_h = max(h1, h2)

# Create a new padded image for both so they match in size exactly
final1 = Image.new("RGBA", (tgt_w, tgt_h), (255, 255, 255, 255))
final2 = Image.new("RGBA", (tgt_w, tgt_h), (255, 255, 255, 255))

final1.paste(cropped1, ((tgt_w - w1) // 2, tgt_h - h1))
final2.paste(cropped2, ((tgt_w - w2) // 2, tgt_h - h2))

# Now merge side-by-side
merged = Image.new("RGBA", (tgt_w * 2, tgt_h), (255, 255, 255, 255))
merged.paste(final1, (0, 0))
merged.paste(final2, (tgt_w, 0))

out_path = r"f:\AntiGravity\Slideshow\merged_monk.png"
merged.save(out_path)
print("Merged image saved to", out_path)
