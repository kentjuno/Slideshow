import os
from PIL import Image
import numpy as np

img_path = r"C:\Users\Kent\.gemini\antigravity\brain\072a3b75-c43c-4b8d-9bef-f0396b7cafdf\pixel_monk_spritesheet_1776309460374.png"
img = Image.open(img_path).convert("RGBA")
arr = np.array(img)

is_background = np.all(arr[:, :, :3] > 230, axis=2)
non_bg_rows = np.any(~is_background, axis=1)
non_bg_cols = np.any(~is_background, axis=0)

row_indices = np.where(non_bg_rows)[0]
col_indices = np.where(non_bg_cols)[0]

min_y, max_y = row_indices[0], row_indices[-1]
min_x, max_x = col_indices[0], col_indices[-1]

# Crop out the main content
cropped_arr = arr[min_y:max_y+1, min_x:max_x+1]
cropped_is_bg = np.all(cropped_arr[:, :, :3] > 230, axis=2)

# Check if stacked vertically or horizontally by finding empty gaps
# Let's project sum of non-bg pixels
row_sum = np.sum(~cropped_is_bg, axis=1)
col_sum = np.sum(~cropped_is_bg, axis=0)

# Find gap in rows and cols (where sum == 0)
gap_rows = np.where(row_sum == 0)[0]
gap_cols = np.where(col_sum == 0)[0]

out_path = "f:\\AntiGravity\\Slideshow\\fixed_monk.png"

# Assuming we either find a gap or just split in half based on aspect ratio
height, width = cropped_arr.shape[:2]

if height > width * 1.5:
    # Stacked vertically! Split at height // 2
    f1 = cropped_arr[:height//2, :]
    f2 = cropped_arr[height//2:, :]
    # Make them same size
    h1 = f1.shape[0]
    h2 = f2.shape[0]
    max_h = max(h1, h2)
    new_img = Image.new('RGBA', (width * 2, max_h), (255, 255, 255, 255))
    new_img.paste(Image.fromarray(f1), (0, 0))
    new_img.paste(Image.fromarray(f2), (width, 0))
    new_img.save(out_path)
    print("Vertical stack merged to horizontal. Saved to", out_path)
elif width > height * 1.5:
    # Stacked horizontally, just save cropped
    f1 = cropped_arr[:, :width//2]
    f2 = cropped_arr[:, width//2:]
    Image.fromarray(cropped_arr).save(out_path)
    print("Horizontal stack. Saved to", out_path)
else:
    # Just in case, assume it's just fine or needs 50/50 split
    if height > width:
        f1 = cropped_arr[:height//2, :]
        f2 = cropped_arr[height//2:, :]
        new_img = Image.new('RGBA', (width * 2, height//2), (255, 255, 255, 255))
        new_img.paste(Image.fromarray(f1), (0, 0))
        new_img.paste(Image.fromarray(f2), (width, 0))
        new_img.save(out_path)
        print("Fallback verical merge.", out_path)
    else:
        Image.fromarray(cropped_arr).save(out_path)
        print("Fallback save", out_path)
