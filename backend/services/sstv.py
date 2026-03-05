from pysstv.color import Robot36
from PIL import Image
import os

class SSTV:
    def encode(self, image_path="image.jpg", output_wav="downlink.wav"):
        if not os.path.exists(image_path):
            print(f"[SSTV] Image not found: {image_path}")
            return False
            
        try:
            img = Image.open(image_path)
            # Resize if necessary as Robot36 expects specific sizes usually 320x240
            img = img.resize((320, 240))
            
            sstv = Robot36(img, 44100, 16)
            with open(output_wav, "wb") as f:
                sstv.write_wav(f)
            return True
        except Exception as e:
            print(f"[SSTV] Encoding failed: {e}")
            return False
