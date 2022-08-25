# -*- coding: utf-8 -*-

import numpy
import math
from matrixutil import vector
from byteutil import to_bytes

import imageutil

def a_matrix(a, b, c, d):
	return numpy.array(
			[
				[
					(2*b + c)*(d + 1) + 3*d + 1,
					2*(b + 1),
					2*b*c + c + 3,
					4*b + 3
				],
				[
					2*(a + 1)*(d + b*c*(d + 1)) + a*(c + 1)*(d + 1),# E
					2*(a + b + a*b) + 1,
					a*(c + 3) + 2*b*c*(a + 1) + 2,# F
					3*a + 4*b*(a + 1) + 1
				],
				[
					3*b*c*(d + 1) + 3*d,
					3*b + 1,
					3*b*c + 3,
					6*b + 1
				],
				[
					c*(b + 1)*(d + 1) + d,
					b + 1,
					b*c + c + 1,
					2*b + 2
				]
			]
		)

def cat_map(a, b):
	
	return numpy.array(
			[
				[
					1,
					a
				],
				[
					b,
					a*b + 1
				]
			]
		)

def omega_matrix(a, x, height, width):
	
	l = height*width
	y = []
	z = []
	u = vector(2, 3, 5, 1)

	for i in range(math.ceil(l/16.0)):
		t = math.floor(numpy.dot(u, x)[0][0]) + 1

		for j in range(t):
			x = a.dot(x) % 1

		n = (numpy.floor(x * (2**32))).T

		y.append(x)
		z.append(vector(to_bytes(numpy.uint32(n), 4)))

	return (numpy.reshape(numpy.reshape(numpy.array(z), [math.ceil(l/16.0)*16])[:l], [height, width]), 
		numpy.reshape(numpy.array(y), [math.ceil(l/16.0)*4]))

def shuffling_sequence(a, x, n):
	
	r1 = []
	r2 = []
	u = vector(2, 3)

	for i in range(n):
		t = math.floor(numpy.dot(u, x)[0][0]) + 1

		for j in range(t):
			x = a.dot(x) % 1

		r1.append(x[0][0])
		r2.append(x[1][0])

	r1 = [i[0] for i in sorted(enumerate(r1), key = lambda x : x[1])]
	r2 = [i[0] for i in sorted(enumerate(r2), key = lambda x : x[1])]

	return r1, r2

def shuffle_block(i, omega, l, a1, x1, a2, x2):
	
	s1 = shuffling_sequence(a1, x1, l)
	s2 = shuffling_sequence(a2, x2, l)

	#Shuffling de columnas
	i = numpy.array([[i[1] for i in sorted(enumerate(j), key = lambda x : s1[0][x[0]])] for j in i])
	omega = numpy.array([[i[1] for i in sorted(enumerate(j), key = lambda x : s1[1][x[0]])] for j in omega])

	#Shuffling de filas
	i = numpy.array([i[1] for i in sorted(enumerate(i), key = lambda x : s2[0][x[0]])])
	omega = numpy.array([i[1] for i in sorted(enumerate(omega), key = lambda x : s2[1][x[0]])])

	return i, omega

def shuffle_image(image, mask, omega, a1, x1, a2, x2):
	
	s = len(image) // len(mask)
	res = numpy.zeros_like(image)

	for i in range(len(mask[0])):
		for j in range(len(mask)):
			if not mask[j][i]:
				res[j*s:(j+1)*s, i*s:(i+1)*s] = image[j*s:(j+1)*s, i*s:(i+1)*s]

			else:
				res[j*s:(j+1)*s, i*s:(i+1)*s] = shuffle_block(image[j*s:(j+1)*s, i*s:(i+1)*s], 
														omega, s, a1, x1, a2, x2)[0]

	return res

def unshuffle_block(i, omega, l, a1, x1, a2, x2):
	
	s1 = shuffling_sequence(a1, x1, l)
	s2 = shuffling_sequence(a2, x2, l)

	#Shuffling de columnas
	i = numpy.array([[i[1] for i in sorted(zip(numpy.argsort(s1[0]), j), key = lambda x : x[0])] for j in i])
	omega = numpy.array([[i[1] for i in sorted(zip(numpy.argsort(s1[1]), j), key = lambda x : x[0])] for j in omega])

	#Shuffling de filas
	i = numpy.array([i[1] for i in sorted(zip(numpy.argsort(s2[0]), i), key = lambda x : x[0])])
	omega = numpy.array([i[1] for i in sorted(zip(numpy.argsort(s2[1]), i), key = lambda x : x[0])])

	return i, omega

def unshuffle_image(image, mask, omega, a1, x1, a2, x2):
	
	s = len(image) // len(mask)
	res = numpy.zeros_like(image)

	for i in range(len(mask[0])):
		for j in range(len(mask)):
			if not mask[j][i]:
				res[j*s:(j+1)*s, i*s:(i+1)*s] = image[j*s:(j+1)*s, i*s:(i+1)*s]

			else:
				res[j*s:(j+1)*s, i*s:(i+1)*s] = unshuffle_block(image[j*s:(j+1)*s, i*s:(i+1)*s], 
														omega, s, a1, x1, a2, x2)[0]

	return res

def mask_block(i, omega, l, y):
	
	p = 1

	for j in range(l):
		o = (int)(1 + (omega.T[j].dot(numpy.array([numpy.product(i) for i in numpy.transpose(i, (1, 0, 2))])) % math.floor((l*l)/4)))
		numpy.roll(omega.T[j], -p)
		p = 1 + math.floor(l*y[o])

		for k in range(l):
			i[k][j] = (i[k][j] + omega[j][k]) % 256

	return i

def mask_image(image, mask, omega, y):
	
	s = len(image) // len(mask)
	res = numpy.zeros_like(image)

	for i in range(len(mask[0])):
		for j in range(len(mask)):
			if not mask[j][i]:
				res[j*s:(j+1)*s, i*s:(i+1)*s] = image[j*s:(j+1)*s, i*s:(i+1)*s]

			else:
				res[j*s:(j+1)*s, i*s:(i+1)*s] = mask_block(image[j*s:(j+1)*s, i*s:(i+1)*s], omega, s, y)

	return res

def unmask_block(i, omega, l, y):
	for j in reversed(range(l)):
		for k in range(l):
			i[k][j] = (i[k][j] - omega[j][k]) % 256

	return i

def unmask_image(image, mask, omega, y):
	
	s = len(image) // len(mask)
	res = numpy.zeros_like(image)

	for i in range(len(mask[0])):
		for j in range(len(mask)):
			if not mask[j][i]:
				res[j*s:(j+1)*s, i*s:(i+1)*s] = image[j*s:(j+1)*s, i*s:(i+1)*s]

			else:
				res[j*s:(j+1)*s, i*s:(i+1)*s] = unmask_block(image[j*s:(j+1)*s, i*s:(i+1)*s], omega, s, y)

	return res

def cypher_image(image, a_matrix, a_vector, cat_map1, cat_map1_init, cat_map2, cat_map2_init, block_size, std_limit):
	omega, y = omega_matrix(a_matrix, a_vector, block_size, block_size)

	paddedImage, shape = imageutil.pad_image(image, block_size)

	mask = imageutil.divide_regions(paddedImage, block_size, std_limit)

	shuffled_image = shuffle_image(paddedImage.copy(), mask, omega, cat_map1, cat_map1_init, cat_map2, cat_map2_init)
	masked_image = mask_image(shuffled_image.copy(), mask, omega, y)

	return masked_image, mask, shape

def decypher_image(image, mask, shape, a_matrix, a_vector, cat_map1, cat_map1_init, cat_map2, cat_map2_init, block_size):
	omega, y = omega_matrix(a_matrix, a_vector, block_size, block_size)

	unmasked_image = unmask_image(image.copy(), mask, omega, y)
	unshuffled_image = unshuffle_image(unmasked_image.copy(), mask, omega, cat_map1, cat_map1_init, cat_map2, cat_map2_init)

	return imageutil.unpad_image(unshuffled_image, shape)