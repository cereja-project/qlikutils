from .utils import draw_texts, resize_image, BASE_DIR
from PIL import Image
import argparse
import os
import sys
import path
import platform


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Qlik Tools')
    parser.add_argument('--title', type=str, required=True, help='project title to be displayed in the thumbnail (max 20 characters)')
    parser.add_argument('--subtitle', type=str, required=True, help='project subtitle to be displayed in the thumbnail (max 30 characters)')
    parser.add_argument('--version', type=str, required=True, help='project version to be displayed in the thumbnail (max 10 characters) (e.g. "v1.0", "v2.0")')
    parser.add_argument('--background', type=str, required=False, default=str(path.Path(__file__).parent/'assets'/'images'/'background.png'), help='Background image to be used (default: "assets/images/background.png")')
    parser.add_argument('--output_dir', type=str, required=False, default=str(path.Path(__file__).parent.parent/'output'), help='Output directory to save the thumbnail (default: "output/")')
    parser.add_argument('--title_position', type=str, required=False, default='center', choices=['center', 'left', 'right'], help='Title position (default: "center")')
    parser.add_argument('--version_position', type=str, required=False, default='center', choices=['center', 'left', 'right'], help='Version position (default: "center")')
    parser.add_argument('--color', type=str, required=False, default='white', choices=['white', 'blue'], help='Text color (default: "white")')
    # parser.add_argument('--title_font', type=str, required=False, default=str(path.Path(__file__).parent/'assets'/'fonts'/'Rubik-Medium.ttf'), help='Font to be used (default: "assets/fonts/Rubik-Medium.ttf")')
    # parser.add_argument('--subtitle_font', type=str, required=False, default=str(path.Path(__file__).parent/'assets'/'fonts'/'Rubik-Regular.ttf'), help='Font to be used (default: "assets/fonts/Rubik-Regular.ttf")')
    # parser.add_argument('--version_font', type=str, required=False, default=str(path.Path(__file__).parent/'assets'/'fonts'/'Rubik-Regular.ttf'), help='Font to be used (default: "assets/fonts/Rubik-Regular.ttf")')

    args = parser.parse_args()

    assert len(args.title) <= 20, "--title str has more than 20 characters"
    assert len(args.subtitle) <= 30, "--subtitle str has more than 30 characters"
    assert len(args.version) <= 10, "--version str has more than 10 characters"

    background_img = Image.open(f'{args.background}')
    background_img = resize_image(background_img, 800, 500)

    final_img = draw_texts(background_img, args.title, args.subtitle, args.version, title_position=args.title_position, version_position=args.version_position, color=args.color)

    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)
    project_name = args.title.strip().replace(" ", "_").replace("\\", "").replace("/", "")
    filepath = f'{args.output_dir}/{project_name}_{args.subtitle}_thumbnail_{args.version}.png'
    final_img.save(filepath)

    if platform.system() == "Darwin":  # macOS
        os.system(f'open "{filepath}"')
    elif platform.system() == "Linux":
        os.system(f'xdg-open "{filepath}"')
    
    sys.stdout.write(f'The file was created in the following path: {filepath}.\n')
