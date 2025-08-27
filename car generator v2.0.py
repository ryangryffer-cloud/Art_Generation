from PIL import Image, ImageDraw

# Create a blank image with a transparent background
width, height = 30, 50
image = Image.new('RGBA', (width, height), (255, 255, 255, 0))  # Transparent background
draw = ImageDraw.Draw(image)

# Define colors
car_color = (0, 0, 255, 255)  # Blue with full opacity
window_color = (135, 206, 250, 255)  # Light Blue with full opacity
wheel_color = (0, 0, 0, 255)  # Black with full opacity
headlight_color = (255, 255, 0, 255)  # Yellow with full opacity
grille_color = (169, 169, 169, 255)  # Dark Gray with full opacity
door_handle_color = (192, 192, 192, 255)  # Silver with full opacity
shading_color = (0, 0, 139, 255)  # Dark Blue for shading

# Draw the car body (main shape)
draw.rectangle([5, 20, 25, 40], fill=car_color)  # Main body
draw.polygon([(5, 20), (10, 15), (20, 15), (25, 20)], fill=car_color)  # Roof
draw.rectangle([5, 20, 25, 22], fill=shading_color)  # Roof shading

# Draw the windows
draw.rectangle([8, 22, 12, 30], fill=window_color)  # Front window
draw.rectangle([18, 22, 22, 30], fill=window_color)  # Rear window
draw.line([8, 22, 12, 22], fill=shading_color)  # Front window shading
draw.line([18, 22, 22, 22], fill=shading_color)  # Rear window shading

# Draw the wheels
draw.ellipse([7, 35, 13, 41], fill=wheel_color)  # Front wheel
draw.ellipse([17, 35, 23, 41], fill=wheel_color)  # Rear wheel
draw.ellipse([8, 36, 12, 40], fill=(128, 128, 128, 255))  # Front wheel rim
draw.ellipse([18, 36, 22, 40], fill=(128, 128, 128, 255))  # Rear wheel rim

# Draw the headlights (front of the car)
draw.rectangle([24, 25, 26, 27], fill=headlight_color)  # Front headlight
draw.rectangle([24, 28, 26, 30], fill=headlight_color)  # Front headlight

# Draw the grille (front of the car)
draw.rectangle([22, 32, 24, 34], fill=grille_color)  # Grille

# Draw the door handle
draw.rectangle([12, 32, 14, 34], fill=door_handle_color)  # Door handle

# Add wheel spokes
draw.line([10, 36, 10, 40], fill=(192, 192, 192, 255), width=1)  # Front wheel spoke
draw.line([8, 38, 12, 38], fill=(192, 192, 192, 255), width=1)  # Front wheel spoke
draw.line([20, 36, 20, 40], fill=(192, 192, 192, 255), width=1)  # Rear wheel spoke
draw.line([18, 38, 22, 38], fill=(192, 192, 192, 255), width=1)  # Rear wheel spoke

# Save the image
image.save('car_sprite.png')

# Optionally, show the image
image.show()