"""
Raspberry Pi Face Recognition Treasure Box
Face Recognition Training Script
Copyright 2013 Tony DiCola

Run this script to train the face recognition system with positive and
negative training images. The face recognition model is based on the
eigen faces algorithm implemented in OpenCV. You can find more details
on the algorithm and face recognition here:
  http://docs.opencv.org/modules/contrib/doc/facerec/facerec_tutorial.html
"""

import fnmatch
import os
import cv2
import numpy as np
import config
import face

# pylint: disable=no-member

MEAN_FILE = "mean.png"
POSITIVE_EIGENFACE_FILE = "positive_eigenface.png"
NEGATIVE_EIGENFACE_FILE = "negative_eigenface.png"


def walk_files(directory, match="*"):
    """Generator function to iterate through all files in a directory
    recursively which match the given filename match parameter.
    """
    for root, _, files in os.walk(directory):
        for name in fnmatch.filter(files, match):
            yield os.path.join(root, name)


def prepare_image(name):
    """Read an image as grayscale and resize it to the appropriate size for
    training the face recognition model.
    """
    return face.resize(cv2.imread(name, cv2.IMREAD_GRAYSCALE))


def normalize(input_array, low, high, dtype=None):
    """Normalizes a given array in input_array to a value between low
    and high. Adapted from python OpenCV face recognition example at:
    https://github.com/Itseez/opencv/blob/2.4/samples/python2/facerec_demo.py
    """
    input_array = np.asarray(input_array)
    array_min, array_max = np.min(input_array), np.max(input_array)
    # normalize to [0...1].
    input_array = input_array - float(array_min)
    input_array = input_array / float((array_max - array_min))
    # scale to [low...high].
    input_array = input_array * (high - low)
    input_array = input_array + low
    if dtype is None:
        return np.asarray(input_array)
    return np.asarray(input_array, dtype=dtype)


if __name__ == "__main__":
    print("Reading training images...")
    faces = []
    labels = []
    POS_COUNT = 0
    NEG_COUNT = 0
    # Read all positive images
    for filename in walk_files(config.POSITIVE_DIR, "*.pgm"):
        faces.append(prepare_image(filename))
        labels.append(config.POSITIVE_LABEL)
        POS_COUNT += 1
    # Read all negative images
    for filename in walk_files(config.NEGATIVE_DIR, "*.pgm"):
        faces.append(prepare_image(filename))
        labels.append(config.NEGATIVE_LABEL)
        NEG_COUNT += 1
    print("Read", POS_COUNT, "positive images and", NEG_COUNT, "negative images.")

    # Train model
    print("Training model...")
    model = cv2.face.EigenFaceRecognizer_create()
    model.train(np.asarray(faces), np.asarray(labels))

    # Save model results
    model.save(config.TRAINING_FILE)
    print("Training data saved to", config.TRAINING_FILE)

    # Save mean and eignface images which summarize the face recognition model.
    mean = model.getMean().reshape(faces[0].shape)
    cv2.imwrite(MEAN_FILE, normalize(mean, 0, 255, dtype=np.uint8))
    eigenvectors = model.getEigenVectors()
    pos_eigenvector = eigenvectors[:, 0].reshape(faces[0].shape)
    cv2.imwrite(
        POSITIVE_EIGENFACE_FILE, normalize(pos_eigenvector, 0, 255, dtype=np.uint8)
    )
    neg_eigenvector = eigenvectors[:, 1].reshape(faces[0].shape)
    cv2.imwrite(
        NEGATIVE_EIGENFACE_FILE, normalize(neg_eigenvector, 0, 255, dtype=np.uint8)
    )
