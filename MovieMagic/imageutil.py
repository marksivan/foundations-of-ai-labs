from PIL import Image
import numpy as np
import torch


def read_image(filename):
    """Reads an image from the specified file."""
    orig_img = Image.open(filename)
    t = torch.from_numpy(np.array(orig_img))
    return t.transpose(0, 1).transpose(0, 2)


def read_image_as_grayscale(filename):
    """Reads an image from the specified file and then converts it to grayscale."""
    orig_img = Image.open(filename).convert("L")
    return torch.from_numpy(np.array(orig_img))


def show_image(image, magnification=1):
    """Displays an image in a pop-up window."""
    if image.dim() == 3:
        image = image.repeat_interleave(magnification, dim=1).repeat_interleave(
            magnification, dim=2
        )
        image = image.transpose(0, 2).transpose(0, 1)
    else:
        image = image.repeat_interleave(magnification, dim=1).repeat_interleave(
            magnification, dim=0
        )
    array = np.array(image).astype(np.uint8)
    img = Image.fromarray(array)
    img.show()
