import cv2
import numpy as np
import os

def create_synthetic_image(height=300, width=300):
    """
    Creates a synthetic image with distinct color regions for testing.
    The image consists of 3x3 grid of 100x100 pixel squares.
    """
    img = np.zeros((height, width, 3), dtype=np.uint8)

    # Define various colors in BGR format
    colors = {
        'Blue': [255, 0, 0],
        'Green': [0, 255, 0],
        'Red': [0, 0, 255],
        'Cyan': [255, 255, 0],    # Blue + Green
        'Magenta': [255, 0, 255], # Blue + Red
        'Yellow': [0, 255, 255],  # Green + Red
        'White': [255, 255, 255],
        'Black': [0, 0, 0],
        'Gray': [128, 128, 128]
    }

    # Arrange colors in a 3x3 grid
    square_size = 100
    color_keys = list(colors.keys())

    for r_idx in range(3):
        for c_idx in range(3):
            start_y, end_y = r_idx * square_size, (r_idx + 1) * square_size
            start_x, end_x = c_idx * square_size, (c_idx + 1) * square_size
            
            color_name = color_keys[r_idx * 3 + c_idx]
            img[start_y:end_y, start_x:end_x] = colors[color_name]
            
            # Optionally, add text to show the color name in the original image
            # For non-GUI, we might skip this on the initial image, but for output it's fine.
            # Here we just generate the image, no text overlay for source.
            
    return img

def analyze_and_mark_dominant_channel(image_path="input_image.png", output_path="output_image.png"):
    """
    Main function to simulate a click, analyze the region, and save the result.
    """
    if not os.path.exists(image_path):
        print(f"Error: Input image '{image_path}' not found. Please ensure it exists.")
        return

    img = cv2.imread(image_path)
    if img is None:
        print(f"Error: Could not read image from '{image_path}'.")
        return

    height, width, _ = img.shape
    
    # --- Simulate User Click ---
    # For a non-interactive script, we define a fixed "click" point.
    # We choose a point within the Green square of the synthetic image.
    click_x, click_y = 150, 50 # Example: point in the Green square [0:100, 100:200]
    region_size = 20 # Size of the square region around the click point

    print(f"Simulating click at (x={click_x}, y={click_y}).")

    # Calculate region boundaries
    half_size = region_size // 2
    x1 = max(0, click_x - half_size)
    y1 = max(0, click_y - half_size)
    x2 = min(width, click_x + half_size + 1) # +1 for exclusive upper bound
    y2 = min(height, click_y + half_size + 1)

    # Ensure the region is at least 1x1 if click is near edge
    if x2 <= x1: x2 = x1 + 1
    if y2 <= y1: y2 = y1 + 1

    # Extract the region
    region = img[y1:y2, x1:x2]

    # Calculate average BGR values
    avg_b = np.mean(region[:, :, 0])
    avg_g = np.mean(region[:, :, 1])
    avg_r = np.mean(region[:, :, 2])

    print(f"Average BGR in region: B={avg_b:.2f}, G={avg_g:.2f}, R={avg_r:.2f}")

    # Identify dominant channel
    averages = {'Blue': avg_b, 'Green': avg_g, 'Red': avg_r}
    dominant_channel = max(averages, key=averages.get)

    print(f"Dominant channel: {dominant_channel}")

    # --- Overlay results on a copy of the image ---
    output_img = img.copy()

    # Draw a circle at the "clicked" point
    cv2.circle(output_img, (click_x, click_y), 5, (0, 255, 255), -1) # Yellow circle

    # Draw a rectangle around the analyzed region
    cv2.rectangle(output_img, (x1, y1), (x2 - 1, y2 - 1), (255, 255, 0), 1) # Cyan rectangle

    # Overlay dominant channel name
    text = f"Dominant: {dominant_channel}"
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.7
    font_thickness = 2
    text_color = (255, 255, 255) # White text

    # Position text near the clicked point, adjust if it goes out of bounds
    text_x = click_x + half_size + 5
    text_y = click_y - half_size - 5
    
    # Get text size to adjust position if needed
    (text_w, text_h), baseline = cv2.getTextSize(text, font, font_scale, font_thickness)

    # Adjust text_x
    if text_x + text_w > width - 5:
        text_x = width - text_w - 5
    if text_x < 5:
        text_x = 5

    # Adjust text_y
    if text_y < text_h + 5: # If text is too high, move it below the click point
        text_y = click_y + half_size + text_h + 5
    if text_y > height - 5: # If text is too low, move it above
        text_y = height - 5

    cv2.putText(output_img, text, (text_x, text_y), font, font_scale, text_color, font_thickness, cv2.LINE_AA)
    
    # Save the output image
    cv2.imwrite(output_path, output_img)
    print(f"Output image saved to '{output_path}'")

if __name__ == "__main__":
    input_filename = "input_image.png"
    output_filename = "output_image.png"

    print("Generating synthetic input image...")
    synthetic_img = create_synthetic_image()
    cv2.imwrite(input_filename, synthetic_img)
    print(f"Synthetic image saved as '{input_filename}'")

    print("\nStarting channel analysis...")
    analyze_and_mark_dominant_channel(input_filename, output_filename)
    print("\nScript finished.")