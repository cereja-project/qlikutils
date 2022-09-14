from PIL import ImageDraw, ImageFont

def get_text_dimensions(text_string, font):
    # https://stackoverflow.com/a/46220683/9263761
    ascent, descent = font.getmetrics()

    text_width = font.getmask(text_string).getbbox()[2]
    text_height = font.getmask(text_string).getbbox()[3] + descent

    return (text_width, text_height)

def draw_title(img, title, subtitle, color=(255, 255, 255)):
    img_width, img_height = img.size
    draw = ImageDraw.Draw(img)

    title_font = ImageFont.truetype("Arial Black.ttf", 400)
    subtitle_font = ImageFont.truetype("Arial.ttf", int(400 * 0.30))

    title_width, title_height = get_text_dimensions(title, title_font)
    subtitle_width, subtitle_height = get_text_dimensions(subtitle, subtitle_font)

    title_position = ((img_width-title_width)/2, 100)
    subtitle_position = ((img_width - subtitle_width) / 2, 600)

    draw.text(title_position, title, color, font=title_font)
    draw.text(subtitle_position, subtitle, color, font=subtitle_font)

    return img
