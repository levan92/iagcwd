# Improved Adaptive Gamma Correction

Forked from [here](https://github.com/leowang7/iagcwd).

## Requirements

- Python >= 3.6
- Opencv >= 3.4.1
- Numpy >= 1.14.4

## Example Usage

See `run.py` for example

```
python3 run.py --input example_images
```

## Adjustable Params

By default you don't need to define any arguments in the `AdaptiveGamma` class. But you can adjust them if you want:

- `thresh`: threshold to determin image is bright or dim (Default: 0.3)
- `exp_in`: expected global average intensity (Default: 112)

In the AGCWD algorithm, a weighting distribution function is used to smooth the primary histogram. $\alpha$ is an adjusted parameter that affects the smoothing, the smaller, the smoother the histogram. In IAGCWD, bright and dim images receive different treatments and their $\alpha$ values differs. See paper for more info.

- `agcwd_alpha_bright`: As explained above (Default: 0.25)
- `agcwd_alpha_dimmed`: As explained above (Default: 0.75)

<br/>

# [Original README] Improved Adaptive Gamma Correction
This is an python implementation of the paper "Contrast enhancement of brightness-distorted images by improved adaptive gamma correction." at https://arxiv.org/abs/1709.04427. The purpose of the algorithm is to improve the contrast of the image adaptively.

## System Environment
- Ubuntu 18.04.1 LTS
- Python >= 3.6
- Opencv >= 3.4.1
- Numpy >= 1.14.4

## Gamma Correction Results
![results](docs/img/test_results.png)

## Running the tests
```
python IAGCWD.py --input ./input --output ./output
```

## References
Cao, Gang, et al. "Contrast enhancement of brightness-distorted images by improved adaptive gamma correction." Computers & Electrical Engineering 66 (2018): 569-582.
