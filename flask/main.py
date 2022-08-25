# -*- coding: utf-8 -*-

from logging import root
import os
import imageutil
import matrixutil
import crypto
import numpy as np


def encryption(path):
    name=os.path.basename(path)
    image = imageutil.load_image(path)
    a = (crypto.a_matrix(2, 1, 2, 2), matrixutil.vector(0.6, 0.2, 0.8, 0.6).T)
    cm1 = (crypto.cat_map(2, 1), matrixutil.vector(0.9, 0.72).T)
    cm2 = (crypto.cat_map(3, 2), matrixutil.vector(0.235, 0.821).T)
    block_size = 35
    std_limit = 3
    cypheredImage, mask, shape = crypto.cypher_image(image, *a, *cm1, *cm2, block_size, std_limit)
    list1=mask.tolist()
    # print(list1)
    # print(shape)
    root_dir = os.path.dirname(os.getcwd())
    base_image_path = 'Test/process/cyphered_'+name[0:-3]+'jpg'
    file_path = os.path.join(root_dir, base_image_path)
    print(os.path.relpath(file_path))
    print(file_path)
    imageutil.save_image(cypheredImage, file_path)
    return file_path,list1,shape, os.path.relpath(file_path)

def decryption(path,ar,shape):
    name=os.path.basename(path)
    cypheredImage = imageutil.load_image(path)
    a = (crypto.a_matrix(2, 1, 2, 2), matrixutil.vector(0.6, 0.2, 0.8, 0.6).T)
    cm1 = (crypto.cat_map(2, 1), matrixutil.vector(0.9, 0.72).T)
    cm2 = (crypto.cat_map(3, 2), matrixutil.vector(0.235, 0.821).T)
    block_size = 35
    std_limit = 3
    mask=np.array(ar)
    decypheredImage = crypto.decypher_image(cypheredImage, mask, shape, *a, *cm1, *cm2, block_size)
    # url = "../Test/process/decyphered_" + name
    root_dir = os.path.dirname(os.getcwd())
    base_image_path = 'Test/process/decyphered_'+name
    file_path = os.path.join(root_dir, base_image_path)
    print(os.path.relpath(file_path))
    imageutil.save_image(decypheredImage, file_path)
    return file_path, os.path.relpath(file_path)

# print("1:encryption")
# print("2:decryption")
# a=int(input("Enter choice: "))
# if a==1:
#     c=input("Enter path : ")
#     encryption(c)
# elif a==2:
#     c=input("Enter path : ")
#     ar=[[0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0], [0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0], [0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0], [0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0], [0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0], [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0], [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0], [0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0], [0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0], [0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0]]
#     shape=(380, 380, 3)
#     decryption(c,ar,shape)
# else :
#     print("wrong choice")

