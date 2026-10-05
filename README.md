# Channel Spotlight

Identifies and marks the dominant BGR channel in a specified image region.

## Description

This project demonstrates a simple computer vision task: generating a test image, simulating a user click at a predefined coordinate, calculating the average Blue, Green, and Red (BGR) channel intensities in a small square region around that point, and then identifying which channel has the highest average intensity. The result, including the dominant channel name, is overlaid onto the image and saved to a file.

This script is designed to run non-interactively, making it suitable for headless environments. It explicitly avoids any GUI or display-related functions.

## How to Run

1.  **Install dependencies:**
    Make sure you have `pip` installed. Then, install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Run the script:**
    Execute the main Python script:
    ```bash
    python main.py
    ```

The script will:
*   Generate a `300x300` synthetic image named `input_image.png` with various color squares.
*   Simulate a "user click" at a fixed coordinate within this image.
*   Analyze a `20x20` pixel region around the simulated click.
*   Identify the dominant BGR channel in that region.
*   Save the original image with a circle indicating the click, a rectangle showing the analyzed region, and text displaying the dominant channel, to `output_image.png`.

After running, you can inspect `output_image.png` to see the results.