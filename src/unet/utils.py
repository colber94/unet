from typing import Tuple

import numpy as np


def crop_to_shape(data, shape: Tuple[int, int, int]):
    """
    Crops the array to the given image shape by removing the border

    :param data: the array to crop, expects a tensor of shape [batches, nx, ny, channels]
    :param shape: the target shape [batches, nx, ny, channels]
    """
    diff_nx = (data.shape[0] - shape[0])
    diff_ny = (data.shape[1] - shape[1])

    if diff_nx == 0 and diff_ny == 0:
        return data

    offset_nx_left = diff_nx // 2
    offset_nx_right = diff_nx - offset_nx_left
    offset_ny_left = diff_ny // 2
    offset_ny_right = diff_ny - offset_ny_left

    cropped = data[offset_nx_left:(-offset_nx_right), offset_ny_left:(-offset_ny_right)]

    assert cropped.shape[0] == shape[0]
    assert cropped.shape[1] == shape[1]
    return cropped


def crop_labels_to_shape(shape: Tuple[int, int, int]):
    def crop(image, label):
        return image, crop_to_shape(label, shape)
    return crop


def crop_image_and_label_to_shape(shape: Tuple[int, int, int]):
    def crop(image, label):
        return crop_to_shape(image, shape), \
               crop_to_shape(label, shape)
    return crop


def to_rgb(img: np.array):
    """
    Converts the given array into a RGB image. If the number of channels is not
    3 the array is tiled such that it has 3 channels. Finally, the values are
    rescaled to [0,255)

    :param img: the array to convert [nx, ny, channels]

    :returns img: the rgb image [nx, ny, 3]
    """
    img = img.astype(np.float32)
    img = np.atleast_3d(img)

    channels = img.shape[-1]
    if channels < 3:
        img = np.tile(img, 3)

    img[np.isnan(img)] = 0
    img -= np.amin(img)
    if np.amax(img) != 0:
        img /= np.amax(img)

    # img *= 255
    return img
