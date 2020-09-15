import argparse
from pathlib import Path

import cv2

from iagcwd import AdaptiveGamma


parser = argparse.ArgumentParser(description='IAGCWD')
parser.add_argument('--input', dest='input_dir', default='./example_images/', type=str, \
                    help='Input directory for image(s), defaults to ./example_images/')
args = parser.parse_args()

input_dir = Path(args.input_dir)
assert input_dir.is_dir()

gamma_adjuster = AdaptiveGamma(
                            thresh=0.3, 
                            exp_in = 112, 
                            agcwd_alpha_bright=0.25, 
                            agcwd_alpha_dimmed=0.75
                            )

imgs = [ img for img in input_dir.glob('*') if img.is_file() and img.suffix.casefold() in ['.jpg','.png'] ]

for img_path in imgs:
    img = cv2.imread(str(img_path), 1)
    img_out = gamma_adjuster.adjust(img)

    out_path = img_path.parent / f'{img_path.stem}_agced.jpg'
    cv2.imwrite( str(out_path), img_out)

    # cv2.imshow('Original', img)
    # cv2.imshow('AGCed', img_out)
    # cv2.waitKey(0)