import streamlit as st
import datetime
import pytz
from utils.metrics import log_runtime
#from fastai.vision.all import load_learner

short_title = "fastai Image Classification"
long_title = "Image Classification with fastai and PyTorch"
key = 3
content_date = datetime.datetime(2021, 8, 19).astimezone(pytz.timezone("US/Eastern"))
assets_dir = "./assets/" + str(key) + '/'

#@st.cache
'''def predict(image: str)-> str:
    learn_inf = load_learner(assets_dir + 'woodpecker_fastai.pkl')

    return learn_inf.predict(image)[0]'''

@log_runtime
def render(location: st):
    location.markdown(f"## [{long_title}](/?content={key})")
    location.write(f"*{content_date.strftime('%m.%d.%Y')}*")

    location.markdown(
        "Fastai makes transfer learning easy. The main idea behind transfer learning is to use a pre-trained model to "        
        "train a new, more specific model. The new model leverages the strengths of the pre-trained model and fine-tunes it for a specific "
        "task. In some cases, pre-trained models have been trained for hundreds or thousands of hours on very large data sets. In "
        "computer vison, pre-trained models excel at detecting basic image features such as gradients, edges and colors. "
        "Transfer learning allows you to save time and money by customizing a pre-trained model to solve your specific problem."
    )  

    location.markdown(
        "In this post, based on [Chapter 2 of Practical Deep Learning for Coders](https://colab.research.google.com/github/fastai/fastbook/blob/master/02_production.ipynb) "
        ", we'll use a pre-trained model to classify woodpeckers. If you're planning to train your model locally, check out [this article](/?content=2) "
        "to set up your GPU inside a Docker container. The Github repo for this post can be found [here](https://github.com/tkeech1/fastai-image-classification)."
    )
    location.markdown("### Labelled Images")
    location.markdown(
        "First we need to gather labelled woodpecker images for training the model. I had good luck using the Python package [bing-image-downloader](https://pypi.org/project/bing-image-downloader/) to "
        "find images on Bing and save them locally. A word of caution - you'll need to review each image and make sure it's appropriate. You may find that some of the downloaded images "
        "aren't useful. For example, my search for *pileated woodpecker* returned a number of cartoon woodpeckers, paintings, t-shirts, statues and other likenesses of "
        "pileated woodpeckers that aren't relevant for identifying actual birds in images. Other images were simply labelled incorrectly and needed to be removed from the data set."
    )

    location.markdown(
        "Luckily, you don't need thousands of labelled images to get decent results. I found that about 75 images "
        "of each woodpecker type produced good results."
    )

    location.code(
"""
from bing_image_downloader import downloader
downloader.download("pileated woodpecker", limit=150,  output_dir='images', adult_filter_off=True, force_replace=False, timeout=60, verbose=True)
downloader.download("red bellied woodpecker", limit=150,  output_dir='images', adult_filter_off=True, force_replace=False, timeout=60, verbose=True)
"""
    )

    c1, c2 = location.columns(2)
    c1.image(assets_dir + 'pileated woodpecker/Image_145.jpg', width=200)
    c1.markdown("**Pileated Woodpecker**")
    c2.image(assets_dir + 'red bellied woodpecker/Image_143.jpg', width=200)
    c2.markdown("**Red-bellied Woodpecker**")

    location.markdown(
        "bing-image-downloader places images in a directory with the same name as the search term. This works well since fastai provides a `DataBlock` "
        "object for loading images and labels from a directory structure in which the parent directory name is the image label. "
    )

    location.markdown("### DataBlock, Dataset, DataLoader and DataLoaders Images")

    location.markdown(
        "fastai has several APIs that work with and extend PyTorch types. A PyTorch `Dataset` is a collection of tuples containing data (images, in this case) and labels. "
        "One item from a `Dataset` might be a tuple `(<PIL.Image.Image image mode=L size=28x28 at 0x7F5DD45019E8>, 9)` that contains a PIL image and the class label 9. "
        "A PyTorch `DataLoader` wraps a `Dataset` and allows you to easily access batches of images and labels. It also supports shuffling batches after each iteration through the `Dataset`."        
    )

    location.markdown(
        "We could create a `DataLoader` by hand but fastai provides a `DataBlock` API to simplify the creation of the `DataLoader`. To use the `DataBlock` API, "
        "create a `DataBlock` object, passing it a number of parameters that specify the `DataBlock`'s behavior. A few examples are noted below. "
    )

    location.code(
"""
woodpeckers = DataBlock(
    blocks=(ImageBlock, CategoryBlock), # A tuple specifying the type of independent data and dependent data 
    get_items=get_image_files, # A function that can load the data - get_image_files is a fastai function that loads all images in a given path
    splitter=RandomSplitter(valid_pct=.2, seed=42), # A class that splits the data into a training and validation set
    get_y=parent_label, # A function that gets the dependent variable - parent_label labels each image with its parent folder name
    item_tfms=Resize(128), # Transforms to apply to the data - since downloaded images are different sizes, resize them
)

# Now, create the DataLoaders
woodpeckers_dataloaders = woodpeckers.dataloaders(path)
"""        
    )

    location.markdown(
        "Calling `.dataloaders(path)` on the `DataBlock` returns a fastai `DataLoaders` object. A `DataLoaders` wraps a `DataLoader` and splits the  "
        "data into a training data set and a validation data set. fastai uses `DataLoaders` for many API calls for data augmentation and "
        "model training. "
    )

    location.markdown(
        "The diagram below shows how the Dataset, DataLoader and DataLoaders objects are related to one another."
    )

    location.image(f'{assets_dir}data_apis.png', caption='Dataset, DataLoader and DataLoaders Objects', width=None, use_column_width=None, clamp=False, channels='RGB', output_format='auto')

    location.markdown("### Image Augmentation")

    location.markdown(
        "In an image classification problem, it's often useful to create random variations in the training images, a practice known as "
        "image augmentation. Random image transformations such as cropping, flipping, blurring and adding other elements of visual noise can "
        "help create a more generalizeable model. "
        "fastai provides a function, `aug_transforms()`, that implements a number of transforms which can be applied to training data. When `batch_tfms=aug_transforms()` is used "
        "as shown below, image transformations are applied on the GPU so it's extremely fast. "        
    )

    location.code(
"""
woodpeckers = woodpeckers.new(item_tfms=RandomResizedCrop(224, min_scale=.5), batch_tfms=aug_transforms())
dls = woodpeckers.dataloaders(path)
dls.train.show_batch(max_n=8, nrows=2, unique=True) # unique=True shows the same image repeated with different ResizedRandomCrop transforms applied
"""        
    )

    location.markdown(
        "The resulting images look like this:"        
    )
    location.image(assets_dir + 'fastai_image_transforms.png')
    
    location.markdown("### Transfer Learning")

    location.markdown("fastai simplifies the transfer learning code down to two lines:")

    location.code(
"""
learn = cnn_learner(dls, resnet18, metrics=error_rate)
learn.fine_tune(8)
"""        
    )

    location.markdown("The first line creates a \"learner\" based on the [RESNET18](https://pytorch.org/hub/pytorch_vision_resnet/) architecture. "
    " The second line instructs fastai to fine-tune the model for 8 epochs.")

    location.markdown('''
Under the hood, fastai performs a number of steps:

1. Removes the last layer of the RESNET18 model and replaces it with a new linear layer containing the appropriate number of outputs based on the number of classes (2 in this case - Pileated Woodpecker and Red-bellied Woodpecker)
2. Initializes random weights for the new linear layer
3. Freezes the weights for the remaining layers of the RESNET18 model
4. Trains the new linear layer for one epoch
5. Unfreezes all model layers and trains the model for the number of epochs specified in `fine_tune()`''')

    location.markdown("`fine_tune()` provides "
    " a simple way to get reasonable results quickly. fastai exposes additional functions such as `fit_one_cycle()`, `freeze()` and `unfreeze()` for customizing"
    " the model building process. Using `fine_tune()` I was able to get around 97% accuracy on the validation set using around 75 training images per class.")

    # commenting this section out since ec2 instance doesn't have enough memory to run predictions
    '''location.markdown("Try making predictions on few samples by clicking the `Predict` button below")

    c1, c2, c3, _ = location.columns((1,1,1,1))
    img1 = assets_dir + 'pileated woodpecker/Image_1.jpg'
    c1.image(img1, width=224)
    location_img1 = c1.empty()
    if c1.button('Predict', key=1):        
        #progress_bar = location.progress(0)
        location_img1.markdown(predict(img1))
        #progress_bar.progress(100) 
    img2 = assets_dir + 'red bellied woodpecker/Image_1.jpg'
    c2.image(img2, width=224)    
    location_img2 = c2.empty()
    if c2.button('Predict', key=2):
        #progress_bar = location.progress(0)
        location_img2.markdown(predict(img2))
        #progress_bar.progress(100)
    img3 = assets_dir + 'red bellied woodpecker/Image_27.jpeg'
    c3.image(img3, width=224)    
    location_img3 = c3.empty()
    if c3.button('Predict', key=3):
        #progress_bar = location.progress(0)
        location_img3.markdown(predict(img3))
        #progress_bar.progress(100)

        '''

    location.markdown(
        "[Practical Deep Learning for Coders](https://course.fast.ai/) is a great introduction to neural "
        "networks and transfer learning using fastai and PyTorch. Jeremy Howard and Sylvain Gugger incrementally step through "
        "excellent examples that help you to form a solid intuition about concepts like loss functions and optmization. "
        "Best of all, the book is freely available online! If you're interested in neural networks, it's definitely worth the time. "
        "Thanks for reading."
    )

    location.markdown("### Resources")

    location.write(
        """
    * [fastai Course](https://course.fast.ai/)
    * [PyTorch Datasets & DataLoaders](https://pytorch.org/tutorials/beginner/basics/data_tutorial.html)
    * [Deep Residual Learning for Image Recognition](https://arxiv.org/abs/1512.03385)
    * [Diagrams.net](https://app.diagrams.net/)
    * [Bing Image Downloader on Pypi](https://pypi.org/project/bing-image-downloader/) 

"""
    )
