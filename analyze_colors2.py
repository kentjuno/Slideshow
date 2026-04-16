import numpy as np
from PIL import Image

img = Image.open('merged_3frames.png').convert('RGBA')
arr = np.array(img)
h, w, c = arr.shape

frame_w = w // 3
print("Image shape:", arr.shape)
print("Frame width:", frame_w)

# The shadow is typically at the bottom corner of the first frame
print("Shadow color roughly at [h-5, 5]:", arr[h-5, 5])

# The cushion is typically at the bottom center of the first frame
print("Cushion color roughly at [h-15, frame_w//2]:", arr[h-15, frame_w//2])
print("Cushion color roughly at [h-5, frame_w//2]:", arr[h-5, frame_w//2])

# Background
print("Background at [0, 0]:", arr[0, 0])
