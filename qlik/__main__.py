from .utils import draw_title
from PIL import Image
import argparse
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Qlik Tools')
    parser.add_argument('--project', type=str, required=True)
    parser.add_argument('--layer', type=str, required=True, choices=['Extração', 'Transformação', 'Visualização'])
    parser.add_argument('--version', type=str, required=True)
    parser.add_argument('--output_dir', type=str, required=True)

    args = parser.parse_args()

    # project = input("Digite o nome do projeto: ")
    # layer = input("Digite o nome da camada: ")
    # version = input("Digite a versão da aplicação: ")

    background_img = Image.open(f'{BASE_DIR}/assets/background.png')

    final_img = draw_title(background_img, args.project, f'{args.layer} - {args.version}')

    final_img.save(f'{args.output_dir}/{args.project}_{args.layer}_tumbnail_{args.version}.png')
