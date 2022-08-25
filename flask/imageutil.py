

import numpy
from PIL import Image

def load_image(path):
	
	return numpy.array(Image.open(path).convert("RGB"))

def save_image(image, path):
	
	Image.fromarray(image, "RGB").save(path)

def pad_image(image, block_size):
	
	height_padding = len(image) % block_size
	width_padding = len(image[0]) % block_size

	height_padding = 0 if height_padding == 0 else block_size - height_padding
	width_padding = 0 if width_padding == 0 else block_size - width_padding

	return numpy.pad(image, ((0, height_padding), (0, width_padding), (0, 0)), 'constant'), image.shape

def unpad_image(image, shape):

	return image[:shape[0], :shape[1]]

def classification_metric(block, threshold):
	
	return numpy.std(block) > threshold

def divide_regions(image, block_size, threshold):
	s = block_size
	width = len(image[0]) // block_size
	height = len(image) // block_size

	mask = numpy.empty([height, width])

	for i in range(width):
		for j in range(height):
			mask[j][i] = classification_metric(image[j*s:(j+1)*s, i*s:(i+1)*s], threshold)

	return mask