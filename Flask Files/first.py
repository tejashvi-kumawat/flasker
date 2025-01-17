from flask import Flask, render_template, request, redirect, url_for, flash, send_file, jsonify
import json
from typing import List, Optional
import sqlite3
from PIL import Image, ImageDraw, ImageFont

# Flask Instance
app = Flask(__name__)
app.secret_key = 'kjashdfjgqewyuofbi238794fb2384rfy7umwiehgfh928374hrb9yqweufn902734trg9y8oiuwqherf9263y47nrf97w8eoifhyn42798634gyt7rhfwnefir7o2gw23y478rh9f8jyeowrhig89rewyqbefuisnf8oyqwehir'

def load_database():
    """Load user data from JSON file and return formatted list."""
    try:
        with open('data/sample.json', 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print("Error: database file not found")
        return {'users': []}
    except json.JSONDecodeError:
        print("Error: invalid JSON format")
        return {'users': []}

def verify_username(input_username: str) -> Optional[dict]:
    """
    Verify username exists in database and return user data if found.
    """
    data = load_database()
    for user in data['users']:
        if user['username'] == input_username:
            return user
    return None
def updateImage(name):
    
    image = Image.open("static/images/1.png")
    # Create a drawing object
    if image.mode == "RGBA":
        img = image.convert("RGB")
        img.save("1.png", format="PNG")
    draw = ImageDraw.Draw(image)
    # Load a font (adjust the path and size as needed)
    font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", size=40)
    # Define the text and its position
    text = name
    position = (450, 450)  # (x, y) coordinates
    # Choose text color (RGB format)
    color = (255, 0, 0)  # Red color
    # Write text on the image
    draw.text(position, text, fill=color, font=font)
    # Save the updated image
    image.save("static/images/2.png")
    # Show the updated image
    
@app.route('/', methods=['GET'])
def login():
    """Render login page."""
    return render_template('login.html')

@app.route('/update-json', methods=['POST'])
def update_json():
    data = load_database()
    username = request.form.get('username')
    name = request.form.get('name')
    
    if not username or not name:
        flash('Please enter both username and name', 'error')
        return render_template('login.html')

    # Check if username already exists
    user_exists = any(user['username'] == username for user in data['users'])
    
    if user_exists:
        message = "User with this username already exists!"
    else:
        # Add new user
        users = data['users']
        user_n = users[-1]
        new_user_id = str(int(user_n["ID"]) + 1)
        data['users'].append({
            'username': username,
            'Name': name,
            'ID': new_user_id
        })
        message = "User data added successfully!"
        
        # Save updated data
        try:
            with open('data/sample.json', 'w') as file:
                json.dump(data, file, indent=4)
        except Exception as e:
            message = f"Error saving data: {str(e)}"
    
    flash(message)
    return render_template('login.html')

@app.route('/verify', methods=['POST'])
def verify():
    username = request.form.get('username')
    
    if not username:
        flash('Please enter a username', 'error')
        return redirect(url_for('login'))
    
    user_data = verify_username(username)
    if user_data:
        return redirect(url_for('index', name=user_data['Name']))
    else:
        flash('Invalid username. Please try again.', 'error')
        return redirect(url_for('login'))

@app.route('/index/<name>')
def index(name):
    updateImage(name)
    return render_template("dashboard.html", name=name.title())

@app.route('/download-image', methods=['GET'])
def download_image():
    try:
        image_path = "static/images/2.png"
        return send_file(image_path, as_attachment=True, download_name="downloaded-image.jpg")
    except FileNotFoundError:
        flash('Image not found', 'error')
        return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)