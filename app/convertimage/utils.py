#!/usr/bin/env python3
import hashlib
from io import BytesIO

import numpy as np
from PIL import Image
from django.core.files.base import ContentFile


class ImageArray:
    """
    Load each image into a array, stack on top on other image arrays
    and run _process_image
    """
    def __init__(self, images):
        self.images = [self._load_image(image)
                       for image in images]
        self.stacked_image_arrays = np.stack(self.images)
        self.flattened_image_array = self._process_image(self.stacked_image_arrays)

    def _load_image(self, _file):
        with Image.open(_file) as img:
            return np.array(img)

    def return_image(self):
        buffer = BytesIO()
        img = Image.fromarray(self.flattened_image_array.astype('uint8'))
        img.save(fp=buffer, format="JPEG")
        return ContentFile(buffer.getvalue())

    def save_image(self, save_location):
        image = Image.fromarray(self.flattened_image_array.astype('uint8'))
        image.save(save_location)
        print(f'Saved to {save_location}')

    def _process_image(self, stacked_image):
        raise AttributeError('Should be defined in subclass')


class ImageMedian(ImageArray):
    """
    Collapse image array into median of each pixel
    """
    def __init__(self, images):
        super().__init__(images)

    def _process_image(self, stacked_image_arrays):
        if len(stacked_image_arrays) < 3:
            raise ValueError('Requires 3 or more images')
        flattened_median_image_array = np.median(stacked_image_arrays, axis=0)
        return flattened_median_image_array


class ImageMean(ImageArray):
    """
    Collapse image array into mean of each pixel
    """
    def __init__(self, images):
        super().__init__(images)

    def _process_image(self, stacked_image_arrays):
        flattened_mean_image_array = np.mean(stacked_image_arrays, axis=0)
        return flattened_mean_image_array

class ImageMode(ImageArray):
    """
    Collapse image array into mode of each pixel
    """
    def __init__(self, images):
        super().__init__(images)

    def _process_image(self, stacked_image_arrays):
        def mode(ndarray, axis=0):
            # https://stackoverflow.com/a/35674754/4172336 by devdev
            # Check inputs
            ndarray = np.asarray(ndarray)
            ndim = ndarray.ndim
            if ndarray.size == 1:
                return (ndarray[0], 1)
            elif ndarray.size == 0:
                raise Exception('Cannot compute mode on empty array')
            try:
                axis = range(ndarray.ndim)[axis]
            except:
                raise Exception('Axis "{}" incompatible with the {}-dimension array'.format(axis, ndim))

            # If array is 1-D and np version is > 1.9 np.unique will suffice
            if all([ndim == 1,
                    int(np.__version__.split('.')[0]) >= 1,
                    int(np.__version__.split('.')[1]) >= 9]):
                modals, counts = np.unique(ndarray, return_counts=True)
                index = np.argmax(counts)
                return modals[index], counts[index]

            # Sort array
            sort = np.sort(ndarray, axis=axis)
            # Create array to transpose along the axis and get padding shape
            transpose = np.roll(np.arange(ndim)[::-1], axis)
            shape = list(sort.shape)
            shape[axis] = 1
            # Create a boolean array along strides of unique values
            strides = np.concatenate([np.zeros(shape=shape, dtype='bool'),
                                         np.diff(sort, axis=axis) == 0,
                                         np.zeros(shape=shape, dtype='bool')],
                                        axis=axis).transpose(transpose).ravel()
            # Count the stride lengths
            counts = np.cumsum(strides)
            counts[~strides] = np.concatenate([[0], np.diff(counts[~strides])])
            counts[strides] = 0
            # Get shape of padded counts and slice to return to the original shape
            shape = np.array(sort.shape)
            shape[axis] += 1
            shape = shape[transpose]
            slices = [slice(None)] * ndim
            slices[axis] = slice(1, None)
            # Reshape and compute final counts
            counts = counts.reshape(shape).transpose(transpose)[slices] + 1

            # Find maximum counts and return modals/counts
            slices = [slice(None, i) for i in sort.shape]
            del slices[axis]
            index = np.ogrid[slices]
            index.insert(axis, np.argmax(counts, axis=axis))
            return sort[index], counts[index]
        return mode(stacked_image_arrays)[0]

conversion_choices = {
    'Mean': ImageMean,
    'Median': ImageMedian,
    'Mode': ImageMode,
}
