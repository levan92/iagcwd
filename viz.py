import time
import argparse
from pathlib import Path

import cv2
import numpy as np

from iagcwd import AdaptiveGamma

parser = argparse.ArgumentParser(description='IAGCWD')
parser.add_argument('input_image', type=str, help='Input image')
args = parser.parse_args()

default_thresh = 0.3
default_exp_in = 112
default_alpha_bright = 0.25
default_alpha_dimmed = 0.75

gamma_adjuster = AdaptiveGamma(
                            thresh= default_thresh, 
                            exp_in= default_exp_in, 
                            agcwd_alpha_bright= default_alpha_bright, 
                            agcwd_alpha_dimmed= default_alpha_dimmed
                            )

cv2_winname = 'Adapative Gamma'
cv2.namedWindow(cv2_winname, cv2.WINDOW_NORMAL)

cv2_winname_orig = 'Original'
cv2.namedWindow(cv2_winname_orig, cv2.WINDOW_NORMAL)


img = cv2.imread(args.input_image)

cv2.imshow(cv2_winname_orig, img)

agcwd_threshold_trackbar_name = 'Threshold'
cv2.createTrackbar(agcwd_threshold_trackbar_name,
                    cv2_winname, 
                    int(gamma_adjuster.threshold*100), 
                    100, 
                    lambda x: gamma_adjuster.update(thresh=x/100) 
                    )  

agcwd_exp_in_trackbar_name = 'Expected Intensity'
cv2.createTrackbar(agcwd_exp_in_trackbar_name,
                    cv2_winname, 
                    gamma_adjuster.exp_in, 
                    255, 
                    lambda x: gamma_adjuster.update(exp_in=x) 
                    )  

agcwd_alpha_bright_trackbar_name = 'Alpha (Bright)'
cv2.createTrackbar(agcwd_alpha_bright_trackbar_name,
                    cv2_winname, 
                    int(gamma_adjuster.agcwd_alpha_bright*100), 
                    100, 
                    lambda x: gamma_adjuster.update(agcwd_alpha_bright=x/100) 
                    )  

agcwd_alpha_dimmed_trackbar_name = 'Alpha(Dimmed)'
cv2.createTrackbar(agcwd_alpha_dimmed_trackbar_name,
                    cv2_winname, 
                    int(gamma_adjuster.agcwd_alpha_dimmed*100), 
                    100, 
                    lambda x: gamma_adjuster.update(agcwd_alpha_dimmed=x/100) 
                    )  

total_dur = 0
dur_count = 0
while True:
    img_in = img.copy()
    tic = time.perf_counter()
    img_out, status = gamma_adjuster.adjust(img_in)
    toc = time.perf_counter()
    total_dur += toc - tic
    dur_count += 1

    # img_show = np.concatenate((img, img_out), axis=1)
    if status == 'dim':
        msg = 'Too Dim'
    elif status == 'bright':
        msg = 'Too Bright'
    else:
        msg = 'Not Adjusted'
    cv2.putText(img_out, msg, (10,10+24), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255,255,0), 2)

    cv2.imshow(cv2_winname, img_out)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    elif key == ord('o'):
        #set back to default values
        cv2.setTrackbarPos(agcwd_threshold_trackbar_name, cv2_winname, int(default_thresh*100) )
        cv2.setTrackbarPos(agcwd_exp_in_trackbar_name, cv2_winname, default_exp_in )
        cv2.setTrackbarPos(agcwd_alpha_bright_trackbar_name, cv2_winname, int(default_alpha_bright*100) )
        cv2.setTrackbarPos(agcwd_alpha_dimmed_trackbar_name, cv2_winname, int(default_alpha_dimmed*100) )

print(f'Adaptive Gamma avg duration: {total_dur/dur_count:.3f}s')
print(f'Final Adapative Gamma Params: ')
print(f"thresh= {gamma_adjuster.threshold}") 
print(f"exp_in= {gamma_adjuster.exp_in}")
print(f"agcwd_alpha_bright= {gamma_adjuster.agcwd_alpha_bright}") 
print(f"agcwd_alpha_dimmed= {gamma_adjuster.agcwd_alpha_dimmed}") 
