from PIL import Image
import os

# Target sizes
SIZES = [512, 256, 128, 64, 32, 24, 16]

INPUT_DIR = "."
IMAGE_EXTENSIONS = tuple("."+ext for ext in ("png", "jpg", "jpeg", "webp"))

def create_folders():
    for size in SIZES:
        folder = f"{size}x{size}"
        os.makedirs(folder, exist_ok=True)

def process_image(file):
    try:
        with Image.open(file) as img:
            w, h = img.size

            # Only process 512x512 images
            if w != 512 or h != 512:
                print(f"Skipping {file} (not 512x512)")
                return

            for size in SIZES:
                resized = img.resize((size, size), Image.LANCZOS)

                output_path = os.path.join(f"{size}x{size}", os.path.basename(file))

                # Preserve PNG transparency if needed
                if resized.mode in ("RGBA", "LA") or (resized.mode == "P" and "transparency" in img.info):
                    resized.save(output_path, "PNG")
                else:
                    resized = resized.convert("RGB")
                    resized.save(output_path)

            print(f"Processed: {file}")

    except Exception as e:
        print(f"Error processing {file}: {e}")

def main():
    create_folders()

    for file in os.listdir(INPUT_DIR):
        if file.lower().endswith(IMAGE_EXTENSIONS):
            process_image(file)

    print("Done.")

if __name__ == "__main__":
    main()
