import rawpy
import imageio
import os
import io
from base64 import encodebytes
from PIL import Image
import numpy as np

def basic_showImg(img, size=4):
    '''Shows an image in a numpy.array type. Syntax:
        basic_showImg(img, size=4), where
            img = image numpy.array;
            size = the size to show the image. Its value is 4 by default.
    '''
    from matplotlib.pyplot import imshow
    import matplotlib.pyplot as plt

    plt.figure(figsize=(size,size))
    plt.imshow(img)
    plt.show()


def whiteBalance(filename, neutral_x, neutral_y):
    # read CR2 File

    path = '../img/' + filename
    base_name = os.path.splitext(filename)[0]

    with rawpy.imread(path) as raw: 
        # post process with linear rgb image and without white balance
        # user_wb is for custom white balance multiplier
        img = raw.postprocess(no_auto_bright=True)


    after_wb = ground_truth(img, img[neutral_y:neutral_y+1, neutral_x:neutral_x+1])
    
    save_dir = '../processed_img/processed_' + base_name + '.jpg'
    print("processed img save_dir: ", save_dir)
    imageio.imsave(save_dir, after_wb)

    pil_img = Image.open(save_dir, mode='r') # reads the PIL image
    byte_arr = io.BytesIO()
    pil_img.save(byte_arr, format='JPEG') # convert the PIL image to byte array
    encoded_img = encodebytes(byte_arr.getvalue()).decode('ascii') # encode as base64

    print('base64 string:', encoded_img[:20])
    return encoded_img
    
def ground_truth(image, patch, mode='mean'):   

    image_patch = patch
    image_patch_mean = image_patch.mean()

    print('Image White Balancing...')
    if mode == 'mean':
        image_patch_wb = (image_patch * (image_patch_mean / \
                    image.mean(axis=(0, 1)))).clip(1, 255)
        image_gt = ((image * (image_patch_mean / \
                    image.mean(axis=(0, 1))))\
                    .clip(1, 255))
        image_gt = (image_gt * (196 / image_patch_wb.mean(axis=(0, 1)))).clip(1, 255).astype(np.uint8)

    #transparency channel
    if image.shape[2] == 4:
        image_gt[:,:,3] = 255

    print('Image White Balancing Done!')

    return image_gt


# basic_showImg(whiteBalance('IMG_8509.CR2', 895, 2665), 8)

# def whiteBalance(filename, x, y):
    # print("x: ", x, "y: ", y)
    # img_path = '../img/' + filename
    # base_name = os.path.splitext(filename)[0]

    # with rawpy.imread(img_path) as raw:
    #     rgb = raw.postprocess(output_color=rawpy.ColorSpace.raw, 
    #                                 gamma=(1, 1),
    #                                 user_wb=[1.0, 1.0, 1.0, 1.0], 
    #                                 no_auto_bright=True,)
    # save_dir = '../processed_img/processed_' + base_name + '.jpg'
    # print("processed img save_dir: ", save_dir)
    # imageio.imsave(save_dir, rgb)


    # pil_img = Image.open(save_dir, mode='r') # reads the PIL image
    # byte_arr = io.BytesIO()
    # pil_img.save(byte_arr, format='JPEG') # convert the PIL image to byte array
    # encoded_img = encodebytes(byte_arr.getvalue()).decode('ascii') # encode as base64

    # print('base64 string:', encoded_img[:20])
    # return encoded_img