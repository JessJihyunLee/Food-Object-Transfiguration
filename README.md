# Food-Object-Transfiguration
Repository for Cognitive Computing final project: image transfer between Chicken Wings and Bluberry Muffins

# Image scraper setup
1. Clone my fork of the recipe-scraper project:
`git clone https://github.com/huynhtastic/recipe-scrapers.git`
2. CD into recipe-scrapers
3. Run `python setup.py install`
4. Before implemented, each folder has images of chicken wings and blueberry muffins and named after food name.

# Cycle GAN setup
1. First split images to train and test data set. I used paperspace python 3.
   Refer to [Preprocess Before Run](https://github.com/JessJihyunLee/Food-Object-Transfiguration/blob/master/Cycle-GAN/preprocess_beforerun.py)
2. Run python files in following order (CD):
`python build_dataset.py foodcycleGAN/trainA foodcycleGAN/trainB trainA trainB`</br>
`python utils.py`</br>
`python generator.py`</br>
`python discriminator.py`</br>
`python cyclegan.py`</br>
`python example.py`</br>
