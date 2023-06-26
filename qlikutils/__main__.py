from .utils import draw_title, BASE_DIR
from PIL import Image
import argparse
import os
import sys
import path


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Qlik Tools')
    parser.add_argument('--project', type=str, required=True, help='project title to be displayed in the thumbnail')
    parser.add_argument('--layer', type=str, required=True, help='layer title to be displayed in the thumbnail (e.g. "Extraction", "Transformation", "Visualization")')
    parser.add_argument('--version', type=str, required=True, help='version title to be displayed in the thumbnail (e.g. "v1.0.0", "v2.0.0")')
    parser.add_argument('--output_dir', type=str, required=False, default=str(path.Path(__file__).parent.parent/'output'), help='Output directory to save the thumbnail (default: "output/")')

    args = parser.parse_args()

    background_img = Image.open(f'{BASE_DIR}/assets/images/background.png')

    final_img = draw_title(background_img, args.project, f'{args.layer} - {args.version}')

    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)
    project_name = args.project.strip().replace(" ", "_").replace("\\", "").replace("/", "")
    filepath = f'{args.output_dir}/{project_name}_{args.layer}_thumbnail_{args.version}.png'
    final_img.save(filepath)

    if sys.platform == 'win32':
        os.system(filepath)
    else:
        sys.stdout.write(f'The file was created in the following path: {filepath}.\n')