import random
import os
from PIL import Image, ImageDraw

def generate_car_image(direction, filename):
    # Set the dimensions to match the player in the game (30x50)
    width, height = 50, 30
    image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    # Flip function for reversing coordinates for left-facing cars
    def flip_coords(x1, y1, x2=None, y2=None):
        if x2 is not None and y2 is not None:  # Rectangle or polygon
            return width - x2, y1, width - x1, y2
        return width - x1, y1  # Single point

    # Randomize car type and features
    car_type = random.choice(["car", "truck", "bus"])  # Base type
    car_color = random.choice([ 
        (255, 0, 0, 255), (0, 0, 255, 255), (0, 255, 0, 255), 
        (255, 165, 0, 255), (128, 0, 128, 255), (0, 255, 255, 255)
    ])  # Red, Blue, Green, Orange, Purple, Cyan
    has_spoiler = random.choice([True, False])
    has_shaker_hood = random.choice([True, False])
    has_dual_exhaust = random.choice([True, False])
    paint_style = random.choice(["solid", "striped", "double-striped"])

    # Set dimensions based on car type (scaled to fit 50x30 frame)
    if car_type == "truck":
        body_coords = (5, 10, 45, 20)  # Adjusted for truck body size
        roof_height = 5
    elif car_type == "bus":
        body_coords = (5, 10, 45, 20)  # Adjusted for bus body size
        roof_height = 4
    else:  # Default car
        body_coords = (6, 12, 44, 18)  # Adjusted for a regular car body size
        roof_height = 6

    # Scale coordinates to fit the 50x30 frame
    body_coords = (int(body_coords[0] * width / 50), int(body_coords[1] * height / 30),
                   int(body_coords[2] * width / 50), int(body_coords[3] * height / 30))
    roof_height = int(roof_height * height / 30)

    if direction == "left":
        body_coords = flip_coords(*body_coords)

    # Draw the car body
    draw.rectangle(body_coords, fill=car_color)

    # Add paint jobs
    if paint_style == "striped":
        stripe_color = (255, 255, 255, 255)  # White stripe
        stripe_coords = (body_coords[0] + 2, body_coords[1] + 2, body_coords[2] - 2, body_coords[1] + 5)
        if direction == "left":
            stripe_coords = flip_coords(*stripe_coords)
        draw.rectangle(stripe_coords, fill=stripe_color)
    elif paint_style == "double-striped":
        stripe_color = (255, 255, 255, 255)  # White stripes
        stripe1_coords = (body_coords[0] + 2, body_coords[1] + 2, body_coords[2] - 2, body_coords[1] + 5)
        stripe2_coords = (body_coords[0] + 2, body_coords[1] + 10, body_coords[2] - 2, body_coords[1] + 13)
        if direction == "left":
            stripe1_coords = flip_coords(*stripe1_coords)
            stripe2_coords = flip_coords(*stripe2_coords)
        draw.rectangle(stripe1_coords, fill=stripe_color)
        draw.rectangle(stripe2_coords, fill=stripe_color)

    # Draw the car roof
    roof_coords = [(body_coords[0] + 5, body_coords[1] - roof_height),
                   (body_coords[2] - 5, body_coords[1] - roof_height),
                   (body_coords[2] - 4, body_coords[1]),
                   (body_coords[0] + 4, body_coords[1])]
    if direction == "left":
        roof_coords = [flip_coords(x, y) for x, y in roof_coords]
    draw.polygon(roof_coords, fill=car_color)

    # Draw windows
    window_color = (135, 206, 250, 255)  # Light blue
    window_coords = [
        (body_coords[0] + 6, body_coords[1] - roof_height + 3, body_coords[0] + 10, body_coords[1] - 1),
        (body_coords[2] - 10, body_coords[1] - roof_height + 3, body_coords[2] - 6, body_coords[1] - 1)
    ]
    if direction == "left":
        window_coords = [flip_coords(*coords) for coords in window_coords]
    for coords in window_coords:
        draw.rectangle(coords, fill=window_color)

    # Draw wheels (50% of wheel height above the car body)
    wheel_color = (0, 0, 0, 255)  # Black
    wheel_inner_color = (220, 220, 220, 255)  # Dark gray
    wheel_radius = 4 if car_type != "car" else 3  # Larger wheels
    wheel_offset_x = 6  # Increased X offset to center wheels better
    wheel_offset_y = wheel_radius // 2  # 50% of wheel height above the car body

    # Adjust wheel positions based on the car type
    if car_type == "car":
        wheels = [(body_coords[0] + wheel_offset_x, body_coords[3] - wheel_offset_y),  # Front wheel
                  (body_coords[2] - wheel_offset_x, body_coords[3] - wheel_offset_y)]  # Rear wheel
    elif car_type == "truck":
        wheels = [(body_coords[0] + 4, body_coords[3] - wheel_offset_y),  # Front wheel
                  (body_coords[2] - 4, body_coords[3] - wheel_offset_y)]  # Rear wheel
    else:  # Bus
        wheels = [(body_coords[0] + 5, body_coords[3] - wheel_offset_y),  # Front wheel
                  (body_coords[2] - 5, body_coords[3] - wheel_offset_y)]  # Rear wheel
    
    if direction == "left":
        wheels = [flip_coords(x, y) for x, y in wheels]
    
    # Draw the wheels
    for x, y in wheels:
        draw.ellipse((x - wheel_radius, y - wheel_radius, x + wheel_radius, y + wheel_radius), fill=wheel_color)
        draw.ellipse((x - wheel_radius // 2, y - wheel_radius // 2, x + wheel_radius // 2, y + wheel_radius // 2), fill=wheel_inner_color)

    # Add spoiler (optional)
    if has_spoiler:
        spoiler_color = (50, 50, 50, 255)  # Dark gray
        spoiler_coords = [(body_coords[2] - 10, body_coords[1] - 4),
                          (body_coords[2] - 5, body_coords[1] - 4),
                          (body_coords[2] - 7, body_coords[1] - 2),
                          (body_coords[2] - 8, body_coords[1] - 2)]
        if direction == "left":
            spoiler_coords = [flip_coords(x, y) for x, y in spoiler_coords]
        draw.polygon(spoiler_coords, fill=spoiler_color)

    # Add shaker hood (optional)
    if has_shaker_hood:
        shaker_color = (0, 0, 0, 255)  # Black
        shaker_coords = (body_coords[0] + 4, body_coords[1] - 6, body_coords[0] + 6, body_coords[1] - 3)
        if direction == "left":
            shaker_coords = flip_coords(*shaker_coords)
        draw.rectangle(shaker_coords, fill=shaker_color)

    # Add dual side exhaust (optional)
    if has_dual_exhaust:
        exhaust_color = (169, 169, 169, 255)  # Gray
        exhaust_coords = [
            (body_coords[0] + 2, body_coords[1] + 2, body_coords[0] + 4, body_coords[1] + 4),
            (body_coords[2] - 4, body_coords[1] + 2, body_coords[2] - 2, body_coords[1] + 4)
        ]
        if direction == "left":
            exhaust_coords = [flip_coords(*coords) for coords in exhaust_coords]
        for coords in exhaust_coords:
            draw.rectangle(coords, fill=exhaust_color)

    # Save the image
    image.save(filename)

# Create a folder for the cars
output_folder = "cars"
os.makedirs(output_folder, exist_ok=True)

# Generate 50 right-facing cars and 50 left-facing cars
for i in range(1, 51):
    generate_car_image("right", os.path.join(output_folder, f"car_right_{i}.png"))
    generate_car_image("left", os.path.join(output_folder, f"car_left_{i}.png"))

print(f"100 car images saved to the '{output_folder}' folder.")
