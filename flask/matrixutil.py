

import numpy

def vector(*a):

	if len(a) == 0:
		raise ValueError
	return numpy.atleast_2d(numpy.array([*a]))
