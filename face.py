"""
Raspberry Pi Face Recognition Treasure Box
Face Detection Helper Functions
Copyright 2013 Tony DiCola

Functions to help with the detection and cropping of faces.
"""

import cv2
import config

# pylint: disable=no-member

haar_faces = cv2.CascadeClassifier(config.HAAR_FACES)


def detect_single(image):
    """Return bounds (x, y, width, height) of detected face in grayscale image.
    If no face or more than one face are detected, None is returned.
    """
    faces = haar_faces.detectMultiScale(
        image,
        scaleFactor=config.HAAR_SCALE_FACTOR,
        minNeighbors=config.HAAR_MIN_NEIGHBORS,
        minSize=config.HAAR_MIN_SIZE,
        flags=cv2.CASCADE_SCALE_IMAGE,
    )
    if len(faces) != 1:
        return None
    return faces[0]


def crop(image, left, top, width, height):
    """Crop box defined by left, top (upper left corner) and width, height
    to an image with the same aspect ratio as the face training data.
    Might return a smaller crop if the box is near the edge of the image.
    """
    mid_y = top + height // 2  # Orig. center y
    height = int(height * config.FACE_HEIGHT / config.FACE_WIDTH)
    top = max(0, mid_y - height // 2)  # Revised top
    bottom = min(image.shape[0], top + height)  # Revised bottom
    return image[top:bottom, left : left + width]


def resize(image):
    """Resize a face image to the proper size for training and detection."""
    return cv2.resize(
        image, (config.FACE_WIDTH, config.FACE_HEIGHT), interpolation=cv2.INTER_LANCZOS4
    )
