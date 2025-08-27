from PIL import Image, ImageDraw

def generate_muscle_car():
    width, height = 60, 35  # Increased height for a taller roof
    image = Image.new('RGBA', (width, height), (0, 0, 0, 0))  # Transparent background
    draw = ImageDraw.Draw(image)

    # Car Body - Main body of the car
    draw.rectangle([2, 15, 58, 27], fill=(0, 0, 255, 255))  

    # Roof - Rounded, taller roof
    draw.ellipse([10, 3, 50, 19], fill=(0, 0, 255, 255))  

    # Windows - Left and right windows
    draw.rectangle([18, 8, 26, 15], fill=(135, 206, 235, 255))  
    draw.rectangle([34, 8, 42, 15], fill=(135, 206, 235, 255))  

    # Tires - Left and right tires (black)
    draw.ellipse([6, 22, 18, 34], fill=(0, 0, 0, 255))  
    draw.ellipse([42, 22, 54, 34], fill=(0, 0, 0, 255))  

    # Rims - Light grey rims inside the tires
    draw.ellipse([9, 25, 15, 31], fill=(200, 200, 200, 255))  # Left rim
    draw.ellipse([45, 25, 51, 31], fill=(200, 200, 200, 255))  # Right rim

    # Stripe - Orange accent stripe across the body
    draw.line([10, 19, 50, 19], fill=(255, 165, 0, 255), width=2)  

    # Spoiler - Adds a rectangular spoiler to the front of the car
    draw.rectangle([2, 10, 15, 14], fill=(0, 0, 255, 255))  

    # Tail Light - Moves the red rectangle to the front of the car
    draw.rectangle([2, 20, 5, 24], fill=(255, 0, 0, 255))  

    # Exhaust - Moves the small gray rectangle below the front of the car
    draw.rectangle([2, 26, 6, 28], fill=(169, 169, 169, 255))  

    # Headlight - Adds a yellow rectangle at the back of the car
    draw.rectangle([55, 20, 58, 24], fill=(255, 255, 0, 255))  

    # Front Bumper - Adds a dark gray bumper at the back of the car
    draw.rectangle([54, 26, 58, 28], fill=(100, 100, 100, 255))  

    return image

# Generate the muscle car image
muscle_car_image = generate_muscle_car()

# Show the image
muscle_car_image.show()

# Optionally save the image
muscle_car_image.save("muscle_car_with_rims.png")