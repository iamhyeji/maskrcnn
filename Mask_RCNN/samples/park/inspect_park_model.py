import os
import sys
import random
import math
import numpy as np
import collections
import skimage.io
import matplotlib
import matplotlib.pyplot as plt

# Root directory of the project
ROOT_DIR = os.path.abspath("../../")

# Import Mask RCNN
sys.path.append(ROOT_DIR)  # To find local version of the library
from mrcnn import utils
import mrcnn.model as modellib
from mrcnn import visualize
# Import COCO config
sys.path.append(os.path.join(ROOT_DIR, "samples/park/"))  # To find local version
import park


# Directory to save logs and trained model
MODEL_DIR = os.path.join(ROOT_DIR, "logs")

# Local path to trained weights file
PARK_MODEL_PATH = os.path.join(ROOT_DIR, "mask_rcnn_area_0010.h5")
# Download COCO trained weights from Releases if needed
if not os.path.exists(PARK_MODEL_PATH):
    utils.download_trained_weights(PARK_MODEL_PATH)

# Directory of images to run detection on
IMAGE_DIR = os.path.join(ROOT_DIR, "samples/park/park_Camera")

class InferenceConfig(park.ParkConfig):
    # Set batch size to 1 since we'll be running inference on
    # one image at a time. Batch size = GPU_COUNT * IMAGES_PER_GPU
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1

config = InferenceConfig()
config.display()

# Create model object in inference mode.
model = modellib.MaskRCNN(mode="inference", model_dir=MODEL_DIR, config=config)


# Load weights trained on MS-COCO
model.load_weights(PARK_MODEL_PATH, by_name=True)

class_names = ['BG', 'park', 'drive']


# Load a random image from the images folder
file_names = next(os.walk(IMAGE_DIR))[2]
image = skimage.io.imread(os.path.join(IMAGE_DIR,'park_test' ,'210809_0735_000022866.jpg'))

# Run detection
results = model.detect([image], verbose=1)

# Visualize results
r = results[0]
print(collections.Counter(r['class_ids'])[1])
visualize.display_instances(image, r['rois'], r['masks'], r['class_ids'], 
                            class_names, r['scores'])