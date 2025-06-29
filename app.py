from flask import Flask, request, render_template, send_file
from PIL import Image, ImageDraw, ImageFont
import os

app = Flask(__name__)

UPLOAD_FOLDER = "./uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route("/")
def index():
    return render_template("home_page.html")

@app.route("/upload", methods=["POST"])
def upload():
    # Get the uploaded file and label
    print("In def function")
    image_file = request.files["image"]
    label = request.form["label"]
    
    # Open the image and prepare it for processing
    original_image = Image.open(image_file)
    angles = [0, 30, 60, 90, 120, 150, 180]  # Rotation angles
    saved_file_paths = []  # To store paths of saved images

    # Counter for sequential labeling
    counter = 1

    for angle in angles:
        # Rotate the image
        rotated_image = original_image.rotate(angle, expand=True)
        
        # Draw the label on the rotated image
        draw = ImageDraw.Draw(rotated_image)
        font = ImageFont.truetype("arial.ttf", size=80)
        padding = 40
        text_position = (padding, padding)  # Place the label with padding
        draw.text(text_position, f"{label}_{counter}", fill="white", font=font)

        # Generate a unique filename for each rotated image
        labeled_image_path = os.path.join(
            UPLOAD_FOLDER, f"labeled_{counter}_{image_file.filename}"
        )
        
        # Save the labeled image
        rotated_image.save(labeled_image_path)
        saved_file_paths.append(labeled_image_path)  # Keep track of saved images
        
        counter += 1  # Increment the counter for the next label

    # Return the last saved image to the client for download
    return send_file(
        saved_file_paths[-1],  # Send the last image in the loop
        as_attachment=True,
        download_name=f"labeled_{counter - 1}_{image_file.filename}"
    )

if __name__ == "__main__":
    app.run(debug=True)
