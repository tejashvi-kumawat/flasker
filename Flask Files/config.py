class Config:
    SECRET_KEY = '123asdfghj123'  # Use environment variable in production
    JSON_DB_PATH = 'data/sample.json'
    BASE_IMAGE_PATH = 'static/images/1.png'
    OUTPUT_IMAGE_PATH = 'static/images/2.png'
    FONT_PATH = "/System/Library/Fonts/Supplemental/Arial.ttf"
    FONT_SIZE = 40
    TEXT_POSITION = (450, 450)
    TEXT_COLOR = (255, 0, 0)  # Red
    QR_SIZE = (200, 200)
    QR_POSITION = (50, 50)
