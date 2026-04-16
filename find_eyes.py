from PIL import Image
import numpy as np

img_path = r"C:\Users\Kent\.gemini\antigravity\brain\072a3b75-c43c-4b8d-9bef-f0396b7cafdf\pixel_monk_closed_1776309589763.png"
img = Image.open(img_path).convert("RGBA")
arr = np.array(img)

# Find non-white bounds (character bounds)
is_bg = np.all(arr[:, :, :3] > 230, axis=2)
non_bg_rows = np.any(~is_bg, axis=1)
non_bg_cols = np.any(~is_bg, axis=0)

ymin, ymax = np.where(non_bg_rows)[0][[0, -1]]
xmin, xmax = np.where(non_bg_cols)[0][[0, -1]]

print(f"Character bounds: X({xmin}-{xmax}) Y({ymin}-{ymax})")

# Let's crop to character exactly
c_arr = arr[ymin:ymax+1, xmin:xmax+1]
h, w, _ = c_arr.shape

# The eyes should be in the top half of the character, probably roughly horizontally centered.
# We look for black pixels (RGB < 50) within the top 30% to 50%
top_half = c_arr[int(h*0.3):int(h*0.55), :]
is_black = np.all(top_half[:, :, :3] < 50, axis=2)

black_y, black_x = np.where(is_black)
if len(black_x) > 0:
    min_bx, max_bx = black_x.min(), black_x.max()
    min_by, max_by = black_y.min(), black_y.max()
    print(f"Eyes bounding box relative to crop: X({min_bx}-{max_bx}) Y({int(h*0.3) + min_by}-{int(h*0.3) + max_by})")
else:
    print("No black pixels found in expected eye region.")
    
# Let's output a 1/10th scaled version of the eye region as ascii to see it!
eye_region = c_arr[int(h*0.3) + min_by - 10 : int(h*0.3) + max_by + 10, min_bx - 10 : max_bx + 10]
for r in range(0, eye_region.shape[0], 4):
    line = ""
    for c in range(0, eye_region.shape[1], 4):
        if np.all(eye_region[r,c,:3] < 50): line += "##"
        elif np.all(eye_region[r,c,:3] > 230): line += ".."
        else: line += "::"
    print(line)
