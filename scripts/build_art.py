import os 
import re 
import glob 
import math 
from PIL import Image, ImageFilter
import pandas

this_dir = os.path.dirname(os.path.dirname(__file__))


def add_glow_around_image(image, glow_color=(0, 0, 0), radius=10):
    # Create a glow effect by blurring the alpha channel of the image
    blurred_mask = image.filter(ImageFilter.GaussianBlur(radius=radius))

    # Create a solid color image with the darker glow color and apply the blurred alpha as its mask
    glow_image = Image.new("RGBA", image.size, (0, 0, 0, 0))
    colored_glow = Image.new("RGBA", image.size, glow_color + (255,))

    # Paste the original image on top of the glow effect
    glow_image.paste(colored_glow, (0, 0), blurred_mask)
    glow_image.paste(image, (0, 0), image)

    return glow_image


def apply_blur(image, radius=3):
    # Apply a Gaussian blur to the image
    return image.filter(ImageFilter.GaussianBlur(radius=radius))


def add_spiral_effect(image_path, output_path, angle=90):
    # Open the image
    image = Image.open(image_path).convert("RGBA")

    # Create a new image with the same size and a transparent background
    new_image = Image.new("RGBA", image.size, (0, 0, 0, 0))

    # Get the center of the image
    center_x, center_y = image.size[0] // 2, image.size[1] // 2

    # Apply the spiral effect
    for y in range(image.size[1]):
        for x in range(image.size[0]):
            # Calculate the distance and angle from the center
            dx = x - center_x
            dy = y - center_y
            distance = (dx**2 + dy**2)**0.5
            original_angle = math.atan2(dy, dx)

            # Apply the spiral transformation
            twist_angle = angle * (distance / max(image.size))
            new_angle = original_angle + math.radians(twist_angle)

            # Calculate the new coordinates
            new_x = int(center_x + distance * math.cos(new_angle))
            new_y = int(center_y + distance * math.sin(new_angle))

            # Copy the pixel if it's within bounds
            if 0 <= new_x < image.size[0] and 0 <= new_y < image.size[1]:
                new_image.putpixel((x, y), image.getpixel((new_x, new_y)))

    # Save the new image
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    new_image.save(output_path, "PNG")
    print(f"Saved: {output_path}")

# Load the default background image
default_background_image = Image.open(os.path.join(this_dir, "resource/pokemon_backgrounds/default.png")).convert("RGBA")


def build_art(pokemon_image_path, background_image_path, output_image_path):
    # Open the images
    pokemon_image = Image.open(pokemon_image_path).convert("RGBA")

    # Use a cached default background image if the background image is not found
    global default_background_image
    if not os.path.exists(background_image_path):
        print(f"Background image not found: {background_image_path}")
        background_image = default_background_image.copy()
    else:
        background_image = Image.open(background_image_path).convert("RGBA")

    # Resize both images 
    size = (564, 396)
    # Make sure the pokemon image size is not larger than the size 
    # and keep the aspect ratio the same 
    factor = min(size[0] / pokemon_image.size[0], size[1] / pokemon_image.size[1]) * 0.6  # Multiplier to take up size compared to the background
    pokemon_size = (int(pokemon_image.size[0] * factor), int(pokemon_image.size[1] * factor))
    
    pokemon_image = pokemon_image.resize(pokemon_size)
    background_image = background_image.resize(size)

    # Add space around the pokemon image so that it can be centered on the background and its size matches the background size
    new_pokemon_image = Image.new("RGBA", size, (0, 0, 0, 0))
    new_pokemon_image.paste(pokemon_image, ((size[0] - pokemon_image.size[0]) // 2, (size[1] - pokemon_image.size[1]) // 2), pokemon_image)
    pokemon_image = new_pokemon_image

    # Apply effects to the images
    pokemon_image = add_glow_around_image(pokemon_image)
    background_image = apply_blur(background_image)

    # Create a new image with the same size as the background
    new_image = Image.new("RGBA", size)

    # Paste the background and pokemon images onto the new image
    new_image.paste(background_image, (0, 0))
    new_image.paste(pokemon_image, (0, 0), pokemon_image)

    # Save the new image
    os.makedirs(os.path.dirname(output_image_path), exist_ok=True)
    new_image.save(output_image_path, "PNG")
    print(f"Saved: {output_image_path}")


def get_pokemon_name_number(card_name):
    num = int(card_name.split(" ")[0])
    name = card_name.split(" ")[1]
    return num, name 


if __name__ == "__main__":
    # Loop through all the images in the folder
    pokemon_path_folder = os.path.join(this_dir, "resource/pokemon_art")
    background_path_folder = os.path.join(this_dir, "resource/pokemon_backgrounds")

    output_path_folder = os.path.join(this_dir, "generated_card_art")

    for image in os.listdir(pokemon_path_folder):
        try:
            pokemon_image_path = f"{pokemon_path_folder}/{image}"

            pkmn_num, pkmn_name = get_pokemon_name_number(image)
            output_image_path = f"{output_path_folder}/{pkmn_num}_{pkmn_name}.png"

            
            background_image_path = f"{background_path_folder}/{pkmn_num}.*"
            background_image_path = glob.glob(background_image_path)[0] if glob.glob(background_image_path) else ''

            build_art(pokemon_image_path, background_image_path, output_image_path)
        except Exception as e:
            print(f"Error processing {image}: {e}")
            continue
