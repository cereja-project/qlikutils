from PIL import ImageDraw, ImageFont
import os
from unidecode import unidecode

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def get_font_size(text: str, font: ImageFont, image_size: float, max_font_size: int = 400, padding_percent: float = 0.15):
    # Get the biggest word in the text
    largest_word = max(text.split('\n'), key=len).strip()
    largest_word_size = len(largest_word)

    font = ImageFont.truetype(font.path, max_font_size)
    while font.getsize(largest_word)[0] > (image_size * (1-padding_percent)) and font.size > 10:
        font = ImageFont.truetype(font.path, font.size - 10)

    return font.size

def get_wrapped_text(text: str, max_size: int = 20) -> str:
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

def draw_title(img, title, subtitle, color=(255, 255, 255)):
    img_width, img_height = img.size
    draw = ImageDraw.Draw(img)

    wrapped_text = get_wrapped_text(title)

    title_font = ImageFont.truetype(f'{BASE_DIR}/assets/fonts/Arial Black.ttf',
                                    get_font_size(wrapped_text, ImageFont.truetype(f'{BASE_DIR}/assets/fonts/Arial Black.ttf'), img_width, 400))
    # subtitle_font = ImageFont.truetype(f'{BASE_DIR}/assets/fonts/Arial.ttf', 
                                    # get_font_size(subtitle, ImageFont.truetype(f'{BASE_DIR}/assets/fonts/Arial.ttf'), img_width, int(400 * 0.30)))
    subtitle_font = ImageFont.truetype(f'{BASE_DIR}/assets/fonts/Arial.ttf', int(400 * 0.30))

    title_width, title_height = get_text_dimensions(wrapped_text, title_font, img_width, img_height)
    subtitle_width, subtitle_height = get_text_dimensions(subtitle, subtitle_font, img_width, img_height)

    lines_qty = len(wrapped_text.split('\n'))
    fixed_margin_top = 0.05 * img_height # 5% of the image height
    title_block_height = (img_height // 2) - fixed_margin_top # Area where the title will be drawn
    line_spacing_size = min(70, (title_block_height - (lines_qty * title_height)) / (lines_qty - 1)) if lines_qty > 1 else 0
    var_margin_top = ( title_block_height - (lines_qty * title_height) - ((lines_qty - 1) * line_spacing_size) ) // 2
    
    current_h = fixed_margin_top + var_margin_top
    for title_line in wrapped_text.split('\n'):
        w, h = draw.textsize(title_line, font=title_font)
        draw.text(((img_width - w) / 2, current_h), title_line, color, font=title_font)
        current_h += title_height + line_spacing_size

    subtitle_position = ((img_width - subtitle_width) / 2, 600)
    draw.text(subtitle_position, subtitle, color, font=subtitle_font)

    return img