from PIL import Image, ImageDraw
import qrcode

class QRCodeGenerator:
    def __init__(self, version=1, box_size=10, border=4):
        self.version = version
        self.box_size = box_size
        self.border = border
        
    def create_qr_code(self, data, fill_color="black", back_color="white"):
        qr = qrcode.QRCode(
            version=self.version,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=self.box_size,
            border=self.border,
        )
        qr.add_data(data)
        qr.make(fit=True)
        return qr.make_image(fill_color=fill_color, back_color=back_color)
    
    def add_qr_to_image(self, base_image_path, qr_data, qr_size=(150, 150), 
                        position=None, output_path=None, show_image=False):
        qr_img = self.create_qr_code(qr_data)
        qr_img = qr_img.resize(qr_size)
        
        base_image = Image.open(base_image_path)
        
        if position is None:
            position = (
                base_image.width - qr_size[0] - 10,
                base_image.height - qr_size[1] - 10
            )
        
        base_image.paste(qr_img, position)
        
        if output_path:
            base_image.save(output_path)
        
        if show_image:
            base_image.show()
            
        return base_image