import rawpy
import imageio
import os
import io
from base64 import encodebytes
from PIL import Image
  

def img_conv(filename):
    img_path = '../img/' + filename
    base_name = os.path.splitext(filename)[0]

    with rawpy.imread(img_path) as raw:
        rgb = raw.postprocess()
    save_dir = '../processed_img/processed_' + base_name + '.jpg'
    print("processed img save_dir: ", save_dir)
    imageio.imsave(save_dir, rgb)


    pil_img = Image.open(save_dir, mode='r') # reads the PIL image
    byte_arr = io.BytesIO()
    pil_img.save(byte_arr, format='JPEG') # convert the PIL image to byte array
    encoded_img = encodebytes(byte_arr.getvalue()).decode('ascii') # encode as base64

    print('base64 string:', encoded_img[:20])
    return encoded_img