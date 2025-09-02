from PIL import Image, ImageDraw
import random

def make_detailed_sprite(size=16):
    """Return a detailed humanoid base sprite with clothing, hair, and shoes."""
    img = Image.new("RGBA", (size, size), (0,0,0,0))
    d = ImageDraw.Draw(img)

    # Colors
    skin = random.choice([(255,224,189),(229,194,152),(141,85,36)])
    hair = random.choice([(0,0,0),(120,60,20),(200,180,50),(255,255,255)])
    shirt = random.choice([(200,50,50),(50,200,50),(50,50,200),
                           (200,200,50),(200,100,200)])
    pants = random.choice([(40,40,120),(80,40,0),(20,100,80)])
    shoes = random.choice([(60,60,60),(200,200,200),(100,0,0)])
    eye = (255,255,255)
    outline = (0,0,0)

    # Body (torso with shirt)
    d.rectangle([4,6,size-5,size-2], fill=shirt, outline=outline)

    # Head (skin)
    d.rectangle([5,0,size-6,6], fill=skin, outline=outline)

    # Eyes
    d.point((6,2), fill=eye)
    d.point((size-7,2), fill=eye)

    # Hair (random style)
    style = random.choice(["short","long","mohawk"])
    if style == "short":
        d.rectangle([5,-1,size-6,2], fill=hair)  # top row
    elif style == "long":
        d.rectangle([4,0,size-5,4], fill=hair)
        d.rectangle([4,0,4,6], fill=hair)  # sideburns
        d.rectangle([size-5,0,size-5,6], fill=hair)
    elif style == "mohawk":
        d.rectangle([7,-1,8,3], fill=hair)

    # Arms (shirt color)
    d.rectangle([3,7,4,11], fill=shirt, outline=outline)
    d.rectangle([size-5,7,size-4,11], fill=shirt, outline=outline)

    # Pants
    d.rectangle([4,11,size-5,14], fill=pants, outline=outline)

    # Legs
    d.rectangle([6,size-6,7,size-2], fill=pants, outline=outline)
    d.rectangle([size-8,size-6,size-7,size-2], fill=pants, outline=outline)

    # Shoes
    d.rectangle([6,size-3,7,size-2], fill=shoes, outline=outline)
    d.rectangle([size-8,size-3,size-7,size-2], fill=shoes, outline=outline)

    return img

def animate_sprite(base, col, row):
    """Modify base sprite slightly depending on frame col and direction row."""
    frame = base.copy()
    d = ImageDraw.Draw(frame)
    w,h = base.size

    # Animate legs
    if col == 0: # left step
        d.rectangle([6,h-6,7,h-2], fill=(0,0,0,0)) # clear
        d.rectangle([5,h-7,6,h-3], fill=(0,0,0))   # step
    elif col == 2: # right step
        d.rectangle([w-8,h-6,w-7,h-2], fill=(0,0,0,0))
        d.rectangle([w-9,h-7,w-8,h-3], fill=(0,0,0))

    # Animate arms
    if col == 0:
        d.rectangle([3,7,4,11], fill=(0,0,0,0)) # hide left arm
    elif col == 2:
        d.rectangle([w-5,7,w-4,11], fill=(0,0,0,0)) # hide right arm

    return frame

def generate_sheet(size=16, scale=4):
    base = make_detailed_sprite(size)
    w,h = base.size
    sheet = Image.new("RGBA", (w*3, h*4), (0,0,0,0))

    for row in range(4): # down,left,right,up
        for col in range(3): # stepL,idle,stepR
            frame = animate_sprite(base, col, row)
            sheet.paste(frame, (col*w,row*h))

    # Scale up for game
    sheet = sheet.resize((w*3*scale,h*4*scale), Image.NEAREST)
    sheet.save("character_sheet.png")
    print("✅ Saved character_sheet.png")

if __name__=="__main__":
    generate_sheet()
