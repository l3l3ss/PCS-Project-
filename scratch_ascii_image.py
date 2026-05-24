from PIL import Image
import numpy as np

def print_image_ascii(image_path, width=80):
    try:
        img = Image.open(image_path).convert('L')
        # Calculate height keeping aspect ratio
        w, h = img.size
        height = int((h / w) * width * 0.5) # 0.5 to adjust for character aspect ratio
        img = img.resize((width, height))
        
        pixels = np.array(img)
        # Characters from dark to light
        chars = " .:-=+*#%@"
        
        print(f"\n--- {image_path} ---")
        for row in pixels:
            line = "".join(chars[int(p / 256 * len(chars))] for p in row)
            print(line)
    except Exception as e:
        print(f"Error reading {image_path}: {e}")

print_image_ascii('output/auto_scar_k_848.png')
print_image_ascii('output/auto_scar_k_805.png')
print_image_ascii('output/auto_scar_k_887.png')
print_image_ascii('output/auto_scar_k_904.png')
