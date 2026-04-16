import cv2
import numpy as np
from PIL import Image

# Read the image
img = np.array(Image.open('merged_3frames.png').convert('RGBA'))

# The background color is white [255, 255, 255, 255]
# Let's create a mask of the background
h, w, c = img.shape
diff = np.abs(img[:, :, :3] - [255, 255, 255])
bg_mask = np.max(diff, axis=2) < 10

# Now, let's find the shadow. Shadow is dark, and sits at the very bottom.
# We will do a connected component analysis on everything that is NOT background
fg_mask = ~bg_mask

# We know the main character is in the center of each frame
frames = w // 258
for i in range(frames):
    x_start = i * 258
    x_end = (i + 1) * 258
    
    frame_fg = fg_mask[:, x_start:x_end].astype(np.uint8)
    
    # Get all connected components
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(frame_fg, connectivity=8)
    
    # Label 0 is background.
    # The main character will be the largest component by area
    areas = stats[1:, cv2.CC_STAT_AREA]
    if len(areas) == 0: continue
    
    main_component_label = np.argmax(areas) + 1
    
    # We want to remove all components EXCEPT the main character
    # This automatically removes floating shadows, artifacts, etc.
    for label in range(1, num_labels):
        if label != main_component_label:
            # Clear these pixels
            img[:, x_start:x_end][labels == label] = [0, 0, 0, 0]

# Save the cleaned image back
Image.fromarray(img).save('merged_3frames_clean.png')
print("Successfully cleaned.")
