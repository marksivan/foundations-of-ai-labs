import torch


def swiss_flag():
    left_channel = torch.tensor(
        [
            [255, 255, 255, 255, 255],
            [255, 255, 255, 255, 255],
            [255,  255 ,255, 255, 255],
            [255, 255, 255, 255, 255],
            [255, 255, 255, 255, 255],
            
        ]
    )
      
    middle_channel = torch.tensor(
        [
            [0, 0,   0,  0, 0],
            [0, 0, 255, 0, 0],
            [0, 255, 255, 255, 0],
            [0, 0, 255,  0, 0],
            [0, 0, 0,  0, 0],
            
        ]
    )


    right_channel = torch.tensor(
        [
            [0, 0, 0, 0, 0],
            [0, 0, 255, 0, 0],
            [0, 255, 255, 255, 0],
            [0, 0, 255, 0, 0],
            [0, 0, 0, 0, 0],
            
        ]
    )
    return torch.stack([left_channel, middle_channel, right_channel])


def crop_to_smallest(image1, image2):
    image1_dimensions = image1.shape
    image2_dimensions = image2.shape

    image1_height = image1_dimensions[1]
    image1_width = image1_dimensions[2]

    image2_height = image2_dimensions[1]
    image2_width = image2_dimensions[2]


    height = min(image1_height, image2_height)
    width = min(image1_width, image2_width)

    return image1[:, :height, :width] , image2[:, :height, :width]
    


def compute_mask(image):
    C, H, W = image.shape
    img = torch.zeros((H, W), dtype=torch.int)

    col1, col2, col3 = image
    for r in range(H):
        for c in range(W):
            if (col2[r][c] > 1.5 * col1[r][c]) and  (col2[r][c] > 1.5 * col3[r][c]):
                img[r][c] = 1
    
    return img
                  
                  

 

def green_screen(background, foreground):
    background, foreground = crop_to_smallest(background, foreground)
    mask = compute_mask(foreground)
    result = mask * background + (1 - mask) * foreground
    


    return result



if __name__ == "__main__":
    from imageutil import read_image, show_image
    import sys

    background = read_image(sys.argv[1])
    foreground = read_image(sys.argv[2])
    img = green_screen(background, foreground)
    show_image(img)
