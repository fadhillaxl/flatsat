import os
import subprocess

class Payload:
    def capture(self, filename="image.jpg"):
        try:
            # Using fswebcam as specified
            cmd = f"fswebcam -r 320x240 --no-banner {filename}"
            subprocess.run(cmd.split(), check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return filename
        except Exception as e:
            print(f"[Payload] Camera capture failed: {e}")
            # Create a dummy image if capture fails for testing
            return None
