from .utils import draw_title, resize_image, BASE_DIR
from PIL import Image
import argparse
import os
import sys
import path


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Qlik Tools')
    parser.add_argument('--title', type=str, required=True, help='project title to be displayed in the thumbnail (max 50 characters)')
    parser.add_argument('--subtitle', type=str, required=True, help='project subtitle to be displayed in the thumbnail (max 20 characters)')
    parser.add_argument('--version', type=str, required=True, help='project version to be displayed in the thumbnail (max 10 characters) (e.g. "v1.0", "v2.0")')
    parser.add_argument('--background', type=str, required=False, default=str(path.Path(__file__).parent/'assets'/'images'/'background.png'), help='Background image to be used (default: "assets/images/background.png")')
    parser.add_argument('--output_dir', type=str, required=False, default=str(path.Path(__file__).parent.parent/'output'), help='Output directory to save the thumbnail (default: "output/")')

    args = parser.parse_args()

    assert len(args.title) <= 50, "--title str has more than 50 characters"
    assert len(args.subtitle) <= 20, "--subtitle str has more than 20 characters"
    assert len(args.version) <= 10, "--version str has more than 10 characters"

    background_img = Image.open(f'{args.background}')
    background_img = resize_image(background_img, 1572, 980)

    final_img = draw_title(background_img, args.title, f'{args.subtitle} - {args.version}')

    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)
    project_name = args.title.strip().replace(" ", "_").replace("\\", "").replace("/", "")
    filepath = f'{args.output_dir}/{project_name}_{args.subtitle}_thumbnail_{args.version}.png'
    final_img.save(filepath)

    if sys.platform == 'win32':
        os.system(filepath)
    else:
        sys.stdout.write(f'The file was created in the following path: {filepath}.\n')