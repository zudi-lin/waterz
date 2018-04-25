import h5py
import numpy as np
import scipy

def create_border_mask(input_data, max_dist, background_label,axis=0):
    """
    Overlay a border mask with background_label onto input data.
    A pixel is part of a border if one of its 4-neighbors has different label.
    
    Parameters
    ----------
    input_data : h5py.Dataset or numpy.ndarray - Input data containing neuron ids
    target : h5py.Datset or numpy.ndarray - Target which input data overlayed with border mask is written into.
    max_dist : int or float - Maximum distance from border for pixels to be included into the mask.
    background_label : int - Border mask will be overlayed using this label.
    axis : int - Axis of iteration (perpendicular to 2d images for which mask will be generated)
    """
    target = input_data.copy()
    sl = [slice(None) for d in xrange(len(target.shape))]

    for z in xrange(target.shape[axis]):
        sl[ axis ] = z
        border = create_border_mask_2d(input_data[tuple(sl)], max_dist)
        target_slice = input_data[tuple(sl)] if isinstance(input_data,h5py.Dataset) else np.copy(input_data[tuple(sl)]) 
        target_slice[border] = background_label
        target[tuple(sl)] = target_slice
    return target

def create_border_mask_2d(image, max_dist):
    """
    Create binary border mask for image.
    A pixel is part of a border if one of its 4-neighbors has different label.
    
    Parameters
    ----------
    image : numpy.ndarray - Image containing integer labels.
    max_dist : int or float - Maximum distance from border for pixels to be included into the mask.

    Returns
    -------
    mask : numpy.ndarray - Binary mask of border pixels. Same shape as image.
    """
    max_dist = max(max_dist, 0)
    
    padded = np.pad(image, 1, mode='edge')
    
    border_pixels = np.logical_and(
        np.logical_and( image == padded[:-2, 1:-1], image == padded[2:, 1:-1] ),
        np.logical_and( image == padded[1:-1, :-2], image == padded[1:-1, 2:] )
        )

    distances = scipy.ndimage.distance_transform_edt(
        border_pixels,
        return_distances=True,
        return_indices=False
        )

    return distances <= max_dist
    
