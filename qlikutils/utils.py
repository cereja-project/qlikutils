from PIL import ImageDraw, ImageFont, Image
import os
from unidecode import unidecode

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def get_file_name(title: str, subtitle: str, version: str) -> str:
    """
    Get the file name based on the title, subtitle and version.
    
    Args:
        title (str): The project title.
        subtitle (str): The project subtitle.
        version (str): The project version.

    Returns:
        str: The file name with png extension.
    """
    project_name = title.strip().replace(" ", "_").replace("\\", "").replace("/", "")
    subtitle_name = subtitle.strip().replace(" ", "_").replace("\\", "").replace("/", "")
    version_name = version.strip().replace(" ", "_").replace("\\", "").replace("/", "")
    return f'{project_name}_{subtitle_name}_thumbnail_{version_name}.png'

def parse_color(value):
    value = value.lstrip('#')  # Remove the '#' character if present
    length = len(value)

    if length not in (3, 6):
        print("Error: The color must be a 3 or 6-digit hexadecimal code (e.g., 'FFA500' or 'F00').")
        return None  # Return None to indicate an error

    try:
        # Try to convert the value into an RGB tuple
        rgb = tuple(int(value[i:i + length // 3], 16) for i in range(0, length, length // 3))
        return rgb
    except ValueError:
        print(f"Error: Invalid color value: '{value}'. The color must be a valid hexadecimal code.")
        return None  # Return None to indicate an error


def get_font_size(text: str, font: ImageFont, image_size: float, max_font_size: int = 400, padding_percent: float = 0.15):
    # Get the biggest word in the text
    largest_word = max(text.split('\n'), key=len).strip()
    largest_word_size = len(largest_word)

    font = ImageFont.truetype(font.path, max_font_size)
    while font.getsize(largest_word)[0] > (image_size * (1-padding_percent)) and font.size > 10:
        font = ImageFont.truetype(font.path, font.size - 10)

    return font.size

def wrap_text(text: str, max_size: int = 11) -> str:
    # Get max line size
    text_size = len(text)
    biggest_word_size = max([len(word) for word in text.split()])
    max_line_size = max_size if biggest_word_size < max_size else biggest_word_size
    
    # Get the lines
    lines = ['']
    for word in text.split():
        line = f'{lines[-1]} {word}'.strip()
        if '\\n' in line:                               
            # If the line has a line break
            lines[-1] = line.split('\\n')[0].strip()
            lines.append(line.split('\\n')[1].strip())
        elif len(line) < max_line_size * 1.1:           
            # If the line is smaller than the max line size
            lines[-1] = line
        else:                                           
            # If the line is bigger than the max line size
            lines.append(word)

    return '\n'.join(lines).strip()


def get_text_dimensions(text_string, font, img_width, img_height):
    # https://stackoverflow.com/a/46220683/9263761
    ascent, descent = font.getmetrics()

    # Get the largest line in the text
    largest_line = max(text_string.split('\n'), key=len).strip()
    lines_count = len(text_string.split('\n'))

    text_width = font.getmask(largest_line).getbbox()[2]
    text_height = font.getmask(largest_line).getbbox()[3] - descent

    return (text_width, text_height)
    
def draw_texts(img, title, subtitle, version, color=(255, 255, 255), title_position='center', version_position='center'):
    img_width, img_height = img.size
    draw = ImageDraw.Draw(img)

    wrapped_text = wrap_text(title)

    # Get color
    if color == 'white':
        color = (255, 255, 255)
    elif color == 'black':
        color = (0, 0, 0)
    elif color.startswith('#'):
        color = parse_color(color)


    # Draw title
    title_font = ImageFont.truetype(f'{BASE_DIR}/assets/fonts/Rubik-Medium.ttf', 95)
    title_width, title_height = get_text_dimensions(wrapped_text, title_font, img_width, img_height)

    lines_qty = len(wrapped_text.split('\n'))
    title_margin_top = 0.175 * img_height # 17.5% of the image height
    title_block_height = (0.30 if lines_qty == 1 else 0.40) * img_height # 40% of the image height
    line_spacing_height = min(35, ( title_block_height - (lines_qty * title_height) ) // (lines_qty - 1)) if lines_qty > 1 else 0
    title_padding_top = ( title_block_height - (lines_qty * title_height) - ( (lines_qty - 1) * line_spacing_height) ) // 2
    title_padding_top += 0.05 * img_height if lines_qty == 1 else 0 # 0.36% of margin between title and subtitle area
    
    current_h = title_margin_top + title_padding_top
    for title_line in wrapped_text.split('\n'):
        # TODO: For some reason neither the variables 'h' or 'title_height' has the exactly font size. But it is almost in the center
        w, h = draw.textsize(title_line, font=title_font)

        if title_position == 'center':
            title_position_axis = ((img_width - w) // 2, current_h)
        elif title_position == 'left':
            title_position_axis = (0.125 * img_width, current_h)
        elif title_position == 'right':
            title_position_axis = (img_width - w - (0.125 * img_width), current_h)

        draw.text(title_position_axis, title_line, color, font=title_font, spacing=0, anchor="lt")
        current_h += title_height + line_spacing_height

    # Draw subtitle
    subtitle_font = ImageFont.truetype(f'{BASE_DIR}/assets/fonts/Rubik-Regular.ttf', 45)

    subtitle_width, subtitle_height = get_text_dimensions(subtitle, subtitle_font, img_width, img_height)
    subtitle_margin_top = title_margin_top + title_block_height + (0.036 * img_height) 

    if title_position == 'center':
        subtitle_position_axis = ((img_width - subtitle_width) // 2, subtitle_margin_top)
    elif title_position == 'left':
        subtitle_position_axis = (0.125 * img_width, subtitle_margin_top)
    elif title_position == 'right':
        subtitle_position_axis = (img_width - subtitle_width - (0.125 * img_width), subtitle_margin_top)

    draw.text(subtitle_position_axis, subtitle, color, font=subtitle_font, anchor="lt")

    # Draw version'
    version_font = ImageFont.truetype(f'{BASE_DIR}/assets/fonts/Rubik-Regular.ttf', 35)
    version_width, version_height = get_text_dimensions(version, version_font, img_width, img_height)

    if version_position == 'center':
        version_position_axis = ((img_width - version_width) // 2, img_height - (0.175 * img_height))
    elif version_position == 'left':
        version_position_axis = (0.125 * img_width, img_height - (0.175 * img_height))
    elif version_position == 'right':
        version_position_axis = (img_width - version_width - (0.125 * img_width), img_height - (0.175 * img_height))

    draw.text(version_position_axis, version, color, font=version_font, anchor="lt")

    return img

def resize_image(img, img_width, img_height):
    # Resize proportionally
    original_proportion = img.size[0] / img.size[1]
    new_proportion = img_width / img_height
    if original_proportion > new_proportion: # If the original image is wider than the desired proportion, fit it by the height
        new_proportional_width = img.size[0] - ((img.size[1] - img_height) * original_proportion)
        img = img.resize((int(new_proportional_width), img_height), Image.ANTIALIAS)
    elif original_proportion < new_proportion: # If the original image is taller than the desired proportion, fit it by the width
        new_proportion_height = int(img.size[1] - ((img.size[0] - img_width) / original_proportion))
        img = img.resize((img_width, int(new_proportion_height)), Image.ANTIALIAS)
    else: # If the original image has the same proportion as the desired size, just resize it
        img.thumbnail((img_width, img_height), Image.ANTIALIAS)
        return img

    # Crop the image to the desired size
    if img.size[0] != img_width: # If the image is wider than the desired size, crop it by the width
        x0 = (img.size[0] - img_width) // 2
        x1 = x0 + img_width
        y0 = 0
        y1 = img_height
        img = img.crop((x0, y0, x1, y1))
    
    if img.size[1] != img_height: # If the image is taller than the desired size, crop it by the height
        x0 = 0
        x1 = img_width
        y0 = (img.size[1] - img_height) // 2
        y1 = y0 + img_height
        img = img.crop((x0, y0, x1, y1))

    return img
