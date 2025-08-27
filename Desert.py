from PIL import Image, ImageDraw
import random

def generate_desert_ground(filename="desert_ground.png"):
    width, height = 100, 100

    # Create a new image with RGB mode
    img = Image.new("RGB", (width, height), "#F4A460")
    draw = ImageDraw.Draw(img)

    # Generate random pebbles and details
    for _ in range(300):
        x, y = random.randint(0, width - 1), random.randint(0, height - 1)
        size = random.randint(1, 3)  # Size of pebbles
        color_variation = random.randint(-20, 20)
        color = (
            max(0, min(255, 244 + color_variation)),  # R
            max(0, min(255, 164 + color_variation)),  # G
            max(0, min(255, 96 + color_variation))   # B
        )
        draw.ellipse([x, y, x + size, y + size], fill=color)

    # Add larger rocks
    for _ in range(20):
        x, y = random.randint(0, width - 1), random.randint(0, height - 1)
        size = random.randint(5, 10)  # Size of rocks
        color_variation = random.randint(-40, 40)
        color = (
            max(0, min(255, 160 + color_variation)),  # R
            max(0, min(255, 82 + color_variation)),   # G
            max(0, min(255, 45 + color_variation))    # B
        )
        draw.ellipse([x, y, x + size, y + size], fill=color)

    # Add wavy patterns for texture
    for _ in range(10):
        start_x = random.randint(0, width // 2)
        end_x = random.randint(width // 2, width)
        start_y = random.randint(0, height - 10)
        end_y = start_y + random.randint(-3, 3)
        draw.line([(start_x, start_y), (end_x, end_y)], fill="#E9967A", width=1)

    img.save(filename)
    print(f"Generated desert ground image saved as {filename}")

# Generate the image
generate_desert_ground()
