from PIL import Image
import numpy as np

img = Image.open('merged_3frames.png').convert('RGBA')
arr = np.array(img)

# Print the top-left color (background)
print("Background color:", arr[0, 0])

# Find the shadow color at the bottom
h, w, _ = arr.shape
print("Bottom-left color:", arr[-1, 0])
print("Bottom-center color:", arr[-1, w//2])

# Let's see some unique colors that look like grey
unique_colors = np.unique(arr.reshape(-1, 4), axis=0)
print("Found", len(unique_colors), "unique colors.")

greys = []
for c in unique_colors:
    c = [int(v) for v in c]
    if max(c[:3]) - min(c[:3]) < 20 and c[3] > 100:
        greys.append(c)

print("Greys:", greys)
