# Food-Object-Transfiguration
Repository for Cognitive Computing final project: image transfer between Chicken Wings and Bluberry Muffins

# Image scraper setup
1. Clone my fork of the recipe-scraper project:
`git clone https://github.com/huynhtastic/recipe-scrapers.git`
2. CD into recipe-scrapers
3. Run `python setup.py install`
4. Before implemented, each folder has images of chicken wings and blueberry muffins and named after food name.</br>
   Folders are under higher level folder name 'foodcycleGAN'

# Performance Comparison among Cycle GAN, DualGAN, and XGAN on Food Object Transfiguraion
* Model performance and insights are posted on Medium:</br> *
[Object Transfiguration : Chicken Wings to Blueberry Muffins using GANs](https://medium.com/@carollee827/object-transfiguration-chicken-wings-to-blueberry-muffins-using-discogan-cyclegan-dualgan-and-d4953be7a0ce)

# GAN setup
### Cycle GAN setup
1. First split images to train and test data set. I used paperspace python 3.
   Refer to [Preprocess Before Run](https://github.com/JessJihyunLee/Food-Object-Transfiguration/blob/master/Cycle-GAN/preprocess_beforerun.py)
2. Run python files in following order (CD) :</br>
`python build_dataset.py foodcycleGAN/trainA foodcycleGAN/trainB trainA trainB`</br>
`python utils.py`</br>
`python generator.py`</br>
`python discriminator.py`</br>
`python cyclegan.py`</br>
`python example.py`</br>

### DualGAN setup
1. Split images
2. Run python files in following order (CD) :<br/>
`python utils.py`</br>
`python ops.py`</br>
`python model.py`</br>
`python main.py --phase train --dataset_name fooddualGAN`</br>

### XGAN setup
1. Split images same as [XGAN Preprocess Before Run](https://github.com/JessJihyunLee/Food-Object-Transfiguration/blob/master/X-GAN/Preprocess_beforerun.py)
2. Run python files in following order (CD) :</br>
`python utils.py`</br>
`python ops.py`</br>
`python flip_gradient.py`</br>
`python module.py`</br>
`python model.py`</br>
`python main.py --dataset './foodXGAN'`</br>

### Reference
Codes are modified from :</br>
* [DualGAN](https://github.com/watsonyanghx/DualGAN)</br>
* [XGAN](https://github.com/CS2470FinalProject/X-GAN)</br>
