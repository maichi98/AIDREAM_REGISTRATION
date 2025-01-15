from skimage.morphology import remove_small_objects
from skimage.filters import threshold_otsu
from numba import njit, prange
import numpy as np
import ants


@njit(parallel=True)
def fill_mask(mask_arr: np.ndarray) -> np.ndarray:
    """
    Fill a 3D mask array. Useful when use a threshold function and need to fill hole

    :param mask_arr: mask to fill
    :return: mask filled
    """
    assert mask_arr.ndim == 3, "Mask to fill need to be a 3d array"

    for z in prange(0, mask_arr.shape[0]):  # we use np convention -> z,y,x
        for x in prange(0, mask_arr.shape[2]):
            if np.max(mask_arr[z, :, x]) == 1:
                a0 = mask_arr.shape[1] - 1
                b0 = 0
                while mask_arr[z, a0, x] == 0:
                    if a0 != 0:
                        a0 = a0 - 1  # Top of the data. Above it is zero.

                while mask_arr[z, b0, x] == 0:
                    if b0 != mask_arr.shape[1] - 1:
                        b0 = b0 + 1  # Bottom of the data. Below it is zero.
                for k in prange(b0, a0 + 1):
                    mask_arr[z, k, x] = 1
        for y in prange(0, mask_arr.shape[1]):
            if np.max(mask_arr[z, y, :]) == 1:
                c0 = mask_arr.shape[2] - 1
                d0 = 0
                while mask_arr[z, y, c0] == 0:
                    if c0 != 0:
                        c0 = c0 - 1  # Top of the data. Above it is zero.

                while mask_arr[z, y, d0] == 0:
                    if d0 != mask_arr.shape[1] - 1:
                        d0 = d0 + 1  # Bottom of the data. Below it is zero.
                for j in prange(d0, c0 + 1):
                    mask_arr[z, y, j] = 1
    return mask_arr


def get_mask(input_array: np.ndarray) -> np.ndarray:
    """
    Get a (head) mask. Based on Otsu threshold and noise reduced. Then result mask is holes filled.

    :param input_array: input image array
    :return: binary head mask
    """
    thresh = threshold_otsu(input_array)
    otsu_mask = input_array > thresh
    noise_reduced = remove_small_objects(otsu_mask, 10, )
    head_mask = fill_mask(noise_reduced.astype(np.uint8))
    return head_mask


def pad_image(image: ants.ANTsImage, shape: tuple):

    new_image = np.zeros(shape)
    indices = tuple(slice(0, min(image.shape[i], shape[i])) for i in range(3))

    new_image[indices] = image.numpy()[indices]
    new_image = ants.from_numpy(new_image, spacing=image.spacing, origin=image.origin)

    return new_image


def compute_kl_divergence(hist_p, hist_q):

    epsilon = 1e-10

    # Compute the KL divergence :
    kl_divergence = np.sum(hist_p * np.log(hist_p / (hist_q + epsilon) + epsilon))
    return kl_divergence


# Function to compute the JS divergence :
def compute_js_divergence(hist_p, hist_q):

    # Compute the mean histogram :
    hist_m = 0.5 * (hist_p + hist_q)

    # Compute the JS divergence :
    js_divergence = 0.5 * (compute_kl_divergence(hist_p, hist_m) + compute_kl_divergence(hist_q, hist_m))

    return js_divergence


def detect_outliers(df, col, multiplier=1.5, lower_bound=None, upper_bound=None):

    quartile_1 = df[col].quantile(0.25)
    quartile_3 = df[col].quantile(0.75)

    iqr = quartile_3 - quartile_1

    if lower_bound is None:
        lower_bound = quartile_1 - (multiplier * iqr)

    if upper_bound is None:
        upper_bound = quartile_3 + (multiplier * iqr)

    return df.loc[(df[col] < lower_bound) | (df[col] > upper_bound)], lower_bound, upper_bound
