import os
import subprocess
from PIL import Image

def render_image_in_terminal(image_path, width=80):
    """Render image in terminal — full-pixel if Kitty, else fallback to ANSI color blocks."""

    # 1️⃣  Try Kitty protocol for true pixel rendering ---
    if os.environ.get("TERM", "").startswith("xterm-kitty"):
        try:
            subprocess.run(["kitty", "+kitten", "icat", "--silent", image_path], check=True)
            print("| Rendered with Kitty graphics protocol |")
            print("| IMAGE RENDER END |")
            return
        except Exception as e:
            print(f"[Kitty mode failed: {e}] Falling back to ANSI blocks...")

    # 2️⃣  Fallback: ANSI color block rendering ---
    try:
        img = Image.open(image_path)
        aspect_ratio = img.height / img.width
        new_height = int(aspect_ratio * width * 0.47)
        img = img.resize((width, new_height * 2))
        img = img.convert("RGB")

        output = []
        for y in range(0, img.height, 2):
            row = ""
            for x in range(img.width):
                top_r, top_g, top_b = img.getpixel((x, y))
                if y + 1 < img.height:
                    bottom_r, bottom_g, bottom_b = img.getpixel((x, y + 1))
                else:
                    bottom_r, bottom_g, bottom_b = (0, 0, 0)
                row += f"\033[38;2;{top_r};{top_g};{top_b}m\033[48;2;{bottom_r};{bottom_g};{bottom_b}m▀"
            row += "\033[0m"
            output.append(row)

        print("\n".join(output))
    except Exception as e:
        print(f"Error rendering the image: {e}")

render_image_in_terminal("sample_images/earth.webp")
print("--"*40)
render_image_in_terminal("sample_images/minecraft.webp")
print("--"*40)
render_image_in_terminal("sample_images/nature.webp")

print("Just pass the file path of the image in the Function Parameter :)")
