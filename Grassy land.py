from PIL import Image, ImageDraw
import random

def generate_grass_texture(filename="grass_texture2.png", size=(100, 100)):
    """Generate a seamless grass texture."""
    width, height = size
    img = Image.new("RGB", size, "green")  # Base color for grass
    draw = ImageDraw.Draw(img)

    # Add random grass-like strokes
    for _ in range(200):  # Number of grass blades
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        x2 = x1 + random.randint(-10, 10)  # Slightly angled
        y2 = y1 - random.randint(10, 20)  # Taller strokes
        color = random.choice([(34, 139, 34), (50, 205, 50), (0, 128, 0)])  # Variations of green
        draw.line((x1, y1, x2, y2), fill=color, width=1)

    # Save the texture
    img.save(filename)
    print(f"Grass texture saved as {filename}")

# Generate and save the grass texture
generate_grass_texture()