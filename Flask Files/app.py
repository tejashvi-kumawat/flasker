from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from config import Config
from database import verify_username, add_user,load_database
from image_processor import update_image

app = Flask(__name__)
app.secret_key = Config.SECRET_KEY

@app.route('/', methods=['GET'])
def login():
    """Render login page."""
    return render_template('login.html')

@app.route('/update-json', methods=['POST'])
def update_json():
    """Handle new user registration."""
    username = request.form.get('username')
    name = request.form.get('name')
    
    success, message = add_user(username, name)
    flash(message, 'success' if success else 'error')
    return render_template('login.html')

@app.route('/verify', methods=['POST'])
def verify():
    """Handle user verification."""
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
    """Handle dashboard page."""
    try:
        data = load_database()
        user_data = next((user for user in data['users'] if user['Name'] == name), None)
        
        if not user_data:
            flash('User not found', 'error')
            return redirect(url_for('login'))
            
        if update_image(name):
            return render_template(
                "dashboard.html", 
                name=name.title(),
                qr_string=user_data.get('qr_string', '')
            )
        
        flash('Error generating image. Please check the server logs.', 'error')
        return redirect(url_for('login'))
        
    except Exception as e:
        flash(f'An error occurred: {str(e)}', 'error')
        return redirect(url_for('login'))

@app.route('/download-image', methods=['GET'])
def download_image():
    """Handle image download."""
    try:
        return send_file(
            Config.OUTPUT_IMAGE_PATH,
            as_attachment=True,
            download_name="downloaded-image.png"
        )
    except FileNotFoundError:
        flash('Image not found', 'error')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=50000, debug=True)