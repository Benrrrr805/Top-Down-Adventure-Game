from PIL import Image
import os

def convert_webp_to_png(input_path, output_path):
    """
    Convert a WebP image to PNG format.

    :param input_path: Path to the input WebP file
    :param output_path: Path to save the output PNG file
    """
    try:
        with Image.open(input_path) as img:
            img = img.convert("RGBA")  # Ensure correct format for PNG
            width, height = img.size
            output_path_with_size = os.path.splitext(output_path)[0] + f"_{width}x{height}.png"
            img.save(output_path_with_size, "PNG")
        print(f"Converted: {input_path} -> {output_path_with_size}")
    except Exception as e:
        print(f"Error converting {input_path}: {e}")

def batch_convert_webp_to_png(input_dir, output_dir):
    """
    Convert all WebP images in a directory to PNG format.

    :param input_dir: Directory containing WebP files
    :param output_dir: Directory to save PNG files
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        if filename.lower().endswith(".webp"):
            input_path = os.path.join(input_dir, filename)
            output_filename = os.path.splitext(filename)[0] + ".png"
            output_path = os.path.join(output_dir, output_filename)
            convert_webp_to_png(input_path, output_path)

if __name__ == "__main__":
    input_directory = "./webp"
    output_directory = "./png"

    batch_convert_webp_to_png(input_directory, output_directory)
