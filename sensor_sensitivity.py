import cv2
import numpy as np
import matplotlib.pyplot as plt

x_offset = 0.105
x_scale = 0.817
y_offset = 0.137
y_scale = 0.826

# Load the image (change the filename if needed)
image_path = "sensitivity.png"
img = cv2.imread(image_path)
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# Extracted ethanol data points (approximate, visually derived)
ethanol_x = [50, 100, 300, 700, 950, 2000, 5000]  # ppm
ethanol_y = [3.6, 2, 1.0, 0.6, 0.5, 0.31, 0.18]   # Rs/R0

# Convert to log10 for mapping to image scale
log_x = np.log10(ethanol_x)
log_y = np.log10(ethanol_y)

# Get image dimensions
img_height, img_width, _ = img.shape

# Map log-log data points to pixel coordinates (manually tuned mapping)
x_pixels = (log_x - 1) / 3 * img_width * x_scale + img_width * x_offset
y_pixels = img_height - ((log_y + 1) / 3 * img_height * y_scale + img_height * y_offset)

# Plot overlay again with gridlines added for easier visual verification
plt.figure(figsize=(6, 5))
plt.imshow(img_rgb)

# Plot the ethanol line
plt.plot(x_pixels, y_pixels, color='orange', marker='o', linewidth=2, label='Ethanol (extracted)')

# Overlay log-log grid lines
# Define log scale ticks from 10^1 to 10^4 for x, and 10^-1 to 10^2 for y
x_ticks = np.log10([10, 100, 1000, 10000])
y_ticks = np.log10([0.1, 1, 10, 100])

# Draw vertical gridlines
for xt in x_ticks:
    x_pos = (xt - 1) / 3 * img_width * x_scale + img_width * x_offset
    plt.axvline(x=x_pos, color='gray', linestyle='--', linewidth=0.8)

# Draw horizontal gridlines
for yt in y_ticks:
    y_pos = img_height - ((yt + 1) / 3 * img_height * y_scale + img_height * y_offset)
    plt.axhline(y=y_pos, color='gray', linestyle='--', linewidth=0.8)

plt.axis('off')
plt.title("Overlay with Gridlines for Verification")
plt.legend()
plt.tight_layout()
plt.show()
