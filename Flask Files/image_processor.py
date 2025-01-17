from PIL import Image, ImageDraw, ImageFont
from qr_generator import QRCodeGenerator
from database import verify_username,load_database
from config import Config
qr_generator = QRCodeGenerator()

def update_image(name: str) -> bool:
    """Update image with name and QR code."""
    try:
        # First load database to get user data
        data = load_database()
        user_data = next((user for user in data['users'] if user['Name'] == name), None)
        
        if not user_data or 'qr_string' not in user_data:
            print("User data or QR string not found")
            return False
            
        qr_string = user_data['qr_string']
        
        # Open and process base image
        try:
            image = Image.open(Config.BASE_IMAGE_PATH)
        except FileNotFoundError:
            print(f"Base image not found at: {Config.BASE_IMAGE_PATH}")
            return False
            
        if image.mode == "RGBA":
            image = image.convert("RGB")
        
        # Draw text on image
        draw = ImageDraw.Draw(image)
        
        try:
            font = ImageFont.truetype(Config.FONT_PATH, size=Config.FONT_SIZE)
        except OSError:
            print(f"Font not found at: {Config.FONT_PATH}")
            font = ImageFont.load_default()
        
        # Add text to image
        draw.text(Config.TEXT_POSITION, name, fill=Config.TEXT_COLOR, font=font)
        
        # Save intermediate image
        try:
            image.save(Config.OUTPUT_IMAGE_PATH)
        except Exception as e:
            print(f"Error saving intermediate image: {str(e)}")
            return False
        
        # Add QR code
        try:
            qr_generator.add_qr_to_image(
                base_image_path=Config.OUTPUT_IMAGE_PATH,
                qr_data=qr_string,
                qr_size=Config.QR_SIZE,
                position=Config.QR_POSITION,
                output_path=Config.OUTPUT_IMAGE_PATH,
                show_image=False
            )
        except Exception as e:
            print(f"Error adding QR code: {str(e)}")
            return False
            
        return True
        
    except Exception as e:
        print(f"Error in update_image: {str(e)}")
        return False