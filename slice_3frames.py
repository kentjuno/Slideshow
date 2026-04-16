import os
from PIL import Image
import numpy as np

img_path = r"C:\Users\Kent\.gemini\antigravity\brain\072a3b75-c43c-4b8d-9bef-f0396b7cafdf\monk_3frames_1776309804434.png"
img = Image.open(img_path).convert("RGBA")
arr = np.array(img)

is_bg = np.all(arr[:, :, :3] > 230, axis=2)
non_bg_rows = np.any(~is_bg, axis=1)
non_bg_cols = np.any(~is_bg, axis=0)

try:
    ymin, ymax = np.where(non_bg_rows)[0][[0, -1]]
    xmin, xmax = np.where(non_bg_cols)[0][[0, -1]]

    cropped = arr[ymin:ymax+1, xmin:xmax+1]
    ch, cw = cropped.shape[:2]

    c_is_bg = np.all(cropped[:, :, :3] > 230, axis=2)
    col_sum = np.sum(~c_is_bg, axis=0)

    # Let's find exactly 3 regions in col_sum
    # This identifies the columns with actual content
    in_content = False
    regions = []
    start = -1
    for i in range(cw):
        if col_sum[i] > 0 and not in_content:
            in_content = True
            start = i
        elif col_sum[i] == 0 and in_content:
            in_content = False
            regions.append((start, i - 1))
    
    if in_content:
         regions.append((start, cw - 1))
         
    if len(regions) < 2:
        # Sometimes there's no pixel gap between images.
        # We assume 3 equal partitions
        print("Fallback to 3 equal partition")
        w3 = cw // 3
        regions = [(0, w3), (w3, w3*2), (w3*2, cw)]
    
    print(f"Regions found: {len(regions)}")

    frames = []
    max_h = 0
    max_w = 0
    for r in regions:
        f = cropped[:, r[0]:r[1]+1]
        
        # Crop vertically per frame to get tight bounding box
        f_is_bg = np.all(f[:, :, :3] > 230, axis=2)
        f_non_bg = np.any(~f_is_bg, axis=1)
        if not np.any(f_non_bg):
            continue
            
        f_ymin, f_ymax = np.where(f_non_bg)[0][[0, -1]]
        f = f[f_ymin:f_ymax+1, :]
        
        frames.append(f)
        if f.shape[0] > max_h: max_h = f.shape[0]
        if f.shape[1] > max_w: max_w = f.shape[1]
        
    print(f"Number of frames extracted: {len(frames)}")

    # Pad and merge
    final_img = Image.new("RGBA", (max_w * len(frames), max_h), (255, 255, 255, 255))
    for i, f in enumerate(frames):
        fh, fw = f.shape[:2]
        pad_x = (max_w - fw) // 2
        pad_y = max_h - fh # anchor bottom
        f_img = Image.fromarray(f)
        final_img.paste(f_img, (i * max_w + pad_x, pad_y))

    out_path = r"f:\AntiGravity\Slideshow\merged_3frames.png"
    final_img.save(out_path)
    print("Saved 3 frames to", out_path)
except Exception as e:
    print(e)
