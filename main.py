# Import the necessary modules
import math
import cv2
import numpy as np
import random
import noise

# Load gradient
gradient = cv2.imread("gradient.png", cv2.IMREAD_COLOR)

# Image parameters
width = 512
height = width  # Square image

# Noise parameters
scale = 3000
octaves = 7
persistence = 0.5
lacunarity = 2.5
turbulence = 0.8

# Seed PRNG
random.seed()
seed = random.randint(-9999, 9999)

# Create a noise map
noise_map = np.zeros((width, height), dtype=float)
for i in range(width):
    for j in range(height):
        noise_map[i][j] = noise.pnoise2(i / scale, j / scale, octaves=octaves, persistence=persistence,
                                        lacunarity=lacunarity, repeatx=width, repeaty=height, base=seed)

# Normalize noise
noise_norm = (noise_map - noise_map.min()) / (noise_map.max() - noise_map.min())

# Create a blank image
img = np.zeros((width, height, 3), dtype=np.uint8)
img_color = np.zeros((width, height, 3), dtype=np.uint8)

# Populate image
for x, row in enumerate(img):
    for y, pixel in enumerate(img):
        xValue = (x - height / 2) / height
        yValue = (y - width / 2) / width
        distance_value = math.sqrt((xValue * xValue) + (yValue * yValue)) + (turbulence * noise_norm[x][y])
        cos_value = abs(math.sin(2 * 12 * distance_value * math.pi))
        color_value = cos_value * 255
        img[x][y] = [color_value, color_value, color_value]  # Write the pixel
        img_color[x][y] = gradient[0][int(color_value)] # Write the color pixel

# Save the images, then display the color image
cv2.imwrite('image_bw.png', img)
cv2.imwrite('image_color.png', img_color)
cv2.imshow("New Image", img_color)

# When any key is pressed, close the window
cv2.waitKey(0)
cv2.destroyAllWindows()
